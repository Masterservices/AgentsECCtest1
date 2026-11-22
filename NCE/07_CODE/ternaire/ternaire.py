"""RTC / INV-02, piste A — circuits ternaires équilibrés (et binaires de référence).

Alphabet ternaire équilibré : {-1, 0, 1} (T = -1). Un trit par fil.
Alphabet binaire : {0, 1}. Un bit par fil.

Modèle de coût commun aux deux radix (choix explicite, discuté dans INV-02_RAPPORT.md) :
une porte = une fonction quelconque à au plus 2 entrées sur l'alphabet (16 fonctions en
binaire, 3^9 = 19 683 en ternaire). Les constantes ne sont pas des portes. Les constructions
ci-dessous sont classiques (propagation de retenue, multiplieur tableau) : ce sont des BORNES
SUPÉRIEURES de taille, pas des circuits minimaux.
"""
import math
import sys
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "benchmarks"))
import nce_bench as nb  # noqa: E402

T = -1
TRITS = (-1, 0, 1)
BITS = (0, 1)


def bal(v):
    """Représentant équilibré de v modulo 3, dans {-1, 0, 1}."""
    return (v + 1) % 3 - 1


def sign(v):
    return (v > 0) - (v < 0)


# ------------------------------------------------------------------ portes
OPS3 = {
    "NEG": (1, lambda a: -a),
    "MIN": (2, min),
    "MAX": (2, max),
    "SUM": (2, lambda a, b: bal(a + b)),             # somme modulo 3
    "CONS": (2, lambda a, b: a if a == b else 0),    # consensus = retenue du demi-additionneur
    "MUL": (2, lambda a, b: a * b),
    "CMP": (2, lambda a, b: sign(a - b)),
    "PRIO": (2, lambda h, l: h if h != 0 else l),    # combinaison lexicographique
    "PAR": (2, lambda a, b: (abs(a) + abs(b)) % 2),  # parité du nombre de chiffres non nuls
}
OPS2 = {
    "NOT": (1, lambda a: 1 - a),
    "AND": (2, lambda a, b: a & b),
    "OR": (2, lambda a, b: a | b),
    "XOR": (2, lambda a, b: a ^ b),
    "XNOR": (2, lambda a, b: 1 - (a ^ b)),
    "NAND": (2, lambda a, b: 1 - (a & b)),
    "NOR": (2, lambda a, b: 1 - (a | b)),
    "ANDN": (2, lambda a, b: a & (1 - b)),            # a ET NON b
    "ORN": (2, lambda a, b: a | (1 - b)),
}


