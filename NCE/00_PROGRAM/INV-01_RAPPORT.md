# INV-01 — La largeur structurelle survit-elle aux traductions ? (rapport v1)

**Question.** La largeur arborescente du graphe sous-jacent est-elle préservée le long de la chaîne MT → CNF, circuit → CNF et circuit → réseau à seuil ? Prédit-elle le coût de résolution CDCL ?

## 1. Antériorité (audit ciblé du 2026-11-22)

- **H-B1 est connu.** Monien et Sudborough ont observé que la réduction de Cook, appliquée à des machines d'espace borné, donne des formules de largeur bornée. Cette observation est rapportée dans des travaux récents ; la source originale reste à identifier. Des énoncés précis, de la forme largeur de chemin O(s + h), figurent dans arXiv:1509.05896 et arXiv:1509.01014. **Ce n'est pas une contribution du programme.**
- **H-B2.** Aucun énoncé publié identique n'a été trouvé dans cette recherche. Le résultat probablement folklorique est celui-ci : un encodage porte par porte reste proche du graphe du circuit, et la borne dépend du degré d'entrée. Sur les encodages à variables auxiliaires, la référence proche est arXiv:1905.05290. Le lemme L-01 ci-dessous est donc marqué *PROUVÉ, antériorité non établie*.

## 2. Résultats mathématiques

**Lemme L-01 (Tseitin préserve la largeur).** Soit C un circuit de degré d'entrée ≤ k, et w la largeur arborescente du graphe non orienté G sous-jacent à C. Alors le graphe primal de la CNF de Tseitin de C a une largeur arborescente ≤ (k+1)(w+1) − 1.

*Preuve.* Soit (T, {B_i}) une décomposition arborescente de G de largeur w. On pose B'_i = ⋃_{x∈B_i} ({x} ∪ entrées(x)).

- **Couverture.** Les clauses de Tseitin d'une porte g portent exactement sur les variables {g} ∪ entrées(g). Toute arête du graphe primal relie donc deux sommets de {g} ∪ entrées(g) pour une certaine porte g. Un sac contenant g existe, et son extension contient tout cet ensemble.
- **Connexité.** Un sommet x apparaît dans B'_i si x ∈ B_i, ou si B_i contient une porte y dont x est une entrée. Chaque tel y est adjacent à x dans G, donc les sous-arbres de x et de y se rencontrent. Leur réunion est connexe.
- **Taille.** On a |B'_i| ≤ (k+1)|B_i| ≤ (k+1)(w+1). ∎

**Lemme L-02 (tableau de Cook-Levin, notre encodage).** Pour la machine à allers-retours de `tm_tableau(s, t)`, le graphe primal a une largeur de chemin ≤ 4s + 1, indépendante de t.

*Preuve.* Toute clause ne porte que sur des variables des pas t et t+1. Les sacs « pas t ∪ pas t+1 », placés le long d'un chemin, forment donc une décomposition en chemin. Chaque pas compte 2s + 1 variables (s bits, s positions de tête, 1 état), donc la largeur vaut 2(2s+1) − 1 = 4s + 1. ∎ Cette borne est vérifiée numériquement pour s = 4 à 10 et t = 10 à 80 : largeurs 17, 25, 33, 41, constantes en t.

**Lemme L-03 (compilation à seuil).** La compilation porte par porte en neurones à seuil a des poids entiers |w| ≤ 2. Elle ajoute un neurone auxiliaire par XOR, adjacent à a, b et z. Elle préserve la largeur à facteur (k+2) : il suffit d'ajouter le neurone auxiliaire de x à B'_i, comme dans L-01. ∎

## 3. Expérience E-01 (code : `07_CODE/benchmarks/e01.py`, données : `08_DATA/`)

| Partie | Observation | Statut |
|---|---|---|
| A. Tableau | L'heuristique de largeur annonce une croissance avec t (jusqu'à 255 pour s=10), alors que la décomposition explicite donne 41. **L'heuristique surestime jusqu'à six fois.** | Échec de méthode : F-004 |
| B. Circuit → Tseitin → seuil | Sur 10 circuits (additionneurs, multiplieurs, circuits aléatoires à fenêtre), les trois largeurs (bornes supérieures) restent très proches. Aucun dépassement de la borne L-01. | EXPÉRIMENTAL, cohérent avec L-01 et L-03 |
| C. Coût CDCL à taille fixée | Corrélation de Spearman de 0,82 entre largeur et conflits (n = 48). Mais les instances sont **trop faciles** : 0 à 58 conflits, et la courbe n'est pas monotone (58, puis 42, puis 20 pour les plus grandes fenêtres). | **Non concluant** : F-005 |
| D. Factorisation | La largeur et les conflits croissent ensemble avec n, mais la taille aussi : rien n'est contrôlé. | Non concluant pour H-B4 |

## 4. Décision et suite

- H-B1 : CONNU ; prouvé ici pour notre encodage (L-02).
- H-B2 : PROUVÉ pour un degré d'entrée borné (L-01), antériorité probable mais non établie.
- H-B3, première partie : PROUVÉ (L-03). Seconde partie, sur les réseaux *entraînés* : OUVERT. C'est l'angle le plus susceptible d'être nouveau.
- H-B4 : OUVERT. Il faut des instances difficiles à taille fixée et une mesure de largeur fiable : décompositions explicites, ou solveur exact de largeur sur les petites instances.

**Prochaine itération (INV-01b).**
1. Remplacer les heuristiques par des largeurs exactes ou des décompositions explicites.
2. Construire des familles difficiles à taille fixée, par exemple des miters d'équivalence ou des inversions de fonctions à fenêtre contrôlée.
3. Tester la seconde partie de H-B3 : entraîner de petits réseaux sur des fonctions de faible largeur, élaguer, puis mesurer la largeur du graphe obtenu.
