"""RTC / INV-02, piste C — chiffrement jouet SPN (réseau substitution-permutation) et sa
traduction en CNF pour la récupération de clé.

JOUET PÉDAGOGIQUE, construit pour l'expérience : AUCUNE prétention de sécurité.
  bloc b = 16 bits (4 boîtes S de 4 bits), clé maître k bits (16, 24 ou 32), R tours :
      pour r = 0..R-1 : x ^= K_r ; x = S(x) ; si r < R-1 : x = P(x)
      puis x ^= K_R.
  K_r = 16 bits de poids faible de rotl_k(K, 7r).
  Boîte S : celle de PRESENT (Bogdanov et al., CHES 2007 ; valeurs vérifiées le 2026-11-22 :
  https://www.iacr.org/archive/ches2007/47270450/47270450.pdf). Les tests vérifient la bijectivité.
  P : bit i -> bit 4i mod 15 (i < 15), bit 15 fixe.
Encodages CNF de la boîte S :
  anf   : forme normale algébrique -> portes ET / OU-exclusif -> Tseitin (traduction « circuit ») ;
  table : clauses directes depuis la table de vérité (64 clauses de 5 littéraux par boîte).
Le clair est connu : la première addition de clé se réduit à des littéraux (x = ±K_0), sans porte.
"""
import itertools

SBOX = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]
B = 16
PERM = [(4 * i) % 15 if i < 15 else 15 for i in range(B)]


def round_keys(K, k, R):
    mask = (1 << k) - 1
    out = []
    for r in range(R + 1):
        s = (7 * r) % k
        rot = ((K << s) | (K >> (k - s))) & mask if s else K
        out.append(rot & 0xFFFF)
    return out


def sub(x):
    return sum(SBOX[(x >> (4 * j)) & 0xF] << (4 * j) for j in range(4))


def perm(x):
    return sum(((x >> i) & 1) << PERM[i] for i in range(B))


def encrypt(P, K, k, R):
    ks = round_keys(K, k, R)
    x = P
    for r in range(R):
        x = sub(x ^ ks[r])
        if r < R - 1:
            x = perm(x)
    return x ^ ks[R]


def anf(table, nbits=4):
    """Coefficients de la forme normale algébrique (transformée de Möbius) d'une fonction
    booléenne donnée par sa table : renvoie l'ensemble des monômes (masques) de coefficient 1."""
    a = list(table)
    for i in range(nbits):
        for x in range(1 << nbits):
            if x >> i & 1:
                a[x] ^= a[x ^ (1 << i)]
    return [m for m in range(1 << nbits) if a[m]]


SBOX_ANF = [anf([(SBOX[x] >> j) & 1 for x in range(16)]) for j in range(4)]


def differential_uniformity():
    return max(sum(1 for x in range(16) if SBOX[x] ^ SBOX[x ^ a] == b) for a in range(1, 16) for b in range(16))


def linearity():
    return max(abs(sum((-1) ** (bin(x & a).count("1") + bin(SBOX[x] & b).count("1") & 1) for x in range(16)))
               for a in range(16) for b in range(1, 16))


class Enc:
    """Construction CNF par littéraux (NON = négation de littéral, sans porte)."""

    def __init__(self):
        self.nv, self.cl = 0, []
        self.order = []   # ordre de création des variables (pour l'ordre d'élimination explicite)

    def new(self):
        self.nv += 1
        self.order.append(self.nv)
        return self.nv

    def AND(self, a, b):
        z = self.new()
        self.cl += [[-z, a], [-z, b], [z, -a, -b]]
        return z

    def XOR(self, a, b):
        z = self.new()
        self.cl += [[-z, a, b], [-z, -a, -b], [z, -a, b], [z, a, -b]]
        return z

    def sbox_anf(self, x):
        mono = {}

        def m(mask):
            if mask in mono:
                return mono[mask]
            bits = [i for i in range(4) if mask >> i & 1]
            if len(bits) == 1:
                mono[mask] = x[bits[0]]
            else:
                top = 1 << bits[-1]
                mono[mask] = self.AND(m(mask ^ top), x[bits[-1]])
            return mono[mask]
        outs = []
        for j in range(4):
            terms = [t for t in SBOX_ANF[j] if t != 0]
            neg = 0 in SBOX_ANF[j]
            acc = m(terms[0])
            for tt in terms[1:]:
                acc = self.XOR(acc, m(tt))
            outs.append(-acc if neg else acc)
        return outs

    def sbox_table(self, x):
        y = [self.new() for _ in range(4)]
        for v in range(16):
            pre = [-x[i] if v >> i & 1 else x[i] for i in range(4)]
            s = SBOX[v]
            self.cl += [pre + [y[j] if s >> j & 1 else -y[j]] for j in range(4)]
        return y


def key_recovery_cnf(pairs, k, R, sbox="anf"):
    """CNF : il existe K (variables 1..k) tel que Enc(K, P) = C pour chaque couple (P, C)."""
    e = Enc()
    K = [e.new() for _ in range(k)]
    mask = (1 << k) - 1

    def kbit(r, i):   # bit i de K_r = bit (i - s) mod k de K
        s = (7 * r) % k
        return K[(i - s) % k]
    for P, C in pairs:
        x = [-kbit(0, i) if P >> i & 1 else kbit(0, i) for i in range(B)]
        for r in range(R):
            if r > 0:
                x = [e.XOR(x[i], kbit(r, i)) for i in range(B)]
            y = []
            for j in range(4):
                y += (e.sbox_anf if sbox == "anf" else e.sbox_table)(x[4 * j:4 * j + 4])
            if r < R - 1:
                z = [None] * B
                for i in range(B):
                    z[PERM[i]] = y[i]
                y = z
            x = y
        for i in range(B):      # x_i XOR K_R,i = C_i
            a, kk = x[i], kbit(R, i)
            if C >> i & 1:
                e.cl += [[a, kk], [-a, -kk]]
            else:
                e.cl += [[-a, kk], [a, -kk]]
    return e, K


def elimination_width(clauses, order):
    """Largeur de l'ordre d'élimination donné sur le graphe primal (borne supérieure de tw)."""
    adj = {}
    for c in clauses:
        vs = {abs(l) for l in c}
        for v in vs:
            adj.setdefault(v, set()).update(vs - {v})
    pos = {v: i for i, v in enumerate(order)}
    w = 0
    for v in order:
        if v not in adj:
            continue
        nb_ = adj.pop(v)
        nb_ = {u for u in nb_ if u in adj}
        w = max(w, len(nb_))
        for u in nb_:
            adj[u].update(nb_ - {u})
            adj[u].discard(v)
    return w
