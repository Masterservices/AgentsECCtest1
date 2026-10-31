#!/usr/bin/env python3
"""Assemble les chansons en un livre PDF en trois modules de langue (français, anglais, derja tunisienne),
chaque module classé par genre puis par tempo, et en chansons.json.

Usage : livre_chansons.py
Les chansons arabes prennent leur version tunisienne (tunisien/<lot>.json) : écriture arabe, romanisation chantable, API.
Contrôle : titres en double retirés, 40 chansons au plus par genre, BPM ramené dans la plage du genre et présent dans le style.
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
pdfmetrics.registerFont(TTFont("DVI", "/usr/share/fonts/truetype/freefont/FreeSansOblique.ttf"))
pdfmetrics.registerFont(TTFont("DVM", D + "DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")
ENCRE, GRIS, ACCENT, FOND = colors.HexColor("#1c2421"), colors.HexColor("#5a6560"), colors.HexColor("#7a2e5f"), colors.HexColor("#f3eef2")
ST = {
    "titre": ParagraphStyle("t", fontName="DVB", fontSize=30, leading=36, alignment=TA_CENTER, textColor=ENCRE),
    "sous": ParagraphStyle("s", fontName="DV", fontSize=12, leading=17, alignment=TA_CENTER, textColor=GRIS),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=19, leading=24, textColor=ACCENT, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=13, leading=17, textColor=ACCENT, spaceBefore=6, spaceAfter=4),
    "corps": ParagraphStyle("c", fontName="DV", fontSize=9.5, leading=14, textColor=ENCRE, spaceAfter=5),
    "num": ParagraphStyle("n", fontName="DVB", fontSize=11, leading=14, textColor=ENCRE, spaceBefore=4),
    "meta": ParagraphStyle("m", fontName="DV", fontSize=7.3, leading=9.5, textColor=GRIS),
    "style": ParagraphStyle("st", fontName="DVM", fontSize=6.8, leading=8.8, textColor=ENCRE, backColor=FOND, borderPadding=3,
                            spaceBefore=3, spaceAfter=5),
    "tag": ParagraphStyle("tg", fontName="DVB", fontSize=7.3, leading=10, textColor=ACCENT, spaceBefore=3),
    "vers": ParagraphStyle("v", fontName="DV", fontSize=8, leading=10.6, textColor=ENCRE),
    "vers_ar": ParagraphStyle("va", fontName="DV", fontSize=8.8, leading=11.4, textColor=ENCRE, alignment=TA_RIGHT, spaceBefore=1.5),
    "rom": ParagraphStyle("ro", fontName="DVI", fontSize=7.6, leading=9.6, textColor=ACCENT),
    "api": ParagraphStyle("ap", fontName="DVM", fontSize=6.9, leading=8.8, textColor=GRIS),
    "idx": ParagraphStyle("i", fontName="DV", fontSize=7.4, leading=9.6, textColor=ENCRE),
}
ST["module"] = ParagraphStyle("h1", fontName="DVB", fontSize=26, leading=32, alignment=TA_CENTER, textColor=ACCENT, spaceAfter=12)
MODULES = [("fr", "Module 1 — Chansons en français", "Pop, chanson, rap, ballades… en français"),
           ("en", "Module 2 — Songs in English", "Pop, R&B, rock, jazz, gospel… in English"),
           ("ar", "Module 3 — Chansons en derja tunisienne", "الدارجة التونسية"),]
SOUS_AR = "Chaque vers en trois lignes : écriture arabe, romanisation chantable pour Suno, transcription API"
LANG = {"fr": "français", "en": "anglais", "ar": "derja tunisienne"}
TEMPOS = [("Lent (moins de 80 BPM)", 0, 79), ("Modéré (80 à 109 BPM)", 80, 109), ("Rapide (110 à 129 BPM)", 110, 129),
          ("Très rapide (130 BPM et plus)", 130, 999)]
CLE_API = [("ħ", "ح", "h soufflé du fond de la gorge"), ("ʕ", "ع", "ayn, son de gorge voisé"), ("χ", "خ", "kh, comme la jota espagnole"),
           ("ɣ", "غ", "gh, r grasseyé parisien"), ("ʃ", "ش", "ch de « chat »"), ("ʒ", "ج", "j de « jour » (prononciation de Tunis)"),
           ("q", "ق", "k profond (à Tunis) ; g dans d'autres régions"), ("ʔ", "ء", "coup de glotte"),
           ("sˤ tˤ dˤ ðˤ", "ص ط ض ظ", "consonnes emphatiques, prononcées avec la langue en arrière"),
           ("ː", "ّ / ا و ي", "consonne doublée (chadda) ou voyelle longue"), ("ə ɪ ʊ", "—", "voyelles brèves, souvent réduites en derja")]
ARABE = re.compile("[؀-ۿ]")
# DejaVu n'a pas le glyphe de la ligature « Allah » (U+FDF2) : on la désactive
RESHAPER = arabic_reshaper.ArabicReshaper(configuration={"ARABIC LIGATURE ALLAH": False})
TAG = re.compile(r"^\[[^\]]+\]$")


def x(t):
    """Échappe le XML et met en forme l'arabe (lettres liées, droite à gauche)."""
    t = str(t)
    if ARABE.search(t):
        t = get_display(RESHAPER.reshape(t))
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cle_titre(t):
    t = unicodedata.normalize("NFKD", str(t).lower())
    return re.sub(r"[\W_]+", "", "".join(c for c in t if not unicodedata.combining(c)))


