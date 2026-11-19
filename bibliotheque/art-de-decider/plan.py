#!/usr/bin/env python3
"""Construit plan.json en petites réponses (le tunnel réseau coupe les réponses très longues) :
1) squelette : titre, thèse, cadre, bibliographie, parties et titres des chapitres ;
2) une réponse par partie : objectifs, sections, exercices, figure de chaque chapitre.
Relançable : chaque morceau réussi est gardé dans plan_*.json."""
import json, os, subprocess, sys
from pathlib import Path
ICI = Path(__file__).resolve().parent
ASK = ICI.parent / "outils" / "ask.py"
MODELE = os.environ.get("DIALAGRAM_MODEL", "qwen-3.8-max-thinking")
CONTEXTE = (ICI / "brief_plan.txt").read_text(encoding="utf-8").split("Réponds UNIQUEMENT")[0]

def demander(nom, prompt, controle, essais=5):
    sortie = ICI / f"plan_{nom}.json"
    if sortie.exists():
        return json.loads(sortie.read_text(encoding="utf-8"))
    (ICI / f"plan_{nom}.prompt.txt").write_text(prompt, encoding="utf-8")
    for _ in range(essais):
        brut = ICI / f"plan_{nom}.raw.txt"
        brut.unlink(missing_ok=True)
        subprocess.run([sys.executable, str(ASK), str(ICI / f"plan_{nom}.prompt.txt"), str(brut)],
                       env={**os.environ, "DIALAGRAM_MODEL": MODELE}, cwd=ICI, capture_output=True, timeout=1800)
        try:
            t = brut.read_text(encoding="utf-8")
            d = json.loads(t[t.find("{"):t.rfind("}") + 1])
            controle(d)
        except Exception as e:  # réponse coupée ou incomplète : on recommence
            print(nom, "essai raté :", str(e)[:120], flush=True)
            continue
        sortie.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(nom, "ok", flush=True)
        return d
    sys.exit(f"{nom} : échec après {essais} essais")

def ctrl_squelette(d):
    assert len(d["bibliographie"]) >= 20 and d["cadre"]["nom"] and d["these"]
    assert sum(len(p["chapitres"]) for p in d["parties"]) >= 28

sq = demander("squelette", CONTEXTE + """
ÉTAPE 1 SEULEMENT : réponds UNIQUEMENT avec un JSON valide, sans balises :
{"titre":"...","sous_titre":"...","these":"...","cadre":{"nom":"...","description":"..."},
 "bibliographie":[{"auteur":"...","titre":"...","annee":"...","idee":"...","apport":"..."}],
 "parties":[{"titre":"...","chapitres":[{"numero":1,"titre":"..."}]}]}
7 parties, 30 chapitres numérotés de 1 à 30, au moins 25 références. Pas encore de sections ni de figures.""", ctrl_squelette)

resume = "\n".join(f"Partie {i+1} — {p['titre']} : " + " ; ".join(f"ch.{c['numero']} {c['titre']}" for c in p["chapitres"])
                   for i, p in enumerate(sq["parties"]))
for i, p in enumerate(sq["parties"]):
    nums = [c["numero"] for c in p["chapitres"]]
    def ctrl(d, nums=nums):
        cs = d["chapitres"]
        assert [c["numero"] for c in cs] == nums
        for c in cs:
            assert c["objectif"] and len(c["sections"]) >= 5 and c["exercices"] and c["figure"]["type"]
    det = demander(f"partie{i+1}", CONTEXTE + f"""
Le squelette du livre est fixé :
Titre : {sq['titre']} — {sq['sous_titre']}
Thèse : {sq['these']}
Cadre : {sq['cadre']['nom']} — {sq['cadre']['description']}
{resume}

ÉTAPE 2 : détaille UNIQUEMENT la partie {i+1} « {p['titre']} » (chapitres {nums}). Pour chaque chapitre : objectif, 6 à 8 sections,
2 exercices pratiques, et la figure (voir les types et champs ci-dessus). Réponds UNIQUEMENT avec un JSON valide :
{{"chapitres":[{{"numero":{nums[0]},"titre":"...","objectif":"...","sections":["..."],"exercices":["..."],"figure":{{"type":"...","titre":"...","elements":["..."]}}}}]}}""", ctrl)
    p["chapitres"] = det["chapitres"]

(ICI / "plan.json").write_text(json.dumps(sq, ensure_ascii=False, indent=1), encoding="utf-8")
print("plan.json :", sq["titre"], "|", sum(len(p["chapitres"]) for p in sq["parties"]), "chapitres")
