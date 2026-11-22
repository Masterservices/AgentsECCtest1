# INV-02 — Ternaire équilibré, théorie de l'information, cryptographie : trois pistes évaluées (rapport v1)

Date : 2026-11-22. Code : `07_CODE/ternaire/`, `07_CODE/crypto/`. Données : `08_DATA/inv02_ternaire.json`, `inv02_info.json`, `inv02_crypto.json`. Environnement : Python 3.13, networkx 3.7, PySAT (Glucose 4 pour les mesures, CaDiCaL 1.5.3 pour la synthèse exacte). Durée totale des trois expériences : environ 6 minutes (e02a 135 s, e02b environ 30 s, e02c 181 s). Graines fixées.

Conventions de statut : PROUVÉ (preuve ici ou vérification exhaustive), CONNU (littérature), EXPÉRIMENTAL, CONJECTURE, RÉFUTÉ, OUVERT. Les références citées de mémoire portent « à vérifier ». Celles qui ont été vérifiées en ligne portent un lien.

## Résumé (10 lignes)

1. **A, ternaire.** Le ternaire ne change aucune classe de complexité. Les traductions dans les deux sens ont un surcoût constant en taille, en profondeur et en largeur (PROUVÉ, §A.6).
2. En comptant une porte ternaire à 2 entrées comme 1, le ternaire paraît 1,6 à 4 fois plus petit. Ce gain est un artefact du modèle de coût : une porte ternaire est une table de 9 cases (EXPÉRIMENTAL, §A.3).
3. Ramené à une même unité, la porte binaire, le ternaire *perd* sur l'arithmétique : ×2,7 pour l'addition et ×1,65 pour la multiplication à n = 8 trits. Il *gagne* sur l'opposé (0 porte en double rail, contre 49) et sur x mod 3 (0 contre 123). Il est à égalité sur la comparaison (EXPÉRIMENTAL, gadgets minimaux PROUVÉS par SAT).
4. Le coût CDCL d'un miter de multiplieur suit le contenu d'information, pas la base. À n = 5 trits contre m = 8 bits, les quatre encodages donnent entre 143 000 et 167 000 conflits (EXPÉRIMENTAL, 3 graines).
5. L'économie de radix favorise 3 sur 2 d'un facteur 0,946 (PROUVÉ, résultat connu). Le gain réel est faible et dépend du modèle de coût.
6. Poids ternaires {−1, 0, 1} : tout circuit {ET, OU, OU-exclusif} se compile avec 3 neurones par OU-exclusif, contre 2 dans L-03, et la largeur est préservée. Un seul neurone caché à poids ternaires ne suffit pas pour le OU-exclusif (PROUVÉ par recherche exhaustive).
7. **B, information.** La borne de coupe H(f(X)) ≤ c·log₂ q se transporte d'un modèle à l'autre (PROUVÉ, élémentaire). La traduction double rail double exactement la coupe minimale mesurée (EXPÉRIMENTAL). Les seules bornes inférieures transportables solides restent celles de la complexité de communication (CONNU).
8. **C, crypto.** Sur un SPN jouet de 16 bits, H-C1 est **RÉFUTÉE dans sa forme forte**. La largeur est bornée par k + constante, quel que soit le nombre de tours (PROUVÉ, esquisse et mesure), alors que le coût CDCL continue de croître : de 11 à 41 000 conflits pour k = 16, et jusqu'à 300 000 pour k = 24.
9. La corrélation entre largeur et conflits vaut 1, mais elle est **confondue** avec le nombre de tours, et la borne supérieure de largeur sature dès R = 3 alors que le coût continue d'augmenter.
10. **Verdict.** A ne mérite pas un tome : c'est un chapitre « changement d'alphabet » d'un tome existant. B mérite un tome, centré sur la communication et les coupes. C mérite un chapitre, qui fournit des contre-exemples à « largeur ⇒ difficulté ».

---

## Piste A — Calcul ternaire équilibré

### A.1 Définitions (PROUVÉ, vérifiées exhaustivement par `test_ternaire.py`)

Alphabet {T, 0, 1}, avec T = −1, et un trit par fil. On note bal(v) le représentant de v mod 3 dans {−1, 0, 1}.

| Porte | Définition | Rôle |
|---|---|---|
| NEG(a) | −a | négation |
| MIN, MAX | ordre T < 0 < 1 | analogues de ET et OU (logique de Kleene ou Łukasiewicz à 3 valeurs, à vérifier) |
| SUM(a, b) | bal(a + b) | somme modulo 3 |
| CONS(a, b) | a si a = b, sinon 0 | consensus |
| MUL(a, b) | a·b | produit de trits |
| CMP(a, b) | sign(a − b) | comparaison d'un chiffre |
| PRIO(h, l) | h si h ≠ 0, sinon l | combinaison lexicographique |
| PAR(a, b) | (\|a\| + \|b\|) mod 2 | parité des chiffres non nuls |

