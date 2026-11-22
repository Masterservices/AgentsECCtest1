# NCE — Index maître

État du programme : **M0 terminé, en attente de la porte G0.**

| Tome | Titre (architecture révisée) | Phase | Dépend de | Statut | Prochaine action |
|---|---|---|---|---|---|
| T0 | Programme NCE et cadre formel des traductions à ressources | I | — | non commencé | INV-00 |
| T1 | Lambda-calcul : structure fonctionnelle, réduction, partage, coût | I | T0 | non commencé | — |
| T2 | Machines de Turing : états, mémoire, simulations | I | T0 | non commencé | — |
| T3 | Circuits booléens, contraintes et SAT | I | T0 | non commencé | alimenté par INV-01 |
| T4 | Réseaux neuronaux : seuil, ReLU, récurrents, transformers ; ressources | I | T0 | non commencé | — |
| T5 | λ ↔ MT | II | T1, T2 | non commencé | — |
| T6 | MT ↔ circuits ↔ SAT | II | T2, T3 | non commencé | alimenté par INV-01 |
| T7 | Circuits/SAT ↔ réseaux | II | T3, T4 | non commencé | alimenté par INV-01 |
| T8 | λ ↔ réseaux | II | T1, T4 | non commencé | — |
| T9 | MT ↔ réseaux | II | T2, T4 | non commencé | — |
| T9b | λ ↔ SAT/preuves (Curry-Howard, complexité des preuves) | II | T1, T3 | **ajouté** | — |
| T10 | Invariants computationnels | III | T5 à T9b | non commencé | — |
| T11 | Théorie NCE | III | T10, porte G3 | conditionnel | — |
| T12 | NCSM | IV | T10, porte G4 | conditionnel | — |
| T13 | Transformations de problèmes (banc d'essai dès la phase I) | IV | banc d'essai, T12 | banc d'essai à créer | M3 |
| Final | NCE — The Architecture of Computation | — | porte G5 | conditionnel | — |

Investigations ouvertes : **INV-00** (définitions) et **INV-01** (largeur structurelle). Les deux attendent G0.

Documents : [Audit](SCIENTIFIC_ASSESSMENT.md) · [Feuille de route](RESEARCH_ROADMAP.md) · [Protocole](RESEARCH_PROTOCOL.md) · [Carte des relations](RELATIONSHIP_MAP.md)