class Circ:
    """Circuit sur l'alphabet {0,1} (q=2) ou {-1,0,1} (q=3).
    Noeuds 0..n_in-1 : entrées ; puis portes (op, entrées). op peut aussi être une table
    (dict {tuple d'entrées: sortie}) — utilisé pour les gadgets synthétisés."""

    def __init__(self, q, n_in):
        assert q in (2, 3)
        self.q, self.n_in = q, n_in
        self.alpha = BITS if q == 2 else TRITS
        self.ops = OPS2 if q == 2 else OPS3
        self.gates = []          # (op, ins) ; op == ("CONST", v) pour une constante
        self.outs = []

    @property
    def n(self):
        return self.n_in + len(self.gates)

    def _raw(self, op, ins):
        self.gates.append((op, tuple(ins)))
        return self.n - 1

    def const(self, v):
        return self._raw(("CONST", v), ())

    def fn(self, op):
        if isinstance(op, dict):
            return lambda *x: op[x]
        return self.ops[op][1]

    def g(self, op, *ins):
        """Ajoute une porte. Les entrées entières Python (ex. 0) sont des constantes : elles
        sont propagées (repliement de constantes) sans créer de porte quand c'est possible."""
        f = self.fn(op)
        consts = [isinstance(i, Const) for i in ins]
        if not any(consts):
            return self._raw(op, ins)
        if all(consts):
            return Const(f(*[i.v for i in ins]))
        # une seule entrée variable (portes à 2 entrées) : table unaire résultante
        k = consts.index(False)
        def u(v):
            args = [i.v if isinstance(i, Const) else v for i in ins]
            return f(*args)
        tab = tuple(u(v) for v in self.alpha)
        if tab == tuple(self.alpha):
            return ins[k]
        if len(set(tab)) == 1:
            return Const(tab[0])
        neg = "NOT" if self.q == 2 else "NEG"
        if tab == tuple(self.fn(neg)(v) for v in self.alpha):
            return self._raw(neg, (ins[k],))
        cn = self.const(ins[1 - k].v)
        args = [cn if isinstance(i, Const) else i for i in ins]
        return self._raw(op, args)

    def set_outs(self, outs):
        self.outs = [self.const(o.v) if isinstance(o, Const) else o for o in outs]
        self._prune()
        return self

    def _prune(self):
        """Élimine les portes qui n'atteignent aucune sortie, et renumérote."""
        live = set(self.outs)
        for k in range(len(self.gates) - 1, -1, -1):
            if self.n_in + k in live:
                live.update(self.gates[k][1])
        new, mp = [], {i: i for i in range(self.n_in)}
        for k, (op, ins) in enumerate(self.gates):
            if self.n_in + k in live:
                mp[self.n_in + k] = self.n_in + len(new)
                new.append((op, tuple(mp[i] for i in ins)))
        self.gates = new
        self.outs = [mp[o] for o in self.outs]

    def eval(self, x):
        v = list(x)
        for op, ins in self.gates:
            if isinstance(op, tuple):
                v.append(op[1])
            else:
                v.append(self.fn(op)(*[v[i] for i in ins]))
        return v

    def run(self, x):
        v = self.eval(x)
        return [v[o] for o in self.outs]

    def is_const(self, node):
        return node >= self.n_in and isinstance(self.gates[node - self.n_in][0], tuple)

    def graph(self):
        g = nx.Graph()
        g.add_nodes_from(i for i in range(self.n) if not self.is_const(i))
        for k, (op, ins) in enumerate(self.gates):
            for i in ins:
                if not self.is_const(i):
                    g.add_edge(self.n_in + k, i)
        return g

    def metrics(self, with_tw=True):
        neg = "NOT" if self.q == 2 else "NEG"
        real = [(k, op, ins) for k, (op, ins) in enumerate(self.gates) if not isinstance(op, tuple)]
        depth = [0] * self.n
        for k, op, ins in real:
            depth[self.n_in + k] = 1 + max([depth[i] for i in ins] or [0])
        d0 = [0] * self.n   # profondeur sans compter les négations (gratuites en double rail)
        for k, op, ins in real:
            d0[self.n_in + k] = (0 if op == neg else 1) + max([d0[i] for i in ins] or [0])
        m = dict(portes=len(real),
                 portes_sans_neg=sum(1 for _, op, _ in real if op != neg),
                 profondeur=max([depth[o] for o in self.outs] or [0]),
                 profondeur_sans_neg=max([d0[o] for o in self.outs] or [0]),
                 fils=sum(1 for _, _, ins in real for i in ins if not self.is_const(i)),
                 entrees=self.n_in, sorties=len(self.outs),
                 bits_par_fil=math.log2(self.q))
        if with_tw:
            lb, ub = nb.tw_bounds(self.graph())
            m.update(tw_inf=lb, tw_sup=ub)
        return m


class Const:
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v


# ------------------------------------------------------------------ codage des nombres

def to_bal(x, n):
    t = []
    for _ in range(n):
        r = bal(x)
        t.append(r)
        x = (x - r) // 3
    assert x == 0, "hors plage"
    return t


def from_bal(t):
    return sum(d * 3 ** i for i, d in enumerate(t))


def to_bin(x, m):
    assert 0 <= x < 2 ** m
    return [(x >> i) & 1 for i in range(m)]


def from_bin(b):
    return sum(d << i for i, d in enumerate(b))


def bits_for(n):
    """Nombre de bits m à information au moins égale à n trits : 2^m >= 3^n."""
    return math.ceil(n * math.log2(3) - 1e-12)


# ------------------------------------------------------------------ additionneurs

def t_ha(c, a, b):
    return c.g("SUM", a, b), c.g("CONS", a, b)


def t_fa(c, a, b, ci):
    s1, c1 = t_ha(c, a, b)
    s, c2 = t_ha(c, s1, ci)
    return s, c.g("SUM", c1, c2)   # c1 et c2 ne sont jamais tous deux non nuls de même signe


def b_ha(c, a, b):
    return c.g("XOR", a, b), c.g("AND", a, b)


def b_fa(c, a, b, ci):
    s1, c1 = b_ha(c, a, b)
    s, c2 = b_ha(c, s1, ci)
    return s, c.g("OR", c1, c2)


def adder(q, n):
    """Addition de deux nombres à n chiffres (ternaire équilibré signé, ou binaire non signé).
    Sorties : n+1 chiffres, poids faible en premier."""
    c = Circ(q, 2 * n)
    ha, fa = (t_ha, t_fa) if q == 3 else (b_ha, b_fa)
    carry, outs = None, []
    for i in range(n):
        if carry is None:
            s, carry = ha(c, i, n + i)
        else:
            s, carry = fa(c, i, n + i, carry)
        outs.append(s)
    return c.set_outs(outs + [carry])