def lignes(t):
    return [l.strip() for l in str(t).split("\n") if l.strip()]


def charger():
    genres = json.loads((ICI / "genres.json").read_text(encoding="utf-8"))
    vus, notes, tout = set(), Counter(), []
    for g in genres:
        pris = 0
        for f in sorted((ICI / "lots").glob(f"{g['cle']}-[0-9].json")):
            ftn = ICI / "tunisien" / f.name
            tn = json.loads(ftn.read_text(encoding="utf-8"))["chansons"] if ftn.exists() else {}
            for i, c in enumerate(json.loads(f.read_text(encoding="utf-8"))["chansons"]):
                if pris >= 40:
                    break
                langue = c.get("langue") if c.get("langue") in LANG else ("ar" if ARABE.search(c["paroles"]) else "fr")
                derja = tn.get(str(i)) if langue == "ar" else None
                if langue == "ar" and not derja:
                    notes["chanson arabe sans version tunisienne"] += 1
                if derja:
                    c = {**c, **{k: v for k, v in derja.items() if v and k != "controle"}}
                k = cle_titre(c["titre"])
                if k in vus:
                    notes["titre en double retiré"] += 1
                    continue
                vus.add(k)
                pris += 1
                m = re.search(r"\d+", str(c.get("bpm", "")))
                bpm = int(m.group()) if m else sum(g["bpm"]) // 2
                b2 = min(max(bpm, g["bpm"][0]), g["bpm"][1])
                if b2 != bpm:
                    notes["BPM ramené dans la plage du genre"] += 1
                style = re.sub(r"\b\d{2,3}\s*bpm\b", f"{b2} BPM", str(c.get("style") or g["style"]), flags=re.I)
                if "bpm" not in style.lower():
                    style = style.rstrip(", ") + f", {b2} BPM"
                tout.append({"genre": g["cle"], "genre_nom": g["nom"], "titre": c["titre"].strip(),
                             "titre_fr": (c.get("titre_fr") or "").strip(), "langue": langue, "theme": c.get("theme", ""), "bpm": b2,
                             "tonalite": c.get("tonalite", ""), "ambiance": c.get("ambiance", ""), "style": style.strip(),
                             "resume_fr": c.get("resume_fr", ""), "paroles": c["paroles"].strip(),
                             "paroles_chant": (c.get("paroles_chant") or "").strip(), "paroles_api": (c.get("paroles_api") or "").strip(),
                             "controle_derja": (derja or {}).get("controle", [])})
    ordre_g = {g["cle"]: i for i, g in enumerate(genres)}
    ordre_l = {l: i for i, (l, *_) in enumerate(MODULES)}
    tout.sort(key=lambda c: (ordre_l[c["langue"]], ordre_g[c["genre"]], c["bpm"], cle_titre(c["titre"])))
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
        if isinstance(fl, Paragraph) and fl.style.name in ("h1", "h2"):
            self.notify("TOCEntry", (0 if fl.style.name == "h1" else 1, fl.getPlainText(), self.page))


