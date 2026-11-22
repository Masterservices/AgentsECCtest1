## Conclusion

### Ce que ce livre a fait : une thèse et seize chapitres

J'ai voulu écrire un livre qui tienne en une seule phrase : *une correspondance n'est pas une identité*. Cette phrase, je l'ai déclinée seize fois, sous seize angles, à travers quatre parties qui tracent un arc allant du lambda-calcul typé aux solveurs SAT, en passant par la déduction naturelle, la normalisation, l'encodage de Tseitin, la réduction de Cook et la borne de Haken. À chaque étape, la même question : quand on traduit un objet d'un modèle de calcul vers un autre, qu'est-ce qui passe, qu'est-ce qui se perd, et combien cela coûte-t-il ?

Le programme RTC — Ressources, Traductions, Calculs — fournit le cadre méthodologique. Toute traduction entre modèles est munie d'une fiche : son sens, sa définition, son coût sur sept ressources (taille, temps, mémoire, profondeur, largeur, précision, partage), les invariants qu'elle conserve, les propriétés qu'elle perd, et son statut. Ce registre des statuts — PROUVÉ, CONNU, EXPÉRIMENTAL, CONJECTURE, RÉFUTÉ, OUVERT — n'est pas une coquetterie éditoriale. Il est la discipline même du livre. Aucune intuition n'y est présentée comme une preuve ; aucun résultat connu n'est démontré intégralement sans que cela soit annoncé ; aucune conjecture n'est utilisée comme hypothèse dans un raisonnement. Le lecteur sait toujours, à chaque ligne, sur quel sol il marche.

La Partie I a posé le dictionnaire. Le lambda-calcul simplement typé (Chapitre 2), la déduction naturelle propositionnelle (Chapitre 3) et la correspondance de Curry-Howard (Chapitre 4) constituent les deux machines et le pont entre elles. J'ai insisté sur un point qui traverse tout le livre : la correspondance de Howard 1980 identifie les types aux formules et les termes aux preuves, mais cette identification est *syntaxique* ; elle ne dit rien, par elle-même, sur la taille des objets, sur la profondeur des réductions, sur la possibilité de partager des sous-calculs. Traduire un terme $\lambda$ en preuve, c'est conserver le sens ; ce n'est pas conserver la mesure.

La Partie II a introduit la dynamique. La normalisation, lue comme élimination des coupures (Chapitre 5), est elle-même une traduction : elle traduit un terme avec coupures en un terme sans coupures, et cette traduction a un coût qui peut être super-exponentiel en taille (Chapitre 6). Le partage — la différence entre un arbre de preuve et son DAG sous-jacent — modifie la taille mesurée d'un facteur polynomial, parfois exponentiel (Chapitre 7). L'encodage de Tseitin 1968 (Chapitre 8) illustre une traduction linéaire en taille qui paie en précision : l'équivalence logique est remplacée par l'équisatisfiabilité, et ce compromis est exactement le type de phénomène que le cadre RTC est conçu pour documenter.

La Partie III a affronté le coût. La réduction de Cook 1971 (Chapitre 9) est une traduction des calculs polynomialement bornés vers SAT ; elle est polynomiale en temps, mais elle ne conserve ni la structure ni la lisibilité de la preuve source. Le cadre de Cook et Reckhow 1979 (Chapitre 10) élève cette observation en théorie : les systèmes de preuve sont des modèles de calcul, et leurs simulations mutuelles sont des traductions mesurables. La résolution, telle qu'elle est implémentée dans les solveurs modernes (Chapitre 11, en s'appuyant sur Biere, Heule, van Maaren et Walsh 2009 et Pipatsrisawat et Darwiche 2011), produit des traces qui sont des preuves, mais dont la taille et la structure dépendent étroitement des heuristiques — la traduction du problème vers la preuve est ici non déterministe et heuristique. Enfin, la borne inférieure de Haken 1985 (Chapitre 12) sur le principe des tiroirs montre qu'il existe des formules dont toute preuve en résolution est exponentielle : la traduction vers le modèle de résolution est intrinsèquement coûteuse pour certaines familles d'instances.

La Partie IV a posé la question de la mesure. La taille d'un terme de preuve (Chapitre 14) n'est pas un nombre : c'est une famille de nombres selon qu'on compte en arbre ou en DAG, selon qu'on mesure le coût de vérification, de recherche ou de normalisation. L'atlas des traductions (Chapitre 15) rassemble toutes les fiches du livre en un tableau unique. Le Chapitre 13 replace le tout dans le paysage P, NP, coNP : la question de savoir si toute tautologie admet une preuve polynomiale est précisément la question de savoir si NP = coNP, et cette question reste OUVERTE.

### Les traductions traversées : rappel des fiches

Le livre a documenté six traductions principales, chacune avec sa fiche complète.

