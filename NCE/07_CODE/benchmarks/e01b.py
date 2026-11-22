"""E-01b — INV-01b.

Partie 1 (H-B4) : à taille FIXÉE (n variables, m = 4,26 n clauses), la largeur prédit-elle le
coût CDCL ? Famille : 3-SAT aléatoire « en bande » (chaque clause prend ses 3 variables dans une
fenêtre de w variables consécutives). Largeur de chemin PROUVÉE <= w - 1 (sacs glissants).
w = n donne le 3-SAT aléatoire uniforme (difficile au seuil).

Partie 2 (H-B3, seconde partie) : un petit réseau ENTRAÎNÉ, puis élagué, retrouve-t-il la faible
largeur du circuit qu'il apprend ? Largeur encadrée par [dégénérescence, heuristique].

Usage : python3 e01b.py   (graines fixées)
"""
import json
import random
import statistics
import sys
from pathlib import Path
import numpy as np
import networkx as nx
import nce_bench as nb

OUT = Path(__file__).resolve().parents[2] / "08_DATA"
rows, lines = [], []


def log(s):
    print(s, flush=True); lines.append(s)


def tw_bounds(g):
    g = g.copy(); g.remove_nodes_from([v for v in list(g) if g.degree(v) == 0])
    if g.number_of_nodes() == 0:
        return 0, 0
    return max(nx.core_number(g).values()), nb.tw(g)

# ------------------------------------------------------------------ partie 1
log("Partie 1 — 3-SAT en bande, n=200, m=852 (rapport 4,26), 10 graines par fenêtre")
N, M = 200, 852
for w in (5, 10, 20, 40, 80, 200):
    cs, ts, ss = [], [], []
    for seed in range(10):
        rng = random.Random(7919 * w + seed)
        cl = []
        for _ in range(M):
            lo = rng.randrange(0, N - w + 1)
            vs = rng.sample(range(lo + 1, lo + w + 1), 3)
            cl.append([v if rng.random() < .5 else -v for v in vs])
        r, dt, conf, _ = nb.solve(cl)
        cs.append(conf); ts.append(dt); ss.append(r)
        rows.append(dict(partie=1, param=w, graine=seed, largeur_max_prouvee=w - 1, tw_inf=None, tw_sup=None,
                         sat=r, conflits=conf, temps_s=dt, aretes=None))
    log(f"  w={w:3d}  pw<= {w-1:3d}  SAT {sum(ss):2d}/10  conflits méd. {statistics.median(cs):9.0f}  max {max(cs):9d}  temps méd. {statistics.median(ts):.3f}s")

# ------------------------------------------------------------------ partie 2
log("\nPartie 2 — réseaux entraînés puis élagués (8 entrées ou 6 entrées, couches cachées 16-16)")


def parity_circuit(n):
    c = nb.Circuit(n); x = 0
    for i in range(1, n):
        x = c.add("XOR", x, i)
    return c


def train(X, Y, seed, steps=4000, h=16, lr=0.02):
    rs = np.random.default_rng(seed)
    sz = [X.shape[1], h, h, Y.shape[1]]
    W = [rs.normal(0, 1 / np.sqrt(a), (a, b)) for a, b in zip(sz, sz[1:])]
    B = [np.zeros(b) for b in sz[1:]]
    P = W + B; m = [np.zeros_like(p) for p in P]; v = [np.zeros_like(p) for p in P]
    def fwd(W, B, mask=None):
        a = [X]
        for i in range(3):
            Wi = W[i] * (mask[i] if mask else 1)
            z = a[-1] @ Wi + B[i]
            a.append(np.tanh(z) if i < 2 else 1 / (1 + np.exp(-z)))
        return a
    for t in range(1, steps + 1):
        a = fwd(W, B)
        d = (a[3] - Y) / len(X)
        gW, gB = [None] * 3, [None] * 3
        for i in (2, 1, 0):
            gW[i] = a[i].T @ d; gB[i] = d.sum(0)
            if i:
                d = (d @ W[i].T) * (1 - a[i] ** 2)
        G = gW + gB
        for k in range(6):
            m[k] = .9 * m[k] + .1 * G[k]; v[k] = .999 * v[k] + .001 * G[k] ** 2
            P[k] -= lr * (m[k] / (1 - .9 ** t)) / (np.sqrt(v[k] / (1 - .999 ** t)) + 1e-8)
    acc = lambda mask=None: float(((fwd(W, B, mask)[3] > .5) == (Y > .5)).all(1).mean())
    return W, B, acc


def prune(W, acc):
    mask = [np.ones_like(w) for w in W]
    if acc(mask) < 1:
        return None
    flat = sorted((abs(W[i][j, k]), i, j, k) for i in range(3) for j in range(W[i].shape[0]) for k in range(W[i].shape[1]))
    best = [mk.copy() for mk in mask]
    step = max(1, len(flat) // 40)
    for c in range(step, len(flat), step):
        for _, i, j, k in flat[c - step:c]:
            mask[i][j, k] = 0
        if acc(mask) == 1:
            best = [mk.copy() for mk in mask]
        else:
            break
    return best


def mask_graph(mask):
    g = nx.Graph(); off = [0]
    for mk in mask:
        off.append(off[-1] + mk.shape[0])
    for i, mk in enumerate(mask):
        for j, k in zip(*np.nonzero(mk)):
            g.add_edge(off[i] + j, off[i + 1] + k)
    return g

tasks = []
X8 = np.array([[(i >> b) & 1 for b in range(8)] for i in range(256)], float)
tasks.append(("parité-8", X8, X8.sum(1, keepdims=True) % 2, parity_circuit(8)))
tasks.append(("majorité-8", X8, (X8.sum(1, keepdims=True) >= 4).astype(float), None))
X6 = np.array([[(i >> b) & 1 for b in range(6)] for i in range(64)], float)
s = (X6[:, :3] @ [1, 2, 4] + X6[:, 3:] @ [1, 2, 4]).astype(int)
tasks.append(("addition-3+3", X6, np.array([[(v >> b) & 1 for b in range(4)] for v in s], float), nb.ripple_adder(3)[0]))
for name, X, Y, circ in tasks:
    ref = tw_bounds(nb.threshold_network(circ)[0]) if circ else (1, 1)
    res = []
    for seed in range(5):
        W, B, acc = train(X, Y, seed)
        mask = prune(W, acc)
        if mask is None:
            res.append("non appris"); continue
        g = mask_graph(mask); lo, hi = tw_bounds(g)
        res.append(f"[{lo},{hi}] ({g.number_of_edges()} arêtes)")
        rows.append(dict(partie=2, param=name, graine=seed, largeur_max_prouvee=None, tw_inf=lo, tw_sup=hi,
                         sat=None, conflits=None, temps_s=None, aretes=g.number_of_edges()))
    log(f"  {name:13s} réseau compilé : largeur [{ref[0]},{ref[1]}]  |  entraînés : " + " ; ".join(res))

(OUT / "e01b_results.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1, default=float))
(OUT / "e01b_summary.txt").write_text("\n".join(lines) + f"\n\nPython {sys.version.split()[0]}, numpy {np.__version__}\n")
