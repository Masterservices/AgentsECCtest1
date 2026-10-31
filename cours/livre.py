#!/usr/bin/env python3
"""Met en page chaque cours en livre PDF (leçons + corrigés) et exporte le paquet WebGL / voix off.

Usage : livre.py [cours ...]
Sorties : <Titre>-Oussama-Ghorbel.pdf et <cours>-webgl.json (personnages, scènes, dialogues, segments de voix off, exercices).
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
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.doctemplate import BaseDocTemplate, Frame, PageTemplate
from reportlab.platypus.tableofcontents import TableOfContents

from generer import COURS

ICI = Path(__file__).resolve().parent
F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", F + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVB")
ENCRE, GRIS, ACCENT, FOND = colors.HexColor("#1d2430"), colors.HexColor("#5b6472"), colors.HexColor("#1f4e8c"), colors.HexColor("#eef3fa")
ST = {
    "titre": ParagraphStyle("t", fontName="DVB", fontSize=28, leading=34, alignment=TA_CENTER, textColor=ENCRE),
    "sous": ParagraphStyle("s", fontName="DV", fontSize=13, leading=18, alignment=TA_CENTER, textColor=GRIS),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=17, leading=22, textColor=ACCENT, spaceAfter=2),
    "h1b": ParagraphStyle("h1b", fontName="DV", fontSize=11, leading=14, textColor=GRIS, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=11.5, leading=15, textColor=ACCENT, spaceBefore=10, spaceAfter=4),
    "h3": ParagraphStyle("h3", fontName="DVB", fontSize=9.8, leading=13, textColor=ENCRE, spaceBefore=5, spaceAfter=2),
    "corps": ParagraphStyle("c", fontName="DV", fontSize=9.3, leading=13.3, textColor=ENCRE, spaceAfter=4),
    "petit": ParagraphStyle("p", fontName="DV", fontSize=8, leading=10.5, textColor=GRIS),
    "cell": ParagraphStyle("ce", fontName="DV", fontSize=8.4, leading=11, textColor=ENCRE),
    "cellg": ParagraphStyle("cg", fontName="DVI", fontSize=8, leading=10.5, textColor=GRIS),
    "boite": ParagraphStyle("b", fontName="DV", fontSize=8.6, leading=12, textColor=ENCRE, backColor=FOND, borderPadding=5,
                            spaceBefore=4, spaceAfter=8),
}
# Intitulés dans la langue de l'apprenant
MOTS = {
    "ru": {"lecon": "Урок", "obj": "Цели урока", "dial": "Диалог", "voc": "Словарь", "gram": "Грамматика", "pron": "Произношение",
           "cult": "Культура", "ex": "Упражнения", "ret": "Запомните", "cor": "Ответы к упражнениям", "persos": "Персонажи",
           "mode": "Как работать с книгой", "sommaire": "Содержание", "scene": "Сцена"},
    "fr": {"lecon": "Leçon", "obj": "Objectifs", "dial": "Dialogue", "voc": "Vocabulaire", "gram": "Grammaire", "pron": "Prononciation",
           "cult": "Culture", "ex": "Exercices", "ret": "À retenir", "cor": "Corrigés des exercices", "persos": "Les personnages",
           "mode": "Mode d'emploi", "sommaire": "Sommaire", "scene": "Scène"},
}
MODE = {
    "ru": "Курс состоит из 36 уроков: 12 уроков уровня A1, 12 — A2 и 12 — B1 (по шкале CEFR). Каждый урок построен одинаково: "
          "цели, сцена, диалог с переводом, словарь с транскрипцией МФА, грамматика с таблицами, произношение, культура, шесть "
          "упражнений и главное, что нужно запомнить. Ответы ко всем упражнениям — в конце книги. Уроки 12, 24 и 36 — итоговые. "
          "Эта книга служит основой интерактивного курса Russtudy: каждая сцена, реплика и упражнение превращаются в 3D-урок с озвучкой. "
          "Совет: сначала прочитайте диалог вслух, затем закройте перевод и попробуйте понять текст сами.",
    "fr": "Le cours compte 36 leçons : 12 de niveau A1, 12 de niveau A2 et 12 de niveau B1 du CECR. Chaque leçon suit le même plan : "
          "objectifs, scène, dialogue traduit, vocabulaire avec translittération (la syllabe accentuée est en majuscules et marquée d'un "
          "accent dans le texte russe), grammaire avec tableaux, prononciation, culture, six exercices et l'essentiel à retenir. Les "
          "corrigés sont à la fin du livre. Les leçons 12, 24 et 36 sont des bilans. Ce livre est la base du cours interactif Russtudy : "
          "chaque scène, réplique et exercice devient une leçon 3D avec voix off. Conseil : lisez le dialogue à voix haute en respectant "
          "l'accent tonique, puis cachez la traduction et relisez.",
}


def x(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Livre(BaseDocTemplate):
    def __init__(self, f, titre):
        super().__init__(f, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.6 * cm, bottomMargin=1.6 * cm,
                         title=titre, author="Oussama Ghorbel")
        self.titre = titre
        self.addPageTemplates([PageTemplate("p", [Frame(self.leftMargin, self.bottomMargin, self.width, self.height)], onPage=self.pied)])

    def pied(self, c, d):
        c.saveState()
        c.setFont("DV", 7.3)
        c.setFillColor(GRIS)
        c.drawString(1.8 * cm, 0.95 * cm, f"{self.titre} — Russtudy — © 2026 Oussama Ghorbel")
        c.drawRightString(A4[0] - 1.8 * cm, 0.95 * cm, str(d.page))
        c.restoreState()

    def afterFlowable(self, fl):
        if isinstance(fl, Paragraph) and fl.style.name == "h1":
            self.notify("TOCEntry", (0, fl.getPlainText(), self.page))


def tableau(lignes, largeurs, entete=True):
    t = Table([[c if isinstance(c, Paragraph) else Paragraph(x(c), ST["cell"]) for c in l] for l in lignes], colWidths=largeurs,
              repeatRows=1 if entete else 0)
    style = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#d5dbe5")),
             ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    if entete:
        style += [("BACKGROUND", (0, 0), (-1, 0), FOND), ("LINEBELOW", (0, 0), (-1, 0), 0.7, ACCENT)]
    t.setStyle(TableStyle(style))
    return t


def lecon(L, noms, m, W):
    fl = [Paragraph(f"{m['lecon']} {L['num']} · {L['niveau']} — {x(L['titre']['cible'])}", ST["h1"]),
          Paragraph(x(L["titre"]["natif"]), ST["h1b"]),
          Paragraph(f"<b>{m['obj']} :</b> " + " · ".join(x(o) for o in L["objectifs"]), ST["corps"])]
    s = L["scene"]
    fl.append(Paragraph(f"<b>{m['scene']} :</b> {x(s.get('lieu', ''))} — {x(s.get('moment', ''))}", ST["petit"]))
    fl.append(Paragraph(m["dial"], ST["h2"]))
    fl.append(tableau([[Paragraph(f"<b>{x(noms.get(r['perso'], r['perso']))}</b>", ST["cell"]), Paragraph(x(r["texte"]), ST["cell"]),
                        Paragraph(x(r.get("traduction", "")), ST["cellg"])] for r in L["dialogue"]],
                      [2.3 * cm, (W - 2.3 * cm) * 0.52, (W - 2.3 * cm) * 0.48], entete=False))
    fl.append(Paragraph(m["voc"], ST["h2"]))
    lignes = [[Paragraph(f"<b>{x(v['mot'])}</b> <font size='7' color='#5b6472'>{x(v.get('nature', ''))}</font>", ST["cell"]),
               Paragraph(x(v.get("prononciation", "")), ST["cell"]),
               Paragraph(x(v.get("traduction", "")) + (f"<br/><font size='7.3' color='#5b6472'>{x(v['exemple'])} — "
                                                       f"{x(v.get('exemple_traduction', ''))}</font>" if v.get("exemple") else ""),
                         ST["cell"])] for v in L["vocabulaire"]]
    fl.append(tableau(lignes, [W * 0.27, W * 0.2, W * 0.53], entete=False))
    fl.append(Paragraph(m["gram"], ST["h2"]))
    for g in L["grammaire"]:
        fl += [Paragraph(x(g.get("titre", "")), ST["h3"]), Paragraph(x(g.get("explication", "")), ST["corps"])]
        tab = [r for r in g.get("tableau") or [] if isinstance(r, list) and r]
        if len(tab) > 1:
            n = max(len(r) for r in tab)
            fl += [tableau([list(map(str, r)) + [""] * (n - len(r)) for r in tab], [W / n] * n), Spacer(1, 4)]
        fl += [Paragraph(f"• {x(e.get('cible', ''))} — <i>{x(e.get('natif', ''))}</i>", ST["corps"]) for e in g.get("exemples", [])]
    p = L["prononciation"]
    fl += [Paragraph(m["pron"], ST["h2"]), Paragraph(f"<b>{x(p.get('point', ''))}</b> — {x(p.get('explication', ''))}", ST["corps"])]
    if p.get("exemples"):
        fl.append(Paragraph(" · ".join(x(e) for e in p["exemples"]), ST["petit"]))
    c = L["culture"]
    fl += [Paragraph(m["cult"], ST["h2"]), Paragraph(f"<b>{x(c.get('titre', ''))}</b><br/>{x(c.get('texte', ''))}", ST["boite"]),
           Paragraph(m["ex"], ST["h2"])]
    for i, e in enumerate(L["exercices"], 1):
        bloc = [Paragraph(f"<b>{i}.</b> {x(e.get('consigne', ''))}", ST["h3"])]
        for j, it in enumerate(e.get("items", []), 1):
            q = f"{j}) {x(it.get('question', ''))}"
            if it.get("choix"):
                q += "  <font color='#5b6472'>" + "  ".join(f"{'abcdef'[k]}) {x(ch)}" for k, ch in enumerate(it["choix"][:6])) + "</font>"
            bloc.append(Paragraph(q, ST["corps"]))
        fl.append(KeepTogether(bloc))
    fl += [Paragraph(m["ret"], ST["h2"]),
           Paragraph("<br/>".join(f"<b>{x(r.get('cible', ''))}</b> — {x(r.get('natif', ''))}" for r in L["resume"]), ST["boite"]),
           PageBreak()]
    return fl


def corriges(L, m):
    fl = [Paragraph(f"<b>{m['lecon']} {L['num']}</b>", ST["h3"])]
    for i, e in enumerate(L["exercices"], 1):
        rep = " ; ".join(f"{j}) {x(it.get('reponse', ''))}" for j, it in enumerate(e.get("items", []), 1))
        fl.append(Paragraph(f"{i}. {rep}", ST["petit"]))
    return fl


def construire(cle):
    c = COURS[cle]
    m = MOTS[c["code_natif"]]
    prog = json.loads((ICI / "programme" / f"{cle}.json").read_text(encoding="utf-8"))
    lecons = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((ICI / "lecons" / cle).glob("[0-9][0-9].json"))]
    noms = {p["id"]: p["nom"] for p in prog["personnages"]}
    pdf = ICI / (c["titre"].replace(" ", "-").replace("é", "e").replace("ç", "c") + "-Oussama-Ghorbel.pdf")
    doc = Livre(str(pdf), c["titre"])
    W = doc.width
    ru = c["code_natif"] == "ru"
    fl = [Spacer(1, 5 * cm), Paragraph(x(c["titre_natif"] if ru else c["titre"]), ST["titre"]), Spacer(1, 10),
          Paragraph(x(c["titre"] if ru else c["titre_natif"]), ST["sous"]), Spacer(1, 24),
          Paragraph(f"A1 → B1 · {len(lecons)} " + ("уроков" if ru else "leçons"), ST["sous"]),
          Spacer(1, 5 * cm), Paragraph("Oussama Ghorbel", ST["sous"]), Spacer(1, 6),
          Paragraph("Russtudy — e-learning", ST["sous"]), PageBreak()]
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle("toc", fontName="DV", fontSize=9.3, leading=13)]
    fl += [Paragraph(m["sommaire"], ST["h2"]), toc, PageBreak(),
           Paragraph(m["mode"], ST["h1"]), Paragraph(x(MODE[c["code_natif"]]), ST["corps"]), Paragraph(m["persos"], ST["h2"]),
           tableau([[Paragraph(f"<b>{x(p['nom'])}</b>, {p.get('age', '')}", ST["cell"]), Paragraph(x(p.get("role", "")), ST["cell"])]
                    for p in prog["personnages"]], [W * 0.3, W * 0.7], entete=False), PageBreak()]
    for L in lecons:
        fl += lecon(L, noms, m, W)
    fl.append(Paragraph(m["cor"], ST["h1"]))
    for L in lecons:
        fl += corriges(L, m)
    doc.multiBuild(fl)
    paquet = {"cours": cle, "titre": c["titre"], "titre_natif": c["titre_natif"], "langue_cible": c["code_cible"],
              "langue_apprenant": c["code_natif"], "auteur": "Oussama Ghorbel", "plateforme": "Russtudy",
              "personnages": prog["personnages"], "lecons": lecons}
    (ICI / f"{cle}-webgl.json").write_text(json.dumps(paquet, ensure_ascii=False, indent=1), encoding="utf-8")
    defauts = {L["num"]: L["controle"] for L in lecons if L.get("controle")}
    print(f"{cle} : {len(lecons)} leçons | PDF {pdf.name} | défauts restants {defauts or 'aucun'}")


if __name__ == "__main__":
    for k in sys.argv[1:] or list(COURS):
        construire(k)
