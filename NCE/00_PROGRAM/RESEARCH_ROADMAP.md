# NCE — Feuille de route

Principe : on ne passe jamais à un jalon tant que les critères de validation du précédent ne sont pas remplis. Chaque porte de décision (G) demande l'approbation humaine.

| Jalon | Contenu | Livrables | Dépend de | Critère de validation |
|---|---|---|---|---|
| **M0** | Initialisation | Audit, registres, carte des relations | — | Fait (v0.1) |
| **G0** | *Décision humaine* | Approbation de l'architecture révisée et de la première investigation | M0 | — |
| **M1** | INV-00 : traductions à ressources | `00_PROGRAM/DEFINITIONS.md` : traduction (f,g)-bornée, relations ≡_lin, ≡_poly, ≡_param ; cinq traductions standard réexprimées | G0 | Les résultats connus (Cook-Levin, Tseitin, Pippenger-Fischer, Siegelmann-Sontag) s'énoncent sans perte dans le cadre |
| **M2** | Audit bibliographique L-01 | LITERATURE.md vérifié sur sources primaires | G0 (en parallèle de M1) | Plus aucune entrée « à vérifier » parmi celles citées en M1 |
| **M3** | Banc d'essai v0 | `07_CODE/benchmarks/` : générateurs, encodeurs, mesure de largeur, solveur, graines | M1 | Reproduction des mesures à l'identique sur deux exécutions |
| **M4** | INV-01, partie théorique | Énoncés et preuves de H-B1 à H-B3 ; statuts dans THEOREMS.md | M1, M2 | Chaque énoncé est PROUVÉ, CONNU ou RÉFUTÉ, avec sa preuve ou sa source |
| **M5** | INV-01, partie expérimentale | Expérience E-01 : résultats, échecs, comparaison à un solveur CDCL de référence | M3, M4 | Expérience reproduite ; analyse des échecs consignée dans FAILURES.md |
| **M6** | ATTACK de INV-01 | Rapport du reviewer hostile | M4, M5 | Toutes les objections ont reçu une réponse ou ont rétrogradé un statut |
| **G1** | *Décision humaine* | INV-01 suffit-il à rédiger le T0 et les chapitres structurels des T3 et T6 ? | M6 | — |
| **M7** | INV-02 (précision comme ressource) ou INV-03 (partage), selon G1 | Même cycle de M4 à M6 | G1 | idem |
| **M8** | Rédaction des tomes de fondation (T0 à T4) à partir des résultats validés | Manuscrits, annexes, code | Investigations correspondantes | Chaque affirmation du texte renvoie à une entrée de registre |
| **G2** | Fin de la phase II (paires) | — | T5 à T9b | Carte des relations complète, avec surcoûts mesurés |
| **G3** | Le T10 établit-il des invariants non triviaux ? | Décide de l'écriture du T11 | T10 | Au moins un invariant PROUVÉ et non trivial, sinon on documente l'échec |
| **G4** | Une architecture est-elle motivée par les résultats ? | Décide du T12 | T10 (et T11) | Chaque composant de l'architecture est justifié par un résultat du registre |
| **G5** | Un avantage mesurable existe-t-il ? | Décide de l'ouvrage final | T13 | Avantage reproduit face à des références de comparaison fortes, sur des classes d'instances définies |

**Commandes de pilotage** : INITIALIZE, INVESTIGATE [ID], PROVE, ATTACK, REPLICATE, LITERATURE AUDIT, SYNTHESIZE, WRITE BOOK [ID], NEXT BEST ACTION, STATUS.
