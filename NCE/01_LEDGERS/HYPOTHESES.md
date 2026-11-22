# Registre des hypothèses

| ID | Énoncé | Origine | Ce qui la réfuterait | Statut |
|---|---|---|---|---|
| HA | Il existe des correspondances systématiques entre les structures des programmes, des formules, des systèmes de transitions et des réseaux | Intuition I1 | — (trop large : décomposée) | OUVERT, à décomposer |
| HB | Certaines propriétés structurelles ou de ressources sont préservées par les traductions | I2 | — (décomposée en H-B1 à H-B4) | OUVERT |
| HC | Changer de formalisme peut rendre un problème plus facile à résoudre, vérifier ou compresser | I3 | Aucune classe d'instances où l'avantage est mesuré face à une référence forte | OUVERT. *Ne peut pas valoir dans le pire cas pour les problèmes NP-difficiles, sauf si P = NP* |
| HD | Une architecture unifiée exécution + représentation + mémoire + contraintes est motivée | I4 | Composants redondants ou non justifiés par des résultats | OUVERT, porte G4 |
| HE | Il existe des lois quantitatives entre la complexité d'un problème et son coût de représentation | I5 | Contre-exemples ; conflit avec les barrières connues | OUVERT, risque élevé |
| **H-B1** | Pour un calcul de MT en temps t et espace s, le tableau CNF de Cook-Levin a une largeur de chemin O(s·c), où c dépend de la machine et pas de t | INV-01 | Une famille de machines dont la largeur croît avec t à s fixé | CONJECTURE (probablement folklorique : audit d'antériorité requis) |
| **H-B2** | L'encodage de Tseitin d'un circuit C produit une CNF dont le graphe primal a une largeur arborescente ≤ a·tw(C) + b, avec a et b constants | INV-01 | Une famille de circuits où le rapport n'est pas borné | CONJECTURE (énoncés proches connus, source à identifier) |
| **H-B3** | La compilation porte par porte d'un circuit en réseau à seuil préserve la largeur arborescente du graphe sous-jacent, mais un réseau *entraîné* calculant la même fonction ne la préserve pas en général | INV-01 | Une compilation qui fait croître la largeur ; ou des réseaux entraînés qui retrouvent systématiquement une faible largeur | Première partie CONJECTURE (probablement facile) ; seconde partie OUVERT |
| **H-B4** | Le coût de résolution d'un solveur CDCL sur les CNF issues de traductions est mieux prédit par la largeur que par la taille seule | INV-01 | Aucun pouvoir prédictif supplémentaire une fois la taille contrôlée | OUVERT, expérience E-01 |
| **H-P1** | Les bits de précision des poids, la profondeur et la taille obéissent à un compromis pour la représentation exacte de fonctions booléennes | INV-02 (futur) | — | OUVERT |
| **H-S1** | Le partage en λ (graphes de partage), la réutilisation de sous-circuits et le partage de poids sont des instances d'une même notion formelle préservée par traduction | INV-03 (futur) | Une traduction standard qui détruit le partage sans contrepartie | OUVERT |
