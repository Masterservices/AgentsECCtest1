#!/usr/bin/env python3
"""Édition lexicale « Французский в 10 000 словах » (le français pour russophones) : entrées pour livre et cartes mémoire.

Usage : generer.py DEBUT FIN [--lot 10]   (PAR=4 appels en parallèle ; relançable, un lot fini est sauté)
Python : rang de fréquence et forme de base (FrequencyWords + simplemma, liste nettoyée). Dialagram (un appel pour 10 mots) :
nature, API, sens, équivalents russes, exemples, synonymes, formes, pièges pour russophones, expressions, famille.
Explications en russe ; mots et exemples en français. Sortie : entrees/RRRR.json avec "controle" = défauts restants.
"""
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ICI = Path(__file__).resolve().parent
ASK = ICI.parents[1] / "bibliotheque" / "outils" / "ask.py"
MODELES = ["qwen-3.8-max", "qwen-3.8-max", "qwen-3.8-max-thinking"]
CYR = re.compile("[а-яё]", re.I)


def prompt(lot):
    lignes = "\n".join(f"{x['rang']}. {x['lemme']}" for x in lot)
    return f"""Ты — лексикограф (французский–русский) и преподаватель французского языка для русскоговорящих. Ты пишешь статьи
учебного словаря самых частотных французских слов для книги и приложения с карточками.

Слова (ранг частотности, словарная форма) :
{lignes}

Для КАЖДОГО слова напиши точную и полезную статью :
- "mot" : слово (для существительного — с артиклем, например « la maison », « l'ami (m) ») ; "nature" : часть речи по-русски ;
  "genre" : m / f / — ; "api" : транскрипция МФА в квадратных скобках ; "niveau" : A1, A2, B1 или B2.
- "sens" : 2–6 реальных значений, от самого частого ; для каждого : "sens" (краткое определение по-русски), "equivalents" (2–4 русских
  перевода), "exemples" : 2 естественные французские фразы с переводом ("fr", "ru").
- "synonymes" : 1–4 французских синонима, у каждого "nuance" по-русски (регистр, употребление) ; "antonymes" : 0–3 слова.
- "formes" : глагол → "auxiliaire" (avoir/être), "present" (je, tu, il, nous, vous, ils), "passe_compose" (je), "imparfait" (je),
  "futur" (je), "participe_passe" ; существительное → "pluriel" ; прилагательное → "feminin", "pluriel" ; другие → {{}}.
- "pieges" : 1–3 конкретные трудности для русскоговорящего (артикль, род, отличный от русского, предлог, ложные друзья,
  произношение, liaison).
- "expressions" : 0–3 устойчивых выражения ("fr", "ru") ; "famille" : 0–4 однокоренных слова ("mot", "ru").
Никаких выдуманных слов ; для служебных слов (артикль, предлог, местоимение, частица) объясни их употребление.

Ответь ТОЛЬКО валидным JSON : {{"entrees": [{{"rang": 1, "lemme": "...", "mot": "...", "nature": "...", "genre": "...", "api": "...",
"niveau": "A1", "sens": [...], "synonymes": [...], "antonymes": [...], "formes": {{}}, "pieges": [...], "expressions": [...], "famille": [...]}}]}}"""


def controler(e, ref):
    err = []
    if re.search(r"[\u3000-\u9fff\uac00-\ud7af\uff00-\uffef]", json.dumps(e, ensure_ascii=False)):
        err.append("caractères chinois/coréens")
    mot = str(e.get("mot", "")).lower()
    if ref["lemme"].lower() not in mot and ref["lemme"].lower().replace("œ", "oe") not in mot.replace("œ", "oe"):
        err.append("mot différent de la forme de base")
    if not str(e.get("api", "")).startswith("["):
        err.append("API manquante")
    sens = e.get("sens") or []
    if not sens or any(not s.get("equivalents") or not s.get("exemples") for s in sens):
        err.append("sens incomplets")
    expl = " ".join(str(s.get("sens", "")) for s in sens) + " ".join(map(str, e.get("pieges") or []))
    if len(CYR.findall(expl)) < 0.5 * len(re.findall(r"[a-zа-яё]", expl, re.I)):
        err.append("explications pas en russe")
    exemples = " ".join(str(p.get("fr", "")) for s in sens for p in s.get("exemples") or [] if isinstance(p, dict))
    if CYR.search(exemples):
        err.append("exemples français contenant du cyrillique")
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
            if not isinstance(e, dict):
                continue
            ref = next((x for x in lot if x["rang"] == e.get("rang") or x["lemme"] == str(e.get("lemme", "")).lower()), None)
            if ref:
                e.update(rang=ref["rang"], lemme=ref["lemme"], frequence=ref["occurrences"])
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
