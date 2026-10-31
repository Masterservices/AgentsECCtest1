#!/usr/bin/env python3
"""Assemble les lots de chansons en un livre PDF classé par genre puis par tempo, et en chansons.json.

Usage : livre_chansons.py
Contrôle : titres en double retirés, BPM ramené dans la plage du genre, BPM présent dans le style Suno.
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether, NextPageTemplate, PageBreak, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.doctemplate import BaseDocTemplate, Frame, PageTemplate
from reportlab.platypus.tableofcontents import TableOfContents

ICI = Path(__file__).resolve().parent
D = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", D + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", D + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVM", D + "DejaVuSansMono.ttf"))
ENCRE, GRIS, ACCENT, FOND = colors.HexColor("#1c2421"), colors.HexColor("#5a6560"), colors.HexColor("#7a2e5f"), colors.HexColor("#f3eef2")
ST = {
    "titre": ParagraphStyle("t", fontName="DVB", fontSize=30, leading=36, alignment=TA_CENTER, textColor=ENCRE),
    "sous": ParagraphStyle("s", fontName="DV", fontSize=12, leading=17, alignment=TA_CENTER, textColor=GRIS),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=18, leading=23, textColor=ACCENT, spaceAfter=4),
    "corps": ParagraphStyle("c", fontName="DV", fontSize=9.5, leading=14, textColor=ENCRE, spaceAfter=5),
    "num": ParagraphStyle("n", fontName="DVB", fontSize=11, leading=14, textColor=ENCRE, spaceBefore=4),
    "meta": ParagraphStyle("m", fontName="DV", fontSize=7.3, leading=9.5, textColor=GRIS),
    "style": ParagraphStyle("st", fontName="DVM", fontSize=6.8, leading=8.8, textColor=ENCRE, backColor=FOND, borderPadding=3,
                            spaceBefore=3, spaceAfter=5),
    "tag": ParagraphStyle("tg", fontName="DVB", fontSize=7.3, leading=10, textColor=ACCENT, spaceBefore=3),
    "vers": ParagraphStyle("v", fontName="DV", fontSize=8, leading=10.6, textColor=ENCRE),
    "vers_ar": ParagraphStyle("va", fontName="DV", fontSize=8.6, leading=11.2, textColor=ENCRE, alignment=TA_RIGHT),
    "idx": ParagraphStyle("i", fontName="DV", fontSize=7.4, leading=9.6, textColor=ENCRE),
}
LANG = {"fr": "français", "en": "anglais", "ar": "arabe"}
TEMPOS = [("Lent (moins de 80 BPM)", 0, 79), ("Modéré (80 à 109 BPM)", 80, 109), ("Rapide (110 à 129 BPM)", 110, 129),
          ("Très rapide (130 BPM et plus)", 130, 999)]
ARABE = re.compile("[؀-ۿ]")
# DejaVu n'a pas le glyphe de la ligature « Allah » (U+FDF2) : on la désactive
RESHAPER = arabic_reshaper.ArabicReshaper(configuration={"ARABIC LIGATURE ALLAH": False})


def x(t):
    """Échappe le XML et met en forme l'arabe (lettres liées, droite à gauche)."""
    t = str(t)
    if ARABE.search(t):
        t = get_display(RESHAPER.reshape(t))
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cle_titre(t):
    t = unicodedata.normalize("NFKD", str(t).lower())
    return re.sub(r"[\W_]+", "", "".join(c for c in t if not unicodedata.combining(c)))


