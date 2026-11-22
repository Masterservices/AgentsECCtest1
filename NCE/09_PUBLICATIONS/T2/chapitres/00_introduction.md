## Introduction — Tenir le registre des traductions

### Calculer, c'est exécuter

On présente d'ordinaire la machine de Turing comme un critère. Est calculable ce qu'une telle machine calcule ; est décidable ce qu'elle décide. Depuis Turing 1936, ce critère s'est révélé d'une robustesse remarquable : ajoutez des rubans, élargissez l'alphabet, autorisez le non-déterminisme, remplacez la table de transitions par un interprète universel, déroulez l'exécution en circuit booléen — la frontière du calculable ne bouge pas. Cette robustesse est un résultat, et l'un des plus solides de la pensée mathématique du vingtième siècle.

Elle a pourtant un effet de bord : elle rend muet sur la facture. Quand on affirme que « toutes ces machines calculent la même chose », on énonce un invariant ; on ne dit rien de ce que le passage de l'une à l'autre coûte en pas, en cellules, en états, en portes, en bits. Le mot « même » fait un travail considérable, et il le fait en silence.

Je propose de déplacer le regard. Une machine de Turing n'est pas seulement un critère de calculabilité : c'est un système de comptabilité de l'exécution. À chaque pas, elle change d'état, écrit un symbole, déplace une tête. Chaque pas est une écriture au registre : une unité de temps dépensée, une cellule peut-être nouvellement visitée, une description dont la taille a été fixée une fois pour toutes avant de commencer. L'ex��cution est une suite de configurations, et les ressources sont des comptages sur cette suite. Rien de plus mystérieux que cela — et c'est précisément pourquoi le modèle se prête à un audit.

Ce livre tient le registre de ces comptages, non pour une machine, mais pour les traductions entre machines. Chaque résultat y est présenté comme une traduction : une source, une cible, un invariant préservé, des coûts, et un statut explicite. La question n'est jamais seulement « est-ce que cela calcule la même chose ? », mais « qu'est-ce qui est conservé, qu'est-ce qui est déplacé, qu'est-ce qui est perdu, et que savons-nous exactement de cette perte ? ».

### L'invariant et les sept ressources

Commençons par fixer ce qui doit être conservé, car sans cela le mot « traduction » reste vide.

**Définition (invariant sémantique).** Pour une machine qui calcule des valeurs, l'invariant est la fonction partielle $f : \Sigma^* \rightharpoonup \Gamma^*$ qu'elle réalise, domaine de définition compris : une traduction fidèle doit diverger exactement là où la source diverge. Pour une machine qui décide, l'invariant est le langage $L \subseteq \Sigma^*$ reconnu, avec arrêt sur toutes les entrées. Pour une machine non déterministe, l'invariant est le langage accepté — non l'arbre des calculs.

Cette dernière précision est déjà une perte. L'arbre de calcul contient des témoins : une branche acceptante est un certificat. La déterminisation conserve le langage et détruit la structure des témoins. Ce n'est pas un détail technique ; c'est ce qui rend la question de Cook 1971 intéressante, et nous y reviendrons au chapitre 13.

Fixons maintenant ce qui peut être dépensé. Sept ressources sont tenues au registre, et le glossaire de l'appareil en donne les définitions complètes :

- **temps** : $t_M(n)$, le nombre maximal de pas sur les entrées de longueur $n$ ;
- **espace** : $s_M(n)$, le nombre maximal de cellules visitées ;
- **taille de description** : $|M|$, la longueur de la table de transitions et des alphabets, ou le nombre de portes d'un circuit ;
- **profondeur** et **largeur** : pour les circuits, longueur du plus long chemin et nombre maximal de portes simultanément actives par couche ;
- **précision** : le nombre de bits stockés par cellule, soit $\lceil \log_2 |\Gamma| \rceil$ ;
- **partage** : le degré de réutilisation d'un même sous-calcul — sortie d'une porte alimentant plusieurs portes, mémoire commune à plusieurs rubans, uniformité d'une famille de circuits.

