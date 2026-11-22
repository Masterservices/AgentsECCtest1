# Registre des expériences

| ID | Question | Hypothèse | Instances | Méthode | Référence de comparaison | Métriques | Statut |
|---|---|---|---|---|---|---|---|
| E-01 | La largeur survit-elle aux traductions, et prédit-elle le coût de résolution ? | H-B1, H-B2, H-B3, H-B4 | Calculs bornés générés : MT simples, additionneurs, multiplicateurs, parité, circuits aléatoires de largeur contrôlée ; graines fixées | Encodage MT → circuit → CNF (Tseitin) → réseau à seuil ; largeur arborescente exacte (petites instances) et bornes heuristiques (degré minimum, remplissage minimum) | Solveur CDCL moderne (via PySAT) ; régression contrôlée par la taille | Taille, largeur, profondeur, bits de poids, temps de résolution, conflits, décisions | **v1 exécutée le 2026-11-22**. Résultats dans `08_DATA/e01_summary.txt`. B : cohérent avec L-01 et L-03. A et C : non concluants (F-004, F-005). Environnement : Python 3.13, networkx 3.7, PySAT/Glucose 4, graines fixées. |
| E-01b | Mêmes questions, mesure fiable et instances difficiles ; réseaux entraînés (H-B3, seconde partie) | H-B3, H-B4 | Miters, inversions à fenêtre contrôlée ; petits réseaux entraînés puis élagués | Largeur exacte ou décompositions explicites | CDCL (Glucose, CaDiCaL) | idem | **planifiée** |

Exigences pour chaque expérience : question, hypothèse, données, algorithme, référence, métriques, environnement, code, instructions de reproduction, résultats, limites, analyse des échecs.
