#!/usr/bin/env python3
"""Fait écrire par Dialagram 1000 chansons prêtes pour Suno (25 genres x 4 lots de 10).

Usage : generer.py [cle-genre ...]   (PAR=6 lots en parallèle)
        generer.py --complement      (complète chaque genre à 40 chansons uniques, titres déjà pris interdits)
Écrit lots/<cle>-<n>.json. Un lot déjà écrit (>= 8 chansons valides) est sauté : relançable sans perte.
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
LOTS, PAR_LOT = 4, 10
THEMES = ["premier amour", "rupture", "nostalgie de l'enfance", "exil et mal du pays", "la mère", "amitié fidèle", "liberté",
          "espoir après l'épreuve", "travailler dur pour réussir", "victoire et fierté", "nuit en ville", "été et plage",
          "la mer", "le désert", "voyage sur la route", "la pluie", "les rêves", "confiance en soi", "trahison", "pardon",
          "mariage et fête", "danser toute la nuit", "gratitude", "la nature", "le temps qui passe", "résilience",
          "solitude", "amour à distance", "retour au pays", "la paix", "jeunesse insouciante", "festival", "le sport",
          "guérison", "nouveau départ", "le père", "les grands-parents", "la ville natale", "l'automne", "un dernier au revoir"]
LANGUE = {"fr": "français", "en": "anglais", "ar": "arabe"}


def prompt(g, n, nb=PAR_LOT, interdits=()):
    debut = (sum(map(ord, g["cle"])) + n * PAR_LOT) % len(THEMES)
    lignes = []
    for i in range(nb):
        theme = THEMES[(debut + i * 3) % len(THEMES)]
        langue = g["langues"][(n * PAR_LOT + i) % len(g["langues"])]
        lignes.append(f"{i + 1}. thème : {theme} — langue : {LANGUE[langue]}")
    darija = "en darija maghrébine écrite en alphabet arabe" if g["cle"] in ("rai", "chaabi", "gnawa") else "en arabe dialectal simple, alphabet arabe"
    interdit = ("- Titres INTERDITS car déjà utilisés (trouve des titres neufs et des paroles qui ne leur ressemblent pas) : "
                + " | ".join(interdits) + "\n") if interdits else ""
    return f"""Tu es auteur-compositeur professionnel et tu écris pour le générateur musical Suno.
Écris {nb} chansons ORIGINALES du genre « {g['nom']} » (style de base : {g['style']}).

Chanson par chanson, respecte le thème et la langue imposés :
{chr(10).join(lignes)}

CONTRAINTES
- Paroles 100 % originales : aucune reprise, aucune citation d'une chanson existante, aucun nom d'artiste ou de marque réel.
- Tempo entre {g['bpm'][0]} et {g['bpm'][1]} BPM ; varie le tempo d'une chanson à l'autre.
- Structure balisée comme Suno, balises en anglais entre crochets, chacune sur sa ligne : [Intro], [Verse 1], [Pre-Chorus], [Chorus], [Verse 2], [Chorus], [Bridge], [Chorus], [Outro] (adapte au genre).
- 180 à 260 mots de paroles ; refrain court, mémorable et répété ; rimes et rythme chantables.
- Chansons en arabe : {darija}. Chansons en anglais ou français : langue naturelle et idiomatique.
{interdit}- « style » : prompt Suno en anglais de 120 à 200 caractères (genre, instruments, voix, ambiance, BPM), sans aucun nom d'artiste.

FORMAT — réponds UNIQUEMENT avec un JSON valide, sans texte autour :
{{"chansons": [{{"titre": "titre dans la langue de la chanson", "titre_fr": "traduction française du titre si la chanson n'est pas en français, sinon vide", "langue": "fr|en|ar", "theme": "...", "bpm": 110, "tonalite": "La mineur", "ambiance": "2 à 4 mots en français", "style": "...", "resume_fr": "une phrase en français qui résume la chanson", "paroles": "[Intro]\\n...\\n[Verse 1]\\n..."}}]}}"""


def analyser(t):
    d0 = t.find("{")
    if d0 < 0:
        return []
    try:
        return json.loads(t[d0:t.rfind("}") + 1]).get("chansons", [])
    except ValueError:
        pass
    k = t.find('"chansons"')
    i = t.find("[", k) + 1 if k >= 0 else 0
    dec, out = json.JSONDecoder(), []
    while i:
        while i < len(t) and t[i] in " \n\r\t,":
            i += 1
        if i >= len(t) or t[i] != "{":
            break
        try:
            o, i = dec.raw_decode(t, i)
        except ValueError:
            break
        out.append(o)
    return out


def valide(c):
    p = str(c.get("paroles", ""))
    mots = len(re.sub(r"\[[^\]]*\]", " ", p).split())
    if not c.get("titre") or mots < 90 or "[" not in p:
        return False
    if c.get("langue") == "ar" and not re.search("[؀-ۿ]", p):
        return False
    return True


def lot(g, n, nb=PAR_LOT, interdits=()):
    sortie = ICI / "lots" / f"{g['cle']}-{n + 1}.json"
    if sortie.exists() and len(json.loads(sortie.read_text(encoding="utf-8"))["chansons"]) >= nb * 0.8:
        return f"{sortie.name}: déjà fait"
    pf = ICI / "lots" / f"{g['cle']}-{n + 1}.prompt.txt"
    brut = ICI / "lots" / f"{g['cle']}-{n + 1}.raw.txt"
    pf.write_text(prompt(g, n, nb, interdits), encoding="utf-8")
    meilleur, mod = [], ""
    for m in MODELES:
        brut.unlink(missing_ok=True)
        try:
            subprocess.run([sys.executable, str(ASK), str(pf), str(brut)], env={**os.environ, "DIALAGRAM_MODEL": m},
                           cwd=ICI / "lots", capture_output=True, timeout=1500)
        except subprocess.TimeoutExpired:
            continue
        if not brut.exists():
            continue
        ok = [c for c in analyser(brut.read_text(encoding="utf-8")) if valide(c)]
        if len(ok) > len(meilleur):
            meilleur, mod = ok, m
        if len(ok) >= nb - 1:
            break
    if not meilleur:
        return f"{sortie.name}: ÉCHEC"
    sortie.write_text(json.dumps({"genre": g["cle"], "modele": mod, "chansons": meilleur}, ensure_ascii=False, indent=1), encoding="utf-8")
    return f"{sortie.name}: {len(meilleur)} chansons ({mod})"


if __name__ == "__main__":
    genres = json.loads((ICI / "genres.json").read_text(encoding="utf-8"))
    if sys.argv[1:2] == ["--complement"]:
        from livre_chansons import charger
        _, tout, _ = charger()
        titres = sorted({c["titre"] for c in tout})
        taches = []
        for g in genres:
            manque = 40 - sum(c["genre"] == g["cle"] for c in tout)
            if manque > 0:
                n = len(list((ICI / "lots").glob(f"{g['cle']}-[0-9].json")))
                taches.append((g, n, manque + 2, titres))
    else:
        choix = [g for g in genres if not sys.argv[1:] or g["cle"] in sys.argv[1:]]
        taches = [(g, n) for n in range(LOTS) for g in choix]
    with ThreadPoolExecutor(int(os.environ.get("PAR", "6"))) as ex:
        for r in ex.map(lambda t: lot(*t), taches):
            print(r, flush=True)
    (ICI / "lots" / "usage.log").unlink(missing_ok=True)
