## Conclusion — Ce que chaque traduction nous coûte, ce que chaque traduction nous donne

### Le chemin parcouru : du noyau aux atlas

Ce livre est parti d'une conviction simple : le lambda-calcul n'est pas un langage parmi d'autres, mais la structure minimale du calcul fonctionnel. Quatre ingrédients suffisent — des arbres syntaxiques, une équivalence de nommage ($\alpha$-conversion), une seule règle de calcul ($\beta$-réduction), et la substitution qui en concentre tout le coût. À partir de ce noyau, nous avons construit, chapitre après chapitre, une anatomie complète du calcul pur, en suivant une progression que je voulais aussi honnête que possible : d'abord comprendre ce qu'est un terme et ce que signifie « réduire », ensuite mesurer ce que coûte réellement cette réduction, puis explorer les traductions qui déplacent ce coût sans l'annuler, et enfin cartographier l'ensemble de ces déplacements.

La Partie I a posé les fondations. Nous avons défini les termes comme des arbres (Chapitre 2), établi que l'$\alpha$-équivalence n'est pas un détail technique mais la condition même pour que la portée d'une variable ait un sens, et affronté la substitution de face (Chapitre 3) : sa définition récursive, ses captures évitées par le renommage, son coût linéaire en la taille du terme substitué mais potentiellement quadratique en présence de duplications. Le Chapitre 4 a couronné cette partie avec le théorème de Church et Rosser (1936) : la confluence, c'est-à-dire la garantie que si un terme $t$ se réduit en $u$ et en $v$, il existe un terme $w$ atteignable depuis $u$ et depuis $v$. Ce résultat (CONNU, démontré par Church et Rosser 1936) est la colonne vertébrale de tout ce qui suit : sans lui, la notion même de « forme normale » serait ambiguë.

La Partie II a déployé le calcul sans types. Nous avons vu que le choix d'une stratégie d'évaluation — normale, applicative, paresseuse, leftmost-outermost — n'est pas un détail d'implémentation mais une décision qui engage la terminaison elle-même (Chapitre 5). Le Chapitre 6 a confronté le lecteur à la divergence : le terme $\Omega = (\lambda x.\, x\, x)(\lambda x.\, x\, x)$ n'a pas de forme normale, et cette absence n'est pas un bug mais une propriété structurelle indécidable. Les encodages de Church (Chapitre 7) ont montré que les entiers, les booléens, les paires et les listes vivent dans le même univers que les fonctions : $\bar{n} = \lambda f.\,\lambda x.\, f^n(x)$ n'est pas une métaphore mais une définition. Enfin, le Chapitre 8 a introduit les combinateurs $S$, $K$ et le point fixe $Y$, établissant que la récursion n'a pas besoin d'être un axiome ajouté de l'extérieur : elle émerge de l'autoréférence permise par la $\beta$-réduction.

La Partie III a opéré trois traductions majeures. Le lambda-calcul simplement typé (Chapitre 9) restreint les termes pour interdire l'autoréférence ; la normalisation forte (Chapitre 10) en est la récompense : tout terme bien typé termine (CONNU, preuve par réductibilité logique, idée exposée au chapitre). Curry-Howard (Chapitre 11) révèle que réduire un terme typé, c'est simplifier une preuve, et que les types sont des propositions (Howard 1980). Les machines SECD (Landin 1964) et de Krivine (Krivine 2007) traduisent le calcul en séquences d'instructions sur des états finis, déplaçant le coût de la substitution vers la gestion de piles et de fermetures.

La Partie IV a été celle des comptes. Le Chapitre 13 a montré que le nombre de pas $\beta$ n'est pas spontanément une mesure de temps : Accattoli et Dal Lago (2016) ont établi (CONNU) que la réduction leftmost-outermost est invariante, c'est-à-dire qu'elle simule toute autre stratégie à facteur polynomial près, mais le coût réel dépend de la représentation de la substitution. Le Chapitre 14 a introduit le partage comme ressource à part entière : la réduction optimale de Lamping (1990) évite la duplication inutile en partageant les sous-termes, au prix d'une complexité structurelle accrue (crochets, étiquettes). Le Chapitre 15 a dressé l'atlas des traductions : termes $\to$ indices de de Bruijn, termes $\to$ combinateurs, termes $\to$ fermetures, termes $\to$ graphes partagés, termes $\to$ preuves typées. Chaque traduction conserve la puissance de calcul (Church 1936 ; Turing 1937) et la confluence (Church et Rosser 1936), mais déplace le coût entre taille, temps, mémoire, profondeur, largeur, précision et partage.

