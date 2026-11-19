#!/usr/bin/env python3
"""Convertit un livre (plan.json + chapitres Markdown) en document Word modifiable, pour la relecture de l'auteur.

Usage : md2docx.py plan.json chapitres_v2 sortie.docx [--auteur "Oussama Ghorbel"] [--annee 2026]
Gère : titres #/##/###, listes à puces et numérotées, **gras**, *italique*, citations >, illustrations ![légende](chemin.png).
"""
import argparse
import json
import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Cm, Pt, RGBColor

BLEU = RGBColor(0x1F, 0x3A, 0x5F)


def runs(par, texte):
    """Ajoute le texte au paragraphe en interprétant **gras** et *italique*."""
    for morceau in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", texte):
        if not morceau:
            continue
        if morceau.startswith("**") and morceau.endswith("**"):
            par.add_run(morceau[2:-2]).bold = True
        elif morceau.startswith("*") and morceau.endswith("*") and len(morceau) > 2:
            par.add_run(morceau[1:-1]).italic = True
        else:
            par.add_run(morceau)


def chapitre(doc, md):
    for ligne in md.split("\n"):
        s = ligne.strip()
        if not s or re.fullmatch(r"-{3,}|\*{3,}|_{3,}", s):
            continue
        m = re.match(r"^!\[(.*)\]\((.+\.(?:png|jpe?g))\)$", s, re.I)
        if m:
            if Path(m.group(2)).exists():
                doc.add_picture(m.group(2), width=Cm(15))
                doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
                if m.group(1):
                    p = doc.add_paragraph()
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p.add_run(m.group(1)).italic = True
            continue
        m = re.match(r"^(#{1,4})\s+(.*)", s)
        if m:
            doc.add_heading(m.group(2).replace("**", ""), level=min(len(m.group(1)), 3))
            continue
        if re.match(r"^[-*•]\s+", s):
            runs(doc.add_paragraph(style="List Bullet"), re.sub(r"^[-*•]\s+", "", s))
        elif re.match(r"^\d+[.)]\s+", s):
            runs(doc.add_paragraph(style="List Number"), re.sub(r"^\d+[.)]\s+", "", s))
        elif s.startswith(">"):
            runs(doc.add_paragraph(style="Quote"), s.lstrip("> "))
        else:
            runs(doc.add_paragraph(), s)


def saut(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("chapitres")
    ap.add_argument("sortie")
    ap.add_argument("--auteur", default="Oussama Ghorbel")
    ap.add_argument("--annee", type=int, default=2026)
    a = ap.parse_args()
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    dossier = Path(a.chapitres)
    doc = Document()
    doc.styles["Normal"].font.name, doc.styles["Normal"].font.size = "Georgia", Pt(11.5)
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.4)
    for niveau in (1, 2, 3):
        doc.styles[f"Heading {niveau}"].font.color.rgb = BLEU

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run(plan.get("titre", ""))
    r.bold, r.font.size, r.font.color.rgb = True, Pt(30), BLEU
    doc.add_paragraph(plan.get("sous_titre", "")).alignment = WD_ALIGN_PARAGRAPH.CENTER
    au = doc.add_paragraph()
    au.alignment = WD_ALIGN_PARAGRAPH.CENTER
    au.add_run(a.auteur).font.size = Pt(16)
    doc.add_paragraph(f"© {a.annee} {a.auteur}. Tous droits réservés. Première édition.").alignment = WD_ALIGN_PARAGRAPH.CENTER

    fichiers = [dossier / "00_introduction.md"]
    for p in plan["parties"]:
        fichiers.append(p["titre"])
        fichiers += [dossier / f"ch{int(c['numero']):02d}.md" for c in p["chapitres"]]
    fichiers.append(dossier / "99_conclusion.md")
    for f in fichiers:
        saut(doc)
        if isinstance(f, str):
            doc.add_heading(f, level=1).alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif f.exists():
            chapitre(doc, f.read_text(encoding="utf-8"))

    if plan.get("bibliographie"):
        saut(doc)
        doc.add_heading("Bibliographie commentée", level=1)
        for b in plan["bibliographie"]:
            p = doc.add_paragraph(style="List Bullet")
            p.add_run(f"{b.get('auteur', '')} — ").bold = True
            p.add_run(str(b.get("titre", ""))).italic = True
            p.add_run(f" ({b.get('annee', '')}). {b.get('idee', '')}")
    doc.save(a.sortie)
    print("DOCX :", a.sortie)


if __name__ == "__main__":
    main()