**Traduction 1 : Curry-Howard (termes $\lambda$ typés $\to$ preuves en déduction naturelle).** Sens : à chaque terme de type $A$ on associe une preuve de la formule $A$. Coût : taille conservée à un facteur constant près (PROUVÉ, Chapitre 4) ; profondeur de la réduction conservée ; partage non conservé si l'on passe en arbre ; précision conservée (bijection). Statut : CONNU (Howard 1980), vérifié sur les exemples du livre.

**Traduction 2 : Élimination des coupures (preuve avec coupures $\to$ preuve sans coupures).** Sens : normaliser un terme, c'est éliminer les détours. Coût : la taille peut croître de façon super-exponentielle (CONNU, Chapitre 6, d'après Girard, Lafont et Taylor 1989) ; la profondeur diminue ; la mémoire de normalisation peut être exponentielle en la profondeur ; le partage peut être détruit par la duplication. Statut : CONNU.

**Traduction 3 : Arbre $\to$ DAG (représentation).** Sens : factoriser les sous-termes identiques. Coût : la taille peut diminuer exponentiellement ; le temps de vérification peut augmenter (il faut vérifier la cohérence du partage) ; la profondeur est conservée. Statut : PROUVÉ (Chapitre 7).

**Traduction 4 : Tseitin 1968 (formule propositionnelle $\to$ CNF équisatisfiable).** Sens : introduire des variables auxiliaires pour linéariser une formule. Coût : taille linéaire en la taille de la formule source ; précision perdue (on passe de l'équivalence à l'équisatisfiabilité) ; partage partiellement conservé. Statut : CONNU (Tseitin 1968), construction détaillée et PROUVÉE dans le livre.

**Traduction 5 : Cook 1971 (calcul polynomial borné $\to$ instance SAT).** Sens : encoder l'acceptation d'une machine de Turing non déterministe en clauses. Coût : taille polynomiale ; temps polynomial ; structure de la preuve source perdue ; précision conservée (équivalence). Statut : CONNU (Cook 1971), idée de construction donnée.

**Traduction 6 : Résolution comme trace de solveur (instance SAT $\to$ preuve par résolution).** Sens : la trace d'exécution d'un solveur CDCL est une preuve par résolution. Coût : taille imprévisible, potentiellement exponentielle (Haken 1985) ; dépendance aux heuristiques ; partage variable selon l'apprentissage de clauses. Statut : CONNU (Pipatsrisawat et Darwiche 2011 ; Biere, Heule, van Maaren et Walsh 2009).

Chaque fiche illustre la thèse : la traduction conserve le sens mais redistribue les ressources. Aucune traduction ne conserve simultanément les sept ressources.

### Ce que la thèse change : relire les grands résultats

La thèse méthodologique du livre n'est pas nouvelle. Ce qui est proposé ici, c'est une *lecture unifiée* de résultats classiques à travers le prisme des traductions à ressources. Cette lecture change la façon dont on énonce les théorèmes.

La NP-complétude de SAT (Cook 1971) n'est plus seulement « SAT est difficile ». Elle devient : « la traduction des calculs bornés vers les clauses est polynomiale en taille et en temps, mais elle ne conserve ni la structure de la preuve, ni la lisibilité, ni la profondeur ; elle est universelle mais non structurelle. » Le statut est CONNU ; la reformulation est celle du livre.

La borne de Haken 1985 n'est plus seulement « le principe des tiroirs est difficile pour la résolution ». Elle devient : « il existe une famille de formules pour lesquelles toute traduction vers le modèle de résolution coûte exponentiellement en taille ; la borne porte sur le modèle cible, non sur le problème en soi. » Cette distinction est cruciale : elle signifie qu'un autre système de preuve (un autre modèle cible) pourrait admettre des traductions polynomiales pour ces mêmes formules. Le statut est CONNU.

L'encodage de Tseitin 1968 n'est plus seulement « on peut mettre en CNF sans exploser ». Il devient : « il existe une traduction linéaire en taille qui paie en précision : on perd l'équivalence et on obtient l'équisatisfiabilité ; ce compromis est documenté, mesuré, et c'est un choix de traduction, pas une fatalité. » Le statut est CONNU, la construction est PROUVÉE dans le livre.

Le cadre de Cook et Reckhow 1979 n'est plus seulement « les systèmes de preuve se simulent ». Il devient : « chaque simulation est une traduction avec un coût mesurable ; la question NP = coNP est la question de savoir s'il existe une traduction polynomiale universelle vers un système de preuve unique ; cette question est OUVERTE. »

### Ce qui reste ouvert : questions pour le programme RTC

Le livre se termine par le Chapitre 16, « Transfert vers le programme RTC », et cette conclusion prolonge ce transfert. Voici les questions que ce tome laisse ouvertes, formulées précisément.

