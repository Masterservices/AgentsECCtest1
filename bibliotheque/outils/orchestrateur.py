#!/usr/bin/env python3
"""orchestrateur.py — Qwen orchestre l'usine à livres, sans dépendre d'une session Claude.

1. Qwen reçoit la liste des livres restants et les modèles disponibles (les sous-agents) ;
   il répond par un plan JSON : ordre, modèle et parallélisme de chaque livre.
2. Ce script exécute le plan avec au plus 8 requêtes simultanées (usine.sh, un livre par processus).
3. Un fil de sauvegarde pousse les brouillons dans le dépôt toutes les 5 minutes : une interruption
   (limite de 6 h d'une exécution GitHub Actions, panne) ne fait rien perdre.
4. En fin d'exécution, il indique au workflow s'il faut se relancer (livres restants et progrès réel).

Usage : orchestrateur.py [--cible restants|"slug1 slug2"] [--prefixe ie-] [--minutes 330] [--dry]
Variables : DIALAGRAM_API_KEY (obligatoire en Actions), ORCHESTRATEUR_MODEL, MAX_PARALLELE, W, USINE_SCRIPT.
"""
import argparse
import fcntl
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

R = Path(__file__).resolve().parents[2]              # racine du dépôt
O = R / "bibliotheque" / "outils"
W = Path(os.environ.get("W", "/tmp/usine"))          # dossier de travail (partagé avec usine.sh)
LOCK = Path("/tmp/usine/git.lock")                   # même verrou que usine.sh
USINE = os.environ.get("USINE_SCRIPT", str(O / "usine.sh"))
ORCH_MODEL = os.environ.get("ORCHESTRATEUR_MODEL", "qwen-3.8-max-thinking")
MAX_PAR = int(os.environ.get("MAX_PARALLELE", "8"))
BRANCHE = subprocess.run(["git", "-C", str(R), "branch", "--show-current"],
                         capture_output=True, text=True).stdout.strip() or "main"

MODELES = {
    "qwen-3.8-max-thinking": "le plus récent et le plus fort ; à privilégier pour les livres techniques, mathématiques ou longs",
    "qwen-3.7-max-thinking": "très bon généraliste, plus rapide ; livres pratiques",
    "xiaomi-mimo-2.6": "modèle plus léger ; livres pratiques courts ou simples (moins fiable sur les plans)",
}


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def sujets():
    return json.load(open(O / "sujets.json", encoding="utf-8"))


def a_pdf(slug):
    return bool(glob.glob(str(R / "bibliotheque" / slug / "*.pdf")))


def cibles(arg, prefixe):
    tous = sujets()
    if arg.strip() in ("", "restants"):
        return [s["slug"] for s in tous
                if (s["slug"].startswith(prefixe) or "demande" in s) and not a_pdf(s["slug"])]
    voulus = arg.split()
    connus = {s["slug"] for s in tous}
    inconnus = [v for v in voulus if v not in connus]
    if inconnus:
        sys.exit(f"Sujets inconnus dans sujets.json : {inconnus}")
    return [v for v in voulus if not a_pdf(v)]


def total_chapitres():
    return len(glob.glob(str(W / "*" / "chapitres" / "*.md"))) + len(glob.glob(str(W / "*" / "chapitres_v2" / "*.md")))


# ─── Brouillons : restauration et sauvegarde dans le dépôt ───────────────────

def restaurer(slugs):
    D = R / "bibliotheque" / "_brouillons"
    n = 0
    for s in slugs:
        d = D / s
        if not d.is_dir():
            continue
        for src in d.rglob("*"):
            dst = W / s / src.relative_to(d)
            if src.is_file() and not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                n += 1
    if n:
        log(f"{n} fichier(s) de brouillon restauré(s)")


def sauvegarder(slugs):
    D = R / "bibliotheque" / "_brouillons"
    for s in slugs:
        d = W / s
        if not (d / "plan.json").exists():
            continue
        if a_pdf(s):
            shutil.rmtree(D / s, ignore_errors=True)
            continue
        (D / s).mkdir(parents=True, exist_ok=True)
        for f in ("plan.json", "brief_plan.txt", "rapport_nettoyage.json"):
            if (d / f).exists():
                shutil.copy2(d / f, D / s / f)
        for sub in ("chapitres", "chapitres_v2"):
            if (d / sub).is_dir():
                (D / s / sub).mkdir(parents=True, exist_ok=True)
                for f in (d / sub).iterdir():
                    if f.is_file():
                        shutil.copy2(f, D / s / sub / f.name)
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCK, "a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        git = ["git", "-C", str(R)]
        subprocess.run(git + ["add", "-A", "bibliotheque/_brouillons"], capture_output=True)
        if subprocess.run(git + ["diff", "--cached", "--quiet"]).returncode == 0:
            return
        subprocess.run(git + ["commit", "-qm",
                              "Brouillons de l'usine : sauvegarde automatique\n\n"
                              "Orchestrateur : Qwen (usine Dialagram)"], capture_output=True)
        for attente in (2, 4, 8, 16):
            if subprocess.run(git + ["push", "-q", "origin", BRANCHE], capture_output=True).returncode == 0:
                log("brouillons sauvegardés")
                return
            subprocess.run(git + ["pull", "--rebase", "-q", "origin", BRANCHE], capture_output=True)
            time.sleep(attente)
        log("⚠ sauvegarde des brouillons : push impossible")


