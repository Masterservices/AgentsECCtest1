#!/usr/bin/env python3
"""Fait écrire par Dialagram deux cours de langue A1→B1 pour l'e-learning Russtudy :
le français pour russophones et le russe pour francophones.

Usage : generer.py programme          → programme/<cours>.json (personnages récurrents + 36 leçons)
        generer.py lecons [cours ...]  → lecons/<cours>/<NN>.json (PAR=3 en parallèle, relançable)
Chaque leçon nourrit le livre (livre.py) et sert d'entrée aux leçons interactives WebGL avec voix off.
Une leçon est contrôlée par controle_lecon() ; les défauts restants sont notés dans son champ "controle".
"""
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ICI = Path(__file__).resolve().parent
ASK = ICI.parent / "bibliotheque" / "outils" / "ask.py"
MODELES = ["qwen-3.7-max-thinking", "qwen-3.8-max-thinking", "qwen-3.7-max-thinking"]
NIVEAUX = [("A1", 12), ("A2", 12), ("B1", 12)]
COURS = {
    "fr-pour-russes": {
        "cible": "français", "natif": "russe", "code_cible": "fr", "code_natif": "ru", "eleve": "russophones",
        "titre": "Le français pour russophones", "titre_natif": "Французский язык для русскоговорящих",
        "fil": "une jeune russophone s'installe en France (études puis premier emploi) et se fait des amis français",
        "difficultes": "articles (absents en russe), genre des noms souvent différent du russe, verbe être et auxiliaires être/avoir, "
                       "passé composé/imparfait, voyelles nasales, e muet, u/ou, liaisons et enchaînements, accent final fixe, "
                       "pronoms en/y, subjonctif (B1)",
        "prononciation": "transcription API entre crochets, ex. [bɔ̃ʒuʁ]",
    },
    "ru-pour-francais": {
        "cible": "russe", "natif": "français", "code_cible": "ru", "code_natif": "fr", "eleve": "francophones",
        "titre": "Le russe pour francophones", "titre_natif": "Русский язык для франкоговорящих",
        "fil": "un jeune francophone part vivre en Russie (études puis premier emploi) et se fait des amis russes",
        "difficultes": "alphabet cyrillique (leçons 1 à 3), accent tonique mobile, réduction des voyelles inaccentuées, consonnes dures "
                       "et molles, les six cas dans l'ordre nominatif, prépositionnel, accusatif, génitif, datif, instrumental, absence "
                       "d'article et du verbe être au présent, aspects perfectif/imperfectif, verbes de mouvement, préfixes de mouvement (B1)",
        "prononciation": "translittération latine avec la syllabe accentuée en majuscules, ex. moloKO",
    },
}
CYR = re.compile("[Ѐ-ӿ]")
ACCENT = "́"


def demander(prompt: str, nom: str, dossier: Path, controle, essais=MODELES):
    """Appelle Dialagram jusqu'à obtenir un JSON sans défaut ; renvoie (meilleur objet, défauts restants)."""
    dossier.mkdir(parents=True, exist_ok=True)
    pf, brut = dossier / f"{nom}.prompt.txt", dossier / f"{nom}.raw.txt"
    pf.write_text(prompt, encoding="utf-8")
    meilleur, defauts = None, ["aucune réponse"]
    for m in essais:
        brut.unlink(missing_ok=True)
        try:
            subprocess.run([sys.executable, str(ASK), str(pf), str(brut)], env={**os.environ, "DIALAGRAM_MODEL": m},
                           cwd=dossier, capture_output=True, timeout=1800)
        except subprocess.TimeoutExpired:
            continue
        if not brut.exists():
            continue
        t = brut.read_text(encoding="utf-8")
        try:
            d = json.loads(t[t.find("{"):t.rfind("}") + 1])
        except ValueError:
            continue
        err = controle(d)
        if meilleur is None or len(err) < len(defauts):
            meilleur, defauts = d, err
        if not err:
            break
    (dossier / "usage.log").unlink(missing_ok=True)
    return meilleur, defauts