- **Demi-additionneur** : a + b = 3·CONS(a, b) + SUM(a, b), pour tous a, b (PROUVÉ, 9 cas).
- **Additionneur complet** : s₁ = SUM(a, b), c₁ = CONS(a, b), s = SUM(s₁, c), c₂ = CONS(s₁, c), cₒ = SUM(c₁, c₂), en 5 portes comme en binaire. On a a + b + c = 3cₒ + s (PROUVÉ, 27 cas). La retenue s'écrit SUM(c₁, c₂) parce que c₁ et c₂ ne sont jamais non nuls de même signe : c₁ = 1 impose s₁ = −1, donc c₂ ∈ {−1, 0}.
- **Arrondi par troncature** : supprimer les k trits de poids faible donne le multiple de 3^k le plus proche, avec une erreur ≤ (3^k − 1)/2. La raison est que |Σ_{i<k} t_i 3^i| ≤ Σ_{i<k} 3^i = (3^k − 1)/2 (PROUVÉ ; vérifié exhaustivement pour n = 7).

**Modèle de coût (choix explicite).** Une porte est une fonction *quelconque* à au plus 2 entrées sur l'alphabet : 16 fonctions en binaire, 3⁹ = 19 683 en ternaire. Les constantes sont gratuites. Les circuits sont des constructions classiques (retenue propagée, multiplieur tableau, comparateur en chaîne) : ce sont des **bornes supérieures de taille**, pas des circuits minimaux.

### A.2 Fonctions et information égale

On compare n trits à m = ⌈n·log₂3⌉ bits, ce qui donne 2^m ≥ 3^n. Pour les petits n, le binaire reçoit jusqu'à 26 % d'information en plus (n = 2 : 3,17 bits contre 4). Le ternaire est équilibré, donc **signé**. Le binaire est non signé, sauf pour l'opposé, calculé en complément à deux. Fonctions comparées :
- addition, avec n + 1 chiffres en sortie ;
- multiplication, avec 2n chiffres ;
- comparaison à trois issues : une sortie sign(x − y) en ternaire, deux sorties (lt, eq) en binaire ;
- opposé ;
- somme des chiffres modulo la base, c'est-à-dire la parité booléenne en binaire ;
- x mod 2 et x mod 3.

### A.3 Mesures (E-02a, `08_DATA/inv02_ternaire.json`, extrait)

Les largeurs sont données par un encadrement [borne inférieure MMD+, borne supérieure heuristique]. Une valeur unique signifie que les deux bornes coïncident, donc que la largeur est exacte (conformément à F-004). T→B désigne la traduction en double rail par gadgets minimaux (§A.4).

| Fonction | n / m | Portes T | Portes B | Portes T→B | Profondeur T / B / T→B | Largeur T | Largeur B | Largeur T→B |
|---|---|---|---|---|---|---|---|---|
| addition | 8 / 13 | 37 | 62 | 162 | 15 / 25 / 31 | 2 | 2 | [4, 5] |
| addition | 16 / 26 | 77 | 127 | 338 | 31 / 51 / 63 | 2 | 2 | [4, 5] |
| multiplication | 4 / 7 | 64 | 238 | 304 | 16 / 34 / 37 | [5, 12] | [7, 23] | [9, 23] |
| multiplication | 8 / 13 | 320 | 910 | 1 504 | 40 / 70 / 93 | [8, 25] | [11, 41] | [14, 49] |
| comparaison | 16 / 26 | 31 | 128 | 124 | 16 / 51 / 32 | 1 | 3 | 3 |
| opposé | 16 / 26 | 16 (0 hors NEG) | 49 | **0** | 1 / 25 / 0 | 1 | 2 | 0 |
| somme des chiffres mod base | 16 / 26 | 15 | 25 | 90 | 15 / 25 / 45 | 1 | 1 | 3 |
| x mod 2 | 16 / 26 | 15 | **0** | 60 | 15 / 0 / 45 | 1 | 0 | 3 |
| x mod 3 | 16 / 26 | **0** | 123 | 0 | 0 / 74 / 0 | 0 | 3 | 0 |

**Lecture (EXPÉRIMENTAL, n ≤ 16, constructions classiques non minimales).**
- **En portes natives**, le ternaire a moins de portes et une profondeur plus faible :
  - addition : ×0,61 en portes et ×0,61 en profondeur, ce qui correspond au facteur 1/log₂3 = 0,63 attendu, puisqu'il y a 1,58 fois moins de chiffres ;
  - multiplication : ×0,35, le facteur (1/log₂3)² = 0,40 venant des n² produits partiels.
