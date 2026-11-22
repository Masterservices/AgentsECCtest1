"""E-02b — INV-02, piste B : borne de coupe informationnelle (H-I1).

Énoncé (PROUVÉ, élémentaire) : si un ensemble S de noeuds d'un circuit q-aire sépare les entrées
des sorties (tout chemin entrée -> sortie passe par S, S pouvant contenir entrées ou sorties),
alors les sorties sont fonction des valeurs de S, donc H(f(X)) <= H(valeurs de S) <= |S| log2 q,
pour toute loi de X. Conséquence : c_min(C) >= H(f(X)) / log2 q, dans TOUT modèle de circuits.
Mesure : H(f(X)) (X uniforme, exhaustif), coupe minimale c_min (flot, sommets de capacité 1),
pour le circuit ternaire, le circuit binaire natif et la traduction double rail.
Usage : python3 e02b.py   (~ 30 s)
"""
import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ternaire as t   # noqa: E402
import synthese as sy  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "08_DATA"


def entropy(circ):
    al = t.TRITS if circ.q == 3 else t.BITS
    cnt = Counter(tuple(circ.run(x)) for x in itertools.product(al, repeat=circ.n_in))
    N = sum(cnt.values())
    return -sum(c / N * math.log2(c / N) for c in cnt.values())


def min_cut(circ):
    g = nx.DiGraph()
    for v in range(circ.n):
        if not circ.is_const(v):
            g.add_edge(("i", v), ("o", v), capacity=1)
    for k, (op, ins) in enumerate(circ.gates):
        for i in ins:
            if not circ.is_const(i):
                g.add_edge(("o", i), ("i", circ.n_in + k))
    for v in range(circ.n_in):
        g.add_edge("s", ("i", v))
    for o in set(circ.outs):
        if not circ.is_const(o):
            g.add_edge(("o", o), "t")
    if "t" not in g:
        return 0
    return nx.maximum_flow_value(g, "s", "t")


code = sy.ENCODINGS["double_rail"]
gad = {op: sy.min_gadget(op, code)[1] for op in t.OPS3}
rows = []
for name in ("addition", "multiplication", "comparaison", "x_mod_3"):
    for n in (2, 3, 4):
        m = t.bits_for(n)
        for label, circ in (("ternaire", t.FUNCTIONS[name](3, n)), ("binaire_natif", t.FUNCTIONS[name](2, m)),
                            ("ternaire_vers_binaire", None)):
            if circ is None:
                tc = t.FUNCTIONS[name](3, n)
                circ = sy.compile_t2b(tc, gad, code)
                H = rows[-2]["H_bits"]        # même fonction que le circuit ternaire, sorties recodées
            else:
                H = entropy(circ)
            c = min_cut(circ)
            cap = c * math.log2(circ.q)
            r = dict(fonction=name, n_trits=n, m_bits=m, circuit=label, H_bits=H, coupe_min=c,
                     capacite_bits=cap, marge=cap - H, rapport=(H / cap if cap else None))
            rows.append(r)
            assert cap + 1e-9 >= H, r       # vérification numérique de l'inégalité
            print(f"{name:15s} n={n} m={m} {label:22s} H={H:6.3f}  c_min={c:3d}  c_min·log2 q={cap:6.2f}"
                  f"  H/cap={r['rapport'] if cap else float('nan'):.3f}", flush=True)
(OUT / "inv02_info.json").write_text(json.dumps(dict(mesures=rows), indent=1, ensure_ascii=False))
