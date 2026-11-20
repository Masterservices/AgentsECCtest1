#!/usr/bin/env python3
"""Met en page un tome de l'édition « Le russe en 10 000 mots » (une page ou plus par mot) et exporte les cartes mémoire.

Usage : livre.py DEBUT FIN [--tome 1]
Sorties : Le-russe-en-10000-mots-Tome-N-Oussama-Ghorbel.pdf et cartes-tomeN.json (entrées complètes + cartes recto/verso).
"""
import json
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.doctemplate import BaseDocTemplate, Frame, PageTemplate

ICI = Path(__file__).resolve().parent
F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", "/usr/share/fonts/truetype/freefont/FreeSansOblique.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")
ENCRE, GRIS, ROUGE, BLEU, FOND, FOND2 = (colors.HexColor(c) for c in ("#1d2430", "#5b6472", "#8c1f2f", "#1f3a5f", "#f6e9eb", "#eef2f6"))
ST = {
    "titre": ParagraphStyle("t", fontName="DVB", fontSize=28, leading=34, alignment=TA_CENTER, textColor=ENCRE),
    "sous": ParagraphStyle("s", fontName="DV", fontSize=13, leading=18, alignment=TA_CENTER, textColor=GRIS),
    "rang": ParagraphStyle("r", fontName="DV", fontSize=8.5, leading=11, textColor=GRIS),
    "mot": ParagraphStyle("m", fontName="DVB", fontSize=30, leading=36, textColor=ROUGE, spaceBefore=2),
    "pron": ParagraphStyle("p", fontName="DV", fontSize=11, leading=15, textColor=ENCRE),
    "nat": ParagraphStyle("n", fontName="DVI", fontSize=10, leading=14, textColor=GRIS, spaceAfter=6),
    "h": ParagraphStyle("h", fontName="DVB", fontSize=10.5, leading=14, textColor=BLEU, spaceBefore=9, spaceAfter=3),
    "corps": ParagraphStyle("c", fontName="DV", fontSize=9.2, leading=12.6, textColor=ENCRE),
    "cell": ParagraphStyle("ce", fontName="DV", fontSize=8.6, leading=11.2, textColor=ENCRE),
    "carte": ParagraphStyle("ca", fontName="DV", fontSize=8.8, leading=12, textColor=ENCRE, backColor=FOND, borderPadding=6,
                            spaceBefore=10),
}


