# Registre des expériences

| ID | Question | Hypothèse | Instances | Méthode | Référence de comparaison | Métriques | Statut |
|---|---|---|---|---|---|---|---|
| E-01 | La largeur survit-elle aux traductions, et prédit-elle le coût de résolution ? | H-B1, H-B2, H-B3, H-B4 | Calculs bornés générés : MT simples, additionneurs, multiplicateurs, parité, circuits aléatoires de largeur contrôlée ; graines fixées | Encodage MT → circuit → CNF (Tseitin) → réseau à seuil ; largeur arborescente exacte (petites instances) et bornes heuristiques (degré minimum, remplissage minimum) | Solveur CDCL moderne (via PySAT) ; régression contrôlée par la taille | Taille, largeur, profondeur, bits de poids, temps de résolution, conflits, décisions | **planifiée** (après G0 et M3) |

Exigences pour chaque expérience : question, hypothèse, données, algorithme, référence, métriques, environnement, code, instructions de reproduction, résultats, limites, analyse des échecs.