def charger():
    genres = json.loads((ICI / "genres.json").read_text(encoding="utf-8"))
    vus, notes, tout = set(), Counter(), []
    for g in genres:
        lot = []
        for f in sorted((ICI / "lots").glob(f"{g['cle']}-[0-9].json")):
            lot += json.loads(f.read_text(encoding="utf-8"))["chansons"]
        for c in lot:
            k = cle_titre(c["titre"])
            if sum(x["genre"] == g["cle"] for x in tout) >= 40:
                break
            if k in vus:
                notes["titre en double retiré"] += 1
                continue
            vus.add(k)
            m = re.search(r"\d+", str(c.get("bpm", "")))
            bpm = int(m.group()) if m else sum(g["bpm"]) // 2
            b2 = min(max(bpm, g["bpm"][0]), g["bpm"][1])
            if b2 != bpm:
                notes["BPM ramené dans la plage du genre"] += 1
            style = re.sub(r"\b\d{2,3}\s*bpm\b", f"{b2} BPM", str(c.get("style") or g["style"]), flags=re.I)
            if "bpm" not in style.lower():
                style = style.rstrip(", ") + f", {b2} BPM"
            langue = c.get("langue") if c.get("langue") in LANG else ("ar" if ARABE.search(c["paroles"]) else "fr")
            tout.append({"genre": g["cle"], "genre_nom": g["nom"], "titre": c["titre"].strip(), "titre_fr": (c.get("titre_fr") or "").strip(),
                         "langue": langue, "theme": c.get("theme", ""), "bpm": b2, "tonalite": c.get("tonalite", ""),
                         "ambiance": c.get("ambiance", ""), "style": style.strip(), "resume_fr": c.get("resume_fr", ""),
                         "paroles": c["paroles"].strip()})
    ordre = {g["cle"]: i for i, g in enumerate(genres)}
    tout.sort(key=lambda c: (ordre[c["genre"]], c["bpm"], cle_titre(c["titre"])))
    for i, c in enumerate(tout, 1):
        c["numero"] = i
    return genres, tout, notes


class Livre(BaseDocTemplate):
    def __init__(self, f):
        super().__init__(f, pagesize=A4, leftMargin=1.4 * cm, rightMargin=1.4 * cm, topMargin=1.5 * cm, bottomMargin=1.5 * cm,
                         title="1000 chansons pour Suno", author="Oussama Ghorbel")
        w, h = self.width, self.height
        col = (w - 0.8 * cm) / 2
        self.addPageTemplates([
            PageTemplate("une", [Frame(self.leftMargin, self.bottomMargin, w, h, id="u")], onPage=self.pied),
            PageTemplate("deux", [Frame(self.leftMargin, self.bottomMargin, col, h, id="g"),
                                  Frame(self.leftMargin + col + 0.8 * cm, self.bottomMargin, col, h, id="d")], onPage=self.pied)])

    def pied(self, c, d):
        c.saveState()
        c.setFont("DV", 7)
        c.setFillColor(GRIS)
        c.drawString(1.4 * cm, 0.9 * cm, "1000 chansons pour Suno — © 2026 Oussama Ghorbel")
        c.drawRightString(A4[0] - 1.4 * cm, 0.9 * cm, str(d.page))
        c.restoreState()

    def afterFlowable(self, fl):
        if isinstance(fl, Paragraph) and fl.style.name == "h1":
            self.notify("TOCEntry", (0, fl.getPlainText(), self.page))


def chanson(c):
    titre = x(c["titre"])
    if c["titre_fr"] and c["titre_fr"] != c["titre"]:
        titre += f"  <font size='8' color='#5a6560'>({x(c['titre_fr'])})</font>"
    meta = " · ".join(v for v in (LANG[c["langue"]], f"{c['bpm']} BPM", c["tonalite"], c["ambiance"], c["theme"]) if v)
    tete = [Paragraph(f"{c['numero']}. {titre}", ST["num"]), Paragraph(x(meta), ST["meta"])]
    if c["resume_fr"] and c["langue"] != "fr":
        tete.append(Paragraph(f"<i>{x(c['resume_fr'])}</i>", ST["meta"]))
    tete.append(Paragraph("<b>Style :</b> " + x(c["style"]), ST["style"]))
    corps = []
    for ligne in c["paroles"].split("\n"):
        ligne = ligne.strip()
        if not ligne:
            continue
        if re.fullmatch(r"\[[^\]]+\]", ligne):
            corps.append(Paragraph(x(ligne), ST["tag"]))
        else:
            corps.append(Paragraph(x(ligne), ST["vers_ar"] if ARABE.search(ligne) else ST["vers"]))
    # l'en-tête et les premiers vers restent ensemble ; le reste coule d'une colonne à l'autre
    return [KeepTogether(tete + corps[:4])] + corps[4:] + [Spacer(1, 10)]