- **Le compte natif n'est pas une comparaison équitable.** Ramené en portes binaires par la traduction, le ternaire coûte ×2,7 pour l'addition et ×1,65 pour la multiplication (avec un rapport qui croît de 0,63 à n = 2 jusqu'à 1,65 à n = 8). Il fait jeu égal sur la comparaison (124 contre 128).
- **Avec le « coût de radix »** (fils × base, la mesure de l'économie de radix), l'addition à n = 16 donne 462 en ternaire contre 508 en binaire, soit un rapport de 0,91. Ce rapport est proche du 0,946 théorique.
- **Largeur.** Elle est de même ordre dans les trois versions. La traduction multiplie au plus par une constante (addition : 2 → [4, 5]), comme le prévoit L-T2.
- **Asymétries structurelles exactes** : x mod 3 est gratuit en ternaire et coûte 123 portes en binaire, x mod 2 est gratuit en binaire et coûte 15 portes en ternaire. Le gain dépend de l'arithmétique de la fonction et non d'une supériorité générale.

### A.4 Traductions ternaire → binaire → SAT

**Gadgets minimaux.** Ils ont été obtenus par synthèse exacte SAT (`synthese.py`) : un trit est codé sur 2 bits, les portes binaires sont quelconques à 2 entrées, et les codes invalides sont traités comme indifférents. La minimalité est PROUVÉE, au sens où le rang r − 1 est insatisfaisable, relativement à la correction de l'encodage. Les gadgets sont vérifiés exhaustivement.

| Code | NEG | MIN | MAX | SUM | CONS | MUL | CMP | PRIO | PAR |
|---|---|---|---|---|---|---|---|---|---|
| double rail : 1 = 10, 0 = 00, T = 01 | **0** | 2 | 2 | 6 | 2 | 6 | 4 | 4 | 4 |
| décalé (t + 1 en binaire) | 1 | 5 | 3 | 6 | 4 | 3 | 6 | 3 | 2 |
| signe-module (non nul, signe) | 1 | 3 | 5 | 6 | 4 | 3 | 6 | 3 | 2 |

- **Négation gratuite** : en double rail, NEG consiste à échanger deux fils, soit 0 porte (PROUVÉ). C'est l'avantage ternaire le plus net, mais il appartient au *codage double rail* et pas au ternaire en soi : un binaire en double rail a aussi la négation gratuite (CONNU en logique double rail, à vérifier).
- **Le code compte.** Aucun code n'est meilleur pour toutes les portes : MUL coûte 6 en double rail et 3 en signe-module, MIN coûte 2 en double rail et 5 en code décalé. Le coût de la traduction T→B dépend donc d'un choix de codage, ce qui illustre la remarque de DEFINITIONS.md D2 sur la notion trop permissive de « codage ».
- **Correction conditionnelle (PROUVÉ et vérifié).** La traduction par gadgets n'est correcte que si les entrées portent des codes valides. Sans la clause d'exclusion du code invalide, le miter du multiplieur compilé à 3 trits devient **satisfaisable** (test `test_encodages_sat_coherents`). Une traduction à ressources doit donc emporter son *invariant de codage* comme précondition.

**Lemme L-T2 (la traduction par gadgets préserve la largeur, PROUVÉ).** On note :
- C un circuit ternaire de degré d'entrée ≤ k et de largeur w ;
- s la taille maximale d'un gadget, sorties comprises.

Alors le circuit binaire traduit a une largeur ≤ (s + 2k)(w + 1) − 1.

*Preuve.* On reprend celle de L-01. On remplace chaque nœud x d'un sac par S(x), formé des nœuds du gadget de x et des 2k bits de sortie des gadgets de ses entrées. La couverture et la connexité s'établissent comme pour L-01. ∎ Les mesures, par exemple addition 2 → [4, 5], sont très en dessous de la borne.

**SAT : miter de commutativité du multiplieur M(a, b) ≠ M(b, a)**, insatisfaisable, 3 graines de mélange (renommage des variables, ordre des clauses), Glucose 4. Valeurs médianes :

| n / m | direct, 3 variables par trit | table, 2 bits par trit | Tseitin des gadgets, 2 bits par trit | binaire natif, m bits |
|---|---|---|---|---|
| 2 / 4 | 186 | 245 | 181 | 624 |
| 3 / 5 | 1 797 | 2 428 | 1 985 | 2 525 |
| 4 / 7 | 16 370 | 18 872 | 18 069 | 39 262 |
| 5 / 8 | 167 170 (8,3 s) | 153 635 (7,4 s) | 142 847 (10,4 s) | 156 365 (8,2 s) |

- Taille des instances à n = 5 (variables / clauses) : 750 / 3 021 en direct, 500 / 4 271 en table, 1 100 / 4 251 pour Tseitin, 688 / 2 625 en natif.
- Écart entre graines : ±10 %.

**Lecture (EXPÉRIMENTAL, 4 tailles × 3 graines, un seul solveur, une seule famille).** À information presque égale (n = 5, m = 8 : 243² = 59 049 contre 65 536 couples d'entrées), les quatre encodages se valent à ±15 %. L'avance apparente du ternaire à n ≤ 4 s'explique par l'excès d'information du binaire : à n = 4, il a 2,5 fois plus de couples d'entrées. Aucun encodage ternaire ne rend l'instance qualitativement plus facile, et aucun ne la rend plus difficile.

### A.5 Économie de radix (PROUVÉ, résultat CONNU)

Représenter N valeurs en base b coûte E(b) = b·log_b N = (b / ln b)·ln N, si l'on suppose un coût proportionnel à la base par chiffre. Posons f(b) = b / ln b. On a f′(b) = (ln b − 1)/ln²b, qui s'annule en b = e. Comme f est décroissante sur ]1, e] et croissante ensuite, le minimum est atteint en b = e. Parmi les entiers :
- f(2) = f(4) = 2,885 et f(3) = 2,731, donc **3 est optimal**, avec un gain de 5,4 % sur 2 ;
- f(5) = 3,107 et f(10) = 4,343.

Ce résultat est classique (Knuth, *TAOCP* vol. 2, §4.1, à vérifier ; le calculateur ternaire Setun, Université de Moscou, fin des années 1950, à vérifier).

**Limites du résultat.** L'hypothèse « coût ∝ base » est un *modèle* et non une loi physique. Avec le coût par porte de A.3, le classement s'inverse pour l'arithmétique.

**Densité.**
- Un trit porte log₂3 = 1,585 bit.
- Coder un trit sur 2 bits a une efficacité de 79,2 %.
- Grouper 5 trits dans 8 bits (3⁵ = 243 ≤ 256) a une efficacité de 99,06 % (PROUVÉ, arithmétique).

### A.6 Ce que le ternaire ne change pas (PROUVÉ)

- **Binaire → ternaire.** Un bit est un trit restreint à {0, 1}. On a ET = MIN et OU = MAX. OU-exclusif = MUL(d, d) avec d = SUM(a, NEG b), soit 3 portes. NON(a) = SUM(NEG a, 1), avec une constante.
- **Ternaire → binaire.** On utilise les gadgets de A.4, de taille ≤ 6.

Les deux surcoûts sont des facteurs constants en taille et en profondeur, et la largeur est préservée à facteur constant (L-T2). Il en résulte que **toutes les classes de circuits définies à facteur constant ou polynomial près sont identiques** : AC⁰ (MIN et MAX non bornés traduisent ET et OU non bornés), NC¹, P/poly. Par la même traduction appliquée au ruban, les machines de Turing ternaires et binaires définissent les mêmes classes de temps et d'espace à facteur constant près (CONNU). Le facteur est constant : **aucune classe de complexité ne change**.

### A.7 Réseaux à poids ternaires et lien avec L-03

**Lemme L-T1 (PROUVÉ, vérifié exhaustivement).** Tout circuit {ET, OU, OU-exclusif} de degré 2 se compile en un réseau de neurones à seuil à **poids dans {−1, 0, 1}** avec seuils dans {1, 2} :
- ET = [a + b ≥ 2] ;
- OU = [a + b ≥ 1] ;
- OU-exclusif = [o − h ≥ 1], avec o = OU(a, b) et h = ET(a, b) comme neurones auxiliaires.

La largeur est ≤ (k + 3)(w + 1) − 1, par l'argument de L-03 avec deux auxiliaires.

**Proposition (PROUVÉ, recherche exhaustive complète).** Aucun réseau formé d'un neurone caché h, à poids ternaires sur (a, b), et d'un neurone de sortie à poids ternaires sur (a, b, h) ne calcule le OU-exclusif. La recherche est complète parce que les seuils au-delà de la somme des |poids| donnent des constantes. Le poids −2 de L-03 n'est donc pas un artefact : passer des poids ≤ 2 aux poids ternaires coûte un neurone de plus par OU-exclusif dans cette architecture.

**Mesures.**

| Circuit | Largeur du circuit | L-03 : neurones, arêtes, largeur | Poids ternaires : neurones, arêtes, largeur |
|---|---|---|---|
| additionneur 8 bits | 2 | 52, 119, 3 | 67, 134, 3 |
| multiplieur 4×4 | [5, 12] | 84, 188, [5, 12] | 104, 208, [6, 12] |

Coût mesuré : environ 25 % de neurones en plus, et une largeur inchangée (EXPÉRIMENTAL).

**Lien général (CONNU, à vérifier).** Un poids entier |w| ≤ W se remplace par W copies d'arête de poids ±1, ce qui multiplie le degré d'entrée par W. Pour des poids exponentiels (K-08, Håstad), il faut des constructions en profondeur plus grande : la simulation de portes à grands poids par des circuits de profondeur bornée à petits poids est due à Goldmann, Håstad et Razborov, ainsi qu'à Siu et Bruck (vers 1991-1992, à vérifier).

**Réseaux ternaires appris.** BitNet b1.58 (Ma et al., 2024, [arXiv:2402.17764](https://arxiv.org/abs/2402.17764), vérifié) utilise des poids dans {−1, 0, 1}. Les « 1,58 bits » de son titre valent log₂3. Le résultat L-T1 dit seulement que ces poids suffisent à la *représentation exacte* d'un circuit, à facteur constant près. Il ne dit rien de l'apprentissage : sur ce point, voir H-B3 dans INV-01.

### A.8 Limites de la piste A

- Circuits non minimaux : les rapports de taille sont des rapports entre constructions, pas entre complexités de circuits.
- Largeur encadrée, avec un encadrement lâche pour les multiplieurs.
- SAT : une seule famille d'instances (miters), n ≤ 5, un solveur, 3 graines.
- Aucune mesure physique : énergie et surface ne sont pas modélisées.

---

## Piste B — La théorie de l'information comme fil conducteur

### B.1 Ce qui est CONNU (toutes références à vérifier sur source primaire, sauf lien)

| Mesure | Résultat | Ce qu'il dit pour RTC |
|---|---|---|
| Kolmogorov | Théorème d'invariance : K_U(x) ≤ K_V(x) + c_{U,V} (Solomonoff, Kolmogorov, Chaitin, années 1960, à vérifier) | C'est **exactement** un énoncé de traduction : la *taille de description* est préservée à une constante additive près par toute traduction entre modèles universels, la constante étant la taille du compilateur. La version bornée en temps K^t ne se préserve qu'avec le surcoût temporel de la simulation : K^{t′}_V ≤ K^t_U + c, avec t′ = surcoût(t). |
| Comptage, entropie | Presque toutes les fonctions booléennes à n variables exigent des circuits de taille ≈ 2ⁿ/n (Shannon 1949 ; Lupanov, à vérifier) | Argument informationnel valable dans tout modèle à facteur constant près : il se transporte, mais il est non constructif. |
| Communication | Karchmer et Wigderson (1990) : la profondeur d'une formule pour f égale la complexité de communication de la relation KW_f ; application : la connectivité monotone exige une profondeur Ω(log²n) ([SIAM J. Discrete Math. 3(2), 1990, notes de cours](https://www.cs.princeton.edu/courses/archive/spring19/cos522/KW.pdf), vérifié) | C'est le prototype de **borne inférieure transportable** : une même quantité, la communication, borne la profondeur des formules. |
| Communication | Machines à un ruban : reconnaître les palindromes demande un temps Ω(n²), par l'argument des séquences de croisement (Hennie 1965, à vérifier) ; VLSI : borne AT² ≥ Ω(CC²) (Thompson 1979 ; Yao 1979, à vérifier) ; algorithmes de flux : l'espace est borné par la communication à un sens | La même borne de communication se transporte vers trois modèles. Chaque fois, la traduction coupe le calcul en deux parties qui échangent c symboles. |
| Taille de formule | Khrapchenko : n² pour la parité (1971, à vérifier) ; record n^{3−o(1)} (Håstad 1998 ; Tal 2014, à vérifier) ; conjecture KRW (Karchmer, Raz et Wigderson 1995, à vérifier) : OUVERT | Les bornes de communication *ne sont pas* connues pour dépasser n³ sur les formules. |
| Information mutuelle couche à couche | Inégalité de traitement des données : I(X ; L_{k+1}) ≤ I(X ; L_k) pour une chaîne X → L₁ → L₂ (CONNU) ; « goulot d'information » de Tishby et Zaslavsky (2015, à vérifier), critiqué par Saxe et al. (2018, à vérifier) | Pour un réseau déterministe à valeurs réelles, I(X ; L) est mal définie, voire infinie, sans discrétisation. Elle dépend donc du *codage* et n'est pas un invariant de traduction. |
| Barrières | Preuves naturelles : si des fonctions pseudo-aléatoires fortes existent, aucune propriété « naturelle » ne prouve de borne superpolynomiale contre P/poly (Razborov et Rudich 1997, K-14, à vérifier) | Une mesure informationnelle calculable à partir de la table de vérité et vérifiée par la plupart des fonctions est « naturelle ». Elle ne séparera pas P/poly si des fonctions pseudo-aléatoires fortes existent. |

### B.2 Résultat du programme : la borne de coupe informationnelle

**Lemme L-I1 (PROUVÉ, élémentaire ; antériorité folklorique probable).** Soit C un circuit q-aire et S un ensemble de nœuds qui sépare les entrées des sorties. Pour toute loi de X, on a H(f(X)) ≤ |S|·log₂q, donc c_min(C) ≥ H(f(X)) / log₂q.

*Preuve.* Les sorties sont fonction des valeurs de S, donc H(f(X)) ≤ H(S) ≤ |S| log₂ q. ∎

**Corollaire (transport).** Soit T une traduction par gadgets qui code chaque symbole sur b symboles q′-aires. Alors :
- c_min(T(C)) ≤ b·c_min(C) : l'image d'une coupe est une coupe, formée des sorties des gadgets ;
- c_min(T(C)) ≥ H(f) / log₂ q′.

La quantité H(f) est un **invariant de la fonction**, et elle minore la coupe dans **tous** les modèles de circuits.

**E-02b (`08_DATA/inv02_info.json`).** Entrées uniformes, calcul exhaustif, n ≤ 4.

| Fonction, n = 4 | H(f) en bits | c_min T | c_min B natif (m = 7) | c_min T→B | H / capacité : T, B, T→B |
|---|---|---|---|---|---|
| addition | 7,06 | 5 | 8 | 10 | 0,89, 0,97, 0,71 |
| multiplication | 9,73 | 8 | 14 | 16 | 0,77, 0,84, 0,61 |
| comparaison | 1,08 | 1 | 2 | 2 | 0,68, 0,53, 0,54 |
| x mod 3 | 1,585 | 1 | 2 | 2 | 1,00, 0,79, 0,79 |

L'inégalité est vérifiée dans les 36 cas mesurés. Sur ces 12 circuits, la traduction double rail donne **exactement** c_min(T→B) = 2·c_min(T) (EXPÉRIMENTAL ; l'inégalité ≤ est PROUVÉE). La borne transportée est atteinte à un facteur 1,1 à 2 près.

**Limites.** L-I1 est une borne faible : elle ne donne que des bornes linéaires sur la largeur d'une coupe, jamais de borne superpolynomiale en taille. Les arguments de comptage et de communication sont plus forts, et déjà connus.

### B.3 Hypothèses testables (au plus 2)

- **H-I1 (transport de coupe).** Pour toute traduction par gadgets T de facteur de codage b, on a c_min(T(C)) ∈ [H(f)/log₂q′, b·c_min(C)]. De plus, l'*efficacité de coupe* H(f)/(c_min log₂ q) est conservée à un facteur log₂q / (b log₂q′) près.
  - Statut : PROUVÉ pour les bornes ; EXPÉRIMENTAL, favorable, pour l'égalité c_min(T→B) = 2c_min(T) (12 cas sur 12).
  - Protocole : étendre E-02b aux traductions Tseitin (L-01) et seuil (L-03, L-T1), avec c_min mesuré par flot, à n ≤ 6 et sur 20 circuits aléatoires à fenêtre (graines 0 à 19).
  - Réfutation : une traduction par gadgets pour laquelle c_min(T(C)) < b·c_min(C) de façon systématique, ce qui signalerait une compression non triviale, ou une violation numérique, ce qui signalerait un bogue.
- **H-I2 (excès d'entropie des réseaux entraînés, lié à H-B3).** Dans les réseaux entraînés d'E-01b (fonction exacte, entrées uniformes, activations binarisées), l'entropie des couches cachées H(L_k) dépasse H(f) beaucoup plus que dans les réseaux compilés (L-03, L-T1). De plus, cet excès Σ_k (H(L_k) − H(f)) est corrélé positivement à la largeur mesurée.
  - Statut : CONJECTURE, non testée ici.
  - Protocole : reprendre les 15 réseaux d'E-01b et les réseaux compilés de parité, majorité et addition ; calcul exhaustif sur 2⁸ entrées ; corrélation de Spearman avec la borne inférieure de largeur ; graines 0 à 4.
  - Réfutation : un excès comparable entre réseaux entraînés et compilés, ou une corrélation inférieure ou égale à 0.

### B.4 OUVERT pour RTC

- Existe-t-il une mesure informationnelle *non naturelle*, attachée à la représentation plutôt qu'à la table de vérité, qui soit préservée par les traductions et qui minore la largeur ? C'est OUVERT, et c'est ce qui la ferait échapper à Razborov et Rudich.
- Le lien entre largeur et communication (un circuit de largeur w, pour une bipartition des entrées induite par une décomposition, donne un protocole à O(w log q) symboles par séparateur) est probablement CONNU, sous la forme « circuits de largeur bornée », Jansen et Sarma (vers 2008, à vérifier). Il faut faire un audit d'antériorité avant d'en faire un énoncé du programme.

---

## Piste C — La cryptographie comme fil conducteur

### C.1 Construction (`07_CODE/crypto/spn.py`, tests dans `test_spn.py`)

SPN jouet, construit pour l'expérience, **sans aucune prétention de sécurité** :
- bloc de 16 bits, 4 boîtes S de 4 bits, R tours, clé maître de k ∈ {16, 24} bits ;
- sous-clés : 16 bits de poids faible de rotl(K, 7r) ;
- permutation de bits i → 4i mod 15 ;
- boîte S de PRESENT (Bogdanov et al., CHES 2007, valeurs vérifiées : [iacr.org](https://www.iacr.org/archive/ches2007/47270450/47270450.pdf)). Ses propriétés mesurées sont une uniformité différentielle de 4 et une linéarité de 8.

Récupération de clé à clair connu : 2 couples (P, C) pour k = 16, 3 couples pour k = 24, ce qui suffit à déterminer la clé dans tous les essais observés. Deux traductions en CNF :
- **anf** : forme normale algébrique → portes ET et OU-exclusif → Tseitin ;
- **table** : 64 clauses de 5 littéraux par boîte S.

Le clair connu est replié à la construction : la première addition de clé devient ±K₀, sans variable. Correction vérifiée : la vraie clé satisfait la CNF, un chiffré faux est rejeté, et la clé trouvée chiffre correctement.

### C.2 Mesures (E-02c, `08_DATA/inv02_crypto.json`)

5 graines par ligne (3 pour k = 24, R = 5), Glucose 4, toutes les instances résolues. La largeur est un encadrement [MMD+, min(heuristiques, ordre explicite)].

| k | R | Largeur, anf | Conflits médians, anf | Largeur, table | Conflits médians, table |
|---|---|---|---|---|---|
| 16 | 1 | [7, 10] | 11 | [7, 8] | 15 |
| 16 | 2 | [10, 24] | 370 | [12, 16] | 342 |
| 16 | 3 | [13, 34] | 2 995 | [14, 27] | 2 926 |
| 16 | 4 | [14, 41] | 8 213 | [15, 31] | 15 792 |
| 16 | 5 | [15, 43] | 36 336 | [16, **35**] | 26 243 |
| 16 | 6 | [17, 49] | 41 434 (3,1 s) | [17, **35**] | 9 194 |
| 24 | 3 | [14, 39] | 6 132 | [15, 34] | 3 306 |
| 24 | 4 | [16, 50] | 43 461 | [18, **43**] | 52 658 |
| 24 | 5 | [18, 50] | 155 390 (9,5 s) | [18, **43**] | 301 449 (13,4 s) |

**Lemme L-C1 (largeur bornée indépendamment du nombre de tours ; PROUVÉ en esquisse, confirmé numériquement).** Pour la CNF de récupération de clé à R tours et N couples, on a tw ≤ k + c_enc, où c_enc dépend de la taille du bloc et de l'encodage de la boîte S, **mais pas de R ni de N**.

*Esquisse.* On élimine les variables non-clé dans l'ordre de création, puis les variables de clé. Quand on élimine v, ses voisins encore présents dans le graphe d'élimination sont :
- des variables de clé, au plus k ;
- des variables créées après v et adjacentes au préfixe déjà éliminé.

Ces dernières sont des portes qui consomment un « fil vivant » du préfixe. Leur nombre est borné par (fils vivants : au plus l'état de 16 bits plus les intermédiaires d'une boîte S) × (sortance maximale dans une boîte S), une quantité indépendante de R. Les couples ne communiquent que par la clé. ∎

Valeurs mesurées de cet ordre : **k + 19** pour l'encodage table (35 pour k = 16, 43 pour k = 24), constantes pour tout R ≥ 3. Pour l'encodage anf, l'ordre explicite donne 92 à 100, constant pour R ≥ 2.

### C.3 Hypothèse H-C1 : verdict

- **« La largeur croît avec les tours. »** Elle est **RÉFUTÉE dans sa forme forte** (croissance sans borne) : par L-C1, la largeur est ≤ k + c pour tout R, et la borne supérieure de l'encodage table est atteinte dès R = 3. Seule la forme faible tient : la borne *inférieure* croît lentement, de 7 à 17 ou 18 entre R = 1 et R = 6 (EXPÉRIMENTAL). Il s'agit d'une croissance transitoire, qui dure tant que la diffusion n'est pas complète.
- **« Le temps suit la largeur. »** Le résultat est **non concluant, avec confusion documentée**. La corrélation de Spearman entre largeur inférieure et conflits vaut 1,0 dans 3 groupes sur 4, mais la largeur inférieure et R ont *exactement les mêmes rangs* : la corrélation ne distingue pas les deux variables. Deux observations vont contre le lien :
  - pour l'encodage table et k = 16, la borne supérieure reste fixe à 35 de R = 5 à R = 6 alors que le coût varie (26 000 puis 9 200 conflits, avec seulement 5 graines) ;
  - pour k = 24, elle reste fixe à 43 de R = 4 à R = 5 alors que les conflits passent de 52 000 à 301 000.

  Le coût suit davantage (R, k) que la largeur.
- **Comparaison avec la force brute.** Pour k = 16 et R = 6, il faut environ 41 000 conflits pour 2¹⁶ = 65 536 clés. Pour k = 24 et R = 5, il en faut 155 000 à 300 000, contre 2²⁴ ≈ 1,7·10⁷ clés. Un conflit n'est pas une clé testée, donc ces deux nombres ne se comparent pas directement (EXPÉRIMENTAL).
- La borne théorique 2^{O(tw)}·poly, valable pour les algorithmes de largeur bornée (CONNU), donne ici environ 2^{O(k)}. Elle est compatible avec la force brute, mais trop lâche pour prédire le coût CDCL.

### C.4 Ce que cela apprend sur les traductions

1. Une traduction peut **préserver la largeur** (Tseitin : L-01 ; ici anf et table restent de même ordre) **sans préserver le coût de résolution**. Pour ces instances, la difficulté vient de l'algèbre (non-linéarité et diffusion répétées), pas de la structure du graphe. C'est un **contre-exemple de principe** à « largeur ⇒ difficulté » : la largeur est une borne supérieure de difficulté (CONNU), pas une mesure de difficulté.
2. L'encodage de la boîte S change la taille (4,4 fois moins de variables pour table) et la largeur (35 contre 92 à 100 pour l'ordre explicite), mais **pas l'ordre de grandeur du coût**. La difficulté est conservée par les deux traductions (EXPÉRIMENTAL).
3. **Liens connus**, dont le statut est indiqué :
   - L'existence de fonctions à sens unique implique P ≠ NP (CONNU : si P = NP, on inverse toute fonction calculable en temps polynomial). La réciproque est OUVERTE : on ne sait pas obtenir de fonction à sens unique de P ≠ NP, ni même de NP ⊄ BPP (les « cinq mondes » d'Impagliazzo, 1995, à vérifier).
   - Preuves naturelles : l'existence de fonctions pseudo-aléatoires fortes interdit les preuves naturelles de bornes contre P/poly (Razborov et Rudich 1997, K-14, CONNU, à vérifier). Pour RTC, *toute* mesure de difficulté facile à calculer à partir de la fonction et vérifiée par une fonction aléatoire ne séparera pas P de NP. Les invariants de représentation comme la largeur ne sont pas concernés directement, car ce ne sont pas des propriétés de la fonction. Mais min_C tw(C), calculé sur les circuits C qui calculent f, l'est potentiellement (CONJECTURE à examiner).
   - Cryptanalyse par SAT : « cryptanalyse logique » de DES (Massacci et Marraro, vers 2000, à vérifier) ; CryptoMiniSat et ses clauses OU-exclusif (Soos et al., 2009, à vérifier). Les formules de Tseitin sur des expandeurs sont difficiles pour la résolution (Urquhart 1987, à vérifier), et la difficulté pour la résolution est liée à la largeur de résolution (Ben-Sasson et Wigderson 2001, à vérifier).
4. **Limites.** Il s'agit d'un seul chiffrement jouet sur un bloc de 16 bits, avec R ≤ 6, k ≤ 24, 3 à 5 graines par point et un seul solveur. Les largeurs ne sont qu'encadrées. L'ordre explicite de L-C1 n'est pas optimal.

---

## Verdict

| Piste | Statut global | Mérite un tome ? |
|---|---|---|
| **A. Ternaire équilibré** | Résultats propres mais attendus. Pas de changement de classe (PROUVÉ). Gains constants qui dépendent du modèle de coût (EXPÉRIMENTAL). Négation gratuite (en réalité une propriété du double rail). Poids ternaires suffisants à facteur constant (L-T1). | **Non : impasse comme thème autonome.** Les acquis, à savoir L-T1, L-T2, les gadgets minimaux et la « précondition de codage », vont dans un chapitre « changement d'alphabet et codages » du tome sur les circuits, et dans le tome sur les réseaux pour les poids ternaires. |
| **B. Information** | La complexité de communication est la seule source CONNUE de bornes inférieures qui se transportent vraiment d'un modèle à l'autre. L-I1 est PROUVÉ mais faible. H-I1 est favorable, H-I2 est à tester. | **Oui**, un tome « Information, communication, coupes » qui organise le CONNU dans le cadre D2. Il faut un audit d'antériorité serré, car le risque de redécouverte est élevé. |
| **C. Crypto** | H-C1 est réfutée dans sa forme forte : largeur bornée (L-C1) et coût croissant. On obtient un contre-exemple instructif à « largeur ⇒ difficulté ». | **Un chapitre**, pas un tome : « Traductions qui préservent la structure sans préserver la difficulté », couplé à H-B4. Le plus utile est d'en faire la **famille d'instances difficiles à largeur contrôlée** qui manquait à INV-01 (F-005). |

**Suite proposée (INV-02b).**
- Tester H-I2 sur les réseaux d'E-01b.
- Étendre E-02c : 10 graines ; CaDiCaL en plus de Glucose ; clauses OU-exclusif natives (CryptoMiniSat, présent dans PySAT sous le nom `cryptosat`) ; variante à sous-clés indépendantes, pour séparer l'effet de k de celui de R ; et largeur exacte sur R ≤ 2.
