"""Tests exhaustifs de la piste A (INV-02). Usage : python3 test_ternaire.py (ou pytest)."""
import itertools
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ternaire as t          # noqa: E402
import synthese as sy         # noqa: E402
import sat_ternaire as st     # noqa: E402
from pysat.solvers import Solver  # noqa: E402

nb = t.nb
_GAD = {}


def gadgets(code_name):
    if code_name not in _GAD:
        code = sy.ENCODINGS[code_name]
        _GAD[code_name] = {op: sy.min_gadget(op, code)[1] for op in t.OPS3}
    return _GAD[code_name]


def test_portes_demi_et_complet():
    for a, b in itertools.product(t.TRITS, repeat=2):
        assert a + b == 3 * t.OPS3["CONS"][1](a, b) + t.OPS3["SUM"][1](a, b)
    c = t.Circ(3, 3)
    s, co = t.t_fa(c, 0, 1, 2)
    c.set_outs([s, co])
    for x in itertools.product(t.TRITS, repeat=3):
        s_, c_ = c.run(x)
        assert sum(x) == 3 * c_ + s_
    assert len(c.gates) == 5


def test_fonctions_exhaustif():
    for name, f in t.FUNCTIONS.items():
        for q, ns in ((3, (1, 2, 3)), (2, (1, 2, 3, 4, 5))):
            for n in ns:
                c = f(q, n)
                al = t.TRITS if q == 3 else t.BITS
                for x in itertools.product(al, repeat=c.n_in):
                    assert t.decode_out(name, q, c.run(x)) == t.reference(name, q, n, x), (name, q, n, x)


def test_gadgets_et_compilation():
    for cname, code in sy.ENCODINGS.items():
        gad = gadgets(cname)
        dec = {v: k for k, v in code.items()}
        for name, f in t.FUNCTIONS.items():
            for n in (1, 2):
                tc = f(3, n)
                bc = sy.compile_t2b(tc, gad, code)
                for x in itertools.product(t.TRITS, repeat=tc.n_in):
                    bx = [b for v in x for b in code[v]]
                    out = bc.run(bx)
                    trits = [dec[tuple(out[2 * i:2 * i + 2])] for i in range(len(tc.outs))]
                    assert trits == tc.run(x), (cname, name, n, x)


def test_negation_gratuite_double_rail():
    r, _ = sy.min_gadget("NEG", sy.ENCODINGS["double_rail"])
    assert r == 0


def test_arrondi_par_troncature():
    """Tronquer les k trits de poids faible arrondit au multiple de 3^k le plus proche."""
    n = 7
    for x in range(-(3 ** n - 1) // 2, (3 ** n - 1) // 2 + 1):
        d = t.to_bal(x, n)
        for k in range(1, n):
            y = t.from_bal([0] * k + d[k:])
            assert abs(x - y) <= (3 ** k - 1) // 2
            assert all(abs(x - z * 3 ** k) >= abs(x - y) for z in range(-3 ** (n - k), 3 ** (n - k) + 1))


def test_seuil_poids_ternaires():
    rng = random.Random(1)
    circs = [nb.ripple_adder(3)[0], nb.array_multiplier(2)[0], nb.banded_random(5, 25, 4, rng)]
    for c in circs:
        for comp, wmax in ((t.threshold_ternary, 1), (t.threshold_l03, 2)):
            net, mp = comp(c)
            assert net.max_weight() == wmax
            for x in itertools.product(t.BITS, repeat=c.n_in):
                v, w = c.eval([bool(b) for b in x]), net.eval(x)
                assert all(int(v[i]) == w[mp[i]] for i in range(c.n))


def test_xor_un_seul_neurone_cache_ternaire_impossible():
    assert t.xor_one_hidden_ternary_exists() == []


def test_encodages_sat_coherents():
    rng = random.Random(3)
    code = sy.ENCODINGS["double_rail"]
    gad = gadgets("double_rail")
    tc = t.multiplier(3, 2)
    tb = sy.compile_t2b(tc, gad, code)
    for _ in range(20):
        x = [rng.choice(t.TRITS) for _ in range(tc.n_in)]
        want = tc.run(x)
        # direct
        cnf = st.CNF(); V = st.enc_direct(cnf, tc)
        units = [[V[i][x[i] + 1]] for i in range(tc.n_in)]
        with Solver(name="glucose4", bootstrap_with=cnf.cl + units) as s:
            assert s.solve(); m = set(s.get_model())
        assert [next(v for v in t.TRITS if V[o][v + 1] in m) for o in tc.outs] == want
        # table2
        cnf = st.CNF(); V = st.enc_table2(cnf, tc, code)
        units = [[V[i][j] if code[x[i]][j] else -V[i][j]] for i in range(tc.n_in) for j in range(2)]
        dec = {v: k for k, v in code.items()}
        with Solver(name="glucose4", bootstrap_with=cnf.cl + units) as s:
            assert s.solve(); m = set(s.get_model())
        assert [dec[tuple(int(V[o][j] in m) for j in range(2))] for o in tc.outs] == want
    for enc in (st.enc_direct, lambda c, z, i: st.enc_table2(c, z, code, i)):
        assert st.solve_budget(st.miter_commut(enc, tc).cl)[0] is False
    assert st.solve_budget(st.miter_commut(st.enc_binary, tb, st.valid_pairs(code)).cl)[0] is False
    # sans la contrainte de codes valides, la traduction est incorrecte : le miter du multiplieur
    # compilé à 3 trits devient satisfaisable (constaté avec les gadgets produits ici)
    tb3 = sy.compile_t2b(t.multiplier(3, 3), gad, code)
    assert st.solve_budget(st.miter_commut(st.enc_binary, tb3).cl)[0] is True
    assert st.solve_budget(st.miter_commut(st.enc_binary, tb3, st.valid_pairs(code)).cl)[0] is False


def test_economie_de_radix():
    f = lambda b: b / math.log(b)
    assert f(3) < f(2) and abs(f(2) - f(4)) < 1e-12
    xs = [1.5 + i / 10000 for i in range(30000)]
    assert abs(min(xs, key=f) - math.e) < 1e-3


if __name__ == "__main__":
    for k, v in list(globals().items()):
        if k.startswith("test_"):
            v()
            print("OK", k, flush=True)
