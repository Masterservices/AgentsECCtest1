"""E-01 — la largeur survit-elle aux traductions, et prédit-elle le coût de résolution ?

Usage : python3 e01.py   (graines fixées ; écrit NCE/08_DATA/e01_results.json et e01_summary.txt)
"""
import json
import random
import statistics
import sys
from pathlib import Path
import nce_bench as nb

OUT = Path(__file__).resolve().parents[2] / "08_DATA"
OUT.mkdir(exist_ok=True)
rows, lines = [], []


def log(s):
    print(s); lines.append(s)


def spearman(x, y):
    def rank(a):
        o = sorted(range(len(a)), key=lambda i: a[i]); r = [0] * len(a)
        for k, i in enumerate(o):
            r[i] = k
        return r
    rx, ry = rank(x), rank(y)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else float("nan")


def units(c, x, outs):
    val = c.eval(x)
    return [[o + 1] if val[o] else [-(o + 1)] for o in outs]

# A. H-B1 : largeur du tableau de Cook-Levin en fonction du temps, à espace fixé
log("A. Tableau de Cook-Levin : largeur (borne sup.) selon espace s et temps t")
for s in (4, 6, 8, 10):
    ws = []
    for t in (10, 20, 40, 80):
        cl, nv = nb.tm_tableau(s, t)
        w = nb.tw(nb.primal_graph(cl)); ws.append(w)
        r, dt, conf, _ = nb.solve(cl)
        rows.append(dict(famille="tableau", param=f"s={s},t={t}", graine=0, n_vars=nv, n_clauses=len(cl),
                         tw_circuit=None, tw_cnf=w, tw_seuil=None, sat=r, conflits=conf, temps_s=dt))
    log(f"  s={s:2d}  t=10,20,40,80 -> largeur {ws}  (SAT attendu : {r})")

# B. H-B2 / H-B3 : largeur circuit -> CNF de Tseitin -> réseau à seuil
log("\nB. Largeur : circuit / CNF Tseitin / réseau à seuil ; borne du lemme L-01 : 3(w+1)-1")
fam = [("additionneur", n, nb.ripple_adder(n)[0]) for n in (8, 16, 32)]
fam += [("multiplieur", n, nb.array_multiplier(n)[0]) for n in (4, 6, 8)]
fam += [("bande", w, nb.banded_random(20, 400, w, random.Random(w))) for w in (4, 8, 16, 32)]
viol = 0
for name, p, c in fam:
    wc = nb.tw(c.graph()); wt = nb.tw(nb.primal_graph(nb.tseitin(c))); ws = nb.tw(nb.threshold_network(c)[0])
    if wt > 3 * (wc + 1) - 1:
        viol += 1
    rows.append(dict(famille=name, param=p, graine=0, n_vars=c.n, n_clauses=len(nb.tseitin(c)),
                     tw_circuit=wc, tw_cnf=wt, tw_seuil=ws, sat=None, conflits=None, temps_s=None))
    log(f"  {name:12s} {p:3d}  circuit {wc:3d}  Tseitin {wt:3d}  seuil {ws:3d}")
log(f"  Dépassements de la borne 3(w+1)-1 (sur bornes sup. heuristiques) : {viol}")

# C. H-B4 : à taille fixée, le coût CDCL suit-il la largeur ?
log("\nC. Coût de résolution à taille fixée (40 entrées, 800 portes, 40 sorties contraintes)")
W, C = [], []
for w in (4, 8, 16, 32, 64, 128):
    confs, tws = [], []
    for seed in range(8):
        rng = random.Random(1000 * w + seed)
        c = nb.banded_random(40, 800, w, rng)
        x = [rng.random() < .5 for _ in range(40)]
        cl = nb.tseitin(c) + units(c, x, list(range(c.n - 40, c.n)))
        wt = nb.tw(nb.primal_graph(cl))
        r, dt, conf, _ = nb.solve(cl)
        confs.append(conf); tws.append(wt); W.append(wt); C.append(conf)
        rows.append(dict(famille="bande-sat", param=w, graine=seed, n_vars=c.n, n_clauses=len(cl),
                         tw_circuit=None, tw_cnf=wt, tw_seuil=None, sat=r, conflits=conf, temps_s=dt))
    log(f"  fenêtre {w:3d}  largeur méd. {statistics.median(tws):5.0f}  conflits méd. {statistics.median(confs):8.0f}")
log(f"  Spearman(largeur, conflits) à taille fixée : {spearman(W, C):.2f}  (n={len(W)})")

# D. Famille structurée difficile : factorisation par multiplieur
log("\nD. Factorisation (multiplieur contraint à p*q)")
P = {6: (37, 59), 8: (151, 233), 10: (613, 997), 12: (2459, 4001)}
for n, (p, q) in P.items():
    c, outs = nb.array_multiplier(n)
    x = [(p >> i) & 1 == 1 for i in range(n)] + [(q >> i) & 1 == 1 for i in range(n)]
    cl = nb.tseitin(c) + units(c, x, outs)
    wt = nb.tw(nb.primal_graph(cl))
    r, dt, conf, _ = nb.solve(cl)
    rows.append(dict(famille="factorisation", param=n, graine=0, n_vars=c.n, n_clauses=len(cl),
                     tw_circuit=None, tw_cnf=wt, tw_seuil=None, sat=r, conflits=conf, temps_s=dt))
    log(f"  n={n:2d}  variables {c.n:5d}  largeur {wt:3d}  conflits {conf:8d}  temps {dt:.2f}s")

(OUT / "e01_results.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
(OUT / "e01_summary.txt").write_text("\n".join(lines) + f"\n\nPython {sys.version.split()[0]}\n")
