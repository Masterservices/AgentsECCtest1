#!/usr/bin/env python3
"""Édition lexicale « Le russe en 10 000 mots » : entrées détaillées pour livre et application de cartes mémoire.

Usage : generer.py DEBUT FIN [--lot 10]   (PAR=4 appels en parallèle ; relançable, un lot fini est sauté)
Répartition du travail pour économiser Dialagram :
- Python : rang de fréquence, forme de base, nature, translittération, contrôle des formes grammaticales (pymorphy3).
- Dialagram (un appel pour 10 mots) : accent, API, sens, équivalents, exemples, synonymes, pièges, expressions, famille.
Sortie : entrees/RRRR.json (liste des entrées du lot commençant au rang RRRR), avec "controle" = défauts restants.
"""
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pymorphy3

ICI = Path(__file__).resolve().parent
ASK = ICI.parents[1] / "bibliotheque" / "outils" / "ask.py"
MODELES = ["qwen-3.8-max", "qwen-3.8-max", "qwen-3.8-max-thinking"]
MORPH = pymorphy3.MorphAnalyzer()
ACC = "́"
NATURE = {"NOUN": "nom", "VERB": "verbe", "INFN": "verbe", "ADJF": "adjectif", "ADJS": "adjectif", "ADVB": "adverbe",
          "PREP": "préposition", "CONJ": "conjonction", "PRCL": "particule", "NPRO": "pronom", "INTJ": "interjection",
          "NUMR": "numéral", "COMP": "comparatif", "PRED": "prédicatif", "PRTF": "participe", "PRTS": "participe"}
LAT = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
               ["a", "b", "v", "g", "d", "e", "io", "j", "z", "i", "ï", "k", "l", "m", "n", "o", "p", "r", "s", "t", "ou", "f",
                "kh", "ts", "tch", "ch", "chtch", "", "y", "", "è", "iou", "ia"]))
VOY = set("аеёиоуыэюя")


def translit(accentue: str) -> str:
    """Translittération à la française ; la voyelle accentuée (suivie de U+0301, ou ё) est en majuscules."""
    t, out = accentue.lower(), []
    for i, c in enumerate(t):
        if c == ACC:
            continue
        lat = LAT.get(c, c)
        accent = (i + 1 < len(t) and t[i + 1] == ACC) or c == "ё"
        out.append(lat.upper() if accent and c in VOY else lat)
    return "".join(out)


def prompt(lot):
    lignes = "\n".join(f"{x['rang']}. {x['lemme']} ({NATURE.get(x['pos'], x['pos'])})" for x in lot)
    return f"""Tu es lexicographe (russe-français) et professeur de russe pour francophones. Tu rédiges les entrées d'un dictionnaire
d'apprentissage des mots russes les plus fréquents, destiné à un livre et à une application de cartes mémoire.

Mots (rang de fréquence, forme de base, nature) :
{lignes}

Pour CHAQUE mot, rédige une entrée exacte et utile :
- "mot" : le mot avec l'accent tonique marqué par U+0301 après la voyelle accentuée (ex. говори́ть) ; un mot d'une syllabe sans accent.
- "api" : transcription API entre crochets, avec réduction vocalique et palatalisation (ex. [ɡəvɐˈrʲitʲ]).
- "niveau" : A1, A2, B1 ou B2.
- "aspect" (verbes seulement) : "imperfectif" ou "perfectif", et "paire" = le verbe de l'autre aspect, accentué.
- "sens" : 2 à 6 sens réels, du plus courant au plus rare ; pour chacun : "sens" (définition courte en français), "equivalents" (2 à 4
  traductions françaises), "exemples" : 2 phrases russes naturelles et courantes, accentuées, avec leur traduction ("ru", "fr").
- "synonymes" : 1 à 4 mots russes de même sens, accentués, chacun avec sa "nuance" en français (registre, emploi) ; liste vide si aucun.
- "antonymes" : 0 à 3 mots accentués.
- "formes" : verbes → "present" (je, tu, il, nous, vous, ils ; pour un perfectif, le futur), "passe" (m, f, n, pl), "imperatif" (tu, vous) ;
  noms → "genre" (m, f, n) et "declinaison" : 6 cas × singulier/pluriel (nominatif, génitif, datif, accusatif, instrumental, prépositionnel) ;
  adjectifs → nominatif m, f, n, pl et forme courte m si elle existe ; autres → {{}}. Toutes les formes accentuées.
- "pieges" : 1 à 3 difficultés précises pour un francophone (faux amis, régime, aspect, accent mobile).
- "expressions" : 0 à 3 expressions figées courantes ("ru", "fr").
- "famille" : 0 à 4 mots de la même famille ("mot" accentué, "fr").
Aucun mot inventé ; si un mot a un sens grammatical (particule, préposition), explique ses emplois.

Réponds UNIQUEMENT avec un JSON valide : {{"entrees": [{{"rang": 1, "lemme": "...", "mot": "...", "api": "...", "niveau": "A1", "sens": [...], ...}}]}}"""


