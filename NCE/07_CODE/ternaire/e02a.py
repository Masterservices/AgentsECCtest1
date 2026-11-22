"""E-02a — INV-02, piste A : ternaire équilibré contre binaire, à information égale.

A.3  mesures (portes, profondeur, fils, largeur [borne inf. MMD+, borne sup. heuristique])
     pour n trits et m = ceil(n log2 3) bits ;
A.4  traduction ternaire -> binaire (gadgets minimaux par synthèse exacte SAT, 3 codes) et
     ternaire -> SAT (miter de commutativité du multiplieur, 4 encodages, 3 graines de mélange) ;
A.5  économie de radix ; neurones à seuil à poids ternaires contre L-03.
Usage : python3 e02a.py    (déterministe : graines fixées 0, 1, 2 ; durée ~ 3 min)
"""
import json
import math
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ternaire as t          # noqa: E402
import synthese as sy         # noqa: E402
import sat_ternaire as st     # noqa: E402

nb = t.nb
OUT = Path(__file__).resolve().parents[2] / "08_DATA"
data = {"meta": dict(python=sys.version.split()[0], graines=[0, 1, 2], solveur="glucose4",
                     budget_conflits=2_000_000, date="2026-11-22")}
T0 = time.time()


def log(s=""):
    print(s, flush=True)


# ------------------------------------------------------------------ A.4 (gadgets d'abord)
log("A.4 — gadgets binaires minimaux (synthèse exacte SAT, portes à 2 entrées quelconques)")
gad, gad_cost = {}, {}
for cname, code in sy.ENCODINGS.items():
    gad[cname], gad_cost[cname] = {}, {}
    for op in t.OPS3:
        r, g = sy.min_gadget(op, code)
        gad[cname][op], gad_cost[cname][op] = g, r
    log(f"  {cname:13s} " + "  ".join(f"{op}={r}" for op, r in gad_cost[cname].items()))
data["gadgets_cout_minimal"] = gad_cost

# ------------------------------------------------------------------ A.3
log("\nA.3 — mêmes fonctions, information égale (n trits, m bits, 2^m >= 3^n)")
NS = {"multiplication": (2, 3, 4, 6, 8)}
rows = []
for name, f in t.FUNCTIONS.items():
    for n in NS.get(name, (2, 3, 4, 6, 8, 12, 16)):
        m = t.bits_for(n)
        tc, bc = f(3, n), f(2, m)
        r = dict(fonction=name, n_trits=n, m_bits=m, ternaire=tc.metrics(), binaire=bc.metrics())
        for cname, code in sy.ENCODINGS.items():
            r["t2b_" + cname] = sy.compile_t2b(tc, gad[cname], code).metrics()
        rows.append(r)
        T, B, D = r["ternaire"], r["binaire"], r["t2b_double_rail"]
        log(f"  {name:24s} n={n:2d} m={m:2d} | portes T {T['portes']:5d} B {B['portes']:5d} T->B {D['portes']:5d}"
            f" | prof T {T['profondeur']:3d} B {B['profondeur']:3d} T->B {D['profondeur']:3d}"
            f" | tw T [{T['tw_inf']},{T['tw_sup']}] B [{B['tw_inf']},{B['tw_sup']}] T->B [{D['tw_inf']},{D['tw_sup']}]"
            f" | fils(bits) T {T['fils'] * math.log2(3):7.1f} B {B['fils']:5d}")
data["A3_mesures"] = rows

