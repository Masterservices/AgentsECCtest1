"""RTC / INV-02, piste A.4 — traduction ternaire -> binaire.

Un trit est codé sur 2 bits. Pour chaque porte ternaire, on calcule par SAT (synthèse exacte)
un circuit binaire MINIMAL (portes quelconques à 2 entrées, les 16 fonctions) qui la réalise
sur les codes valides ; les codes invalides sont des « indifférents ». La minimalité est
certifiée par l'insatisfaisabilité au rang r-1 (PROUVÉ, relativement à la correction de
l'encodage SAT, lui-même vérifié par les tests exhaustifs des gadgets).
"""
import itertools
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType

from ternaire import OPS3, TRITS, Circ

# codes : trit -> (bit0, bit1)
ENCODINGS = {
    "double_rail": {1: (1, 0), 0: (0, 0), -1: (0, 1)},   # (p, n) ; (1,1) invalide
    "decale": {-1: (0, 0), 0: (1, 0), 1: (0, 1)},        # t+1 en binaire (poids faible d'abord) ; 11 invalide
    "signe_module": {0: (0, 0), 1: (1, 0), -1: (1, 1)},  # (non nul, signe) ; (0,1) invalide
}


def synth(rows, n_in, n_out, r, solver="cadical153"):
    """Synthèse exacte : existe-t-il un circuit à r portes (2 entrées, fonction quelconque) dont
    les n_out sorties valent rows[t][1] sur l'entrée rows[t][0] ? Renvoie le circuit ou None.
    Une sortie peut être directement une entrée (ex. NEG en double rail : 0 porte)."""
    cnt = [0]

    def new():
        cnt[0] += 1
        return cnt[0]

    N = n_in + r
    cl = []
    sel, fun, val = {}, {}, {}
    for i in range(n_in, N):
        pairs = [(j, k) for j in range(i) for k in range(j + 1, i)]
        if not pairs:
            return None
        for p in pairs:
            sel[i, p] = new()
        lits = [sel[i, p] for p in pairs]
        enc = CardEnc.equals(lits=lits, bound=1, top_id=cnt[0], encoding=EncType.seqcounter)
        cnt[0] = max(cnt[0], enc.nv)
        cl += enc.clauses
        for a in (0, 1):
            for b in (0, 1):
                fun[i, a, b] = new()
        for t in range(len(rows)):
            val[i, t] = new()

    def lit(node, t, v):
        """Littéral « valeur du noeud = v » ; pour une entrée, True/False."""
        if node < n_in:
            return rows[t][0][node] == v
        return val[node, t] if v else -val[node, t]

    for i in range(n_in, N):
        for (ii, p), s in [(k, s) for k, s in sel.items() if k[0] == i]:
            j, k = p
            for t in range(len(rows)):
                for a in (0, 1):
                    for b in (0, 1):
                        la, lb = lit(j, t, a), lit(k, t, b)
                        if la is False or lb is False:
                            continue
                        for c in (0, 1):
                            # (s ∧ x_j=a ∧ x_k=b ∧ f(a,b)=c) -> x_i = c
                            clause = [-s, -fun[i, a, b] if c else fun[i, a, b], val[i, t] if c else -val[i, t]]
                            if la is not True:
                                clause.append(-la)
                            if lb is not True:
                                clause.append(-lb)
                            cl.append(clause)
    out = {}
    for o in range(n_out):
        lits = []
        for h in range(N):
            ok = True
            if h < n_in:
                ok = all(rows[t][0][h] == rows[t][1][o] for t in range(len(rows)))
                if not ok:
                    continue
            out[o, h] = new()
            lits.append(out[o, h])
            if h >= n_in:
                for t in range(len(rows)):
                    cl.append([-out[o, h], val[h, t] if rows[t][1][o] else -val[h, t]])
        if not lits:
            return None
        cl.append(lits)
    # brisure de symétrie : toute porte est utilisée (par une porte ultérieure ou une sortie)
    for i in range(n_in, N):
        users = [s for (g, p), s in sel.items() if i in p]
        users += [out[o, i] for o in range(n_out) if (o, i) in out]
        cl.append(users)
    with Solver(name=solver, bootstrap_with=cl) as S:
        if not S.solve():
            return None
        m = set(l for l in S.get_model() if l > 0)
    gates = []
    for i in range(n_in, N):
        p = next(p for (g, p), s in sel.items() if g == i and s in m)
        tab = {(a, b): int(fun[i, a, b] in m) for a in (0, 1) for b in (0, 1)}
        gates.append((p, tab))
    outs = [next(h for (oo, h), v in out.items() if oo == o and v in m) for o in range(n_out)]
    return gates, outs


def gadget_rows(op, code):
    ar, f = OPS3[op]
    rows = []
    for xs in itertools.product(TRITS, repeat=ar):
        bits = tuple(b for x in xs for b in code[x])
        rows.append((bits, code[f(*xs)]))
    return rows, 2 * ar


def min_gadget(op, code, rmax=9):
    rows, n_in = gadget_rows(op, code)
    for r in range(0, rmax + 1):
        res = synth(rows, n_in, 2, r)
        if res is not None:
            return r, res
    return None, None


def compile_t2b(tc, gadgets, code):
    """Traduit un circuit ternaire en circuit binaire (2 bits par trit) avec les gadgets donnés.
    Les constantes ternaires deviennent des paires de constantes binaires."""
    bc = Circ(2, 2 * tc.n_in)
    wire = {i: (2 * i, 2 * i + 1) for i in range(tc.n_in)}
    for k, (op, ins) in enumerate(tc.gates):
        node = tc.n_in + k
        if isinstance(op, tuple):
            b0, b1 = code[op[1]]
            wire[node] = (bc.const(b0), bc.const(b1))
            continue
        gates, outs = gadgets[op]
        loc = [b for i in ins for b in wire[i]]
        for (j, kk), tab in gates:
            loc.append(bc._raw(dict(tab), (loc[j], loc[kk])))
        wire[node] = (loc[outs[0]], loc[outs[1]])
    bc.outs = [b for o in tc.outs for b in wire[o]]
    return bc
