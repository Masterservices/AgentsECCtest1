"""NCE / RTC — banc d'essai v0 (INV-01).

Circuits booléens -> CNF (Tseitin) -> réseau à seuil ; tableau de Cook-Levin ;
mesure de largeur arborescente ; résolution CDCL.

Les largeurs calculées ici sont des BORNES SUPÉRIEURES (meilleure des heuristiques
min-fill-in et min-degree de networkx), pas des valeurs exactes.
"""
import time
import networkx as nx
from networkx.algorithms.approximation import treewidth_min_fill_in, treewidth_min_degree
from pysat.solvers import Solver

# ---------------------------------------------------------------- circuits
# Noeuds 0..n_in-1 = entrées, puis portes (op, [entrées]), op dans AND/OR/XOR. Degré d'entrée 2.

class Circuit:
    def __init__(self, n_in):
        self.n_in = n_in
        self.gates = []

    def add(self, op, a, b):
        self.gates.append((op, [a, b]))
        return self.n_in + len(self.gates) - 1

    @property
    def n(self):
        return self.n_in + len(self.gates)

    def eval(self, x):
        v = list(x)
        for op, (a, b) in self.gates:
            v.append({"AND": v[a] and v[b], "OR": v[a] or v[b], "XOR": v[a] != v[b]}[op])
        return v

    def graph(self):
        g = nx.Graph()
        g.add_nodes_from(range(self.n))
        for k, (_, ins) in enumerate(self.gates):
            for i in ins:
                g.add_edge(self.n_in + k, i)
        return g


def _full_add(c, a, b, cin):
    s1 = c.add("XOR", a, b)
    if cin is None:
        return s1, c.add("AND", a, b)
    return c.add("XOR", s1, cin), c.add("OR", c.add("AND", a, b), c.add("AND", s1, cin))


def ripple_adder(n):
    c = Circuit(2 * n)
    carry, outs = None, []
    for i in range(n):
        s, carry = _full_add(c, i, n + i, carry)
        outs.append(s)
    return c, outs + [carry]


def array_multiplier(n):
    """Multiplieur tableau n x n bits ; renvoie (circuit, bits de sortie de poids 0..2n-1)."""
    c = Circuit(2 * n)
    acc = [None] * (2 * n)
    for i in range(n):
        carry = None
        for j in range(n):
            p = c.add("AND", i, n + j)
            k = i + j
            if acc[k] is None and carry is None:
                acc[k] = p
            elif acc[k] is None:
                acc[k], carry = _full_add(c, p, carry, None)
            else:
                acc[k], carry = _full_add(c, acc[k], p, carry)
        k = i + n
        while carry is not None:
            if acc[k] is None:
                acc[k], carry = carry, None
            else:
                acc[k], carry = _full_add(c, acc[k], carry, None)
                k += 1
    return c, [b for b in acc if b is not None]


def banded_random(n_in, n_gates, window, rng):
    """Chaque porte lit deux noeuds parmi les `window` précédents : la fenêtre contrôle
    la largeur, n_gates fixe la taille."""
    c = Circuit(n_in)
    for _ in range(n_gates):
        a, b = rng.sample(range(max(0, c.n - window), c.n), 2)
        c.add(rng.choice(["AND", "OR", "XOR"]), a, b)
    return c

# ---------------------------------------------------------------- Tseitin

def tseitin(c):
    """Variable CNF = noeud + 1."""
    cl = []
    for k, (op, (a, b)) in enumerate(c.gates):
        z, a, b = c.n_in + k + 1, a + 1, b + 1
        if op == "AND":
            cl += [[-z, a], [-z, b], [z, -a, -b]]
        elif op == "OR":
            cl += [[z, -a], [z, -b], [-z, a, b]]
        else:
            cl += [[-z, a, b], [-z, -a, -b], [z, -a, b], [z, a, -b]]
    return cl


def primal_graph(clauses):
    g = nx.Graph()
    for c in clauses:
        vs = sorted({abs(l) for l in c})
        g.add_nodes_from(vs)
        g.add_edges_from((vs[i], vs[j]) for i in range(len(vs)) for j in range(i + 1, len(vs)))
    return g

# ---------------------------------------------------------------- réseau à seuil