Certaines ressources sont sans objet pour certains modèles : la profondeur d'une machine à ruban n'a pas de sens, et je l'écris « sans objet » dans la fiche plutôt que de la mettre à zéro, ce qui serait une affirmation déguisée.

Ces grandeurs ne sont pas indépendantes, et les inégalités élémentaires entre elles sont les premières entrées du registre. Par exemple, $s_M(n) \le t_M(n) + 1$ par ruban : chaque pas visite au plus une cellule nouvelle (PROUVÉ, chapitre 3, par comptage immédiat). Cette trivialité a une conséquence qui ne l'est pas : toute borne en temps est une borne en espace, et l'inverse est faux. Le registre est orienté.

### La fiche de traduction

**Définition (fiche).** Une traduction est décrite par une fiche comportant : le modèle source, le modèle cible, l'invariant préservé, les sept coûts, le statut de l'énoncé, le statut de l'optimalité.

Voici une fiche remplie, celle du chapitre 7, qui servira d'étalon au lecteur.

- **Source** : machine déterministe à $k$ rubans, temps $t(n) \ge n$.
- **Cible** : machine déterministe à un ruban.
- **Invariant** : la fonction partielle calculée, domaine compris.
- **Temps** : $O(t(n)^2)$.
- **Espace** : $O(t(n))$.
- **Description** : $|M| + O(1)$, la constante dépendant de $k$ et des alphabets.
- **Profondeur, largeur** : sans objet.
- **Précision** : multipliée par une constante (l'alphabet cible encode $k$ pistes).
- **Partage** : perdu — les $k$ têtes indépendantes deviennent une unique tête qui balaie.
- **Statut de l'énoncé** : PROUVÉ (preuve complète au chapitre 7).
- **Statut de l'optimalité** : le surcoût quadratique est inévitable en général — CONNU (Hopcroft et Ullman 1979), par un argument de séquences de croisement ; l'idée est donnée, la preuve complète ne figure pas dans ce tome.

Le lecteur voit immédiatement ce que la fiche fait apparaître et que le mot « équivalent » efface : le temps augmente, la description diminue presque, la précision augmente, le partage disparaît. L'invariant est sauf ; la comptabilité a été réécrite.

### Le registre des statuts

Chaque énoncé technique du tome porte l'un des six statuts suivants. Les définitions et les conventions de notation n'en portent pas : ce sont des décisions, non des affirmations, et elles sont signalées comme telles.

**PROUVÉ** : une preuve complète figure dans ce tome. Le statut ne dit rien de la paternité historique — le théorème peut être dû à Savitch 1970 ou à Hartmanis et Stearns 1965 — il dit seulement que le lecteur peut tout vérifier ici, sans aller ailleurs. **CONNU** : l'énoncé est établi dans la littérature, mais ce tome n'en donne que l'idée de preuve, et le dit explicitement à l'endroit même où il l'utilise. La distinction n'est pas décorative : elle sépare ce que le livre démontre de ce qu'il rapporte.

**EXPÉRIMENTAL** : une mesure, obtenue sur de petites entrées avec les machines de la bibliothèque du chapitre 4, selon un protocole reproductible décrit sur place. Une mesure ne prouve jamais un énoncé asymptotique. Si je constate que le rapport des nombres de pas entre deux programmes croît sur les entrées de longueur $n \le 64$, cela n'établit pas un facteur $\log t$ : cela illustre, et le statut le rappelle.

**CONJECTURE** : une hypothèse du programme de traductions à ressources, énoncée parce qu'elle organise les questions, non parce qu'elle est établie. **RÉFUTÉ** : un énoncé dont la négation est démontrée ici, par contre-exemple ou par preuve de non-existence — ainsi « un automate fini reconnaît $\{a^n b^n : n \ge 0\}$ » (RÉFUTÉ, chapitre 12). **OUVERT** : une question que ni ce tome ni, à ma connaissance, la littérature des onze titres cités ne tranche.

Le statut de l'optimalité est une colonne séparée, et c'est souvent la plus intéressante. Savitch 1970 donne $\mathrm{NSPACE}(s(n)) \subseteq \mathrm{DSPACE}(s(n)^2)$ pour $s(n) \ge \log n$ sous hypothèses de constructibilité (PROUVÉ, chapitre 11). Que le carré soit nécessaire est OUVERT. Confondre les deux colonnes — croire qu'une simulation connue est optimale parce qu'aucune meilleure n'est connue — est la faute de lecture que ce registre est conçu pour empêcher.

Enfin, une règle de rédaction : les paragraphes d'intuition sont marqués comme tels et ne portent aucun statut, parce qu'ils n'affirment rien. Une intuition peut guider une preuve ; elle ne peut pas la remplacer, et rien de ce qui est utilisé plus loin ne s'appuie sur elle sans être rétabli.

### Ce que trois traductions classiques coûtent

Pour que le propos ne reste pas abstrait, voici trois factures, choisies parce qu'elles déplacent les ressources dans des directions différentes.

**Le ruban unique paie en temps.** Une machine à deux rubans copie son entrée puis compare les deux moitiés : temps linéaire, espace linéaire. Une machine à un ruban fait des allers-retours : temps quadratique, espace linéaire, description plus courte. La borne inférieure quadratique pour un langage de ce type est CONNU (Hopcroft et Ullman 1979) ; la simulation quadratique, elle, est PROUVÉ au chapitre 7. Le confort de l'accès parallèle se paie donc, et il se paie en temps.

**Deux rubans suffisent presque.** Hennie et Stearns 1966 montrent qu'une machine à $k$ rubans s'exécutant en temps $t(n)$ est simulable par une machine à deux rubans en temps $O(t(n)\log t(n))$ (CONNU ; idée : découpage en blocs hiérarchisés, redistribution amortie, et calendrier de déplacements indépendant de l'entrée). La perte passe de quadratique à logarithmique. Que ce logarithme soit nécessaire dans le cas général est OUVERT.

**Le circuit paie en description et perd l'uniformité.** Dérouler $t$ pas d'exécution en un circuit donne naïvement une taille $O(t^2)$ (PROUVÉ, chapitre 15) ; l'exploitation du calendrier oblivieux améliore cela en $O(t(n)\log t(n))$ (CONNU ; Pippenger et Fischer 1979). Mais un circuit ne traite qu'une longueur d'entrée. L'invariant « fonction partielle sur toutes les entrées » n'est pas conservé par un circuit seul : il faut une famille, et une condition d'uniformité pour que la famille redevienne un algorithme. Ici, la traduction ne déplace pas seulement des ressources : elle change la nature de l'objet, et le registre doit le dire.

Un quatrième exemple, plus petit, montre que même les « gratuités » apparentes sont des déplacements. L'accélération linéaire permet de gagner un facteur constant en temps (CONNU ; Hartmanis et Stearns 1965 ; idée : compression par blocs). Le facteur gagné se paie en taille de description : l'alphabet de la machine accélérée croît exponentiellement avec le facteur demandé. De même, réduire un alphabet de $k$ symboles à deux symboles multiplie le temps par $O(\log k)$ et le nombre de cellules par $\lceil \log_2 k \rceil$, en divisant la précision par le même facteur (PROUVÉ, chapitre 5). Dans ce cas précis, le produit cellules $\times$ bits par cellule est conservé à constante près. Qu'un tel produit soit toujours conservé est une tout autre affaire, et je l'étiquette CONJECTURE au chapitre 16.

### Ce que ce livre n'annonce pas

Aucun résultat nouveau n'est annoncé ici. Je ne revendique aucun théorème, aucune amélioration de borne, aucune séparation de classes. La contribution de ce tome est une contribution de forme : un registre, une discipline de fiche, une séparation stricte entre ce qui est démontré, ce qui est rapporté, ce qui est mesuré, ce qui est conjecturé et ce qui est ouvert.

Le cadre des traductions à ressources — j'écris RTC — est un programme de travail, pas un corps de résultats. Ses « lois » candidates sont étiquetées CONJECTURE, et je les énonce avec leurs garde-fous. Par exemple : « aucune traduction entre modèles distincts, conservant l'invariant sémantique, ne diminue simultanément toutes les ressources dans le pire cas » (CONJECTURE, RTC-A, chapitre 16). Une telle phrase est vide si l'on n'exclut pas la traduction identité, si l'on ne fixe pas ce qu'est le pire cas, et si l'on ne dit pas sur quelle famille d'entrées on quantifie. Le chapitre 16 fait ce travail de formulation, et signale les formulations qui s'effondrent aussitôt — c'est aussi une manière d'apprendre.

La bibliographie est volontairement limitée à onze titres : Turing 1936 ; Kleene 1956 ; Hartmanis et Stearns 1965 ; Hennie et Stearns 1966 ; Savitch 1970 ; Cook 1971 ; Pippenger et Fischer 1979 ; Hopcroft et Ullman 1979 ; Papadimitriou 1994 ; Sipser 1997 ; Arora et Barak 2009. Rien d'autre n'est cité, et je ne prête aucune formule à aucun auteur entre guillemets. Les manuels de cette liste — Hopcroft et Ullman 1979, Sipser 1997, Papadimitriou 1994, Arora et Barak 2009 — sont les compagnons naturels du lecteur qui voudrait les preuves complètes des énoncés marqués CONNU.

### Pour qui, et comment lire

Ce livre s'adresse à un lecteur cultivé non spécialiste : étudiant en informatique, ingénieur curieux de ce que « complexité » veut dire exactement, philosophe ou logicien qui veut vérifier ce qu'on met sous le mot « calcul », ou lecteur à l'aise avec une démonstration par récurrence et sans culture préalable en théorie de la complexité. Les prérequis sont modestes : ensembles, fonctions, induction, et la notation $O(\cdot)$, rappelée dès le chapitre 2. Aucune connaissance des automates n'est supposée.

Trois parcours sont possibles. Le parcours linéaire suit les seize chapitres. Le parcours « traductions » prend les chapitres 5 à 8, puis 15, puis 16 : c'est le cœur du registre. Le parcours « limites » prend les chapitres 9 à 14 : indécidabilité, hiérarchies, classes. Dans tous les cas, les chapitres 2 et 3 sont indispensables, car ils fixent les conventions dont dépendent tous les comptages — un facteur constant mal placé vient presque toujours d'une convention non déclarée.

Chaque chapitre suit le même mouvement : intuition, définition, énoncé avec statut, exemple, exercice. Les exercices portent eux aussi un statut : certains demandent une preuve (et deviennent PROUVÉ une fois corrigés), d'autres demandent une mesure (EXPÉRIMENTAL), d'autres demandent de remplir une fiche dont une case reste OUVERT. Trois exercices d'entrée, pour prendre la main :

1. Montrer que $s_M(n) \le t_M(n) + 1$ par ruban, puis exhiber une machine pour laquelle l'égalité est atteinte à un près. *(Indication : compter les cellules nouvellement visitées à chaque pas.)*
2. Remplir la fiche de la traduction « alphabet de $k$ symboles vers alphabet binaire », en justifiant chaque coût par un comptage explicite. Quel produit de ressources reste invariant ?
3. Expliquer pourquoi une famille de circuits ne conserve pas l'invariant « fonction partielle sur $\Sigma^*$ », et quelle condition supplémentaire le restaure. *(Cette question est reprise au chapitre 15.)*

### Le plan en seize chapitres

**Partie I — La machine : syntaxe et sémantique de l'exécution.** Le chapitre 1 pose la question : pourquoi un modèle mécanique plutôt qu'une liste de fonctions, et ce que le geste de Turing 1936 rend possible. Le chapitre 2 donne la définition et, surtout, ses conventions : ruban infini ou semi-infini, symbole blanc, nombre de têtes, forme de la table de transitions — avec le coût constant de chaque changement de convention. Le chapitre 3 définit les configurations et la relation de pas, et établit les premières inégalités de comptage. Le chapitre 4 construit une petite bibliothèque de machines composables — copier, comparer, incrémenter — et fixe le protocole des mesures EXPÉRIMENTAL.

**Partie II — Traduire sans changer ce qui est calculé.** Le chapitre 5 traite des variantes de ruban et d'alphabet, où la robustesse s'achète à facteur constant, et où la précision entre pour la première fois au registre. Le chapitre 6 construit l'arbre de calcul non déterministe et sa déterminisation en temps $c^{t(n)}$, avec $c$ dépendant de la machine (PROUVÉ), et inventorise ce qui se perd : les témoins. Le chapitre 7 tient la comptabilité des multi-rubans : $O(t^2)$ démontré, $O(t\log t)$ rapporté, optimalité discutée. Le chapitre 8 lit la machine universelle comme une traduction : la description devient donnée, et le temps paie l'interprétation.

**Partie III — Les limites.** Le chapitre 9 démontre l'indécidabilité de l'arrêt et de l'équivalence, et en tire ce qui touche l'optimisation automatique : aucune procédure générale ne certifie qu'une transformation arbitraire préserve le comportement. Le chapitre 10 introduit les classes de temps, l'accélération linéaire et son prix en description, et démontre une hiérarchie (Hartmanis et Stearns 1965). Le chapitre 11 démontre Savitch 1970 et les hiérarchies en espace, avec les hypothèses de constructibilité énoncées. Le chapitre 12 descend à l'espace constant : automates finis, expressions régulières (CONNU ; Kleene 1956), lemme de pompage démontré, et les frontières exactes de ce qu'un espace borné permet.

**Partie IV — Classes, circuits, transfert.** Le chapitre 13 traduit un tableau d'exécution en formule et démontre l'énoncé de base de Cook 1971 ; la zoologie des problèmes complets reste CONNU. Le chapitre 14 déduit $\mathrm{PSPACE} = \mathrm{NPSPACE}$ de Savitch, discute la complétude en espace (CONNU) et dessine la carte des inclusions, en marquant OUVERT chaque flèche dont on ignore s'il est strict. Le chapitre 15 passe aux circuits : déroulage, taille $O(t\log t)$, profondeur, largeur, partage, uniformité. Le chapitre 16, « Transfert vers le programme RTC », fait le bilan : quelles ressources ce tome a su compter, quelles traductions il a su fiches, quelles lois candidates restent CONJECTURE et quelles questions restent OUVERT.

Le volume compte environ 204 pages de chapitres et 16 pages d'appareil : préface, mode d'emploi du registre, table des traductions et de leurs coûts, glossaire des ressources, index. La table est l'outil que j'espère voir le plus souvent consulté : une page où chaque traduction tient sur une ligne, avec ses coûts et ses deux statuts.

### Le geste du registre

Il y a une habitude de pensée que ce livre cherche à rendre difficile : dire « ces modèles sont équivalents » et croire avoir tout dit. L'équivalence est un fait sur l'invariant. Elle est muette sur la comptabilité, et la comptabilité est là où se trouvent toutes les questions qui comptent en pratique — combien de pas, combien de cellules, combien de portes, quelle réutilisation, quelle précision.

Le registre ne rend pas ces questions plus faciles. Il les rend plus honnêtes. Conserver l'invariant, déplacer les coûts, dire exactement ce que l'on sait du déplacement : c'est le seul geste que ce tome répète, seize fois, sans jamais le déguiser en découverte.