### La thèse du livre, reformulée

Si je devais résumer ce livre en une phrase, ce serait celle-ci : *le lambda-calcul est minimal, mais cette minimalité a un prix, et chaque traduction que l'on construit pour le rendre exécutable, vérifiable ou partageable déplace ce prix sans jamais l'annuler.*

La substitution capture le coût de la $\beta$-réduction. Quand on écrit $(\lambda x.\, t)\, u \to_\beta t[x := u]$, tout le travail est dans $t[x := u]$ : parcourir $t$, identifier les occurrences libres de $x$, éviter les captures, potentiellement dupliquer $u$ plusieurs fois. Ce coût est invisible dans la règle elle-même, qui tient en une ligne. Il devient visible dès qu'on implémente : la substitution naïve est en $O(|t| \cdot |u|)$ dans le pire cas, et les duplications successives peuvent créer une explosion exponentielle de la taille du terme.

Les traductions que nous avons étudiées ne suppriment pas ce coût ; elles le déplacent. Les indices de de Bruijn suppriment le coût du renommage mais introduisent un coût de décalage. Les combinateurs $S$ et $K$ suppriment la variable liée mais gonflent la taille du terme (la traduction de $\lambda x.\, t$ en combinateurs peut multiplier la taille par une constante, et la composition itérée par $S$ peut créer des redexes intermédiaires volumineux). Les machines à fermetures déplacent la substitution vers la manipulation de piles et d'environnements, au prix d'une indirection mémoire. Le partage explicite (Lamping 1990) évite la duplication mais introduit des nœuds de partage, des crochets et une discipline de propagation. Le typage simplement typé échange l'expressivité (on perd $Y$, on perd la récursion générale) contre la garantie de terminaison.

Le registre des statuts — PROUVÉ, CONNU, EXPÉRIMENTAL, CONJECTURE, RÉFUTÉ, OUVERT — a été le fil conducteur méthodologique de ce livre. Chaque énoncé y a été rattaché. Les résultats que j'ai démontrés intégralement (propriétés de la substitution, confluence locale par le lemme de substitution, correction des encodages de Church) portent le statut PROUVÉ. Les grands théorèmes — Church-Rosser, normalisation forte, invariance de la réduction leftmost-outermost, optimalité de Lamping — portent le statut CONNU : vrais, démontrés dans la littérature, mais dont je n'ai donné ici que l'idée de preuve, en le disant explicitement. Aucune annonce de découverte n'a été faite, parce qu'il n'y en a pas : ce livre reconstruit, il ne découvre pas.

### Ce que le registre des statuts nous a appris