def boucle_sauvegarde(slugs, arret):
    while not arret.wait(300):
        try:
            sauvegarder(slugs)
        except Exception as e:  # la sauvegarde ne doit jamais arrêter l'usine
            log("⚠ sauvegarde :", e)


# ─── Qwen orchestrateur ──────────────────────────────────────────────────────

def appeler_qwen(prompt, modele=None, essais=3):
    wd = W / "_orchestrateur"
    wd.mkdir(parents=True, exist_ok=True)
    (wd / "brief.txt").write_text(prompt, encoding="utf-8")
    env = {**os.environ, "DIALAGRAM_MODEL": modele or ORCH_MODEL}
    for i in range(essais):
        (wd / "reponse.txt").unlink(missing_ok=True)
        try:
            subprocess.run([sys.executable, str(O / "ask.py"), "brief.txt", "reponse.txt"],
                           cwd=wd, env=env, capture_output=True, text=True, timeout=1800)
            t = (wd / "reponse.txt").read_text(encoding="utf-8").strip()
            if t:
                return t
        except Exception:
            pass
        time.sleep(20)
    return None


def demander_plan(slugs, minutes):
    d = {s["slug"]: s for s in sujets()}
    livres = "\n".join(f"- {s} : {d[s].get('theme', '')} — {d[s]['sujet'][:120]}" for s in slugs)
    modeles = "\n".join(f"- {m} : {desc}" for m, desc in MODELES.items())
    prompt = f"""Tu es l'orchestrateur d'une usine qui écrit des livres complets en français (environ 300 pages, 24 chapitres).
Chaque livre passe par : plan -> rédaction des chapitres -> rectification -> mise en page PDF.

Livres à produire ({len(slugs)}) :
{livres}

Sous-agents disponibles (modèles) :
{modeles}

Contraintes :
- au plus {MAX_PAR} requêtes simultanées au total ; un livre utilise « par » requêtes (1 à 4) ;
- un livre demande environ 40 à 60 minutes avec par=4 ; il reste environ {minutes} minutes dans cette exécution ;
- répartis la charge : varie les modèles, évite de donner xiaomi-mimo-2.6 à un livre technique ou long ;
- l'ordre compte : les livres au plan le plus simple d'abord.

Réponds UNIQUEMENT avec un JSON valide, sans balises markdown :
{{"ordre":[{{"slug":"...","modele":"...","par":4}}],"raison":"deux phrases maximum"}}
Chaque slug de la liste doit apparaître exactement une fois."""
    t = appeler_qwen(prompt)
    if not t:
        return None
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t.strip())
    try:
        return json.loads(t)
    except Exception:
        m = re.search(r"\{.*\}", t, re.S)
        try:
            return json.loads(m.group(0)) if m else None
        except Exception:
            return None


def valider(rep, slugs):
    liste = list(MODELES)
    repli = [{"slug": s, "modele": liste[i % 2], "par": 4} for i, s in enumerate(slugs)]
    if not isinstance(rep, dict) or not isinstance(rep.get("ordre"), list):
        return repli, "plan de repli : réponse de l'orchestrateur absente ou invalide"
    vus, ordre = set(), []
    for e in rep["ordre"]:
        s = e.get("slug") if isinstance(e, dict) else None
        if s in slugs and s not in vus:
            m, par = e.get("modele"), e.get("par")
            ordre.append({"slug": s, "modele": m if m in MODELES else liste[1],
                          "par": par if par in (1, 2, 3, 4) else 4})
            vus.add(s)
    ordre += [e for e in repli if e["slug"] not in vus]
    return ordre, str(rep.get("raison", ""))[:300]


# ─── Exécution du plan ───────────────────────────────────────────────────────

def lancer(e, essai):
    modele = e["modele"] if essai == 0 else list(MODELES)[1]   # 2e essai : modèle généraliste
    env = {**os.environ, "SLUGS": e["slug"], "DIALAGRAM_MODEL": modele, "TAILLE": "1",
           "PAR": str(e["par"]), "W": str(W)}
    out = open(W / f"{e['slug']}.log", "a")
    log(f"[{e['slug']}] démarrage ({modele}, {e['par']} requêtes, essai {essai + 1})")
    return subprocess.Popen(["bash", USINE], env=env, cwd=R, stdout=out, stderr=subprocess.STDOUT)


