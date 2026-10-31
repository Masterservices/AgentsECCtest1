#!/usr/bin/env python3
"""Nettoie, valide et fusionne les dictionnaires de compétences générés par secteur.

Usage : valider.py
Lit secteurs/<cle>.json, écrit competences.json (dictionnaire fusionné) et rapport.md.
Applique les règles du prompt : patterns en minuscules sans accents (3 à 10), motifs courts
ambigus et mots trop généraux retirés, related limités aux id existants, énumérations vérifiées.
"""
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ICI = Path(__file__).resolve().parent
CATEGORIES = {"outil", "methode", "norme", "metier", "transverse", "langue"}
CAT_ALIAS = {"outils": "outil", "logiciel": "outil", "methodes": "methode", "methodologie": "methode", "certification": "norme",
             "normes": "norme", "savoir-faire": "metier", "competence-metier": "metier", "transversal": "transverse",
             "transversale": "transverse", "soft-skill": "transverse", "langues": "langue"}
LEVELS = {"courant", "frequent", "specialise"}
TOPICS = {"web", "seo", "marketing", "business", "project", "consulting", "erp", "textile", "quality", "engineering", "data",
          "ai", "finance", "rh", "logistique", "sante", "juridique", "education", "btp", "hotellerie", "industrie", "design"}
# motifs courts trop ambigus (mots courants ou sigles à plusieurs sens)
AMBIGU = {"ai", "it", "pm", "ia", "po", "pr", "ba", "ma", "rd", "ca", "cv", "bi", "go", "c", "r", "re", "da", "ip", "ui",
          "les", "des", "and", "the", "for", "app", "web", "art", "net", "pro", "mai", "son", "sa", "si", "rp", "on", "ar",
          "ок", "по", "из", "на", "في", "من", "على"}
COURTS_OK = {"c#", "ux", "3d", "2d", "qa", "hr", "rh", "f#"}
# mots seuls trop généraux (faux positifs)
GENERIQUES = {"gestion", "client", "clients", "qualite", "projet", "projets", "service", "services", "equipe", "travail",
              "management", "communication", "organisation", "analyse", "vente", "ventes", "suivi", "conception", "production",
              "developpement", "formation", "strategie", "marketing", "commercial", "technique", "administration", "support",
              "customer", "quality", "project", "team", "work", "sales", "analysis", "development", "design",
              "управлен", "клиент", "качеств", "проект", "команд", "работ", "продаж", "анализ",
              "ادارة", "إدارة", "عميل", "جودة", "مشروع", "فريق", "عمل", "تحليل"}


def sans_accents(s: str) -> str:
    """Minuscules sans accents latins ; garde й (russe), ё -> е ; retire les voyelles courtes arabes."""
    out = []
    for ch in s.lower():
        if ch == "ё":
            out.append("е")
        elif "LATIN" in unicodedata.name(ch, ""):
            out.append("".join(c for c in unicodedata.normalize("NFKD", ch) if not unicodedata.combining(c)))
        elif "ً" <= ch <= "ٟ" or ch in ("ٰ", "ـ"):
            continue
        else:
            out.append(ch)
    s = "".join(out).replace("œ", "oe").replace("æ", "ae").replace("’", "'")
    return re.sub(r"\s+", " ", s).strip()


def norm_id(s: str) -> str:
    s = sans_accents(str(s)).replace("+", "plus").replace("#", "sharp").replace(".", "-")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")


def nettoyer_patterns(pats, label, notes):
    vus, garde = set(), []
    for p in pats or []:
        p = sans_accents(str(p))
        if not p or p in vus:
            continue
        vus.add(p)
        if (len(p) <= 2 and p not in COURTS_OK) or p in AMBIGU:
            notes["motif court ambigu retiré"] += 1
            continue
        if p in GENERIQUES:
            notes["mot trop général retiré"] += 1
            continue
        garde.append(p)
    # compléter avec les libellés si moins de 3 motifs
    for lang in ("fr", "en", "ru", "ar"):
        if len(garde) >= 3:
            break
        p = sans_accents(label.get(lang, ""))
        if p and p not in garde and p not in GENERIQUES and len(p) > 3:
            garde.append(p)
            notes["motif ajouté depuis le libellé"] += 1
    if len(garde) > 10:
        notes["motifs tronqués à 10"] += 1
    return garde[:10]