Au fil des seize chapitres, le registre a rempli une fonction que je ne soupçonnais pas entièrement au moment de planifier l'ouvrage : il a rendu visible la *granularité de la certitude*. Un lecteur qui parcourt le livre peut, à tout moment, savoir s'il lit une définition (qui n'a pas de statut de vérité), un lemme démontré intégralement (PROUVÉ), un théorème classique dont l'idée de preuve est esquissée (CONNU), une observation numérique sur un exemple particulier (EXPÉRIMENTAL), une intuition non encore formalisée (CONJECTURE), ou une question sans réponse connue (OUVERT).

Cette granularité n'est pas un luxe pédagogique. Elle est la traduction, au niveau du texte, de ce que le livre dit au niveau du calcul : chaque opération a un coût, et il faut le rendre explicite. De même que la substitution a un coût qu'il faut compter, chaque affirmation a un statut qu'il faut déclarer. L'honnêteté épistémique est une ressource, au même titre que le partage ou la mémoire.

### Perspectives : vers le programme RTC et au-delà

Le Chapitre 16 a ouvert la porte vers le programme RTC — Traductions à Ressources du Calcul. Ce programme, dont ce livre constitue le socle conceptuel, pose une série de questions que je laisse ici en guise d'horizon :

*Quelles ressources ?* Nous avons identifié la taille, le temps (nombre de pas $\beta$), la mémoire (espace de stockage des termes ou des fermetures), la profondeur (longueur maximale de la pile), la largeur (degré maximal de partage), la précision (fidélité de la traduction à la sémantique opérationnelle) et le partage (nombre de nœuds partagés vs. dupliqués). Cette liste est-elle close ? Rien ne permet de l'affirmer (OUVERT). Il est plausible que des ressources plus fines — coût de la gestion des noms, coût de la vérification de type, coût de la sérialisation — émergent dans des contextes applicatifs que nous n'avons pas couverts.

*Quelles traductions ?* L'atlas du Chapitre 15 en recense six familles. Mais l'espace des traductions possibles est immense : traductions vers des systèmes de réécriture d'ordre supérieur, vers des réseaux de preuve linéaires, vers des calculs de processus, vers des architectures matérielles spécifiques. Chaque traduction supplémentaire est un point dans l'espace des coûts, et la question de savoir si cet espace admet une structure — un ordre partiel, une métrique, une géométrie — reste ouverte (OUVERT).

*Quelles questions ouvertes ?* L'invariance de la réduction (Accattoli et Dal Lago 2016) établit un cadre asymptotique, mais les constantes cachées, le comportement en pratique sur des termes de taille modérée, et l'interaction entre invariance et partage optimal (Lamping 1990) restent partiellement explorés. La question de savoir s'il existe une traduction unique qui soit simultanément optimale en temps, en espace et en partage est, à ma connaissance, ouverte (OUVERT) — et peut-être n'a-t-elle pas de sens sans préciser un modèle de coût plus fin que ceux dont nous disposons.

Le programme RTC, tel que je le conçois, n'est pas un programme de recherche au sens où il annoncerait des résultats à venir. C'est un cadre de questions, une manière de lire toute traduction du lambda-calcul comme un déplacement de coût. Ce livre en fournit la grammaire.

### Un mot final au lecteur

Si vous avez lu ce livre du premier chapitre au dernier, vous avez parcouru un chemin qui va de l'arbre syntaxique le plus élémentaire — $\lambda x.\, x$ — jusqu'aux machines à fermetures et aux réseaux de partage. Vous avez vu comment une seule règle de calcul, la $\beta$-réduction, suffit à engendrer toute la puissance de calcul que Church (1936) et Turing (1937) ont identifiée, et comment cette puissance a un prix : la substitution, la divergence, l'explosion de taille, l'indécidabilité de la normalisation.

Je vous ai demandé, à chaque chapitre, de faire confiance à l'intuition avant la définition, à la définition avant l'énoncé, à l'énoncé avant la preuve, et à la preuve avant l'application. Cette progression n'est pas une coquetterie : elle reflète la structure même du lambda-calcul, où tout se construit par couches successives à partir d'un noyau irréductible.

Ce livre ne vous donne pas de résultats nouveaux. Il ne revendique aucune découverte. Il reconstruit, patiemment, des énoncés connus, en explicitant ce que la littérature passe souvent sous silence : le coût de chaque opération, le statut de chaque affirmation, le prix de chaque traduction. Si, en refermant ces pages, vous regardez une réduction $\beta$ et que vous vous demandez instinctivement « combien coûte cette substitution ? », « combien de fois ce sous-terme sera-t-il dupliqué ? », « quelle traduction rendrait ce calcul plus économe ? » — alors ce livre aura rempli son rôle.

Le lambda-calcul a quatre-vingt-dix ans. Il est né dans les années 1930, dans les travaux de Church, de Kleene, de Rosser, comme un outil de logique mathématique. Il est devenu, par un enchaînement que personne n'avait planifié, le fondement théorique des langages fonctionnels, des assistants de preuve, des vérificateurs de types et des compilateurs. Cette trajectoire n'était pas écrite dans les axiomes ; elle a émergé de la structure même du calcul, de sa minimalité, de sa capacité à se laisser traduire sans se laisser épuiser.

Il me reste à vous remercier. Vous, lecteur, qui avez accepté de suivre un auteur dans un livre qui ne promet ni algorithme miracle ni framework révolutionnaire, mais seulement la compréhension patiente d'un objet mathématique. Le lambda-calcul n'a pas besoin d'être défendu ni vendu. Il a besoin d'être compris. C'est, modestement, ce que j'ai tenté de faire ici.

La dernière formule du livre sera la première que vous avez rencontrée :

$$\lambda x.\, x$$

L'identité. Le terme le plus simple. Celui qui ne fait rien, sinon renvoyer ce qu'on lui donne. Toute la complexité que nous avons traversée — la substitution, la confluence, les types, les machines, le partage, l'optimalité — est contenue en puissance dans ce terme, comme un pli dans un papier que l'on n'a pas encore déplié.

Le calcul continue.

---

*Oussama Ghorbel*
*Novembre 2026*

### Ce que ce livre ne dit pas

Un livre qui se veut honnête doit aussi déclarer ses silences. Celui-ci n'est pas un traité de sémantique dénotationnelle : nous n'avons pas construit de modèles ensemblistes ou domainaux du lambda-calcul, nous n'avons pas parlé de modèles de Scott, de filtres, de réalisabilité au sens de Kleene. La raison en est simple : la thèse de ce tome est syntaxique et opérationnelle. Chaque coût que nous avons identifié — substitution, duplication, partage, profondeur de pile — se lit dans la structure des termes et dans les règles qui les transforment. Passer aux modèles, c'est changer de registre : on ne compte plus les pas, on interprète. Ce n'est pas un défaut des modèles ; c'est une autre traduction, avec ses propres coûts, que ce livre n'a pas la place d'aborder.

Nous n'avons pas non plus traité des systèmes de types avancés — types dépendants, types polymorphes de System F, types inductifs, types linéaires. Le lambda-calcul simplement typé du Chapitre 9 et la correspondance de Curry-Howard du Chapitre 11 (Howard 1980) constituent un seuil : au-delà, la correspondance entre preuves et programmes s'enrichit considérablement, mais le prix en complexité syntaxique et en difficulté de normalisation croît en proportion. Pierce (2002) et Hindley et Seldin (2008) offrent des portes d'entrée vers ces territoires. Ce livre s'arrête volontairement avant, pour que le lecteur dispose d'abord d'une compréhension ferme du noyau.

Enfin, nous n'avons pas abordé la question de l'implémentation industrielle : les compilateurs de Haskell, d'OCaml, de ML, les machines virtuelles fonctionnelles, les représentations en mémoire des fermetures dans les runtimes modernes. Le Chapitre 12 (Landin 1964 ; Krivine 2007) donne les architectures abstraites ; le passage à l'ingénierie est une autre traduction encore, avec ses propres contraintes — latence, cache, parallélisme — qui débordent le cadre de ce tome.

### Une note sur les exercices

Les exercices qui ponctuent chaque chapitre ne sont pas des vérifications de compréhension au sens scolaire. Ils sont, pour la plupart, des invitations à *sentir le coût*. Quand je vous demande de réduire $(\lambda x.\, x\, x)(\lambda y.\, y\, z)$ à la main en comptant chaque étape de substitution, le but n'est pas d'obtenir la réponse — elle tient en deux lignes — mais de faire éprouver physiquement ce que signifie « substituer », « renommer », « dupliquer ». De même, les exercices du Chapitre 14 sur le partage vous demandent de dessiner des graphes, de placer des nœuds de duplication, de compter les arêtes : le partage n'est pas une idée abstraite, c'est une topologie.

Si vous avez fait ces exercices avec un crayon et du papier, vous avez fait ce que je considère comme l'acte de lecture le plus fidèle à l'esprit du livre : vous avez *réduit à la main*, vous avez été votre propre machine de Krivine, avec votre mémoire de travail comme pile et votre attention comme environnement.

### Sur l'acte d'écrire un livre qui reconstruit

Il y a une tentation, quand on écrit sur un sujet aussi balisé que le lambda-calcul, de croire que tout a été dit et qu'il ne reste qu'à paraphraser. J'ai résisté à cette tentation non pas en ajoutant des résultats — il n'y en a pas de nouveaux ici — mais en déplaçant le regard. La littérature classique (Barendregt 1984 ; Hindley et Seldin 2008) présente le lambda-calcul comme une théorie : on définit, on démontre, on corollaire. Ce livre le présente comme une *économie* : chaque opération a un coût, chaque traduction déplace ce coût, chaque restriction en échange un autre. Ce déplacement de regard n'est pas un résultat ; c'est un angle. Il ne produit pas de théorème nouveau ; il produit une manière de lire les théorèmes existants qui rend visible ce qui était implicite.

Le registre des statuts est l'outil de cet angle. En obligeant chaque énoncé à se déclarer — PROUVÉ, CONNU, EXPÉRIMENTAL, CONJECTURE, RÉFUTÉ, OUVERT — il interdit la confusion entre ce que l'auteur démontre et ce qu'il emprunte, entre ce qui est établi et ce qui est espéré. Dans un domaine où les résultats sont anciens et les preuves souvent difficiles, cette distinction est une forme de respect envers le lecteur et envers la littérature.

### Le pli qui reste

J'ai clos la conclusion précédente sur $\lambda x.\, x$, l'identité, le terme qui ne fait rien. J'y reviens une dernière fois, non pour me répéter, mais pour ajouter une couche.

Ce terme est aussi le plus petit programme qui soit : il prend une entrée et la retourne. En termes de traduction, il est invariant par toutes les traductions que nous avons étudiées : en indices de de Bruijn, il devient $\lambda.\, 0$ ; en combinateurs, il est $S\, K\, K$ ; dans la machine de Krivine, il est une fermeture triviale qui, appliquée, renvoie son argument sans consulter l'environnement ; dans la correspondance de Curry-Howard, il est la preuve de $A \Rightarrow A$, la preuve la plus courte possible, celle qui dit « si l'on me donne $A$, je rends $A$ ».

Quatre traductions, quatre représentations, un même contenu computationnel. Le coût de chaque traduction, sur ce terme, est minimal : une constante de taille, un pas de réduction, zéro partage nécessaire. C'est le point zéro de l'atlas, l'origine des coordonnées. Toute la complexité que nous avons traversée dans ce livre est une déviation par rapport à ce point.

Mais c'est aussi un rappel : la complexité n'est pas dans le calcul lui-même. Elle est dans la *représentation* du calcul, dans la manière dont on choisit de le porter, de le stocker, de le réduire, de le partager. Le lambda-calcul, en tant que système formel, est d'une simplicité désarmante. Ce sont nos besoins — exécuter efficacement, vérifier formellement, partager sans dupliquer, typer pour garantir — qui introduisent la complexité. Chaque traduction est une réponse à un besoin, et chaque réponse a un prix.

C'est, je crois, la leçon la plus durable que ce livre puisse transmettre : la complexité n'est pas une propriété intrinsèque des objets mathématiques ; elle est une propriété de la relation entre ces objets et les contraintes qu'on leur impose. Le lambda-calcul n'est pas complexe. Nos exigences le rendent complexe. Et comprendre cette distinction, c'est déjà commencer à choisir ses traductions en connaissance de cause.

### Remerciements

Je remercie le lecteur d'avoir accepté la lenteur. Ce livre ne se lit pas en diagonale. Il demande qu'on s'arrête sur une définition de substitution, qu'on vérifie à la main qu'une capture est bien évitée, qu'on compte les pas d'une réduction. Cette lenteur est voulue. Elle est le rythme même du calcul : un pas $\beta$ à la fois, une substitution après l'autre.

Je remercie aussi, sans les nommer — car ce livre ne contient pas d'anecdotes et n'en inventera pas —, celles et ceux qui, par leurs questions, leurs objections, leurs silences, ont shaped la forme de ces chapitres. Un livre sur le lambda-calcul est, d'une certaine manière, une longue conversation avec des interlocuteurs qui ne savent pas toujours qu'ils en sont.

### Dernier mot

Le calcul continue. Il continue dans les compilateurs qui réduisent des fermetures, dans les assistants de preuve qui vérifient des types, dans les moteurs de recherche qui partagent des sous-expressions, dans les cours où un étudiant trace pour la première fois un arbre syntaxique et se demande pourquoi $\lambda x.\, \lambda y.\, x$ et $\lambda y.\, \lambda x.\, y$ ne sont pas la même chose.

Il continue parce qu'il est minimal, et que la minimalité est inépuisable : on peut toujours la traduire autrement, la regarder sous un autre angle, lui demander un autre coût. Ce livre est une de ces traductions. Il y en aura d'autres.

En attendant, réduisez.