def multiplier(q, n):
    """Multiplieur tableau n x n chiffres -> 2n chiffres (ternaire : signé, produits partiels MUL ;
    binaire : non signé, produits partiels AND)."""
    c = Circ(q, 2 * n)
    pp = (lambda a, b: c.g("MUL", a, b)) if q == 3 else (lambda a, b: c.g("AND", a, b))
    ha, fa = (t_ha, t_fa) if q == 3 else (b_ha, b_fa)
    acc = [None] * (2 * n + 2)
    for i in range(n):
        carry = None
        for j in range(n):
            p, k = pp(j, n + i), i + j
            if acc[k] is None and carry is None:
                acc[k] = p
            elif acc[k] is None:
                acc[k], carry = ha(c, p, carry)
            elif carry is None:
                acc[k], carry = ha(c, acc[k], p)
            else:
                acc[k], carry = fa(c, acc[k], p, carry)
        k = i + n
        while carry is not None:
            if acc[k] is None:
                acc[k], carry = carry, None
            else:
                acc[k], carry = ha(c, acc[k], carry)
                k += 1
    outs = [a if a is not None else Const(0) for a in acc[:2 * n]]
    return c.set_outs(outs)


def comparator(q, n):
    """Comparaison à trois issues de x et y (n chiffres chacun).
    Ternaire : une sortie, sign(x - y) dans {-1,0,1}.
    Binaire (non signé) : deux sorties (lt, eq)."""
    c = Circ(q, 2 * n)
    if q == 3:
        s = c.g("CMP", 0, n)
        for i in range(1, n):
            s = c.g("PRIO", c.g("CMP", i, n + i), s)
        return c.set_outs([s])
    d = c.g("XOR", 0, n)
    lt = c.g("ANDN", n, 0)
    ne = d
    for i in range(1, n):
        d = c.g("XOR", i, n + i)
        lt = c.g("OR", c.g("ANDN", n + i, i), c.g("ANDN", lt, d))
        ne = c.g("OR", ne, d)
    return c.set_outs([lt, c.g("NOT", ne)])


def negation(q, n):
    """Opposé : ternaire, -x chiffre à chiffre ; binaire, complément à deux modulo 2^n."""
    c = Circ(q, n)
    if q == 3:
        return c.set_outs([c.g("NEG", i) for i in range(n)])
    outs, o = [0], 0
    for i in range(1, n):
        outs.append(c.g("XOR", i, o))
        if i < n - 1:
            o = c.g("OR", o, i)
    return c.set_outs(outs)


def digit_sum(q, n):
    """Somme des chiffres modulo la base (parité booléenne en binaire, somme mod 3 en ternaire)."""
    c = Circ(q, n)
    s = 0
    for i in range(1, n):
        s = c.g("XOR" if q == 2 else "SUM", s, i)
    return c.set_outs([s])


def mod2(q, n):
    """x mod 2. Binaire : le bit de poids faible (0 porte). Ternaire : parité du nombre de
    chiffres non nuls, car 3 ≡ 1 (mod 2)."""
    c = Circ(q, n)
    if q == 2:
        return c.set_outs([0])
    s = 0
    for i in range(1, n):
        s = c.g("PAR", s, i)
    if n == 1:
        s = c.g("PAR", 0, Const(0))
    return c.set_outs([s])


def mod3(q, n):
    """x mod 3. Ternaire : le trit de poids faible (0 porte), à valeur dans {-1,0,1}.
    Binaire : accumulateur modulo 3 sur 2 bits (r1 r0 = résidu en binaire), poids 2^i ≡ ±1."""
    c = Circ(q, n)
    if q == 3:
        return c.set_outs([0])
    r1, r0 = Const(0), 0
    for i in range(1, n):
        b = i
        if i % 2 == 0:   # poids +1
            nr0 = c.g("XOR", r0, c.g("ANDN", b, r1))
            nr1 = c.g("XOR", r1, c.g("AND", b, c.g("XOR", r1, r0)))
        else:            # poids 2 ≡ -1
            nr1 = c.g("XOR", r1, c.g("ANDN", b, r0))
            nr0 = c.g("XOR", r0, c.g("AND", b, c.g("XOR", r0, r1)))
        r0, r1 = nr0, nr1
    return c.set_outs([r0, r1])


FUNCTIONS = {
    "addition": adder,
    "multiplication": multiplier,
    "comparaison": comparator,
    "opposé": negation,
    "somme_chiffres_mod_base": digit_sum,
    "x_mod_2": mod2,
    "x_mod_3": mod3,
}