def notifier(livres):
    """Réveille Claude (vérificateur final) via l'API d'une routine Claude Code, si elle est configurée.
    Variables : ROUTINE_FIRE_URL et ROUTINE_FIRE_TOKEN (jeton sk-ant-oat01-… propre à la routine)."""
    url, token = os.environ.get("ROUTINE_FIRE_URL"), os.environ.get("ROUTINE_FIRE_TOKEN")
    if not url or not token or not livres:
        return
    texte = ("L'usine (orchestrateur Qwen) a terminé ces livres : " + " ".join(livres) +
             f". PDF, chapitres et rapports sont sur la branche {BRANCHE}, dans bibliotheque/<slug>/. "
             "Vérifie-les (dernière étape).")
    req = urllib.request.Request(
        url, data=json.dumps({"text": texte}).encode("utf-8"), method="POST",
        headers={"Authorization": f"Bearer {token}", "anthropic-version": "2023-06-01",
                 "Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=30).read()
        log(f"Claude notifié pour {len(livres)} livre(s)")
    except Exception as e:  # la notification ne doit jamais arrêter l'usine
        log("⚠ notification de Claude impossible :", e)


def executer(ordre, deadline, on_fini=lambda s: None):
    attente, en_cours, essais = list(ordre), {}, {}
    while (attente or en_cours) and time.time() < deadline:
        for s, (p, e) in list(en_cours.items()):
            if p.poll() is None:
                continue
            del en_cours[s]
            if a_pdf(s):
                log(f"[{s}] terminé")
                on_fini(s)
            elif essais[s] < 2:
                log(f"[{s}] incomplet, nouvel essai plus tard")
                attente.append(e)
            else:
                log(f"[{s}] abandonné après 2 essais")
        utilise = sum(e["par"] for _, e in en_cours.values())
        if time.time() < deadline - 3600:        # pas de nouveau livre dans la dernière heure
            for e in list(attente):
                if utilise + e["par"] <= MAX_PAR:
                    attente.remove(e)
                    essais[e["slug"]] = essais.get(e["slug"], -1) + 1
                    en_cours[e["slug"]] = (lancer(e, essais[e["slug"]]), e)
                    utilise += e["par"]
        elif not en_cours:
            break
        time.sleep(20)
    for s, (p, _) in en_cours.items():
        log(f"[{s}] arrêt à l'échéance (le brouillon est sauvegardé)")
        p.terminate()


def sortie(relancer, livres):
    log(f"relancer={relancer} livres={' '.join(livres)}")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"relancer={'true' if relancer else 'false'}\nlivres={' '.join(livres)}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cible", default="restants")
    ap.add_argument("--prefixe", default="ie-")
    ap.add_argument("--minutes", type=int, default=330)
    ap.add_argument("--dry", action="store_true", help="demander le plan à Qwen sans rien exécuter")
    a = ap.parse_args()
    W.mkdir(parents=True, exist_ok=True)

    slugs = cibles(a.cible, a.prefixe)
    log(f"{len(slugs)} livre(s) à produire")
    if not slugs:
        return sortie(False, [])
    if not appeler_qwen("Réponds uniquement : OK", essais=1):
        sys.exit("API Dialagram inaccessible, ou clé DIALAGRAM_API_KEY absente ou invalide : arrêt.")

    restaurer(slugs)
    ordre, raison = valider(demander_plan(slugs, a.minutes), slugs)
    log("Plan de l'orchestrateur :", raison)
    for e in ordre:
        log(f"  {e['slug']} -> {e['modele']} (par={e['par']})")
    if a.dry:
        print(json.dumps({"ordre": ordre, "raison": raison}, ensure_ascii=False, indent=1))
        return

    avant, deadline = total_chapitres(), time.time() + a.minutes * 60
    arret = threading.Event()
    fil = threading.Thread(target=boucle_sauvegarde, args=(slugs, arret), daemon=True)
    fil.start()
    lot, taille_lot = [], int(os.environ.get("NOTIFIER_LOT", "5"))   # une notification par lot de livres terminés

    def fini(s):
        lot.append(s)
        if len(lot) >= taille_lot:
            notifier(list(lot))
            lot.clear()

    try:
        executer(ordre, deadline, fini)
    finally:
        arret.set()
        sauvegarder(slugs)
        notifier(list(lot))

    produits = [s for s in slugs if a_pdf(s)]
    restants = [s for s in slugs if not a_pdf(s)]
    progres = bool(produits) or total_chapitres() > avant
    log(f"{len(produits)} livre(s) terminé(s), {len(restants)} restant(s), progrès={progres}")
    sortie(bool(restants) and progres, produits)


if __name__ == "__main__":
    main()
