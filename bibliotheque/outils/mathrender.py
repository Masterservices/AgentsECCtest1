#!/usr/bin/env python3
"""mathrender.py — formules LaTeX -> images PNG pour le PDF (mathtext de matplotlib, police STIX).

Usage depuis mise_en_page.py :
    protect(text)            -> (texte avec jetons, liste des formules)   [avant toute mise en forme]
    restore(text, maths, fs) -> texte avec balises <img/> reportlab
    display_rows(tex, fs)    -> liste de dicts {path, w, h, d} pour une formule hors texte
"""
import hashlib
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mimage
import numpy as np
from matplotlib import mathtext, rcParams
from matplotlib.font_manager import FontProperties

rcParams["mathtext.fontset"] = "stix"
rcParams["font.family"] = "STIXGeneral"

DPI = 300
_PARSER = mathtext.MathTextParser("agg")
CACHE = Path("math_cache")
TOKEN = "\u00a7"  # § : reste intact dans sanitize_winansi / escape_xml / inline_markup


def set_cache(directory):
    global CACHE
    CACHE = Path(directory)
    CACHE.mkdir(parents=True, exist_ok=True)


# ─── Adaptation LaTeX -> sous-ensemble compris par mathtext ──────────────────

_SIMPLE = [
    (r"\\operatorname\*?\{([^{}]*)\}", r"\\mathrm{\1}"),
    (r"\\tag\*?\{[^{}]*\}", ""),
    (r"\\(?:big|Big|bigg|Bigg)[lrm]?(?![a-zA-Z])", ""),
    (r"\\[td]frac", r"\\frac"),
    (r"\\xrightarrow\{((?:[^{}]|\{[^{}]*\})*)\}", r"\\rightarrow^{\1}"),
    (r"\\xleftarrow\{((?:[^{}]|\{[^{}]*\})*)\}", r"\\leftarrow^{\1}"),
    (r"\\bmod(?![a-zA-Z])", r"\\ \\mathrm{mod}\\ "),
    (r"\\pmod\{([^{}]*)\}", r"\\ (\\mathrm{mod}\\ \1)"),
    (r"\\underbrace\{((?:[^{}]|\{[^{}]*\})*)\}_\{((?:[^{}]|\{[^{}]*\})*)\}", r"{\1}_{\2}"),
    (r"\\underbrace\{((?:[^{}]|\{[^{}]*\})*)\}", r"{\1}"),
    (r"\\overbrace\{((?:[^{}]|\{[^{}]*\})*)\}\^\{([^{}]*)\}", r"{\1}^{\2}"),
    (r"\\overbrace\{((?:[^{}]|\{[^{}]*\})*)\}", r"{\1}"),
    (r"\\!", ""),
    (r"\\displaystyle|\\textstyle|\\scriptstyle|\\limits|\\nolimits", ""),
    (r"\\mathbbm\{", r"\\mathbb{"),
    (r"\\(?:bm|boldsymbol)\{", r"\\mathbf{"),
    (r"\\argmax", r"\\mathrm{arg\\,max}"),
    (r"\\argmin", r"\\mathrm{arg\\,min}"),
    (r"\\(?:textbf|mathit)\{", r"\\mathbf{"),
    (r"\\mathrm\{\s*\}", ""),
]

_ENV = re.compile(
    r"\\begin\{(cases|pmatrix|bmatrix|vmatrix|matrix|aligned|align\*?|array|split|gathered)\}"
    r"(?:\{[^}]*\})?(.*?)\\end\{\1\}",
    re.S,
)


