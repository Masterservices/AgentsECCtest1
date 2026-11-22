# Registre des théorèmes

## Résultats du programme

| ID | Énoncé | Preuve | Statut |
|---|---|---|---|
| L-01 | Tseitin, degré d'entrée ≤ k : tw(primal) ≤ (k+1)(tw(C)+1) − 1 | INV-01_RAPPORT.md §2 | PROUVÉ (antériorité probable, non établie) |
| L-02 | Tableau `tm_tableau(s,t)` : largeur de chemin ≤ 4s+1, indépendante de t | INV-01_RAPPORT.md §2, vérifié numériquement | PROUVÉ (cas particulier d'un résultat CONNU) |
| L-03 | Compilation à seuil porte par porte : poids \|w\| ≤ 2, largeur ≤ (k+2)(tw(C)+1) − 1 | INV-01_RAPPORT.md §2 | PROUVÉ (élémentaire) |
| L-T1 | Circuit {ET, OU, OU-exclusif} de degré 2 → réseau à seuil à poids {−1,0,1} : 3 neurones par OU-exclusif, largeur ≤ (k+3)(w+1)−1 ; un seul neurone caché ternaire ne suffit pas pour le OU-exclusif | INV-02_RAPPORT.md §A.7, `test_ternaire.py` (vérification exhaustive) | PROUVÉ (élémentaire) |
| L-T2 | Traduction ternaire → binaire par gadgets de taille ≤ s : largeur ≤ (s+2k)(w+1)−1 ; gadgets minimaux certifiés par SAT (double rail : NEG = 0, SUM = 6, MUL = 6, …) | INV-02_RAPPORT.md §A.4 | PROUVÉ (variante de L-01) |
| L-I1 | Toute coupe S séparant entrées et sorties d'un circuit q-aire vérifie \|S\| log₂q ≥ H(f(X)) ; transport par gadgets : c_min(T(C)) ≤ b·c_min(C) | INV-02_RAPPORT.md §B.2 | PROUVÉ (élémentaire, antériorité folklorique probable) |
| L-C1 | CNF de récupération de clé du SPN jouet : tw ≤ k + c_enc, indépendamment du nombre de tours et du nombre de couples | INV-02_RAPPORT.md §C.2 (esquisse) ; mesuré k + 19 pour l'encodage table | PROUVÉ (esquisse) |

## Littérature

Les premiers résultats démontrés du programme figurent dans le tableau ci-dessus. Ce registre ne contient pour l'instant que des résultats de la littérature, **tous à vérifier sur source primaire (audit L-01)** avant de servir de base à une preuve.

| ID | Énoncé (résumé) | Source | Statut |
|---|---|---|---|
| K-01 | Les fonctions λ-définissables sont exactement les fonctions calculables par machine de Turing | Turing 1937 ; Kleene 1936 | CONNU (à vérifier) |
| K-02 | SAT est NP-complet | Cook 1971 ; Levin 1973 | CONNU (à vérifier) |
| K-03 | Tout circuit se transforme en CNF équisatisfaisable de taille linéaire (variables auxiliaires) | Tseitin 1968 | CONNU (à vérifier) |
| K-04 | Une MT en temps t se simule par des circuits de taille O(t log t) | Pippenger et Fischer 1979 | CONNU (à vérifier) |
| K-05 | Un réseau récurrent à poids rationnels simule une MT universelle | Siegelmann et Sontag 1995 | CONNU (à vérifier) |
| K-06 | Avec des poids réels, un réseau récurrent calcule en temps polynomial la classe P/poly | Siegelmann et Sontag 1994 | CONNU (à vérifier) |
| K-07 | La réduction gauche-externe du λ-calcul est un modèle de coût invariant (polynomialement lié aux MT) | Accattoli et Dal Lago 2016 | CONNU (à vérifier) |
| K-08 | Certaines portes à seuil exigent des poids de taille exponentielle en n | Håstad 1994 | CONNU (à vérifier) |
| K-09 | La parité n'est pas dans AC⁰ | Furst, Saxe et Sipser 1984 ; Håstad 1986 | CONNU (à vérifier) |
| K-10 | Il existe des fonctions calculables par des réseaux ReLU profonds qui exigent une taille exponentielle à faible profondeur | Telgarsky 2016 | CONNU (à vérifier) |
| K-11 | La vérification de propriétés de réseaux ReLU est NP-complète | Katz et al. 2017 | CONNU (à vérifier) |
| K-12 | CDCL, avec redémarrages, p-simule la résolution | Pipatsrisawat et Darwiche 2011 | CONNU (à vérifier) |
| K-13 | Les transformers à précision logarithmique sont dans TC⁰ uniforme | Merrill et Sabharwal 2023 | CONNU (à vérifier) |
| K-14 | Barrières : relativisation, preuves naturelles, algébrisation | Baker, Gill et Solovay 1975 ; Razborov et Rudich 1997 ; Aaronson et Wigderson 2009 | CONNU (à vérifier) |