def prompt_programme(c):
    return f"""Tu es concepteur pédagogique expert du CECR et de l'enseignement du {c['cible']} aux {c['eleve']}.
Conçois le programme complet du cours e-learning « {c['titre']} » ({c['titre_natif']}) pour la plateforme Russtudy :
36 leçons — 12 de niveau A1, 12 de niveau A2, 12 de niveau B1 — avec une progression rigoureuse en spirale (chaque leçon réemploie les acquis).
Le cours sera transformé en leçons interactives WebGL (scènes 3D, personnages animés, voix off) : chaque leçon se déroule dans un lieu concret et visuel.
Fil narratif continu sur les 36 leçons : {c['fil']}. 4 à 6 personnages récurrents, variés en âge et en caractère.
Difficultés propres aux {c['eleve']} à traiter explicitement au bon moment : {c['difficultes']}.
Les leçons 12, 24 et 36 sont des bilans de niveau (révision + mise en situation).

Réponds UNIQUEMENT avec un JSON valide :
{{"personnages": [{{"id": "identifiant ascii court", "nom": "...", "age": 25, "role": "rôle dans l'histoire", "apparence": "description visuelle précise pour un modèle 3D", "voix": "timbre, âge, débit pour la synthèse vocale"}}],
 "lecons": [{{"num": 1, "niveau": "A1", "titre": "titre en {c['cible']}", "titre_trad": "titre en {c['natif']}", "lieu": "lieu précis", "situation": "une phrase : qui fait quoi", "communication": ["savoir-faire visés"], "grammaire": ["points de grammaire"], "vocabulaire": "champ lexical", "prononciation": "point de prononciation", "culture": "point culturel"}}]}}
Sauf les titres, rédige les champs en français."""


