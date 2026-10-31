#!/usr/bin/env python3
"""Réécrit en derja tunisienne toutes les chansons en arabe, avec romanisation chantable (Suno) et transcription API.

Usage : tunisien.py            (PAR=4 lots en parallèle, relançable : une chanson sans défaut n'est pas refaite)
Lit lots/<cle>-<n>.json, écrit tunisien/<cle>-<n>.json : {"chansons": {"<index>": {titre, titre_fr, style, paroles,
paroles_chant, paroles_api, controle}}}. Les défauts (mots marocains/algériens, lignes désalignées…) restent notés
dans "controle" pour la relecture par Claude.
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
# Mots typiques du Maroc ou de l'Algérie, à exclure de la derja tunisienne
INTERDITS = ["بزاف", "دابا", "بغيت", "نبغي", "ديال", "ديالي", "واش", "كيراك", "مزيان", "شحال", "هادي", "هاديك", "بصح", "دروك", "ماشي"]
TUNISIENS = ["برشا", "نحب", "شنوة", "توة", "توّة", "باهي", "موش", "فمّا", "فما", "يزّي", "يزي", "علاش", "وقتاش", "كيفاش", "إنتي",
             "انتي", "نعرفش", "ماعادش", "زادة", "زادا", "هوني", "ياسر", "شبيك", "ملّا", "يعيشك", "نمشي"]
IPA = re.compile("[ʃʒħʕχɣθðəɛɪʊːˈʔ]")
TAG = re.compile(r"^\[[^\]]+\]$")
CHAMPS = ("titre", "titre_fr", "style", "paroles", "paroles_chant", "paroles_api", "controle")


def lignes(t):
    return [l.strip() for l in str(t).split("\n") if l.strip()]


def prompt(chansons):
    blocs = "\n\n".join(f"### CHANSON {i}\nTitre : {c['titre']} ({c.get('titre_fr', '')})\nThème : {c.get('theme', '')} — "
                        f"style : {c.get('style', '')}\n{c['paroles']}" for i, c in chansons)
    return f"""Tu es parolier tunisien natif de Tunis. Réécris chaque chanson ci-dessous en DERJA TUNISIENNE authentique (parler de Tunis),
écrite en alphabet arabe, comme la chanterait un artiste tunisien d'aujourd'hui.

RÈGLES
- Garde le sens, les images, la structure et les balises Suno ([Intro], [Verse 1], [Chorus]…) EXACTEMENT : mêmes balises, même nombre de lignes, une ligne pour une ligne. Les indications entre parenthèses (ex. « (Darbuka solo) ») restent en anglais.
- Vrai lexique et vraie grammaire tunisiens : إنتي (tu, masculin et féminin), نحبّك، برشا، شنوة، توّة، باهي، موش، فمّا، يزّي، علاش، وقتاش، ياسر، زادة، هوني، نمشي, négation ما…ش (ما نعرفش).
- INTERDITS (marocain, algérien ou arabe littéraire figé) : {"، ".join(INTERDITS)}.
- Rimes et rythme chantables ; refrain court et mémorable.
- « paroles_chant » : la même chanson en romanisation latine CHANTABLE pour Suno, ligne pour ligne, balises identiques, sans chiffres (pas de 3, 7, 9) : ch, kh, gh, voyelles longues doublées, ex. « nhebbek barcha ».
- « paroles_api » : la transcription phonétique en Alphabet Phonétique International, ligne pour ligne, balises identiques, avec ħ ʕ χ ɣ ʃ ʔ et la gémination notée ː, ex. « nħibːik barʃa ».
- « style » : prompt Suno en anglais de 120 à 200 caractères ; reprends le style d'origine en remplaçant toute mention algérienne ou marocaine par tunisienne et ajoute « Tunisian Arabic vocals ».

FORMAT — réponds UNIQUEMENT avec un JSON valide :
{{"chansons": [{{"num": 1, "titre": "titre en derja (alphabet arabe)", "titre_fr": "traduction française", "style": "...", "paroles": "...", "paroles_chant": "...", "paroles_api": "..."}}]}}