def main():
    genres, tout, notes = charger()
    (ICI / "chansons.json").write_text(json.dumps({"total": len(tout), "chansons": tout}, ensure_ascii=False, indent=1), encoding="utf-8")
    par_genre = Counter(c["genre"] for c in tout)
    langues = Counter(c["langue"] for c in tout)
    fl = [Spacer(1, 6 * cm), Paragraph(f"{len(tout)} chansons pour Suno", ST["titre"]), Spacer(1, 14),
          Paragraph("Paroles originales en français, anglais et " + x("العربية") + " — classées par genre et par tempo", ST["sous"]),
          Spacer(1, 6 * cm), Paragraph("Oussama Ghorbel", ST["sous"]), Spacer(1, 6),
          Paragraph("Écrites par Dialagram (Qwen), dirigées et contrôlées par Claude", ST["sous"]), PageBreak()]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle("toc", fontName="DV", fontSize=9.5, leading=13.5)]
    fl += [Paragraph("Sommaire", ST["corps"]), toc, PageBreak()]
    fl += [Paragraph("Comment utiliser ce livre avec Suno", ST["h1"]),
           Paragraph("1. Dans Suno, activez le mode <b>Custom</b>. 2. Copiez l'encadré <b>Style</b> de la chanson dans le champ "
                     "« Style of Music ». 3. Copiez les paroles, balises comprises, dans le champ « Lyrics ». Les balises entre crochets "
                     "([Verse 1], [Chorus], [Bridge]…) indiquent la structure à Suno : gardez-les telles quelles. 4. Donnez le titre "
                     "et lancez la génération ; essayez deux ou trois versions et gardez la meilleure.", ST["corps"]),
           Paragraph("Chaque genre est rangé du tempo le plus lent au plus rapide. L'index final regroupe toutes les chansons par "
                     "tempo pour choisir selon l'énergie voulue. Les chansons en arabe sont écrites en darija maghrébine (raï, chaabi, "
                     "gnawa) ou en arabe dialectal simple ; leur titre et leur résumé sont traduits en français.", ST["corps"]),
           Paragraph(f"<b>Langues</b> : {langues.get('fr', 0)} en français, {langues.get('en', 0)} en anglais, "
                     f"{langues.get('ar', 0)} en arabe.", ST["corps"]),
           Paragraph("<b>Droits</b> : paroles originales écrites avec l'assistance de l'intelligence artificielle sous la direction "
                     "d'Oussama Ghorbel. © 2026 Oussama Ghorbel, tous droits réservés. Vérifiez les conditions d'utilisation de Suno "
                     "pour l'exploitation commerciale des morceaux générés.", ST["corps"]), Spacer(1, 6)]
    lignes = [["Genre", "Tempo", "Chansons"]] + [[g["nom"], f"{g['bpm'][0]}–{g['bpm'][1]} BPM", str(par_genre[g["cle"]])] for g in genres]
    t = Table(lignes, colWidths=[9 * cm, 3.5 * cm, 2.5 * cm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "DV", 8.5), ("FONT", (0, 0), (-1, 0), "DVB", 8.5),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, ACCENT), ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
    fl += [t, NextPageTemplate("deux"), PageBreak()]
    for g in genres:
        gs = [c for c in tout if c["genre"] == g["cle"]]
        if not gs:
            continue
        fl.append(Paragraph(f"{x(g['nom'])} · {g['bpm'][0]}–{g['bpm'][1]} BPM", ST["h1"]))
        for c in gs:
            fl += chanson(c)
        fl.append(PageBreak())
    fl.append(Paragraph("Index par tempo", ST["h1"]))
    for nom, a, b in TEMPOS:
        sel = sorted((c for c in tout if a <= c["bpm"] <= b), key=lambda c: (c["bpm"], c["numero"]))
        fl.append(Paragraph(f"<b>{nom} — {len(sel)} chansons</b>", ST["tag"]))
        fl += [Paragraph(f"{c['bpm']} · n° {c['numero']} · {x(c['titre'])} <font color='#5a6560'>({x(c['genre_nom'])})</font>", ST["idx"])
               for c in sel]
    sortie = ICI / "1000-chansons-pour-Suno-Oussama-Ghorbel.pdf"
    Livre(str(sortie)).multiBuild(fl)
    print(f"{len(tout)} chansons | {dict(notes)} | {dict(langues)} | {dict(par_genre)} | PDF : {sortie}")


if __name__ == "__main__":
    main()