def vers(ligne):
    if TAG.match(ligne):
        return Paragraph(x(ligne), ST["tag"])
    return Paragraph(x(ligne), ST["vers_ar"] if ARABE.search(ligne) else ST["vers"])


def chanson(c):
    titre = x(c["titre"])
    if c["titre_fr"] and c["titre_fr"] != c["titre"]:
        titre += f"  <font size='8' color='#5a6560'>({x(c['titre_fr'])})</font>"
    meta = " · ".join(v for v in (f"{c['bpm']} BPM", c["tonalite"], c["ambiance"], c["theme"]) if v)
    tete = [Paragraph(f"{c['numero']}. {titre}", ST["num"]), Paragraph(x(meta), ST["meta"])]
    if c["resume_fr"] and c["langue"] != "fr":
        tete.append(Paragraph(f"<i>{x(c['resume_fr'])}</i>", ST["meta"]))
    tete.append(Paragraph("<b>Style :</b> " + x(c["style"]), ST["style"]))
    p, ch, api = lignes(c["paroles"]), lignes(c["paroles_chant"]), lignes(c["paroles_api"])
    corps = []
    if c["langue"] == "ar" and ch and api and len(p) == len(ch) == len(api):
        # trois lignes par vers : écriture arabe, romanisation chantable, API
        for a, r, i in zip(p, ch, api):
            if TAG.match(a):
                corps.append(Paragraph(x(a), ST["tag"]))
            else:
                corps.append(KeepTogether([Paragraph(x(a), ST["vers_ar"]), Paragraph(x(r), ST["rom"]), Paragraph(x(i), ST["api"])]))
    else:
        corps = [vers(l) for l in p]
        if ch:
            corps += [Paragraph("Paroles chantables (Suno)", ST["tag"])] + [Paragraph(x(l), ST["rom"]) for l in ch if not TAG.match(l)]
        if api:
            corps += [Paragraph("Transcription API", ST["tag"])] + [Paragraph(x(l), ST["api"]) for l in api if not TAG.match(l)]
    # l'en-tête et les premiers vers restent ensemble ; le reste coule d'une colonne à l'autre
    return [KeepTogether(tete + corps[:3])] + corps[3:] + [Spacer(1, 10)]


