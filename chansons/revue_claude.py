#!/usr/bin/env python3
"""Relecture par Claude des chansons en derja tunisienne.

Usage : revue_claude.py export [N]   → revue/lot-1..N.json (les chansons arabes retenues dans le livre) + revue/GUIDE.md
        revue_claude.py merge        → applique revue/corrige-*.json dans tunisien/<lot>.json (contrôle refait, relu_claude=true)
Schéma d'un élément : {ref: "<lot>.json#<index>", titre, titre_fr, paroles, paroles_chant, paroles_api}
"""
import json
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
REVUE = ICI / "revue"
CHAMPS = ("titre", "titre_fr", "paroles", "paroles_chant", "paroles_api")
GUIDE = """# Guide de relecture — derja tunisienne (parler de Tunis)

Tu corriges des paroles de chansons pour qu'elles sonnent comme écrites par un parolier tunisien natif.

## Règles de fond
- Garde le sens, les images, les rimes autant que possible, les balises Suno ([Intro], [Verse 1]…) et les indications entre
  parenthèses en anglais. MÊME NOMBRE DE LIGNES dans les trois versions, ligne pour ligne.
- Remplace toute forme d'arabe littéral ou d'un autre dialecte par la forme tunisienne :
  danser → شطح (نشطحو) ; vouloir/aimer → نحب ; maintenant → توّة ; quoi → شنوّة ; comment → كيفاش ; pourquoi → علاش ;
  quand → وقتاش ; où → وين ; il y a → فمّا ; pas → موش / ما…ش ; beaucoup → برشا ; assez → يزّي ; aussi → زادة ;
  viens → إيجا ; je → آنا ; nous → أحنا ; vous → إنتوما ; ils → هوما ; tu (m. et f.) → إنتي ; famille → العايلة ;
  plage → البحر / الشط ; amis → الصحاب ; fille → طفلة / بنيّة ; garçon → طفل / ولد ; bien → باهي.
- Grammaire : futur باش + verbe ; progressif قاعد + verbe ; 1re pers. du pluriel en -و (نمشيو، نشطحو) ; négation ما…ش.
- Interdits : سوف، لن، لم، الذي، أريد، ماذا، لماذا، الآن، جدًّا، كيف (littéral), بزاف، دابا، بغيت، ديال، واش, et tout mot
  inventé ou sans sens. Si un vers n'a pas de sens, réécris-le simplement en gardant l'idée.
- Orthographe tunisienne courante : عايلة (pas عائلة), ما نعرفش, الصحاب.

## Romanisation chantable (paroles_chant) — pour Suno
- Lettres latines seulement, AUCUN chiffre : ch = ش, kh = خ, gh = غ, h = ح et ه, q = ق, ' = ع (ou rien),
  voyelles longues aa, ii, ou. Exemple : « nhebbek barcha, ya qalbi ».

## Transcription API (paroles_api) — convention unique pour tout le livre
- Consonnes : ت t · ث θ · ج ʒ · ح ħ · خ χ · د d · ذ ð · ر r · ز z · س s · ش ʃ · ص sˤ · ض/ظ ðˤ · ط tˤ · ع ʕ · غ ɣ · ف f ·
  ق q (Tunis) · ك k · ل l · م m · ن n · ه h · و w · ي j · ء ʔ (souvent muet).
- Voyelles : a i u (brèves), aː iː uː (longues), eː pour l'imala tunisienne (باب → beːb), ə pour une voyelle réduite.
  N'utilise PAS æ ɛ ɑ.
- Gémination et chadda : consonne suivie de ː (ħubː, nħibːik). Article assimilé : əʃːams, əlbħar.
- Ne transcris jamais ت par θ ni ق par ʔ ou g.

## Sortie
Un fichier JSON : la liste des objets {ref, titre, titre_fr, paroles, paroles_chant, paroles_api} dans le même ordre,
`ref` inchangé, sans aucun texte autour.
"""


def exporter(n_lots):
    from livre_chansons import charger
    _, tout, _ = charger()
    REVUE.mkdir(exist_ok=True)
    (REVUE / "GUIDE.md").write_text(GUIDE, encoding="utf-8")
    # retrouve la référence <lot>#<index> de chaque chanson du livre par le début de ses paroles
    refs = {}
    for f in sorted((ICI / "lots").glob("*-[0-9].json")):
        for i, c in enumerate(json.loads(f.read_text(encoding="utf-8"))["chansons"]):
            refs.setdefault(c["paroles"].strip()[:80], f"{f.name}#{i}")
    for f in sorted((ICI / "tunisien").glob("*-[0-9].json")):
        for k, v in json.loads(f.read_text(encoding="utf-8"))["chansons"].items():
            refs[v["paroles"].strip()[:80]] = f"{f.name}#{k}"
    arabes = [{"ref": refs.get(c["paroles"][:80]), **{k: c[k] for k in CHAMPS}} for c in tout if c["langue"] == "ar"]
    taille = -(-len(arabes) // n_lots)
    for k in range(n_lots):
        (REVUE / f"lot-{k + 1}.json").write_text(json.dumps(arabes[k * taille:(k + 1) * taille], ensure_ascii=False, indent=1),
                                                 encoding="utf-8")
    print(f"{len(arabes)} chansons en {n_lots} lots ; sans référence : {sum(not a['ref'] for a in arabes)}")


def fusionner():
    import tunisien
    faits, rejets = 0, []
    for f in sorted(REVUE.glob("corrige-*.json")):
        for c in json.loads(f.read_text(encoding="utf-8")):
            lot, _, idx = str(c.get("ref", "")).partition("#")
            if not lot or not idx.isdigit():
                rejets.append((c.get("ref"), "référence invalide"))
                continue
            src = json.loads((ICI / "lots" / lot).read_text(encoding="utf-8"))["chansons"][int(idx)]
            ft = ICI / "tunisien" / lot
            d = json.loads(ft.read_text(encoding="utf-8")) if ft.exists() else {"chansons": {}}
            nouveau = {**d["chansons"].get(idx, {}), **{k: c[k] for k in CHAMPS if c.get(k)}}
            nouveau["controle"] = tunisien.controle(nouveau, src["paroles"])
            if any(m in e for e in nouveau["controle"] for m in ("lignes", "manquante", "balises")):
                rejets.append((c["ref"], nouveau["controle"]))
                continue
            nouveau["relu_claude"] = True
            d["chansons"][idx] = nouveau
            ft.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
            faits += 1
    print(f"{faits} chansons relues intégrées ; rejetées : {rejets}")


if __name__ == "__main__":
    if sys.argv[1:2] == ["export"]:
        exporter(int(sys.argv[2]) if len(sys.argv) > 2 else 8)
    elif sys.argv[1:2] == ["merge"]:
        fusionner()
    else:
        print(__doc__)