def x(t):
    return str(t if t is not None else "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def liste(v):
    """Valeurs d'un champ qui peut être une liste, un dictionnaire ou une chaîne."""
    if isinstance(v, dict):
        return [str(w) for w in v.values()]
    if isinstance(v, list):
        return [str(w) for w in v]
    return [str(v)] if v else []


def tab(lignes, largeurs, entete=True):
    t = Table([[c if isinstance(c, Paragraph) else Paragraph(x(c), ST["cell"]) for c in l] for l in lignes], colWidths=largeurs)
    s = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#d5dbe5")),
         ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    if entete:
        s += [("BACKGROUND", (0, 0), (-1, 0), FOND2)]
    t.setStyle(TableStyle(s))
    return t


class Livre(BaseDocTemplate):
    def __init__(self, f, titre):
        super().__init__(f, pagesize=A4, leftMargin=1.9 * cm, rightMargin=1.9 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm,
                         title=titre, author="Oussama Ghorbel")
        self.titre, self.mot = titre, ""
        # pied de page dessiné en fin de page, pour afficher le mot de la page en cours
        self.addPageTemplates([PageTemplate("p", [Frame(self.leftMargin, self.bottomMargin, self.width, self.height)],
                                            onPageEnd=self.pied)])

    def pied(self, c, d):
        c.saveState()
        c.setFont("DV", 7.3)
        c.setFillColor(GRIS)
        c.drawString(1.9 * cm, 0.95 * cm, f"{self.titre} — © 2026 Oussama Ghorbel")
        c.drawRightString(A4[0] - 1.9 * cm, 0.95 * cm, f"{self.mot}   {d.page}")
        c.restoreState()

    def afterFlowable(self, fl):
        if isinstance(fl, Paragraph) and fl.style.name == "m":
            self.mot = fl.getPlainText()


def formes(e, W):
    f, nat = e.get("formes") or {}, e.get("nature", "")
    out = []
    if nat == "verbe" and f.get("present"):
        pr = liste(f["present"])
        lignes = [["", "Présent (futur pour un perfectif)"]]
        lignes += [[p, pr[i] if i < len(pr) else ""] for i, p in enumerate(["я", "ты", "он / она", "мы", "вы", "они"])]
        out.append(tab(lignes, [W * 0.25, W * 0.75]))
        if f.get("passe"):
            out.append(Paragraph("<b>Passé</b> (m, f, n, pl) : " + x(" / ".join(liste(f["passe"]))), ST["corps"]))
        if f.get("imperatif"):
            out.append(Paragraph("<b>Impératif</b> : " + x(" / ".join(liste(f["imperatif"]))), ST["corps"]))
    elif nat == "nom" and isinstance(f.get("declinaison"), dict):
        lignes = [["Cas", "Singulier", "Pluriel"]]
        for k, v in f["declinaison"].items():
            if isinstance(v, dict):
                vs = list(v.values())
                lignes.append([k, v.get("singulier") or v.get("sg") or (vs[0] if vs else ""),
                               v.get("pluriel") or v.get("pl") or (vs[1] if len(vs) > 1 else "")])
        if len(lignes) > 1:
            out.append(tab(lignes, [W * 0.3, W * 0.35, W * 0.35]))
        if f.get("genre"):
            out.append(Paragraph(f"<b>Genre</b> : {x(f['genre'])}", ST["corps"]))
    elif f:
        out.append(Paragraph(x(" · ".join(f"{k} : {', '.join(liste(v))}" for k, v in f.items() if v)), ST["corps"]))
    return out


def entree(e, W):
    fl = [Paragraph(f"Mot n° {e['rang']} · {e.get('frequence', 0):,} occurrences · niveau {x(e.get('niveau', ''))}".replace(",", " "),
                    ST["rang"]),
          Paragraph(x(e.get("mot") or e["lemme"]), ST["mot"]),
          Paragraph(f"‹ {x(e.get('translit', ''))} ›   {x(e.get('api', ''))}", ST["pron"])]
    nat = e.get("nature", "")
    if e.get("aspect"):
        nat += f", {e['aspect']}" + (f" · paire : {e['paire']}" if e.get("paire") else "")
    fl.append(Paragraph(x(nat), ST["nat"]))
    fl.append(Paragraph("1. Sens et équivalents en français", ST["h"]))
    lignes = [["Sens", "Équivalents", "Exemples"]]
    for i, s in enumerate(e.get("sens") or [], 1):
        ex = "<br/>".join(f"{x(p.get('ru'))}<br/><font color='#5b6472'><i>{x(p.get('fr'))}</i></font>"
                          for p in s.get("exemples") or [] if isinstance(p, dict))
        lignes.append([Paragraph(f"<b>{i}.</b> {x(s.get('sens'))}", ST["cell"]),
                       Paragraph(x(", ".join(liste(s.get("equivalents")))), ST["cell"]), Paragraph(ex, ST["cell"])])
    fl.append(tab(lignes, [W * 0.27, W * 0.22, W * 0.51]))
    syn, ant = e.get("synonymes") or [], e.get("antonymes") or []
    if syn or ant:
        fl.append(Paragraph("2. Mots russes de même sens", ST["h"]))
        for s in syn:
            mot, nu = (s.get("mot", ""), s.get("nuance", "")) if isinstance(s, dict) else (s, "")
            fl.append(Paragraph(f"• <b>{x(mot)}</b>" + (f" : {x(nu)}" if nu else ""), ST["corps"]))
        if ant:
            fl.append(Paragraph("<b>Contraires</b> : " + x(", ".join(a if isinstance(a, str) else a.get("mot", "") for a in ant)),
                                ST["corps"]))
    fo = formes(e, W)
    if fo:
        fl += [Paragraph("3. Conjugaison" if e.get("nature") == "verbe" else "3. Formes", ST["h"])] + fo
    if e.get("pieges"):
        fl.append(Paragraph("4. Pièges pour un francophone", ST["h"]))
        fl += [Paragraph("• " + x(p), ST["corps"]) for p in liste(e["pieges"])]
    ex = [p for p in e.get("expressions") or [] if isinstance(p, dict)]
    fa = [p for p in e.get("famille") or [] if isinstance(p, dict)]
    if ex or fa:
        fl.append(Paragraph("5. Expressions et famille du mot", ST["h"]))
        if ex:
            fl.append(Paragraph("<b>Expressions</b> : " + " ; ".join(f"{x(p.get('ru'))} (<i>{x(p.get('fr'))}</i>)" for p in ex), ST["corps"]))
        if fa:
            fl.append(Paragraph("<b>Famille</b> : " + ", ".join(f"{x(p.get('mot'))} (<i>{x(p.get('fr'))}</i>)" for p in fa), ST["corps"]))
    s0 = (e.get("sens") or [{}])[0]
    fl.append(Paragraph(f"<b>Carte mémoire</b> — recto : {x(e.get('mot'))}  ·  verso : {x(', '.join(liste(s0.get('equivalents'))[:2]))}"
                        f"  ·  {len(e.get('sens') or [])} carte(s), une par sens", ST["carte"]))
    return fl + [PageBreak()]


def cartes(entrees):
    out = []
    for e in entrees:
        for i, s in enumerate(e.get("sens") or [], 1):
            ex = next((p for p in s.get("exemples") or [] if isinstance(p, dict)), {})
            out.append({"id": f"ru-{e['rang']:05d}-{i}", "rang": e["rang"], "niveau": e.get("niveau"), "recto": e.get("mot"),
                        "verso": ", ".join(liste(s.get("equivalents"))), "sens": s.get("sens"),
                        "exemple_ru": ex.get("ru"), "exemple_fr": ex.get("fr"), "translit": e.get("translit"), "api": e.get("api")})
    return out


def main():
    debut, fin = int(sys.argv[1]), int(sys.argv[2])
    tome = int(sys.argv[sys.argv.index("--tome") + 1]) if "--tome" in sys.argv else 1
    entrees = []
    for f in sorted((ICI / "entrees").glob("[0-9][0-9][0-9][0-9].json")):
        entrees += [e for e in json.loads(f.read_text(encoding="utf-8")) if e and debut <= e["rang"] <= fin and e.get("sens")]
    entrees.sort(key=lambda e: e["rang"])
    titre = f"Le russe en 10 000 mots — Tome {tome}"
    pdf = ICI / f"Le-russe-en-10000-mots-Tome-{tome}-Oussama-Ghorbel.pdf"
    doc = Livre(str(pdf), titre)
    W = doc.width
    fl = [Spacer(1, 5 * cm), Paragraph("Le russe en 10 000 mots", ST["titre"]), Spacer(1, 10),
          Paragraph(f"Tome {tome} — les mots {debut} à {fin}, du plus fréquent au moins fréquent", ST["sous"]), Spacer(1, 8),
          Paragraph("Dictionnaire d'apprentissage russe-français pour francophones", ST["sous"]),
          Spacer(1, 5 * cm), Paragraph("Oussama Ghorbel", ST["sous"]), PageBreak(),
          Paragraph("Comment utiliser ce livre", ST["h"]),
          Paragraph("Chaque mot ouvre une nouvelle page. Les mots sont classés par fréquence réelle d'emploi : en maîtrisant les 1 000 "
                    "premiers, vous comprenez la grande majorité des mots d'une conversation courante. Pour chaque mot : l'accent tonique "
                    "(marqué d'un accent aigu, et en majuscules dans la translittération), la prononciation en Alphabet Phonétique "
                    "International, ses différents sens avec leurs équivalents français et des exemples, les mots russes de sens voisin "
                    "et leurs nuances, les formes grammaticales (conjugaison ou déclinaison), les pièges propres aux francophones, les "
                    "expressions courantes et la famille du mot. L'encadré « Carte mémoire » résume ce que l'application fait "
                    "réviser : une carte par sens.", ST["corps"]), Spacer(1, 6),
          Paragraph("Source de la fréquence : liste FrequencyWords d'Hermit Dave (sous-titres OpenSubtitles 2018, licence MIT), "
                    "regroupée par forme de base avec l'analyseur morphologique pymorphy3. Les noms propres sont exclus.", ST["corps"]),
          Spacer(1, 6),
          Paragraph("© 2026 Oussama Ghorbel. Tous droits réservés. Ouvrage conçu et dirigé par Oussama Ghorbel, rédigé avec "
                    "l'assistance d'outils d'intelligence artificielle ; formes grammaticales contrôlées automatiquement avec pymorphy3.",
                    ST["corps"]), PageBreak()]
    for e in entrees:
        fl += entree(e, W)
    fl.append(Paragraph("Index alphabétique", ST["h"]))
    fl.append(Paragraph(" · ".join(f"{x(e.get('mot'))} {e['rang']}" for e in sorted(entrees, key=lambda e: e["lemme"])), ST["corps"]))
    doc.build(fl)
    c = cartes(entrees)
    (ICI / f"cartes-tome{tome}.json").write_text(json.dumps({"edition": "Le russe en 10 000 mots", "auteur": "Oussama Ghorbel",
                                                               "tome": tome, "rangs": [debut, fin], "mots": entrees, "cartes": c},
                                                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(entrees)} mots | PDF {pdf.name} | {len(c)} cartes")


if __name__ == "__main__":
    main()