def main():
    genres, tout, notes = charger()
    (ICI / "chansons.json").write_text(json.dumps({"total": len(tout), "chansons": tout}, ensure_ascii=False, indent=1), encoding="utf-8")
    langues = Counter(c["langue"] for c in tout)
    W = A4[0] - 2.8 * cm  # largeur utile (marges de 1,4 cm)
    fl = [Spacer(1, 6 * cm), Paragraph(f"{len(tout)} chansons pour Suno", ST["titre"]), Spacer(1, 14),
          Paragraph("Paroles originales en trois modules : français, anglais et derja tunisienne — classées par genre et par tempo", ST["sous"]),
          Spacer(1, 6 * cm), Paragraph("Oussama Ghorbel", ST["sous"]), Spacer(1, 6),
          Paragraph("Écrites par Dialagram (Qwen), dirigées et relues par Claude", ST["sous"]), PageBreak()]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle("toc0", fontName="DVB", fontSize=9.5, leading=14, spaceBefore=4),
                       ParagraphStyle("toc1", fontName="DV", fontSize=8.6, leading=11.5, leftIndent=14)]
    fl += [Paragraph("Sommaire", ST["corps"]), toc, PageBreak()]
    fl += [Paragraph("Comment utiliser ce livre avec Suno", ST["corps"]),
           Paragraph("1. Dans Suno, activez le mode <b>Custom</b>. 2. Copiez l'encadré <b>Style</b> de la chanson dans le champ "
                     "« Style of Music ». 3. Copiez les paroles, balises comprises, dans le champ « Lyrics ». Les balises entre crochets "
                     "([Verse 1], [Chorus], [Bridge]…) indiquent la structure à Suno : gardez-les telles quelles. 4. Donnez le titre "
                     "et lancez la génération ; essayez deux ou trois versions et gardez la meilleure.", ST["corps"]),
           Paragraph(f"Le livre compte trois modules : <b>français</b> ({langues.get('fr', 0)} chansons), <b>anglais</b> "
                     f"({langues.get('en', 0)}) et <b>derja tunisienne</b> ({langues.get('ar', 0)}). Dans chaque module, les chansons sont "
                     "rangées par genre puis du tempo le plus lent au plus rapide. L'index final les regroupe toutes par tempo.", ST["corps"]),
           Paragraph("<b>Module tunisien</b> : chaque vers est donné sur trois lignes — l'écriture arabe, la <font color='#7a2e5f'><i>"
                     "romanisation chantable</i></font> et la transcription en <font name='DVM' color='#5a6560'>Alphabet Phonétique "
                     "International (API)</font>. Pour Suno, collez soit l'écriture arabe, soit la romanisation (souvent mieux prononcée) ; "
                     "l'API sert à vérifier la prononciation exacte.", ST["corps"])]
    cle = Table([["API", "Lettre", "Prononciation"]] + [[a, Paragraph(x(b), ST["vers"]), c] for a, b, c in CLE_API],
                colWidths=[3 * cm, 2.6 * cm, W - 5.6 * cm])
    cle.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "DV", 8.3), ("FONT", (0, 1), (0, -1), "DVM", 8.3), ("FONT", (0, 0), (-1, 0), "DVB", 8.3),
                             ("LINEBELOW", (0, 0), (-1, 0), 0.6, ACCENT), ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    fl += [cle, Spacer(1, 6),
           Paragraph("<b>Droits</b> : paroles originales écrites avec l'assistance de l'intelligence artificielle sous la direction "
                     "d'Oussama Ghorbel. © 2026 Oussama Ghorbel, tous droits réservés. Vérifiez les conditions d'utilisation de Suno "
                     "pour l'exploitation commerciale des morceaux générés.", ST["corps"]), Spacer(1, 4)]
    lignes_t = [["Genre", "Tempo"] + [l.upper() for l, *_ in MODULES]]
    for g in genres:
        n = Counter(c["langue"] for c in tout if c["genre"] == g["cle"])
        lignes_t.append([g["nom"], f"{g['bpm'][0]}–{g['bpm'][1]} BPM"] + [str(n.get(l, "")) for l, *_ in MODULES])
    t = Table(lignes_t, colWidths=[7.5 * cm, 3.2 * cm, 1.6 * cm, 1.6 * cm, 1.6 * cm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "DV", 8), ("FONT", (0, 0), (-1, 0), "DVB", 8),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, ACCENT), ("TOPPADDING", (0, 0), (-1, -1), 1),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 1), ("ALIGN", (2, 0), (-1, -1), "CENTER")]))
    fl.append(t)
    for code, nom, sous in MODULES:
        ms = [c for c in tout if c["langue"] == code]
        if not ms:
            continue
        # page de titre du module sur une colonne, puis les chansons sur deux colonnes
        fl += [NextPageTemplate("une"), PageBreak(), Spacer(1, 7 * cm), Paragraph(x(nom), ST["module"]),
               Paragraph(x(sous), ST["sous"]), Spacer(1, 8), Paragraph(f"{len(ms)} chansons", ST["sous"])]
        if code == "ar":
            fl += [Spacer(1, 8), Paragraph(SOUS_AR, ST["sous"])]
        fl += [NextPageTemplate("deux"), PageBreak()]
        for g in genres:
            gs = [c for c in ms if c["genre"] == g["cle"]]
            if gs:
                fl.append(Paragraph(f"{x(g['nom'])} · {g['bpm'][0]}–{g['bpm'][1]} BPM", ST["h2"]))
                for c in gs:
                    fl += chanson(c)
        fl.append(PageBreak())
    fl.append(Paragraph("Index par tempo", ST["h1"]))
    for nom, a, b in TEMPOS:
        sel = sorted((c for c in tout if a <= c["bpm"] <= b), key=lambda c: (c["bpm"], c["numero"]))
        fl.append(Paragraph(f"<b>{nom} — {len(sel)} chansons</b>", ST["tag"]))
        fl += [Paragraph(f"{c['bpm']} · n° {c['numero']} · {x(c['titre'])} <font color='#5a6560'>({x(c['genre_nom'])}, "
                         f"{c['langue'].upper()})</font>", ST["idx"]) for c in sel]
    sortie = ICI / "1000-chansons-pour-Suno-Oussama-Ghorbel.pdf"
    Livre(str(sortie)).multiBuild(fl)
    print(f"{len(tout)} chansons | {dict(notes)} | {dict(langues)} | PDF : {sortie}")


if __name__ == "__main__":
    main()