def _group(s, i):
    """Contenu du groupe {...} qui commence en s[i] (accolades équilibrées) et indice de fin."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
    return s[i + 1:], len(s)


def _braced_commands(tex):
    r"""\underbrace{X}_{L} -> {X}_{L} ; \overbrace{X}^{L} -> {X}^{L} (mathtext ne les connaît pas)."""
    for cmd, link in ((r"\underbrace", "_"), (r"\overbrace", "^")):
        while True:
            k = tex.find(cmd + "{")
            if k < 0:
                break
            body, end = _group(tex, k + len(cmd))
            label = ""
            if tex[end:end + 2] == link + "{":
                label, end2 = _group(tex, end + 1)
                end = end2
                tex = tex[:k] + "{" + body + "}" + link + "{" + label + "}" + tex[end:]
            else:
                tex = tex[:k] + "{" + body + "}" + tex[end:]
    return tex


def adapt(tex):
    tex = _braced_commands(tex.strip())
    for pattern, repl in _SIMPLE:
        tex = re.sub(pattern, repl, tex)
    return re.sub(r"\s+", " ", tex).strip()


def split_rows(tex):
    """Les environnements multi-lignes (cases, matrices, aligned) sont rendus ligne par ligne."""
    m = _ENV.search(tex)
    if not m:
        return [tex]
    pre, post = tex[: m.start()].strip(), tex[m.end():].strip()
    rows = [r.strip() for r in re.split(r"\\\\", m.group(2)) if r.strip()]
    rows = [re.sub(r"\s*&\s*", r"\\quad ", r) for r in rows]
    if m.group(1) == "cases":
        rows = [r"\{\; " + r for r in rows]
    if rows:
        if pre:
            rows[0] = pre + " " + rows[0]
        if post:
            rows[-1] = rows[-1] + " " + post
    return rows or [tex]


def _attempts(tex):
    yield tex
    t2 = re.sub(r"\\text\{", r"\\mathrm{", tex)
    yield t2
    yield re.sub(r"\\(?:left|right)(?![a-zA-Z])", "", t2)


def _render_one(tex, fontsize):
    key = hashlib.sha1(f"{fontsize:.2f}|{tex}".encode("utf-8")).hexdigest()[:20]
    png, meta = CACHE / f"{key}.png", CACHE / f"{key}.json"
    if png.exists() and meta.exists():
        d = json.loads(meta.read_text())
        return {"path": str(png), **d}
    CACHE.mkdir(parents=True, exist_ok=True)
    for variant in _attempts(tex):
        try:
            rp = _PARSER.parse(f"${variant}$", dpi=DPI, prop=FontProperties(size=fontsize))
            ink = rp.image.astype(float) / 255.0  # masque : 1 = encre
            rgb = np.repeat((1.0 - ink)[..., None], 3, axis=2)  # encre noire sur fond blanc
            mimage.imsave(str(png), rgb.clip(0, 1))
            h_px, w_px = ink.shape
            d = {"w": w_px * 72.0 / DPI, "h": h_px * 72.0 / DPI, "d": float(rp.depth) * 72.0 / DPI}
            meta.write_text(json.dumps(d))
            return {"path": str(png), **d}
        except Exception:  # formule non prise en charge par mathtext
            continue
    return None


def render(tex, fontsize):
    """Rend une formule (une seule ligne) ; None si mathtext ne sait pas l'écrire."""
    return _render_one(adapt(tex), fontsize)


def display_rows(tex, fontsize):
    rows = []
    for r in split_rows(adapt(tex)):
        img = _render_one(r, fontsize)
        if img is None:
            return None
        rows.append(img)
    return rows


# ─── Extraction / réinjection dans un texte markdown ─────────────────────────

_DOLLAR2 = re.compile(r"(?<![\\$])\$\$(.+?)\$\$", re.S)
_DOLLAR1 = re.compile(r"(?<![\\$])\$(?!\s)([^$\n]+?)(?<![\s\\])\$")


def protect(text):
    """Remplace chaque formule par un jeton §Mn§ avant la mise en forme du texte."""
    maths = []

    def grab(m):
        maths.append(m.group(1))
        return f"{TOKEN}M{len(maths) - 1}{TOKEN}"

    def grab_inline(m):
        # "$5 et $10" (prix) : un $ fermant suivi d'un chiffre n'est une formule que si elle contient du LaTeX
        if m.string[m.end():m.end() + 1].isdigit() and not re.search(r"[\\^_{]", m.group(1)):
            return m.group(0)
        return grab(m)

    text = text.replace("\\$", f"{TOKEN}D{TOKEN}")
    text = _DOLLAR2.sub(grab, text)
    text = _DOLLAR1.sub(grab_inline, text)
    return text, maths


_LIMIT_OPS = re.compile(
    r"\\(sum|prod|coprod|int|oint|bigcup|bigcap|bigoplus|lim|max|min|sup|inf|argmax|argmin)(?![a-zA-Z])(?=\s*[_^])"
)


def inline_style(tex):
    r"""En ligne, les bornes des opérateurs vont à droite (style texte) : {\sum}_{i=1}^{n}."""
    return _LIMIT_OPS.sub(lambda m: "{\\" + m.group(1) + "}", tex)


def restore(text, maths, fontsize, fallback=lambda s: s):
    def sub(m):
        tex = maths[int(m.group(1))]
        rows = split_rows(inline_style(adapt(tex)))
        parts = []
        for r in rows:
            img = _render_one(r, fontsize)
            if img is None:
                return "<i>" + fallback(tex) + "</i>"
            parts.append(
                f'<img src="{img["path"]}" width="{img["w"]:.2f}" height="{img["h"]:.2f}" '
                f'valign="{-img["d"]:.2f}"/>'
            )
        return " ; ".join(parts)

    text = re.sub(f"{TOKEN}M(\\d+){TOKEN}", sub, text)
    return text.replace(f"{TOKEN}D{TOKEN}", "$")