def threshold_network(c):
    """Compilation porte par porte en neurones à seuil (poids entiers, |w| <= 2) :
    AND = [a+b>=2], OR = [a+b>=1], XOR = [a+b-2*h>=1] avec h = AND(a,b) neurone auxiliaire.
    Renvoie le graphe sous-jacent et le nombre de neurones."""
    g = c.graph()
    nxt = c.n
    for k, (op, (a, b)) in enumerate(c.gates):
        if op == "XOR":
            g.add_edges_from([(nxt, a), (nxt, b), (nxt, c.n_in + k)])
            nxt += 1
    return g, nxt


def tw(g):
    if g.number_of_nodes() == 0:
        return 0
    return min(treewidth_min_fill_in(g)[0], treewidth_min_degree(g)[0])

# ---------------------------------------------------------------- Cook-Levin

def tm_tableau(space, steps):
    """Tableau CNF d'une MT déterministe simple sur `space` cellules : la tête fait des
    allers-retours en inversant chaque bit visité (états R et L). Variables à chaque pas :
    s[t,p] (bit), h[t,p] (tête), q[t] (vrai = état R). Renvoie (clauses, nb variables)."""
    var = {}
    def v(*k):
        return var.setdefault(k, len(var) + 1)
    cl = []
    for t in range(steps + 1):
        cl.append([v("h", t, p) for p in range(space)])
        cl += [[-v("h", t, p), -v("h", t, r)] for p in range(space) for r in range(p + 1, space)]
    cl += [[-v("s", 0, p)] for p in range(space)]
    cl += [[v("h", 0, 0)], [v("q", 0)]]
    for t in range(steps):
        qt, qn = v("q", t), v("q", t + 1)
        for p in range(space):
            h, s, s2 = v("h", t, p), v("s", t, p), v("s", t + 1, p)
            # cellule sous la tête : inversée ; ailleurs : inchangée
            cl += [[-h, s, s2], [-h, -s, -s2], [h, -s, s2], [h, s, -s2]]
            # mouvement : R avance (rebond en L au bord droit), L recule (rebond en R au bord gauche)
            if p < space - 1:
                cl += [[-h, -qt, v("h", t + 1, p + 1)], [-h, -qt, qn]]
            else:
                cl += [[-h, -qt, v("h", t + 1, p - 1 if p > 0 else p)], [-h, -qt, -qn]]
            if p > 0:
                cl += [[-h, qt, v("h", t + 1, p - 1)], [-h, qt, -qn]]
            else:
                cl += [[-h, qt, v("h", t + 1, min(1, space - 1))], [-h, qt, qn]]
    return cl, len(var)

# ---------------------------------------------------------------- résolution

def solve(clauses, solver="glucose4"):
    with Solver(name=solver, bootstrap_with=clauses) as s:
        t0 = time.perf_counter()
        r = s.solve()
        dt = time.perf_counter() - t0
        st = s.accum_stats()
    return r, dt, st.get("conflicts", -1), st.get("decisions", -1)


# ---------------------------------------------------------------- borne inférieure (ajout INV-02)

def tw_lower_mmd(g):
    """Borne INFÉRIEURE de largeur arborescente : heuristique de contraction « minor-min-width »
    (MMD+, variante min-d). La largeur arborescente est monotone par mineur et majore le degré
    minimum de tout mineur : max des degrés minimum rencontrés est une borne inférieure valide."""
    adj = {v: set(g[v]) - {v} for v in g}
    lb = 0
    while len(adj) > 1:
        v = min(adj, key=lambda x: len(adj[x]))
        d = len(adj[v])
        lb = max(lb, d)
        if d == 0:
            del adj[v]
            continue
        u = min(adj[v], key=lambda x: len(adj[x]))
        # contraction de v dans u
        for w in adj[v]:
            adj[w].discard(v)
            if w != u:
                adj[w].add(u)
                adj[u].add(w)
        del adj[v]
    return lb


def tw_bounds(g):
    """(borne inférieure MMD+, borne supérieure heuristique). Égalité => valeur exacte."""
    g = g.copy()
    g.remove_nodes_from([v for v in list(g) if g.degree(v) == 0])
    if g.number_of_nodes() == 0:
        return 0, 0
    return tw_lower_mmd(g), tw(g)