def sans_accent(t):
    return str(t).replace(ACC, "").replace("ё", "е").strip().lower()


def valeurs(v):
    if isinstance(v, dict):
        return [x for w in v.values() for x in valeurs(w)]
    if isinstance(v, list):
        return [x for w in v for x in valeurs(w)]
    return [v] if v else []


def controler(e, ref):
    """Défauts restants d'une entrée ; les formes grammaticales sont vérifiées avec pymorphy3 (accents retirés)."""
    err = []
    if re.search(r"[\u3000-\u9fff\uac00-\ud7af\uff00-\uffef]", json.dumps(e, ensure_ascii=False)):
        err.append("caractères chinois/coréens")
    if sans_accent(e.get("mot", "")) != sans_accent(ref["lemme"]):
        err.append("mot différent de la forme de base")
    mot = e.get("mot", "")
    if len(re.findall("[аеиоуыэюя]", sans_accent(mot))) > 1 and ACC not in mot and "ё" not in mot:
        err.append("accent manquant")
    sens = e.get("sens") or []
    if not sens or any(not s.get("equivalents") or not s.get("exemples") for s in sens):
        err.append("sens incomplets")
    f = e.get("formes") or {}
    cle = {"VERB": "present", "INFN": "present", "NOUN": "declinaison"}.get(ref["pos"])
    if cle and f.get(cle):
        attendu = {sans_accent(x.word) for p in MORPH.parse(ref["lemme"])[:3] for x in p.lexeme}
        faux = [sans_accent(x) for x in valeurs(f[cle]) if sans_accent(x).split()[-1] not in attendu]
        if len(faux) > (0 if cle == "present" else 2):
            err.append("formes douteuses : " + ", ".join(faux[:3]))
    return err


def faire_lot(lot):
    sortie = ICI / "entrees" / f"{lot[0]['rang']:04d}.json"
    if sortie.exists() and not any(e.get("controle") for e in json.loads(sortie.read_text(encoding="utf-8"))):
        return f"{sortie.name} : déjà fait"
    pf, brut = sortie.with_suffix(".prompt.txt"), sortie.with_suffix(".raw.txt")
    pf.write_text(prompt(lot), encoding="utf-8")
    meilleur = None
    for m in MODELES:
        brut.unlink(missing_ok=True)
        try:
            subprocess.run([sys.executable, str(ASK), str(pf), str(brut)], env={**os.environ, "DIALAGRAM_MODEL": m},
                           cwd=sortie.parent, capture_output=True, timeout=1500)
            t = brut.read_text(encoding="utf-8")
            rep = json.loads(t[t.find("{"):t.rfind("}") + 1])["entrees"]
        except (subprocess.TimeoutExpired, OSError, ValueError, KeyError, TypeError):
            continue
        par_rang = {}
        for e in rep:
            ref = next((x for x in lot if x["rang"] == e.get("rang") or x["lemme"] == sans_accent(e.get("lemme", ""))), None)
            if ref and isinstance(e, dict):
                e.update(rang=ref["rang"], lemme=ref["lemme"], nature=NATURE.get(ref["pos"], ref["pos"]),
                         frequence=ref["occurrences"], translit=translit(e.get("mot") or ref["lemme"]))
                e["controle"] = controler(e, ref)
                par_rang[ref["rang"]] = e
        entrees = [par_rang.get(x["rang"]) for x in lot]
        score = sum(1 for e in entrees if e and not e["controle"])
        if meilleur is None or score > meilleur[0]:
            meilleur = (score, entrees)
        if score == len(lot):
            break
    (sortie.parent / "usage.log").unlink(missing_ok=True)
    if meilleur is None:
        return f"{sortie.name} : ÉCHEC"
    entrees = [e or {"rang": x["rang"], "lemme": x["lemme"], "controle": ["entrée manquante"]} for e, x in zip(meilleur[1], lot)]
    sortie.write_text(json.dumps(entrees, ensure_ascii=False, indent=1), encoding="utf-8")
    return f"{sortie.name} : {meilleur[0]}/{len(lot)} entrées sans défaut"


if __name__ == "__main__":
    debut, fin = int(sys.argv[1]), int(sys.argv[2])
    taille = int(sys.argv[sys.argv.index("--lot") + 1]) if "--lot" in sys.argv else 10
    liste = [x for x in json.loads((ICI / "frequence.json").read_text(encoding="utf-8")) if debut <= x["rang"] <= fin]
    lots = [liste[i:i + taille] for i in range(0, len(liste), taille)]
    (ICI / "entrees").mkdir(exist_ok=True)
    with ThreadPoolExecutor(int(os.environ.get("PAR", "4"))) as ex:
        for r in ex.map(faire_lot, lots):
            print(r, flush=True)
