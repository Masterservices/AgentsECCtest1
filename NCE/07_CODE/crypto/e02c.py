"""E-02c — INV-02, piste C : récupération de clé d'un SPN jouet par CDCL, en fonction des tours.

Hypothèse testée (H-C1) : la largeur arborescente du graphe primal croît avec le nombre de tours,
et le coût CDCL suit la largeur.
Mesures : variables, clauses, largeur [borne inf. MMD+, borne sup. = min(heuristiques networkx,
ordre d'élimination explicite « création puis clé »)], conflits et temps (Glucose 4).
Graines : instance (clé, clairs) tirée par random.Random(1000*k + 10*R + graine).
Usage : python3 e02c.py   (~ 4-6 min)
"""
import json
import statistics
import sys
import time
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "benchmarks"))
import spn            # noqa: E402
import nce_bench as nb  # noqa: E402
from pysat.solvers import Solver  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "08_DATA"
PLAN = [(16, 2, R, 5, 3_000_000) for R in range(1, 7)] + \
       [(24, 3, R, 5, 3_000_000) for R in range(1, 5)] + [(24, 3, 5, 3, 1_000_000)]
rows = []
T0 = time.time()
print(f"Boîte S : uniformité différentielle {spn.differential_uniformity()}, linéarité {spn.linearity()}")
for k, npairs, R, nseeds, budget in PLAN:
    for sb in ("anf", "table"):
        res, tws = [], None
        for seed in range(nseeds):
            rng = random.Random(1000 * k + 10 * R + seed)
            K = rng.getrandbits(k)
            pairs = [(P, spn.encrypt(P, K, k, R)) for P in (rng.getrandbits(16) for _ in range(npairs))]
            e, Kv = spn.key_recovery_cnf(pairs, k, R, sb)
            if tws is None:   # la structure du graphe ne dépend pas de la graine
                g = nb.primal_graph(e.cl)
                order = [v for v in e.order if v > k] + list(range(1, k + 1))
                ew = spn.elimination_width(e.cl, order)
                lb, ub = nb.tw_bounds(g)
                tws = dict(variables=e.nv, clauses=len(e.cl), tw_inf=lb, tw_sup=min(ub, ew),
                           tw_sup_heuristique=ub, largeur_ordre_explicite=ew)
            with Solver(name="glucose4", bootstrap_with=e.cl) as s:
                s.conf_budget(budget)
                t0 = time.perf_counter()
                r = s.solve_limited()
                dt = time.perf_counter() - t0
                st = s.accum_stats()
                ok = None
                if r:
                    m = set(s.get_model())
                    K2 = sum(1 << i for i in range(k) if Kv[i] in m)
                    ok = all(spn.encrypt(P, K2, k, R) == C for P, C in pairs)
            res.append(dict(graine=seed, resultat=r, cle_coherente=ok, cle_exacte=(r and K2 == K),
                            conflits=st["conflicts"], temps_s=dt))
        row = dict(k=k, couples=npairs, tours=R, encodage_sbox=sb, budget=budget, **tws, essais=res,
                   conflits_med=statistics.median(x["conflits"] for x in res),
                   temps_med=statistics.median(x["temps_s"] for x in res),
                   resolus=sum(1 for x in res if x["resultat"]))
        rows.append(row)
        print(f"k={k} R={R} {sb:5s} vars {row['variables']:5d} tw [{row['tw_inf']},{row['tw_sup']}] "
              f"(heur {row['tw_sup_heuristique']}, ordre {row['largeur_ordre_explicite']}) "
              f"conflits méd {row['conflits_med']:9.0f} temps méd {row['temps_med']:7.3f}s "
              f"résolus {row['resolus']}/{nseeds}", flush=True)

# corrélation de rang (Spearman) entre tw_sup et conflits médians, par (k, encodage)
def spearman(a, b):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
        for p, i in enumerate(o):
            r[i] = p
        return r
    ra, rb = rk(a), rk(b); n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** .5
    return num / den if den else float("nan")

corr = {}
for k in (16, 24):
    for sb in ("anf", "table"):
        sel = [r for r in rows if r["k"] == k and r["encodage_sbox"] == sb]
        corr[f"k{k}_{sb}"] = dict(
            spearman_tw_inf_conflits=spearman([r["tw_inf"] for r in sel], [r["conflits_med"] for r in sel]),
            spearman_tours_conflits=spearman([r["tours"] for r in sel], [r["conflits_med"] for r in sel]))
print(json.dumps(corr, indent=1))
data = dict(meta=dict(solveur="glucose4", python=sys.version.split()[0], duree_s=time.time() - T0,
                      sbox_uniformite_diff=spn.differential_uniformity(), sbox_linearite=spn.linearity(),
                      note="ties possibles dans les rangs ; égalités départagées par ordre d'apparition"),
            mesures=rows, correlations=corr)
(OUT / "inv02_crypto.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))
print(f"Durée {time.time() - T0:.0f} s")
