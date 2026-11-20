#!/usr/bin/env python3
"""Met en page un tome de l'édition « Французский в 10 000 словах » (le français pour russophones) et exporte les cartes mémoire.

Usage : livre.py DEBUT FIN [--tome 1]
Sorties : Frantsuzskiy-v-10000-slovakh-Tom-N-Oussama-Ghorbel.pdf et cartes-tomeN.json (entrées complètes + cartes recto/verso).
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
    if f.get("present"):
        pr = liste(f["present"])
        lignes = [["", "Présent"]] + [[p, pr[i] if i < len(pr) else ""] for i, p in enumerate(["je", "tu", "il / elle", "nous", "vous", "ils / elles"])]
        out.append(tab(lignes, [W * 0.25, W * 0.75]))
        noms = {"auxiliaire": "Вспомогательный глагол", "passe_compose": "Passé composé", "imparfait": "Imparfait", "futur": "Futur simple",
                "participe_passe": "Participe passé"}
        for k, n in noms.items():
            if f.get(k):
                out.append(Paragraph(f"<b>{n}</b> : " + x(" / ".join(liste(f[k]))), ST["corps"]))
    elif f:
        out.append(Paragraph(x(" · ".join(f"{k} : {', '.join(liste(v))}" for k, v in f.items() if v)), ST["corps"]))
    return out


def entree(e, W):
    fl = [Paragraph(f"Слово № {e['rang']} · {e.get('frequence', 0):,} употреблений · уровень {x(e.get('niveau', ''))}".replace(",", " "),
                    ST["rang"]),
          Paragraph(x(e.get("mot") or e["lemme"]), ST["mot"]),
          Paragraph(x(e.get("api", "")), ST["pron"])]
    nat = e.get("nature", "") + (f", род : {e['genre']}" if str(e.get("genre", "")).strip() not in ("", "-", "—", "–", "None") else "")
    fl.append(Paragraph(x(nat), ST["nat"]))
    fl.append(Paragraph("1. Значения и переводы на русский", ST["h"]))
    lignes = [["Значение", "Перевод", "Примеры"]]
    for i, s in enumerate(e.get("sens") or [], 1):
        ex = "<br/>".join(f"{x(p.get('fr'))}<br/><font color='#5b6472'><i>{x(p.get('ru'))}</i></font>"
                          for p in s.get("exemples") or [] if isinstance(p, dict))
        lignes.append([Paragraph(f"<b>{i}.</b> {x(s.get('sens'))}", ST["cell"]),
                       Paragraph(x(", ".join(liste(s.get("equivalents")))), ST["cell"]), Paragraph(ex, ST["cell"])])
    fl.append(tab(lignes, [W * 0.27, W * 0.22, W * 0.51]))
    syn, ant = e.get("synonymes") or [], e.get("antonymes") or []
    if syn or ant:
        fl.append(Paragraph("2. Французские синонимы", ST["h"]))
        for s in syn:
            mot, nu = (s.get("mot", ""), s.get("nuance", "")) if isinstance(s, dict) else (s, "")
            fl.append(Paragraph(f"• <b>{x(mot)}</b>" + (f" : {x(nu)}" if nu else ""), ST["corps"]))
        if ant:
            fl.append(Paragraph("<b>Антонимы</b> : " + x(", ".join(a if isinstance(a, str) else a.get("mot", "") for a in ant)),
                                ST["corps"]))
    fo = formes(e, W)
    if fo:
        fl += [Paragraph("3. Формы и спряжение", ST["h"])] + fo
    if e.get("pieges"):
        fl.append(Paragraph("4. Трудности для русскоговорящих", ST["h"]))
        fl += [Paragraph("• " + x(p), ST["corps"]) for p in liste(e["pieges"])]
    ex = [p for p in e.get("expressions") or [] if isinstance(p, dict)]
    fa = [p for p in e.get("famille") or [] if isinstance(p, dict)]
    if ex or fa:
        fl.append(Paragraph("5. Выражения и однокоренные слова", ST["h"]))
        if ex:
            fl.append(Paragraph("<b>Выражения</b> : " + " ; ".join(f"{x(p.get('fr'))} (<i>{x(p.get('ru'))}</i>)" for p in ex), ST["corps"]))
        if fa:
            fl.append(Paragraph("<b>Однокоренные</b> : " + ", ".join(f"{x(p.get('mot'))} (<i>{x(p.get('ru'))}</i>)" for p in fa), ST["corps"]))
    s0 = (e.get("sens") or [{}])[0]
    fl.append(Paragraph(f"<b>Карточка</b> — лицевая сторона : {x(e.get('mot'))}  ·  оборот : {x(', '.join(liste(s0.get('equivalents'))[:2]))}"
                        f"  ·  карточек : {len(e.get('sens') or [])} (по одной на значение)", ST["carte"]))
    return fl + [PageBreak()]


def cartes(entrees):
    out = []
    for e in entrees:
        for i, s in enumerate(e.get("sens") or [], 1):
            ex = next((p for p in s.get("exemples") or [] if isinstance(p, dict)), {})
            out.append({"id": f"fr-{e['rang']:05d}-{i}", "rang": e["rang"], "niveau": e.get("niveau"), "recto": e.get("mot"),
                        "verso": ", ".join(liste(s.get("equivalents"))), "sens": s.get("sens"),
                        "exemple_fr": ex.get("fr"), "exemple_ru": ex.get("ru"), "api": e.get("api")})
    return out


def main():
    debut, fin = int(sys.argv[1]), int(sys.argv[2])
    tome = int(sys.argv[sys.argv.index("--tome") + 1]) if "--tome" in sys.argv else 1
    entrees = []
    for f in sorted((ICI / "entrees").glob("[0-9][0-9][0-9][0-9].json")):
        entrees += [e for e in json.loads(f.read_text(encoding="utf-8")) if e and debut <= e["rang"] <= fin and e.get("sens")]
    entrees.sort(key=lambda e: e["rang"])
    titre = f"Французский в 10 000 словах — Том {tome}"
    pdf = ICI / f"Frantsuzskiy-v-10000-slovakh-Tom-{tome}-Oussama-Ghorbel.pdf"
    doc = Livre(str(pdf), titre)
    W = doc.width
    fl = [Spacer(1, 5 * cm), Paragraph("Французский в 10 000 словах", ST["titre"]), Spacer(1, 10),
          Paragraph(f"Том {tome} — слова с {debut} по {fin}, от самых частотных", ST["sous"]), Spacer(1, 8),
          Paragraph("Учебный французско-русский словарь для русскоговорящих · Le français en 10 000 mots", ST["sous"]),
          Spacer(1, 5 * cm), Paragraph("Oussama Ghorbel", ST["sous"]), PageBreak(),
          Paragraph("Как пользоваться книгой", ST["h"]),
          Paragraph("Каждое слово начинается с новой страницы. Слова расположены по реальной частотности употребления : зная первую "
                    "тысячу, вы понимаете большую часть слов обычного разговора. Для каждого слова : транскрипция МФА, род и часть речи, "
                    "значения с русскими переводами и примерами, французские синонимы и их оттенки, формы и спряжение, трудности для "
                    "русскоговорящих (артикль, род, предлоги, ложные друзья, liaison), устойчивые выражения и однокоренные слова. "
                    "Рамка « Карточка » показывает, что повторяет приложение : одна карточка на каждое значение.", ST["corps"]), Spacer(1, 6),
          Paragraph("Источник частотности : список FrequencyWords (Hermit Dave, субтитры OpenSubtitles 2018, лицензия MIT), "
                    "сгруппированный по словарной форме (simplemma) ; имена собственные исключены.", ST["corps"]), Spacer(1, 6),
          Paragraph("© 2026 Oussama Ghorbel. Все права защищены. Tous droits réservés. Книга задумана и составлена Oussama Ghorbel "
                    "с помощью инструментов искусственного интеллекта.", ST["corps"]), PageBreak()]
    for e in entrees:
        fl += entree(e, W)
    fl.append(Paragraph("Алфавитный указатель", ST["h"]))
    fl.append(Paragraph(" · ".join(f"{x(e.get('mot'))} {e['rang']}" for e in sorted(entrees, key=lambda e: e["lemme"])), ST["corps"]))
    doc.build(fl)
    c = cartes(entrees)
    (ICI / f"cartes-tome{tome}.json").write_text(json.dumps({"edition": "Французский в 10 000 словах", "auteur": "Oussama Ghorbel",
                                                               "tome": tome, "rangs": [debut, fin], "mots": entrees, "cartes": c},
                                                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(entrees)} mots | PDF {pdf.name} | {len(c)} cartes")


if __name__ == "__main__":
    main()
