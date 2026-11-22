# RTC (ex-NCE) — Index maître

Nom provisoire : **RTC — Resource Translations of Computation** (renommage décidé à la porte G0 ; voir FAILURES.md, F-006).

État du programme : **G0 validée. M1 (INV-00) fait en v0.1. INV-01 et INV-01b faits. T0 à T9b rédigés (Dialagram), relus par audit automatique (références, statuts, exagérations) et publiés. Prochaine étape : T10 (invariants), audit de la littérature, INV-01c.**

- [Définitions INV-00](DEFINITIONS.md) · [Rapport INV-01](INV-01_RAPPORT.md)

| Tome | Titre (architecture révisée) | Phase | Dépend de | Statut | Prochaine action |
|---|---|---|---|---|---|
| T0 | Programme NCE et cadre formel des traductions à ressources | I | — | publié v1 (228 p.) | relecture humaine |
| T1 | Lambda-calcul : structure fonctionnelle, réduction, partage, coût | I | T0 | publié v1 (240 p.) | relecture humaine |
| T2 | Machines de Turing : états, mémoire, simulations | I | T0 | publié v1 (232 p.) | relecture humaine |
| T3 | Circuits booléens, contraintes et SAT | I | T0 | publié v1 (247 p.), inclut L-01 | relecture humaine |
| T4 | Réseaux neuronaux : seuil, ReLU, récurrents, transformers ; ressources | I | T0 | publié v1 (229 p.), inclut L-03 et E-01b | relecture humaine |
| T5 | λ ↔ MT | II | T1, T2 | publié v1 | relecture humaine |
| T6 | MT ↔ circuits ↔ SAT | II | T2, T3 | publié v1, inclut INV-01 | relecture humaine |
| T7 | Circuits/SAT ↔ réseaux | II | T3, T4 | publié v1, inclut INV-01 | relecture humaine |
| T8 | λ ↔ réseaux | II | T1, T4 | publié v1 | relecture humaine |
| T9 | MT ↔ réseaux | II | T2, T4 | publié v1 | relecture humaine |
| T9b | λ ↔ SAT/preuves (Curry-Howard, complexité des preuves) | II | T1, T3 | publié v1 | relecture humaine |
| T10 | Invariants computationnels | III | T5 à T9b | non commencé | — |
| T11 | Théorie NCE | III | T10, porte G3 | conditionnel | — |
| T12 | NCSM | IV | T10, porte G4 | conditionnel | — |
| T13 | Transformations de problèmes (banc d'essai dès la phase I) | IV | banc d'essai, T12 | banc d'essai à créer | M3 |
| Final | NCE — The Architecture of Computation | — | porte G5 | conditionnel | — |

Investigations ouvertes : **INV-00** (définitions) et **INV-01** (largeur structurelle). Les deux attendent G0.

Documents : [Audit](SCIENTIFIC_ASSESSMENT.md) · [Feuille de route](RESEARCH_ROADMAP.md) · [Protocole](RESEARCH_PROTOCOL.md) · [Carte des relations](RELATIONSHIP_MAP.md)

Publication : collection complète (T0 à T9b) sur https://claude.ai/artifact/5t49NGjXxFbNC6kZ9Z3cxy ; T0 à T4 aussi dans la bibliothèque générale.