def controle_programme(d):
    err = []
    if not 4 <= len(d.get("personnages", [])) <= 6:
        err.append("4 à 6 personnages attendus")
    L = d.get("lecons", [])
    if len(L) != 36:
        err.append(f"{len(L)} leçons au lieu de 36")
    for i, l in enumerate(L):
        attendu = NIVEAUX[min(i // 12, 2)][0]
        if l.get("niveau") != attendu:
            err.append(f"leçon {i + 1} : niveau {l.get('niveau')} au lieu de {attendu}")
        if not l.get("grammaire") or not l.get("titre"):
            err.append(f"leçon {i + 1} incomplète")
    return err


def prompt_lecon(c, prog, n):
    l = prog["lecons"][n]
    vus = "; ".join(f"L{p['num']} {', '.join(p['grammaire'])}" for p in prog["lecons"][:n]) or "aucun (première leçon)"
    persos = "\n".join(f"- {p['id']} : {p['nom']}, {p['age']} ans, {p['role']}" for p in prog["personnages"])
    accents = ("Dans TOUT texte russe destiné à l'apprenant (dialogue, vocabulaire, exemples, exercices, voix off des personnages), "
               "marque l'accent tonique par l'accent aigu combinant U+0301 placé après la voyelle accentuée de chaque mot de plus "
               "d'une syllabe (ex. молоко́, говори́ть). ") if c["code_cible"] == "ru" else ""
    part_cible = {"A1": "20 %", "A2": "50 %", "B1": "80 %"}[l["niveau"]]
    return f"""Tu es auteur de manuels de {c['cible']} pour {c['eleve']} et scénariste e-learning.
Rédige la leçon {l['num']}/36 du cours « {c['titre']} » (plateforme Russtudy), niveau {l['niveau']} du CECR.

FICHE DE LA LEÇON
- Titre : {l['titre']} ({l['titre_trad']})
- Lieu : {l['lieu']} — Situation : {l['situation']}
- Savoir-faire : {', '.join(l['communication'])}
- Grammaire : {', '.join(l['grammaire'])}
- Vocabulaire : {l['vocabulaire']} — Prononciation : {l['prononciation']} — Culture : {l['culture']}
Grammaire déjà vue (à réemployer, sans la réexpliquer) : {vus}
Personnages récurrents :
{persos}

RÈGLES
- Langue cible : {c['cible']}. Langue de l'apprenant : {c['natif']}. Explications, consignes, traductions et culture en {c['natif']} ; dialogue, vocabulaire et exemples en {c['cible']}.
- {accents}Prononciation du vocabulaire : {c['prononciation']}.
- Niveau {l['niveau']} strict : n'emploie dans le dialogue que des structures vues ou introduites ici.
- Le dialogue est naturel, vivant, fait avancer l'histoire, et met en scène les points de grammaire et le vocabulaire de la leçon.
- Le cours deviendra une leçon WebGL : décris le décor, les objets 3D et un geste par réplique ; la voix off guide l'apprenant pas à pas.
- Les personnages secondaires (serveur, agent, médecin…) sont déclarés dans scene.figurants et peuvent parler dans le dialogue.
- Voix off : le narrateur parle en {c['natif']} (environ {part_cible} de {c['cible']} à ce niveau), les personnages parlent en {c['cible']}. Couvre dans l'ordre : accueil et objectifs, dialogue complet (une réplique par segment), vocabulaire à répéter, explication de grammaire, consignes des exercices, conclusion.
- Exercices : exactement 6, de types différents parmi qcm, trous, association, ordre, traduction, ecoute, oral ; 4 à 6 items chacun, réponse pour chaque item.

FORMAT — réponds UNIQUEMENT avec un JSON valide :
{{"titre": {{"cible": "...", "natif": "..."}},
 "objectifs": ["3 à 5 objectifs en {c['natif']}"],
 "scene": {{"lieu": "...", "moment": "...", "decor_3d": "description visuelle précise du décor en français", "objets": ["objets 3D utiles"], "personnages": ["ids présents"], "figurants": [{{"id": "ascii court", "nom": "...", "apparence": "description visuelle pour modèle 3D", "voix": "timbre pour la synthèse vocale"}}]}},
 "dialogue": [{{"perso": "id", "texte": "réplique en {c['cible']}", "traduction": "en {c['natif']}", "geste": "animation en français"}}],
 "vocabulaire": [{{"mot": "...", "prononciation": "...", "nature": "nom m. / verbe / adj. …", "traduction": "...", "exemple": "phrase en {c['cible']}", "exemple_traduction": "..."}}],
 "grammaire": [{{"titre": "en {c['natif']}", "explication": "120 à 250 mots en {c['natif']}", "tableau": [["en-tête", "..."], ["...", "..."]], "exemples": [{{"cible": "...", "natif": "..."}}]}}],
 "prononciation": {{"point": "...", "explication": "en {c['natif']}", "exemples": ["..."]}},
 "culture": {{"titre": "...", "texte": "80 à 150 mots en {c['natif']}"}},
 "exercices": [{{"type": "qcm", "consigne": "en {c['natif']}", "items": [{{"question": "...", "choix": ["..."], "reponse": "..."}}]}}],
 "voix_off": [{{"id": "v01", "voix": "narrateur ou id du personnage", "langue": "{c['code_natif']} ou {c['code_cible']}", "texte": "...", "ecran": "ce que montre la scène WebGL (en français)", "interaction": "aucune | repeter | choisir | ecrire | parler"}}],
 "resume": [{{"cible": "phrase clé", "natif": "traduction"}}]}}
Quantités : dialogue 10 à 16 répliques ; vocabulaire 15 à 20 mots ; grammaire 1 ou 2 points ; résumé 4 à 6 phrases ; voix off 20 à 35 segments.
« choix » seulement pour qcm et ecoute ; pour association, « question » = élément de gauche et « reponse » = élément associé."""


def part(texte, motif):
    lettres = [ch for ch in texte if ch.isalpha()]
    return sum(bool(motif.match(ch)) for ch in lettres) / max(len(lettres), 1)


def controle_lecon(c, prog):
    ids = {p["id"] for p in prog["personnages"]}
    cible_cyr = c["code_cible"] == "ru"

    def ctrl(d):
        err = []
        for k in ("titre", "objectifs", "scene", "dialogue", "vocabulaire", "grammaire", "prononciation", "culture", "exercices",
                  "voix_off", "resume"):
            if not d.get(k):
                err.append(f"champ {k} manquant")
        if err:
            return err
        D, V, X, VO = d["dialogue"], d["vocabulaire"], d["exercices"], d["voix_off"]
        if not 10 <= len(D) <= 18:
            err.append(f"dialogue : {len(D)} répliques")
        if not 14 <= len(V) <= 22:
            err.append(f"vocabulaire : {len(V)} mots")
        if len(X) != 6 or any(not e.get("items") or any(not str(i.get("reponse", "")).strip() for i in e["items"]) for e in X):
            err.append("exercices : 6 exercices avec une réponse par item attendus")
        if not 18 <= len(VO) <= 40:
            err.append(f"voix off : {len(VO)} segments")
        if not any(r.get("perso") in ids for r in D):
            err.append("dialogue : aucun personnage récurrent")
        texte_cible = " ".join(r.get("texte", "") for r in D)
        texte_natif = " ".join(g.get("explication", "") for g in d["grammaire"]) + " " + d["culture"].get("texte", "")
        p_cible, p_natif = part(texte_cible, CYR), part(texte_natif, CYR)
        if (cible_cyr and p_cible < 0.8) or (not cible_cyr and p_cible > 0.05):
            err.append("dialogue pas dans la langue cible")
        if (cible_cyr and p_natif > 0.35) or (not cible_cyr and p_natif < 0.6):
            err.append("explications pas dans la langue de l'apprenant")
        if cible_cyr and texte_cible.count(ACCENT) < len(D):
            err.append("accents toniques russes manquants dans le dialogue")
        voix = {v.get("voix") for v in VO}
        if "narrateur" not in voix or not ids & voix:
            err.append("voix off : narrateur et personnages attendus")
        return err
    return ctrl


def completer_figurants(d, prog):
    """Déclare dans scene.figurants tout personnage du dialogue qui n'est ni récurrent ni déjà déclaré (utile au WebGL)."""
    scene = d.setdefault("scene", {}) if isinstance(d.get("scene"), dict) else {}
    figs = [f for f in scene.get("figurants") or [] if isinstance(f, dict)]
    connus = {p["id"] for p in prog["personnages"]} | {f.get("id") for f in figs}
    for r in d.get("dialogue", []):
        if r.get("perso") not in connus:
            figs.append({"id": r.get("perso"), "nom": str(r.get("perso", "")).replace("_", " ").capitalize()})
            connus.add(r.get("perso"))
    scene["figurants"] = figs


def faire_programme(cle):
    sortie = ICI / "programme" / f"{cle}.json"
    if sortie.exists():
        return f"{cle} : programme déjà fait"
    d, err = demander(prompt_programme(COURS[cle]), cle, ICI / "programme", controle_programme)
    if d is None:
        return f"{cle} : ÉCHEC programme"
    sortie.write_text(json.dumps({**d, "controle": err}, ensure_ascii=False, indent=1), encoding="utf-8")
    return f"{cle} : programme {len(d.get('lecons', []))} leçons, défauts {err}"


def faire_lecon(cle, prog, n):
    c = COURS[cle]
    dossier = ICI / "lecons" / cle
    sortie = dossier / f"{n + 1:02d}.json"
    if sortie.exists() and not json.loads(sortie.read_text(encoding="utf-8")).get("controle"):
        return f"{cle} {n + 1:02d} : déjà faite"
    d, err = demander(prompt_lecon(c, prog, n), f"{n + 1:02d}", dossier, controle_lecon(c, prog))
    if d is None:
        return f"{cle} {n + 1:02d} : ÉCHEC"
    l = prog["lecons"][n]
    meta = {"cours": cle, "num": n + 1, "niveau": l["niveau"], "id": f"{cle}-{l['niveau']}-{n + 1:02d}"}
    completer_figurants(d, prog)
    sortie.write_text(json.dumps({**meta, **d, "controle": err}, ensure_ascii=False, indent=1), encoding="utf-8")
    return f"{cle} {n + 1:02d} : {'OK' if not err else err}"


if __name__ == "__main__":
    action, choix = (sys.argv[1:2] or ["lecons"])[0], sys.argv[2:] or list(COURS)
    with ThreadPoolExecutor(int(os.environ.get("PAR", "3"))) as ex:
        if action == "programme":
            taches = [ex.submit(faire_programme, k) for k in choix]
        else:
            progs = {k: json.loads((ICI / "programme" / f"{k}.json").read_text(encoding="utf-8")) for k in choix}
            taches = [ex.submit(faire_lecon, k, progs[k], n) for n in range(36) for k in choix]
        for t in taches:
            print(t.result(), flush=True)