# ------------------------------------------------------------------ A.4 SAT
log("\nA.4 — miter de commutativité du multiplieur (insatisfaisable), 3 graines de mélange")
code = sy.ENCODINGS["double_rail"]
encs = {
    "direct_3var": (lambda n: t.multiplier(3, n), st.enc_direct, None),
    "table_2bits": (lambda n: t.multiplier(3, n), lambda c, x, i: st.enc_table2(c, x, code, i), None),
    "tseitin_gadgets_2bits": (lambda n: sy.compile_t2b(t.multiplier(3, n), gad["double_rail"], code),
                              st.enc_binary, st.valid_pairs(code)),
    "binaire_natif_m_bits": (lambda n: t.multiplier(2, t.bits_for(n)), st.enc_binary, None),
}
sat_rows = []
for n in (2, 3, 4, 5):
    for ename, (build, enc, ic) in encs.items():
        circ = build(n)
        cnf = st.miter_commut(enc, circ, ic)
        lb, ub = nb.tw_bounds(nb.primal_graph(cnf.cl))
        res = []
        for seed in (0, 1, 2):
            r, dt, conf = st.solve_budget(st.shuffle(cnf, seed))
            res.append(dict(graine=seed, resultat=r, temps_s=dt, conflits=conf))
        row = dict(n_trits=n, m_bits=t.bits_for(n), encodage=ename, variables=cnf.nv, clauses=len(cnf.cl),
                   litteraux=sum(map(len, cnf.cl)), tw_inf=lb, tw_sup=ub, essais=res,
                   conflits_med=statistics.median(x["conflits"] for x in res),
                   temps_med=statistics.median(x["temps_s"] for x in res))
        sat_rows.append(row)
        log(f"  n={n} m={row['m_bits']} {ename:22s} vars {cnf.nv:5d} clauses {len(cnf.cl):5d} tw [{lb},{ub}]"
            f" conflits méd {row['conflits_med']:8.0f} temps méd {row['temps_med']:.3f}s "
            f"résultats {[x['resultat'] for x in res]}")
data["A4_sat_miter"] = sat_rows

# ------------------------------------------------------------------ A.5
log("\nA.5 — économie de radix b/ln b (coût ∝ base × nombre de chiffres)")
econ = {b: b / math.log(b) for b in (2, 3, 4, 5, 6, 10)}
for b, v in econ.items():
    log(f"  b={b:2d}  b/ln b = {v:.4f}  rapport à b=2 : {v / econ[2]:.4f}")
pack = {f"{k} trits dans {math.ceil(k * math.log2(3))} bits": k * math.log2(3) / math.ceil(k * math.log2(3))
        for k in (1, 2, 3, 5, 10, 53)}
log("  efficacité de codage des trits en bits : " + ", ".join(f"{k}: {v:.4f}" for k, v in pack.items()))
data["A5_economie_radix"] = dict(b_sur_ln_b=econ, efficacite_paquets=pack)

log("\nA.5 — neurones à seuil : poids ternaires {-1,0,1} contre L-03 (|w| <= 2)")
th_rows = []
for cname, c in [("additionneur 4 bits", nb.ripple_adder(4)[0]), ("additionneur 8 bits", nb.ripple_adder(8)[0]),
                 ("multiplieur 3x3", nb.array_multiplier(3)[0]), ("multiplieur 4x4", nb.array_multiplier(4)[0])]:
    r = dict(circuit=cname, tw_circuit=nb.tw_bounds(c.graph()))
    for comp_name, comp in (("L03_poids_2", t.threshold_l03), ("poids_ternaires", t.threshold_ternary)):
        net, _ = comp(c)
        g = net.graph()
        r[comp_name] = dict(neurones=len(net.neurons), aretes=g.number_of_edges(), poids_max=net.max_weight(),
                            tw=nb.tw_bounds(g))
    th_rows.append(r)
    log(f"  {cname:20s} tw circuit {r['tw_circuit']} | L-03 : {r['L03_poids_2']} | ternaire : {r['poids_ternaires']}")
data["A5_seuil"] = th_rows
data["A5_xor_un_cache_ternaire"] = t.xor_one_hidden_ternary_exists()
log(f"  XOR avec un seul neurone caché à poids ternaires : solutions = {data['A5_xor_un_cache_ternaire']}")

data["meta"]["duree_s"] = time.time() - T0
(OUT / "inv02_ternaire.json").write_text(json.dumps(data, indent=1, ensure_ascii=False, default=str))
log(f"\nDurée totale : {data['meta']['duree_s']:.1f} s ; données : 08_DATA/inv02_ternaire.json")
