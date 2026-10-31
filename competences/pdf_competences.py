#!/usr/bin/env python3
"""Met en page competences.json en PDF lisible (FR · EN · AR · RU), classé par secteur.

Usage : pdf_competences.py [sortie.pdf]
L'arabe est mis en forme (lettres liées, droite à gauche) avec arabic_reshaper + python-bidi.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.doctemplate import BaseDocTemplate, Frame, PageTemplate
from reportlab.platypus.tableofcontents import TableOfContents

ICI = Path(__file__).resolve().parent
F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))
ENCRE, GRIS, ACCENT = colors.HexColor("#1c2421"), colors.HexColor("#5a6560"), colors.HexColor("#2f5d50")
st = {
    "titre": ParagraphStyle("t", fontName="DVB", fontSize=26, leading=32, alignment=TA_CENTER, textColor=ENCRE),
    "sous": ParagraphStyle("s", fontName="DV", fontSize=12, leading=17, alignment=TA_CENTER, textColor=GRIS),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=17, leading=22, textColor=ACCENT, spaceAfter=6),
    "nom": ParagraphStyle("n", fontName="DVB", fontSize=10, leading=13, textColor=ENCRE),
    "ligne": ParagraphStyle("l", fontName="DV", fontSize=8, leading=10.5, textColor=ENCRE),
    "petit": ParagraphStyle("p", fontName="DV", fontSize=7.5, leading=10, textColor=GRIS),
    "corps": ParagraphStyle("c", fontName="DV", fontSize=9.5, leading=13.5, textColor=ENCRE, spaceAfter=5),
}
NIVEAU = {"courant": "courant", "frequent": "fréquent", "specialise": "spécialisé"}
CATEG = {"outil": "outil", "methode": "méthode", "norme": "norme", "metier": "métier", "transverse": "transverse", "langue": "langue"}
RANG = {"courant": 0, "frequent": 1, "specialise": 2}


def x(t: str) -> str:
    """Échappe le XML et met en forme l'arabe (lettres liées, sens droite-gauche)."""
    t = str(t)
    if re.search("[؀-ۿ]", t):
        t = get_display(arabic_reshaper.reshape(t))
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Doc(BaseDocTemplate):
    def __init__(self, f):
        super().__init__(f, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm,
                         title="Dictionnaire des compétences professionnelles", author="Oussama Ghorbel")
        fr = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate("p", [fr], onPage=self.pied)])

    def pied(self, c, d):
        c.saveState()
        c.setFont("DV", 7.5)
        c.setFillColor(GRIS)
        c.drawString(1.6 * cm, 1 * cm, "Dictionnaire des compétences — FR · EN · AR · RU")
        c.drawRightString(A4[0] - 1.6 * cm, 1 * cm, str(d.page))
        c.restoreState()

    def afterFlowable(self, fl):
        if isinstance(fl, Paragraph) and fl.style.name == "h1":
            self.notify("TOCEntry", (0, fl.getPlainText(), self.page))


def fiche(s, noms):
    lab = s["label"]
    tete = f"<b>{x(lab['fr'])}</b>"
    autres = [x(lab[l]) for l in ("en", "ru") if lab[l] != lab["fr"]]
    ar = x(lab["ar"]) if lab["ar"] not in (lab["fr"], lab["en"]) else ""
    rel = ", ".join(x(noms.get(r, r)) for r in s["related"])
    lignes = [
        Paragraph(f"{tete}  <font color='#5a6560' size='8'>{' · '.join(autres)}</font>", st["nom"]),
        Paragraph((f"<font size='9'>{ar}</font>   " if ar else "") +
                  f"<font color='#2f5d50'>{CATEG[s['category']]} · {NIVEAU[s['level']]} · {', '.join(s['topics'])}</font>", st["ligne"]),
        Paragraph("<b>Motifs :</b> " + " · ".join(x(p) for p in s["patterns"]), st["ligne"]),
    ]
    if s["jobs"]:
        lignes.append(Paragraph("<b>Postes :</b> " + ", ".join(x(j) for j in s["jobs"]), st["petit"]))
    if rel:
        lignes.append(Paragraph("<b>Liées :</b> " + rel, st["petit"]))
    return KeepTogether(lignes + [Spacer(1, 7)])


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else str(ICI / "Dictionnaire-competences-FR-EN-AR-RU.pdf")
    d = json.loads((ICI / "competences.json").read_text(encoding="utf-8"))
    secteurs = json.loads((ICI / "secteurs.json").read_text(encoding="utf-8"))
    S = d["skills"]
    noms = {s["id"]: s["label"]["fr"] for s in S}
    flow = [Spacer(1, 6 * cm), Paragraph("Dictionnaire des compétences professionnelles", st["titre"]), Spacer(1, 12),
            Paragraph("Français · English · " + x("العربية") + " · Русский", st["sous"]), Spacer(1, 30),
            Paragraph(f"{len(S)} compétences · {len(secteurs)} secteurs · motifs de détection pour la lecture d'offres d'emploi", st["sous"]),
            Spacer(1, 6 * cm), Paragraph("Généré par Dialagram, contrôlé et consolidé par Claude pour le générateur de CV d'Oussama Ghorbel", st["sous"]),
            PageBreak()]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle("toc", fontName="DV", fontSize=10, leading=15)]
    flow += [Paragraph("Sommaire", st["corps"]), toc, PageBreak()]
    cat, niv = Counter(s["category"] for s in S), Counter(s["level"] for s in S)
    flow += [Paragraph("Comment lire ce dictionnaire", st["h1"]),
             Paragraph("Chaque compétence est rangée dans son secteur principal. Pour chacune : le libellé en français (en gras), "
                       "puis en anglais et en russe ; le libellé arabe ; la catégorie, le niveau et les thèmes ; les <b>motifs</b> "
                       "(formes en minuscules et sans accents qui déclenchent la détection dans une offre, y compris des radicaux russes "
                       "comme « переговор ») ; les postes typiques ; les compétences souvent demandées ensemble.", st["corps"]),
             Paragraph("<b>Niveau</b> : <i>courant</i> = demandé dans la plupart des offres du secteur ; <i>fréquent</i> ; "
                       "<i>spécialisé</i> = demandé pour des postes pointus.", st["corps"]), Spacer(1, 8)]
    lignes = [["Catégorie", "Nombre", "Niveau", "Nombre"]]
    cats, nivs = cat.most_common(), niv.most_common()
    for k in range(max(len(cats), len(nivs))):
        c, n = cats[k] if k < len(cats) else ("", "")
        l, m = nivs[k] if k < len(nivs) else ("", "")
        lignes.append([CATEG.get(c, c), str(n), NIVEAU.get(l, l), str(m)])
    t = Table(lignes, colWidths=[4 * cm, 2.5 * cm, 4 * cm, 2.5 * cm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "DV", 9), ("FONT", (0, 0), (-1, 0), "DVB", 9),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, ACCENT), ("TEXTCOLOR", (0, 0), (-1, -1), ENCRE)]))
    flow += [t, PageBreak()]
    for cle, libelle in secteurs.items():
        groupe = sorted((s for s in S if s["sectors"][0] == cle), key=lambda s: (RANG[s["level"]], s["label"]["fr"].lower()))
        if not groupe:
            continue
        flow += [Paragraph(f"{x(libelle)} ({len(groupe)})", st["h1"])]
        flow += [fiche(s, noms) for s in groupe]
        flow.append(PageBreak())
    Doc(out).multiBuild(flow)
    print("PDF :", out)


if __name__ == "__main__":
    main()
