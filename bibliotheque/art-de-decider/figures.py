#!/usr/bin/env python3
"""Dessine la figure explicative de chaque chapitre (schémas décrits dans plan.json) et l'insère dans le chapitre.

Usage : figures.py plan.json chapitres_v2
Types : matrice, arbre, cycle, entonnoir, balance, courbe, etapes. Écrit figures/chNN.png puis ajoute
« ![Figure N — titre](chemin) » avant la deuxième section du chapitre (une seule fois : l'insertion est idempotente).
"""
import json
import math
import re
import sys
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

ICI = Path(__file__).resolve().parent
ENCRE, BLEU, OCRE, CLAIR, SABLE, GRIS = "#1d2733", "#1f3a5f", "#c8963e", "#eef2f6", "#f6ead6", "#7a8594"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})


def court(t, n=22):
    return "\n".join(textwrap.wrap(str(t), n)) or " "


def boite(ax, x, y, w, h, texte, fond=CLAIR, bord=BLEU, couleur=ENCRE, taille=9.5, gras=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.012,rounding_size=0.025",
                                fc=fond, ec=bord, lw=1.4))
    ax.text(x, y, court(texte, max(10, int(w * 34))), ha="center", va="center", fontsize=taille, color=couleur,
            weight="bold" if gras else "normal")


def fleche(ax, a, b, couleur=GRIS, courbure=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=13, color=couleur, lw=1.3,
                                 connectionstyle=f"arc3,rad={courbure}", shrinkA=4, shrinkB=4))


def matrice(ax, f):
    e = (list(f.get("elements", [])) + ["", "", "", ""])[:4]
    for k, (x, y) in enumerate([(0.32, 0.68), (0.72, 0.68), (0.32, 0.30), (0.72, 0.30)]):
        boite(ax, x, y, 0.36, 0.33, e[k], fond=SABLE if k == 1 else CLAIR, bord=OCRE if k == 1 else BLEU)
    fleche(ax, (0.1, 0.1), (0.95, 0.1), ENCRE)
    fleche(ax, (0.1, 0.1), (0.1, 0.92), ENCRE)
    ax.text(0.52, 0.03, court(f.get("axe_x", ""), 60), ha="center", fontsize=9.5, color=ENCRE)
    ax.text(0.05, 0.5, court(f.get("axe_y", ""), 30), ha="center", va="center", rotation=90, fontsize=9.5, color=ENCRE)


def arbre(ax, f):
    br = [b for b in f.get("elements", []) if isinstance(b, dict)][:4]
    if not br:
        br = [{"branche": str(b), "feuilles": []} for b in f.get("elements", [])[:4]]
    boite(ax, 0.12, 0.5, 0.2, 0.16, f.get("racine", f.get("titre", "")), fond=BLEU, couleur="white", gras=True)
    n = len(br)
    for i, b in enumerate(br):
        y = 0.88 - i * (0.76 / (n - 1)) if n > 1 else 0.5
        boite(ax, 0.45, y, 0.24, 0.13, b.get("branche", ""), fond=SABLE, bord=OCRE)
        fleche(ax, (0.22, 0.5), (0.33, y))
        fs = b.get("feuilles", [])[:3]
        for j, feuille in enumerate(fs):
            yy = y - (j - (len(fs) - 1) / 2) * 0.075  # première feuille en haut
            ax.text(0.65, yy, "• " + str(feuille)[:46], va="center", fontsize=8.6, color=ENCRE)
            fleche(ax, (0.57, y), (0.645, yy))


def cycle(ax, f):
    e = f.get("elements", [])[:6]
    n = max(len(e), 1)
    pts = [(0.5 + 0.33 * math.cos(math.pi / 2 - 2 * math.pi * k / n), 0.5 + 0.36 * math.sin(math.pi / 2 - 2 * math.pi * k / n))
           for k in range(n)]
    for k, (x, y) in enumerate(pts[:len(e)]):
        boite(ax, x, y, 0.22, 0.14, f"{k + 1}. {e[k]}", fond=CLAIR if k % 2 else SABLE, bord=BLEU if k % 2 else OCRE)
    for k in range(len(e)):
        a, b = pts[k], pts[(k + 1) % n]
        fleche(ax, (a[0] + (b[0] - a[0]) * 0.3, a[1] + (b[1] - a[1]) * 0.3),
               (a[0] + (b[0] - a[0]) * 0.7, a[1] + (b[1] - a[1]) * 0.7), BLEU, -0.25)


def entonnoir(ax, f):
    e = f.get("elements", [])[:6]
    n = max(len(e), 1)
    h = 0.84 / n
    for k, t in enumerate(e):
        y0 = 0.92 - k * h
        w0, w1 = 0.9 - k * (0.6 / n), 0.9 - (k + 1) * (0.6 / n)
        ax.add_patch(Polygon([(0.5 - w0 / 2, y0), (0.5 + w0 / 2, y0), (0.5 + w1 / 2, y0 - h + 0.012), (0.5 - w1 / 2, y0 - h + 0.012)],
                             fc=BLEU if k == n - 1 else (CLAIR if k % 2 else SABLE), ec=BLEU, lw=1.2))
        ax.text(0.5, y0 - h / 2, court(t, 50), ha="center", va="center", fontsize=9.5, color="white" if k == n - 1 else ENCRE)


