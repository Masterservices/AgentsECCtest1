"""RTC / INV-02, piste A.4 — traductions ternaire -> SAT.

Trois encodages d'un circuit ternaire, plus le circuit binaire natif :
  direct     : 3 variables par trit (une par valeur), au-moins-un + au-plus-un, et pour chaque
               porte une clause d'implication par combinaison d'entrées (codage « direct » des CSP) ;
  table2     : 2 variables par trit (code donné), clause d'exclusion du code invalide, et pour chaque
               porte et chaque combinaison d'entrées, une clause par bit de sortie ;
  tseitin2   : Tseitin du circuit binaire obtenu par les gadgets minimaux (synthese.compile_t2b) ;
  natif      : Tseitin du circuit binaire natif à m bits (information au moins égale).
Instance de test : miter de commutativité du multiplieur, M(a,b) != M(b,a) (insatisfaisable).
"""
import itertools
import random
import time

from pysat.solvers import Solver

from ternaire import TRITS


class CNF:
    def __init__(self):
        self.nv, self.cl = 0, []

    def new(self):
        self.nv += 1
        return self.nv


def enc_direct(cnf, tc, invars=None):
    """Renvoie la liste des groupes de variables (un groupe [x_-1, x_0, x_1] par noeud)."""
    V = []
    for i in range(tc.n):
        if i < tc.n_in and invars is not None:
            V.append(invars[i])
            continue
        g = [cnf.new() for _ in TRITS]
        V.append(g)
        cnf.cl.append(list(g))
        cnf.cl += [[-g[a], -g[b]] for a in range(3) for b in range(a + 1, 3)]
    for k, (op, ins) in enumerate(tc.gates):
        z = V[tc.n_in + k]
        if isinstance(op, tuple):
            cnf.cl.append([z[op[1] + 1]])
            continue
        f = tc.fn(op)
        for xs in itertools.product(TRITS, repeat=len(ins)):
            cnf.cl.append([-V[i][x + 1] for i, x in zip(ins, xs)] + [z[f(*xs) + 1]])
    return V


def enc_table2(cnf, tc, code, invars=None):
    inv = [c for c in itertools.product((0, 1), repeat=2) if c not in code.values()]
    V = []
    for i in range(tc.n):
        if i < tc.n_in and invars is not None:
            V.append(invars[i])
            continue
        g = [cnf.new(), cnf.new()]
        V.append(g)
        for c in inv:
            cnf.cl.append([-g[j] if c[j] else g[j] for j in range(2)])
    for k, (op, ins) in enumerate(tc.gates):
        z = V[tc.n_in + k]
        if isinstance(op, tuple):
            cb = code[op[1]]
            cnf.cl += [[z[j] if cb[j] else -z[j]] for j in range(2)]
            continue
        f = tc.fn(op)
        for xs in itertools.product(TRITS, repeat=len(ins)):
            pre = []
            for i, x in zip(ins, xs):
                cb = code[x]
                pre += [-V[i][j] if cb[j] else V[i][j] for j in range(2)]
            cz = code[f(*xs)]
            cnf.cl += [pre + [z[j] if cz[j] else -z[j]] for j in range(2)]
    return V


def enc_binary(cnf, bc, invars=None):
    """Tseitin générique d'un circuit binaire (portes nommées ou tables). Un groupe [x] par noeud."""
    V = []
    for i in range(bc.n):
        if i < bc.n_in and invars is not None:
            V.append(invars[i])
        else:
            V.append([cnf.new()])
    for k, (op, ins) in enumerate(bc.gates):
        z = V[bc.n_in + k][0]
        if isinstance(op, tuple):
            cnf.cl.append([z if op[1] else -z])
            continue
        f = bc.fn(op)
        for xs in itertools.product((0, 1), repeat=len(ins)):
            pre = [-V[i][0] if x else V[i][0] for i, x in zip(ins, xs)]
            cnf.cl.append(pre + [z if f(*xs) else -z])
    return V


def valid_pairs(code):
    """Contrainte d'entrée pour un circuit binaire compilé : chaque paire de bits d'entrée porte
    un code valide. SANS elle, la traduction par gadgets n'est pas correcte (les gadgets exploitent
    les codes invalides comme indifférents) : le miter devient satisfaisable."""
    inv = [c for c in itertools.product((0, 1), repeat=2) if c not in code.values()]

    def f(cnf, V, n_in):
        for i in range(0, n_in, 2):
            for c in inv:
                cnf.cl.append([-V[i + j][0] if c[j] else V[i + j][0] for j in range(2)])
    return f


def miter_commut(encode, circ, input_constraint=None):
    """Miter : même circuit, entrées (a,b) puis (b,a) ; au moins un bit de sortie diffère.
    input_constraint(cnf, V, n_in) : clauses supplémentaires sur les entrées (codes valides)."""
    cnf = CNF()
    V1 = encode(cnf, circ, None)
    if input_constraint:
        input_constraint(cnf, V1, circ.n_in)
    n = circ.n_in // 2
    swapped = [V1[(i + n) % (2 * n)] for i in range(2 * n)]  # les groupes de bits restent alignés
    V2 = encode(cnf, circ, swapped)
    ys = []
    for o in circ.outs:
        for x1, x2 in zip(V1[o], V2[o]):
            yp, ym = cnf.new(), cnf.new()
            cnf.cl += [[-yp, x1], [-yp, -x2], [-ym, -x1], [-ym, x2]]
            ys += [yp, ym]
    cnf.cl.append(ys)
    return cnf


def shuffle(cnf, seed):
    """Renommage aléatoire des variables, permutation des clauses et des littéraux."""
    rng = random.Random(seed)
    perm = list(range(1, cnf.nv + 1))
    rng.shuffle(perm)
    mp = {v + 1: perm[v] for v in range(cnf.nv)}
    cl = [[(mp[abs(l)] if l > 0 else -mp[abs(l)]) for l in c] for c in cnf.cl]
    for c in cl:
        rng.shuffle(c)
    rng.shuffle(cl)
    return cl


def solve_budget(clauses, solver="glucose4", budget=2_000_000):
    with Solver(name=solver, bootstrap_with=clauses) as s:
        s.conf_budget(budget)
        t0 = time.perf_counter()
        r = s.solve_limited()
        dt = time.perf_counter() - t0
        st = s.accum_stats()
    return r, dt, st.get("conflicts", -1)