def nettoyer(sk, cle, notes):
    sid = norm_id(sk.get("id") or (sk.get("label") or {}).get("en", ""))
    if not sid:
        return None
    lab = sk.get("label") if isinstance(sk.get("label"), dict) else {}
    base = lab.get("en") or lab.get("fr") or sid
    label = {l: str(lab.get(l) or base).strip() for l in ("fr", "en", "ar", "ru")}
    if any(not lab.get(l) for l in ("fr", "en", "ar", "ru")):
        notes["libellé manquant complété"] += 1
    cat = norm_id(sk.get("category", ""))
    cat = CAT_ALIAS.get(cat, cat)
    if cat not in CATEGORIES:
        notes["catégorie invalide -> metier"] += 1
        cat = "metier"
    lvl = sans_accents(str(sk.get("level", "")))
    if lvl not in LEVELS:
        notes["niveau invalide -> frequent"] += 1
        lvl = "frequent"
    topics = []
    for t in sk.get("topics") or []:
        t = norm_id(t).replace("-", "")
        if t and t not in topics and (t in TOPICS or t.isalpha()):
            topics.append(t)
    topics = topics[:3] or [cle]
    jobs = [str(j).strip() for j in (sk.get("jobs") or []) if str(j).strip()][:5]
    return {"id": sid, "label": label, "patterns": nettoyer_patterns(sk.get("patterns"), label, notes), "category": cat,
            "topics": topics, "level": lvl, "related": [norm_id(r) for r in (sk.get("related") or []) if norm_id(r)],
            "jobs": jobs, "sectors": [cle]}


def fusionner(a, b):
    for p in b["patterns"]:
        if p not in a["patterns"] and len(a["patterns"]) < 10:
            a["patterns"].append(p)
    for k, n in (("topics", 3), ("jobs", 5), ("related", 8), ("sectors", 30)):
        for v in b[k]:
            if v not in a[k] and len(a[k]) < n:
                a[k].append(v)
    rang = {"courant": 0, "frequent": 1, "specialise": 2}
    a["level"] = min(a["level"], b["level"], key=rang.get)


def main():
    secteurs = json.loads((ICI / "secteurs.json").read_text(encoding="utf-8"))
    skills, par_secteur, notes = {}, {}, Counter()
    alias = {}  # libellé anglais normalisé -> id retenu (fusion des quasi-doublons ms-excel / excel)
    for cle in secteurs:
        f = ICI / "secteurs" / f"{cle}.json"
        if not f.exists():
            par_secteur[cle] = None
            continue
        brut = json.loads(f.read_text(encoding="utf-8"))
        n = 0
        for sk in brut.get("skills", []):
            s = nettoyer(sk, cle, notes)
            if not s:
                notes["compétence sans id ignorée"] += 1
                continue
            n += 1
            cle_alias = norm_id(s["label"]["en"])
            sid = s["id"] if s["id"] in skills else alias.get(cle_alias, s["id"])
            if sid in skills:
                notes["doublon fusionné"] += 1
                fusionner(skills[sid], s)
            else:
                skills[sid] = s
                alias.setdefault(cle_alias, sid)
        par_secteur[cle] = (n, brut.get("model", ""))
    # related : uniquement des id existants, sans soi-même, 6 au plus
    ids = set(skills)
    for s in skills.values():
        rel = []
        for r in s["related"]:
            r = r if r in ids else alias.get(r)
            if r and r != s["id"] and r not in rel:
                rel.append(r)
        notes["related inexistant retiré"] += len(s["related"]) - len(rel)
        s["related"] = rel[:6]
    # motifs partagés entre plusieurs compétences (risque de double détection)
    usage = defaultdict(list)
    for s in skills.values():
        for p in s["patterns"]:
            usage[p].append(s["id"])
    partages = {p: v for p, v in usage.items() if len(v) > 1}
    liste = sorted(skills.values(), key=lambda s: s["id"])
    out = {"version": 1, "languages": ["fr", "en", "ar", "ru"], "topics": sorted({t for s in liste for t in s["topics"]}),
           "count": len(liste), "skills": liste}
    (ICI / "competences.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    faibles = [s["id"] for s in liste if len(s["patterns"]) < 3]
    peu_rel = [s["id"] for s in liste if len(s["related"]) < 3]
    lignes = ["# Rapport — dictionnaire de compétences", "",
              f"**{len(liste)} compétences uniques** après fusion de {sum(1 for v in par_secteur.values() if v)} secteurs.", "",
              "| Secteur | Compétences générées | Modèle |", "|---|---|---|"]
    for cle, v in par_secteur.items():
        lignes.append(f"| {secteurs[cle]} | {v[0] if v else 'MANQUANT'} | {v[1] if v else ''} |")
    lignes += ["", "## Corrections automatiques", ""] + [f"- {k} : {n}" for k, n in notes.most_common()]
    lignes += ["", "## Points à surveiller", "", f"- Compétences avec moins de 3 motifs : {len(faibles)} {faibles[:20]}",
               f"- Compétences avec moins de 3 related : {len(peu_rel)}",
               f"- Motifs partagés par plusieurs compétences : {len(partages)}"] + \
              [f"  - `{p}` → {', '.join(v)}" for p, v in sorted(partages.items())[:40]]
    lignes += ["", "## Répartition", "", f"- Catégories : {dict(Counter(s['category'] for s in liste))}",
               f"- Niveaux : {dict(Counter(s['level'] for s in liste))}"]
    (ICI / "rapport.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print("\n".join(lignes[:6 + len(par_secteur)]))
    print("corrections:", dict(notes))


if __name__ == "__main__":
    main()
