#!/usr/bin/env python3
"""Génère via Dialagram le dictionnaire de compétences de chaque secteur.

Usage : generer.py [cle1 cle2 ...]   (sans argument : tous les secteurs de secteurs.json)
Écrit secteurs/<cle>.json (réponse brute parsée). Les secteurs déjà générés sont sautés.
Un JSON tronqué est récupéré compétence par compétence.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ICI = Path(__file__).resolve().parent
ASK = ICI.parent / "bibliotheque" / "outils" / "ask.py"
MODELES = ["qwen-3.7-max-thinking", "qwen-3.8-max-thinking", "qwen-3.7-max-thinking", "xiaomi-mimo-2.6"]
PARALLELE = int(os.environ.get("PAR", "6"))


def analyser(texte: str):
    """Renvoie (secteur, compétences) même si la réponse est tronquée ou entourée de texte."""
    debut = texte.find("{")
    if debut < 0:
        return None, []
    try:
        d = json.loads(texte[debut:texte.rfind("}") + 1])
        return d.get("sector"), d.get("skills", [])
    except ValueError:
        pass
    # récupération : on lit les objets du tableau "skills" un par un jusqu'à la coupure
    k = texte.find('"skills"')
    i = texte.find("[", k) + 1 if k >= 0 else 0
    dec, skills = json.JSONDecoder(), []
    while i:
        while i < len(texte) and texte[i] in " \n\r\t,":
            i += 1
        if i >= len(texte) or texte[i] != "{":
            break
        try:
            obj, i = dec.raw_decode(texte, i)
        except ValueError:
            break
        skills.append(obj)
    return None, skills


def generer(cle: str, libelle: str) -> str:
    sortie = ICI / "secteurs" / f"{cle}.json"
    if sortie.exists():
        return f"{cle}: déjà fait"
    prompt = ICI / "secteurs" / f"{cle}.prompt.txt"
    prompt.write_text((ICI / "prompt.txt").read_text(encoding="utf-8").replace("{SECTEUR}", libelle), encoding="utf-8")
    brut = ICI / "secteurs" / f"{cle}.raw.txt"
    meilleur, modele_ok = [], ""
    for modele in MODELES:
        brut.unlink(missing_ok=True)
        try:
            subprocess.run([sys.executable, str(ASK), str(prompt), str(brut)], env={**os.environ, "DIALAGRAM_MODEL": modele},
                           cwd=ICI / "secteurs", capture_output=True, timeout=1800)
        except subprocess.TimeoutExpired:
            continue
        if not brut.exists():
            continue
        _, skills = analyser(brut.read_text(encoding="utf-8"))
        if len(skills) > len(meilleur):
            meilleur, modele_ok = skills, modele
        if len(skills) >= 60:
            break
    if not meilleur:
        return f"{cle}: ÉCHEC"
    sortie.write_text(json.dumps({"sector": libelle, "key": cle, "model": modele_ok, "skills": meilleur},
                                 ensure_ascii=False, indent=1), encoding="utf-8")
    return f"{cle}: {len(meilleur)} compétences ({modele_ok})"


if __name__ == "__main__":
    secteurs = json.loads((ICI / "secteurs.json").read_text(encoding="utf-8"))
    cles = sys.argv[1:] or list(secteurs)
    with ThreadPoolExecutor(PARALLELE) as ex:
        for r in ex.map(lambda c: generer(c, secteurs[c]), cles):
            print(r, flush=True)
    (ICI / "secteurs" / "usage.log").unlink(missing_ok=True)
