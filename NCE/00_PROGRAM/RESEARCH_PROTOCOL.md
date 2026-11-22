# NCE — Protocole de recherche

## Cycle d'une investigation

1. **Question.** Objectif mathématique ou expérimental précis, avec ses critères de succès et d'échec.
2. **Bibliographie.** Sources primaires vérifiées ; on dit ce qui est déjà connu.
3. **Formalisation.** Objets, espaces, traductions, métriques, hypothèses.
4. **Hypothèses réfutables.** Pour chacune, on dit ce qui la réfuterait.
5. **Mathématiques.** Lemmes, preuves, bornes inférieures et supérieures, contre-exemples. Aucune lacune n'est cachée.
6. **Critique hostile (ATTACK).** Hypothèses cachées, trivialité, antériorité, métriques trompeuses, précision non bornée, mémoire non comptée, coût d'encodage, comparaisons injustes.
7. **Expérience.** Code exécutable, graines, données, environnement, référence de comparaison forte.
8. **Reproduction.** Seconde exécution indépendante.
9. **Arbitrage.** Chaque résultat reçoit un statut.
10. **Synthèse.** Ce que le résultat permet ensuite ; mise à jour de la carte des relations.
11. **Rédaction.** Seulement quand l'investigation est mûre.

## Statuts

| Statut | Sens |
|---|---|
| **PROUVÉ** | Preuve complète sous des hypothèses explicites |
| **CONNU** | Résultat de la littérature vérifié sur source primaire |
| **CONNU (à vérifier)** | Résultat de la littérature cité de mémoire, pas encore vérifié. Ne peut servir de base à une preuve. |
| **EXPÉRIMENTAL** | Observé et reproduit, sans portée universelle |
| **CONJECTURE** | Plausible, sans preuve complète |
| **RÉFUTÉ** | Contredit par un contre-exemple ou une preuve |
| **OUVERT** | Non résolu |

Un statut ne monte **jamais** parce qu'un résultat est souvent répété.

## Règles absolues

- Ne jamais inventer une publication, un DOI, un auteur ou un théorème.
- Ne pas confondre équivalence de calculabilité, équivalence fonctionnelle, équivalence de représentation et équivalence d'efficacité.
- Aucun gain de complexité sans preuve ou mesure. Les mesures sont comparées à des références fortes, par exemple un solveur CDCL moderne, jamais à une référence affaiblie.
- Ne mesurer les ressources jamais au seul nombre de neurones. On mesure aussi : connexions, paramètres, bits de précision, mémoire, profondeur, largeur, transitions, taille d'encodage, erreur, stabilité.
- Conserver les résultats négatifs dans FAILURES.md.
- Aucune revendication de nouveauté sans audit d'antériorité. Un résultat retrouvé est utile, mais il est étiqueté comme tel.
- Toute affirmation de « loi générale » de complexité est confrontée aux barrières de relativisation, de preuves naturelles et d'algébrisation.

## Structure standard d'un tome

Les 15 sections : problématique, état de l'art, définitions, hypothèses, relations connues, nouvelles propositions, preuves, contre-exemples, complexité, expériences reproductibles, comparaison aux références, analyse des échecs, résultats (théorèmes, observations et conjectures séparés), questions ouvertes, transfert vers NCE.