**Question 1 (OUVERTE).** Existe-t-il une traduction de la déduction naturelle vers la résolution qui conserve le partage (représentation DAG) tout en restant polynomiale en taille ? La borne de Haken 1985 interdit une traduction polynomiale universelle, mais pour des familles restreintes de preuves (par exemple, les preuves de profondeur bornée), la question reste entière.

**Question 2 (OUVERTE).** Peut-on définir une mesure de la taille d'une preuve qui soit invariante par changement de représentation arbre/DAG à un facteur polynomial près, et qui soit en même temps un invariant de la traduction de Curry-Howard ? Le Chapitre 14 montre que ces exigences sont en tension ; la résolution de cette tension est un problème ouvert.

**Question 3 (OUVERTE).** Dans le cadre de Cook et Reckhow 1979, la simulation d'un système de preuve par un autre est polynomiale si et seulement si une certaine traduction est polynomiale en taille. Mais qu'en est-il des autres ressources ? Existe-t-il des simulations qui conservent la taille mais perdent la profondeur, ou inversement ? Le registre des sept ressources suggère une hiérarchie plus fine que la simple comparaison polynomiale ; cette hiérarchie reste à construire.

**Question 4 (OUVERTE).** L'apprentissage de clauses dans les solveurs CDCL (Pipatsrisawat et Darwiche 2011) peut être vu comme une forme de partage dynamique : le solveur mémorise des lemmes et les réutilise. Peut-on borner le gain en taille apporté par ce partage dynamique pour des familles d'instances naturelles, au-delà des bornes exponentielles de Haken 1985 qui s'appliquent à la résolution sans apprentissage ? Le statut est OUVERT.

**Question 5 (OUVERTE).** La traduction de Cook 1971 est polynomiale mais détruit la structure. Existe-t-il des traductions structurelles (conservant la profondeur ou la largeur) des calculs bornés vers SAT, même au prix d'une taille super-polynomiale ? Si oui, quel est le compromis optimal taille/structure ? Cette question rejoint celle du coût de la lisibilité d'une preuve.

Ces cinq questions sont des questions de traduction. Elles ne demandent pas de nouveaux théorèmes de logique ou de complexité ; elles demandent qu'on mesure, qu'on compare, qu'on fiche. C'est exactement le programme RTC.

### Un mot final au lecteur

Ce livre a été écrit pour un lecteur cultivé qui n'est pas nécessairement logicien ni informaticien théoricien, mais qui accepte de suivre une définition, un exemple, un exercice. J'ai essayé de ne jamais sacrifier la rigueur à la pédagogie, ni la pédagogie à la rigueur. Chaque affirmation porte un statut ; chaque traduction porte une fiche ; chaque grand théorème est soit démontré, soit annoncé comme connu avec son idée de preuve, et jamais l'un n'est déguisé en l'autre.

Si vous avez parcouru ces chapitres, vous avez maintenant un vocabulaire : modèle, traduction, ressource, invariant, perte, statut. Vous savez que la correspondance de Curry-Howard est une traduction magnifique mais non isométrique. Vous savez que normaliser peut coûter exponentiellement, que Tseitin échange la précision contre la taille, que Cook échange la structure contre l'universalité, que Haken borne un modèle et non un problème. Vous savez que la question « combien est grande cette preuve ? » n'a pas une réponse mais plusieurs, selon qu'on compte en arbre ou en DAG, en temps de vérification ou en temps de recherche, en taille brute ou en taille partagée.

Ce que j'espère, c'est que ce vocabulaire vous serve au-delà de ce livre. Chaque fois que vous rencontrerez une correspondance entre deux formalismes — en logique, en programmation, en mathématiques, ailleurs —, posez les sept questions : qu'est-ce qui est conservé en taille ? en temps ? en mémoire ? en profondeur ? en largeur ? en précision ? en partage ? Et demandez : à quel statut appartient cette affirmation ?

Une correspondance est un pont. Un pont a un coût de construction, une capacité de charge, des pertes de friction. Il relie deux rives sans les confondre. Ce livre est une invitation à regarder les ponts pour ce qu'ils sont : des traductions, magnifiques et coûteuses, entre des mondes qui se parlent sans jamais se confondre.

La collection « Les Traductions du Calcul » continue. D'autres tomes viendront, d'autres modèles, d'autres fiches. Le registre des statuts restera le même. La discipline restera la même. Ce qui change, d'un tome à l'autre, c'est la paire de rives qu'on relie et les ressources qu'on mesure en traversant.

Je vous remercie d'avoir traversé celle-ci.

---

*Oussama Ghorbel*
*« Du Lambda-calcul aux Preuves et à SAT »*
*Collection « Les Traductions du Calcul », programme RTC*