def balance(ax, f):
    g, d = f.get("gauche") or {}, f.get("droite") or {}
    ax.plot([0.5, 0.5], [0.1, 0.72], color=ENCRE, lw=2.5)
    ax.add_patch(Polygon([(0.42, 0.06), (0.58, 0.06), (0.5, 0.12)], fc=ENCRE))
    ax.plot([0.15, 0.85], [0.78, 0.7], color=ENCRE, lw=2.5)
    for x, y, cote, coul in ((0.2, 0.77, g, OCRE), (0.8, 0.71, d, BLEU)):
        ax.plot([x, x], [y, y - 0.12], color=GRIS, lw=1)
        boite(ax, x, y - 0.17, 0.3, 0.08, cote.get("titre", ""), fond=coul, bord=coul, couleur="white", gras=True)
        for j, p in enumerate(cote.get("poids", [])[:4]):
            ax.text(x, y - 0.29 - j * 0.085, court(p, 34), ha="center", va="center", fontsize=8.8, color=ENCRE)


def courbe(ax, f):
    import numpy as np
    x = np.linspace(0, 1, 200)
    y = {"croissante": x ** 0.6, "decroissante": 1 - x ** 0.6, "en_u": 4 * (x - 0.5) ** 2,
         "en_cloche": np.exp(-((x - 0.5) ** 2) / 0.04), "sigmoide": 1 / (1 + np.exp(-12 * (x - 0.5)))}.get(str(f.get("forme")), x)
    X, Y = 0.1 + 0.82 * x, 0.14 + 0.72 * y
    ax.plot(X, Y, color=BLEU, lw=2.6)
    fleche(ax, (0.1, 0.12), (0.96, 0.12), ENCRE)
    fleche(ax, (0.1, 0.12), (0.1, 0.94), ENCRE)
    ax.text(0.53, 0.03, court(f.get("axe_x", ""), 60), ha="center", fontsize=9.5)
    ax.text(0.05, 0.53, court(f.get("axe_y", ""), 30), ha="center", va="center", rotation=90, fontsize=9.5)
    ann = f.get("elements", [])[:4]
    for k, t in enumerate(ann):
        i = int((k + 1) * 199 / (len(ann) + 1))
        ax.plot(X[i], Y[i], "o", color=OCRE, ms=7)
        ax.annotate(court(t, 26), (X[i], Y[i]), xytext=(X[i], Y[i] + 0.14 if Y[i] < 0.7 else Y[i] - 0.18),
                    ha="center", fontsize=8.6, color=ENCRE, arrowprops=dict(arrowstyle="-", color=GRIS, lw=0.8))


def etapes(ax, f):
    e = f.get("elements", [])[:7]
    n = max(len(e), 1)
    w = 0.92 / n
    for k, t in enumerate(e):
        x0 = 0.04 + k * w
        ax.add_patch(Polygon([(x0, 0.32), (x0 + w - 0.03, 0.32), (x0 + w - 0.005, 0.5), (x0 + w - 0.03, 0.68), (x0, 0.68), (x0 + 0.025, 0.5)],
                             fc=BLEU if k == n - 1 else (CLAIR if k % 2 else SABLE), ec=BLEU, lw=1.2))
        ax.text(x0 + w / 2 - 0.005, 0.5, court(t, max(8, int(w * 60))), ha="center", va="center", fontsize=8.6,
                color="white" if k == n - 1 else ENCRE)
        ax.text(x0 + w / 2 - 0.005, 0.76, str(k + 1), ha="center", fontsize=12, color=OCRE, weight="bold")


TYPES = {"matrice": matrice, "arbre": arbre, "cycle": cycle, "entonnoir": entonnoir, "balance": balance, "courbe": courbe,
         "etapes": etapes}


def dessiner(f, sortie, numero):
    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=200)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    TYPES.get(f.get("type"), etapes)(ax, f)
    fig.suptitle(f"Figure {numero} — {f.get('titre', '')}", fontsize=11.5, color=BLEU, weight="bold", y=0.99)
    fig.savefig(sortie, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    plan, dossier = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")), Path(sys.argv[2])
    (ICI / "figures").mkdir(exist_ok=True)
    faites = 0
    for p in plan["parties"]:
        for c in p["chapitres"]:
            n, f = int(c["numero"]), c.get("figure")
            md = dossier / f"ch{n:02d}.md"
            if not f or not md.exists():
                continue
            png = ICI / "figures" / f"ch{n:02d}.png"
            dessiner(f, png, n)
            t = md.read_text(encoding="utf-8")
            if f"]({png})" in t:
                continue
            ligne = f"![Figure {n} — {f.get('titre', '')}]({png})"
            pos = [m.start() for m in re.finditer(r"^## ", t, re.M)]
            t = t[:pos[1]] + ligne + "\n\n" + t[pos[1]:] if len(pos) > 1 else t + "\n\n" + ligne + "\n"
            md.write_text(t, encoding="utf-8")
            faites += 1
    print(f"{faites} figures insérées")


if __name__ == "__main__":
    main()
