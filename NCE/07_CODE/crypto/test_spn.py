"""Tests de la piste C (INV-02). Usage : python3 test_spn.py (ou pytest)."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import spn  # noqa: E402
from pysat.solvers import Solver  # noqa: E402


def test_sbox_permutation_et_anf():
    assert sorted(spn.SBOX) == list(range(16))
    assert sorted(spn.PERM) == list(range(16))
    for x in range(16):
        for j in range(4):
            v = 0
            for mnm in spn.SBOX_ANF[j]:
                v ^= int(all(x >> i & 1 for i in range(4) if mnm >> i & 1))
            assert v == (spn.SBOX[x] >> j) & 1


def test_cnf_correcte():
    rng = random.Random(5)
    for sbox in ("anf", "table"):
        for k in (16, 24):
            for R in (1, 2, 3):
                K = rng.getrandbits(k)
                pairs = [(P, spn.encrypt(P, K, k, R)) for P in (rng.getrandbits(16) for _ in range(2))]
                e, Kv = spn.key_recovery_cnf(pairs, k, R, sbox)
                units = [[Kv[i] if K >> i & 1 else -Kv[i]] for i in range(k)]
                with Solver(name="glucose4", bootstrap_with=e.cl + units) as s:
                    assert s.solve()                      # la vraie clé satisfait la CNF
                bad = [(pairs[0][0], pairs[0][1] ^ 1)]
                e2, Kv2 = spn.key_recovery_cnf(bad, k, R, sbox)
                with Solver(name="glucose4", bootstrap_with=e2.cl + units) as s:
                    assert not s.solve()                  # un chiffré faux est rejeté
                with Solver(name="glucose4", bootstrap_with=e.cl) as s:
                    assert s.solve()
                    m = set(s.get_model())
                K2 = sum(1 << i for i in range(k) if Kv[i] in m)
                assert all(spn.encrypt(P, K2, k, R) == C for P, C in pairs)   # clé trouvée cohérente


if __name__ == "__main__":
    for k_, v in list(globals().items()):
        if k_.startswith("test_"):
            v()
            print("OK", k_, flush=True)