def reference(name, q, n, x):
    """Spécification de référence (valeurs entières) pour les tests exhaustifs."""
    dec = from_bal if q == 3 else from_bin
    if name in ("addition", "multiplication", "comparaison"):
        a, b = dec(x[:n]), dec(x[n:])
        if name == "addition":
            return a + b
        if name == "multiplication":
            return a * b
        return sign(a - b)
    a = dec(x)
    if name == "opposé":
        return -a if q == 3 else (-a) % (2 ** n)
    if name == "somme_chiffres_mod_base":
        return bal(sum(x)) if q == 3 else sum(x) % 2
    if name == "x_mod_2":
        return a % 2
    if name == "x_mod_3":
        return a % 3


def decode_out(name, q, outs):
    if name == "comparaison" and q == 2:
        lt, eq = outs
        return 0 if eq else (-1 if lt else 1)
    if name in ("somme_chiffres_mod_base", "x_mod_2") or (name == "comparaison"):
        return outs[0]
    if name == "x_mod_3":
        return outs[0] % 3 if q == 3 else from_bin(outs)
    return from_bal(outs) if q == 3 else from_bin(outs)


# ------------------------------------------------------------------ neurones à seuil, poids ternaires

class ThresholdNet:
    """Réseau de neurones à seuil : neurone = (entrées, poids, seuil), sortie [Σ w x >= θ]."""

    def __init__(self, n_in):
        self.n_in, self.neurons = n_in, []

    def add(self, ins, ws, th):
        self.neurons.append((tuple(ins), tuple(ws), th))
        return self.n_in + len(self.neurons) - 1

    def eval(self, x):
        v = list(x)
        for ins, ws, th in self.neurons:
            v.append(int(sum(w * v[i] for i, w in zip(ins, ws)) >= th))
        return v

    def graph(self):
        g = nx.Graph()
        g.add_nodes_from(range(self.n_in + len(self.neurons)))
        for k, (ins, _, _) in enumerate(self.neurons):
            g.add_edges_from((self.n_in + k, i) for i in ins)
        return g

    def max_weight(self):
        return max(abs(w) for _, ws, _ in self.neurons for w in ws)


def threshold_ternary(c):
    """Compilation porte par porte d'un nb.Circuit (AND/OR/XOR) en neurones à poids dans {-1,0,1}.
    AND = [a+b>=2], OR = [a+b>=1], XOR = [o-h>=1] avec o = OR, h = AND (deux auxiliaires).
    Renvoie (réseau, table noeud du circuit -> neurone)."""
    net = ThresholdNet(c.n_in)
    mp = {i: i for i in range(c.n_in)}
    for k, (op, (a, b)) in enumerate(c.gates):
        A, B = mp[a], mp[b]
        if op == "AND":
            z = net.add((A, B), (1, 1), 2)
        elif op == "OR":
            z = net.add((A, B), (1, 1), 1)
        else:
            o = net.add((A, B), (1, 1), 1)
            h = net.add((A, B), (1, 1), 2)
            z = net.add((o, h), (1, -1), 1)
        mp[c.n_in + k] = z
    return net, mp


def threshold_l03(c):
    """Compilation L-03 (poids |w| <= 2) : XOR = [a+b-2h>=1], h = AND auxiliaire."""
    net = ThresholdNet(c.n_in)
    mp = {i: i for i in range(c.n_in)}
    for k, (op, (a, b)) in enumerate(c.gates):
        A, B = mp[a], mp[b]
        if op == "AND":
            z = net.add((A, B), (1, 1), 2)
        elif op == "OR":
            z = net.add((A, B), (1, 1), 1)
        else:
            h = net.add((A, B), (1, 1), 2)
            z = net.add((A, B, h), (1, 1, -2), 1)
        mp[c.n_in + k] = z
    return net, mp


def xor_one_hidden_ternary_exists():
    """Recherche exhaustive : XOR(a,b) est-il calculable par un neurone caché h (poids ternaires
    sur a,b) suivi d'un neurone de sortie y (poids ternaires sur a, b, h), seuils entiers ?
    Les seuils utiles sont bornés par la somme des |poids| : la recherche est complète."""
    W = (-1, 0, 1)
    sols = []
    for w1 in W:
        for w2 in W:
            for t1 in range(-2, 4):
                h = {(a, b): int(w1 * a + w2 * b >= t1) for a in BITS for b in BITS}
                for v1 in W:
                    for v2 in W:
                        for v3 in W:
                            for t2 in range(-3, 5):
                                if all(int(v1 * a + v2 * b + v3 * h[a, b] >= t2) == (a ^ b)
                                       for a in BITS for b in BITS):
                                    sols.append((w1, w2, t1, v1, v2, v3, t2))
    return sols