{blocs}"""


def controle(c, origine):
    p, ch, api = lignes(c.get("paroles", "")), lignes(c.get("paroles_chant", "")), lignes(c.get("paroles_api", ""))
    if not p or not ch or not api:
        return ["version manquante"]
    err = []
    if not len(p) == len(ch) == len(api):
        err.append(f"lignes désalignées {len(p)}/{len(ch)}/{len(api)}")
    if [l for l in p if TAG.match(l)] != [l for l in ch if TAG.match(l)]:
        err.append("balises différentes")
    mots = set(re.findall(r"[؀-ۿ]+", " ".join(p)))
    if mots & set(INTERDITS):
        err.append("mots non tunisiens : " + ", ".join(sorted(mots & set(INTERDITS))))
    if len(mots & set(TUNISIENS)) < 2:
        err.append("peu de marqueurs tunisiens")
    if len(IPA.findall(" ".join(api))) < 10:
        err.append("transcription API trop pauvre")
    if re.search(r"[0-9]", " ".join(l for l in ch if not TAG.match(l))):
        err.append("chiffres dans la romanisation")
    if abs(len(p) - len(lignes(origine))) > 4:
        err.append("structure modifiée")
    return err


def lot(f: Path):
    sortie = ICI / "tunisien" / f.name
    src = json.loads(f.read_text(encoding="utf-8"))["chansons"]
    arabes = [(i, c) for i, c in enumerate(src) if c.get("langue") == "ar"]
    if not arabes:
        return None
    fait = json.loads(sortie.read_text(encoding="utf-8"))["chansons"] if sortie.exists() else {}
    a_faire = [(i, c) for i, c in arabes if str(i) not in fait or fait[str(i)]["controle"]]
    for k in range(0, len(a_faire), 4):  # 4 chansons par appel : les 3 versions tiennent dans la limite de sortie
        paquet = a_faire[k:k + 4]
        pf, brut = sortie.with_suffix(f".{k}.prompt.txt"), sortie.with_suffix(f".{k}.raw.txt")
        pf.write_text(prompt([(n + 1, c) for n, (_, c) in enumerate(paquet)]), encoding="utf-8")
        for m in MODELES:
            brut.unlink(missing_ok=True)
            try:
                subprocess.run([sys.executable, str(ASK), str(pf), str(brut)], env={**os.environ, "DIALAGRAM_MODEL": m},
                               cwd=sortie.parent, capture_output=True, timeout=1500)
                t = brut.read_text(encoding="utf-8")
                rep = json.loads(t[t.find("{"):t.rfind("}") + 1])["chansons"]
            except (subprocess.TimeoutExpired, OSError, ValueError, KeyError, TypeError):
                continue
            for r in rep:
                n = int(r.get("num", 0)) - 1 if str(r.get("num", "")).isdigit() else -1
                if not 0 <= n < len(paquet):
                    continue
                i, c = paquet[n]
                r["controle"] = controle(r, c["paroles"])
                ancien = fait.get(str(i))
                if ancien is None or len(r["controle"]) < len(ancien["controle"]):
                    fait[str(i)] = {k2: r.get(k2, "") for k2 in CHAMPS}
            if all(str(i) in fait and not fait[str(i)]["controle"] for i, _ in paquet):
                break
        sortie.write_text(json.dumps({"chansons": fait}, ensure_ascii=False, indent=1), encoding="utf-8")
    return f"{f.name}: {len(fait)}/{len(arabes)} en derja, {sum(bool(v['controle']) for v in fait.values())} à relire"


if __name__ == "__main__":
    (ICI / "tunisien").mkdir(exist_ok=True)
    with ThreadPoolExecutor(int(os.environ.get("PAR", "4"))) as ex:
        for r in ex.map(lot, sorted((ICI / "lots").glob("*-[0-9].json"))):
            if r:
                print(r, flush=True)
    (ICI / "tunisien" / "usage.log").unlink(missing_ok=True)
