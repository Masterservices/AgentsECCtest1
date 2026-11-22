## Introduction

### Une correspondance n'est pas une identité

Il existe, en logique et en informatique théorique, un résultat d'une élégance si frappante qu'on le récite souvent comme une évidence : prouver, c'est programmer. La correspondance de Curry-Howard, formalisée par Howard en 1980 et développée notamment par Girard, Lafont et Taylor en 1989, établit que les propositions de la logique intuitionniste sont des types, que les preuves sont des termes du lambda-calcul, et que la règle d'élimination des coupures coïncide avec la réduction $\beta$. Autrement dit, vérifier une preuve et exécuter un programme seraient, à la lettre, la même opération.

Ce livre est né d'une insatisfaction face à cette formulation. Non pas qu'elle soit fausse — elle est juste, et nous la démontrerons avec soin. Mais elle est incomplète, et son incomplétude est précisément ce qui rend le domaine fécond. Dire que deux objets sont *en correspondance*, ce n'est pas dire qu'ils sont *identiques sous tous les rapports*. Une traduction entre deux langues préserve le sens ; elle ne préserve pas nécessairement la longueur du texte, la profondeur de la subordination syntaxique, le nombre de répétitions, ni la possibilité de réutiliser un paragraphe comme lemme. De même, la correspondance de Curry-Howard traduit les programmes en preuves et les preuves en programmes, mais cette traduction a un *coût* : elle peut gonfler la taille, augmenter la profondeur, détruire le partage, ou au contraire les préserver. Ce coût n'est pas un détail technique. Il est, nous le verrons, au cœur de la complexité computationnelle.

La thèse de ce livre tient en une phrase : **une correspondance est une traduction, et toute traduction se mesure à ce qu'elle conserve et à ce qu'elle perd.** Chaque traduction entre modèles de calcul — lambda-calcul vers déduction naturelle, déduction naturelle vers résolution, formules propositionnelles vers clauses CNF, calculs bornés vers SAT — sera ici traitée comme un objet muni d'une fiche : son sens, sa définition, son coût sur sept ressources, les invariants qu'elle préserve, les pertes qu'elle engendre, et son statut épistémique.

### Le programme RTC et le registre des ressources

Ce tome s'inscrit dans la collection scientifique *Les Traductions du Calcul*, dont le programme de recherche, que nous appelons RTC, se donne pour objet l'étude systématique des traductions entre modèles de calcul et de leur coût en ressources. Le programme RTC identifie sept ressources pertinentes pour décrire un objet computationnel :

- la **taille** : nombre de symboles, de nœuds, de clauses ;
- le **temps** : nombre d'étapes de calcul, de réductions, de résolutions ;
- la **mémoire** : espace nécessaire pour stocker l'objet ou la trace ;
- la **profondeur** : hauteur de l'arbre de preuve ou de la dérivation ;
- la **largeur** : nombre maximal de prémisses actives simultanément ;
- la **précision** : équivalence logique, équisatisfiabilité, ou simple implication ;
- le **partage** : possibilité de factoriser les sous-calculs identiques.

Chaque traduction sera décrite par une fiche unique indiquant, pour chacune de ces sept ressources, si elle est conservée, bornée polynomialement, multipliée exponentiellement, ou perdue. Ce cadre n'est pas une invention ex nihilo : il synthétise et organise des observations dispersées dans la littérature, depuis l'encodage de Tseitin en 1968 jusqu'à l'analyse des solveurs modernes par Pipatsrisawat et Darwiche en 2011. Mais il fournit une grille de lecture unifiée que, à notre connaissance, aucun ouvrage ne propose sous cette forme systématique.

À ces sept ressources s'ajoute un **registre des statuts**. Toute affirmation de ce livre porte l'un des six statuts suivants : PROUVÉ (démontré intégralement dans ces pages), CONNU (résultat établi de la littérature, énoncé avec idée de preuve mais non redémontré ici), EXPÉRIMENTAL (observation mesurée sur des instances, sans portée universelle), CONJECTURE (énoncé cru vrai mais non démontré, jamais utilisé comme hypothèse dans une preuve), RÉFUTÉ (énoncé faux, contre-exemple fourni), ou OUVERT (question non tranchée, formulée précisément). Ce registre est une règle de rédaction, pas une coquetterie : il interdit qu'une intuition se glisse dans le texte avec l'apparence d'une preuve, et il permet au lecteur de savoir, à chaque ligne, sur quel sol il marche.

### Le sujet : trois modèles, deux traductions, une question

Le livre articule trois modèles de calcul :

1. **Le lambda-calcul simplement typé**, notre machine source. C'est le modèle des programmes : les termes sont les programmes, les types sont les spécifications, la réduction $\beta$ est l'exécution. Nous suivons la présentation de Barendregt en 1984 et celle de Pierce en 2002.

2. **La déduction naturelle propositionnelle**, notre machine cible intermédiaire. C'est le modèle des preuves : les formules sont les énoncés, les dérivations sont les preuves, l'élimination des coupures est la normalisation. Nous suivons Girard, Lafont et Taylor en 1989.

3. **Le problème SAT et les systèmes de preuve propositionnels**, notre machine cible finale. C'est le modèle de la vérification automatique : les clauses sont les contraintes, les résolutions sont les inférences, la trace du solveur est la preuve. Nous suivons Cook en 1971, Cook et Reckhow en 1979, Haken en 1985, et le manuel de Biere, Heule, van Maaren et Walsh en 2009.

Entre ces trois modèles circulent deux grandes traductions :

- la **correspondance de Curry-Howard** (Howard 1980), qui traduit programmes en preuves et types en propositions ;
- la **réduction vers SAT** (Cook 1971, Tseitin 1968), qui traduit des problèmes de décision en instances de satisfiabilité propositionnelle.

La question centrale du livre est alors : *que mesure la taille d'un terme de preuve ?* Cette question, apparemment simple, se ramifie dès qu'on la prend au sérieux. Taille-arbre ou taille-DAG ? Coût de vérification ou coût de recherche ? Coût de normalisation ou coût de construction ? La réponse dépend de la traduction choisie, et le choix de la traduction détermine quelles ressources sont visibles et lesquelles sont masquées.

### La démarche : traduire, mesurer, statuer

La démarche de ce livre est triple.

**Traduire.** Chaque passage d'un modèle à l'autre est présenté comme une traduction explicite, avec sa définition formelle. Nous ne disons pas « il existe une correspondance » ; nous définissons la fonction de traduction, nous montrons qu'elle est bien définie, nous calculons son effet sur la taille, la profondeur, le partage. Quand la traduction est l'encodage de Tseitin (1968), nous montrons qu'elle est linéaire en taille mais qu'elle remplace l'équivalence logique par l'équisatisfiabilité : c'est un gain en taille payé en précision. Quand la traduction est la réduction de Cook (1971), nous montrons qu'elle est polynomiale en taille mais qu'elle encode un calcul borné dans une formule propositionnelle dont la satisfiabilité reflète l'acceptation : c'est une traduction du temps vers la taille.

**Mesurer.** Pour chaque traduction, nous remplissons la fiche RTC : effet sur chacune des sept ressources. Ce faisant, nous rendons visibles des phénomènes que la littérature mentionne mais ne systématise pas : la duplication exponentielle des sous-termes lors de la normalisation sans partage, la perte de structure DAG quand on passe d'un terme partagé à un arbre de preuve, l'explosion de la largeur dans les résolutions longues.

**Statuer.** Chaque résultat est marqué. Les démonstrations complètes que nous donnons sont PROUVÉES. Les grands théorèmes — NP-complétude de SAT, borne inférieure de Haken, cadre de Cook-Reckhow — sont énoncés comme CONNUS, avec idée de preuve, et nous disons explicitement qu'ils ne sont pas redémontrés ici. Les questions non tranchées sont marquées OUVERTES. Aucune conjecture n'est utilisée comme lemme. Aucune intuition n'est présentée comme une preuve.

Ce livre n'annonce aucun résultat nouveau. Il démontre complètement ce qu'il déclare démontrer. Pour le reste, il donne l'idée, cite la source, et passe.

### Le public visé

Ce livre s'adresse à un lecteur cultivé, curieux, mais non nécessairement spécialiste de logique mathématique ou de théorie de la complexité. Le contrat de lecture est le suivant : chaque notion technique est introduite par une intuition, puis définie formellement, puis illustrée par un exemple, puis consolidée par un exercice. Le lecteur qui connaît déjà le lambda-calcul peut sauter les rappels ; celui qui découvre la logique propositionnelle trouvera les définitions nécessaires. Le fil conducteur — les traductions et leurs coûts — est maintenu visible à chaque chapitre, de sorte que même une lecture partielle reste cohérente.

Les prérequis sont modestes : une familiarité avec le raisonnement déductif élémentaire, une aisance avec les notations mathématiques de base, et surtout la volonté de suivre un argument pas à pas. Aucune connaissance préalable de la théorie de la démonstration automatique ou de la complexité structurelle n'est supposée.

### Ce que ce livre n'est pas

Il n'est pas un manuel de programmation fonctionnelle, même si le lambda-calcul y tient une place centrale. Il n'est pas un traité de logique mathématique, même si la déduction naturelle et les systèmes de preuve y sont développés. Il n'est pas un guide d'utilisation de solveurs SAT, même si les solveurs y sont analysés comme des moteurs de preuve. Il est un livre sur les *passages* entre ces mondes : ce qui se conserve, ce qui se perd, ce qui se paie.

Il n'est pas non plus un livre d'histoire des idées. Les références sont utilisées pour leur contenu technique, non pour leur narration biographique. Nous citons Cook en 1971 pour la réduction, Tseitin en 1968 pour l'encodage, Haken en 1985 pour la borne inférieure ; nous ne racontons pas les circonstances de ces découvertes.

### Plan du livre

Le livre est organisé en quatre parties et seize chapitres.

**Partie I — Le dictionnaire : trois modèles et une correspondance** (chapitres 1 à 4). Le chapitre 1 pose le cadre méthodologique : qu'est-ce qu'une traduction entre modèles, quelles sont les sept ressources du programme RTC, comment fonctionne le registre des statuts. Le chapitre 2 définit le lambda-calcul simplement typé comme machine source : syntaxe, types, réduction $\beta$, normalisation forte. Le chapitre 3 définit la logique propositionnelle et la déduction naturelle comme machine cible : formules, règles d'introduction et d'élimination, théorème de normalisation. Le chapitre 4 établit la correspondance de Curry-Howard comme traduction : types $\leftrightarrow$ formules, termes $\leftrightarrow$ preuves, réduction $\leftrightarrow$ élimination des coupures. La fiche de traduction est remplie.

**Partie II — La dynamique : normalisation, coupures et partage** (chapitres 5 à 8). Le chapitre 5 montre que normaliser un terme, c'est éliminer les coupures dans la preuve correspondante : la traduction du calcul. Le chapitre 6 analyse le prix de cette normalisation : duplication des sous-termes, augmentation de la profondeur, nombre de tours. Le chapitre 7 introduit la distinction entre arbres et DAG, et montre que le partage des sous-calculs est une ressource que la traduction peut détruire. Le chapitre 8 présente l'encodage de Tseitin (1968) comme une traduction linéaire qui paie en précision (équisatisfiabilité plutôt qu'équivalence) ce qu'elle gagne en taille et en partage.

**Partie III — Le coût : SAT, systèmes de preuve et bornes inférieures** (chapitres 9 à 12). Le chapitre 9 analyse la réduction de Cook (1971) : SAT comme cible universelle, la réduction comme traduction polynomiale du temps vers la taille. Le chapitre 10 développe le cadre de Cook et Reckhow (1979) : les systèmes de preuve comme modèles de calcul, leurs simulations comme traductions mesurables. Le chapitre 11 étudie la résolution et les solveurs SAT modernes : la preuve comme trace d'exécution, l'apprentissage de clauses comme partage, en s'appuyant sur Pipatsrisawat et Darwiche (2011) et Biere, Heule, van Maaren et Walsh (2009). Le chapitre 12 présente la borne inférieure de Haken (1985) sur le principe des tiroirs : anatomie d'une preuve de séparation, ce qu'elle borne et ce qu'elle ne borne pas.

**Partie IV — La mesure : ce que vaut une preuve, et transfert vers RTC** (chapitres 13 à 16). Le chapitre 13 replace la taille des preuves dans le paysage de la complexité : P, NP, coNP, et la question de savoir si les preuves courtes existent toujours. Le chapitre 14 affronte la question centrale : que mesure la taille d'un terme de preuve ? Arbre ou DAG, vérification ou recherche, normalisation ou construction. Le chapitre 15 dresse l'atlas des traductions : le grand tableau croisant chaque traduction avec les sept ressources. Le chapitre 16, enfin, opère le transfert vers le programme RTC : ce que ce tome apporte à l'étude générale des traductions à ressources, quelles questions il ouvre, quelles ressources il a révélées comme critiques.

### Une note sur le style et les preuves

Ce livre est écrit en français, en prose continue, avec des formules LaTeX pour la précision et des exemples concrets pour l'ancrage. Chaque chapitre suit une progression : intuition, définition, énoncé, exemple, exercice. Les exercices ne sont pas des appendices décoratifs : ils sont le lieu où le lecteur vérifie qu'il a compris la traduction en la pratiquant lui-même.

Les preuves complètes sont données pour les résultats que ce livre démontre : les propriétés de la correspondance de Curry-Howard en tant que traduction, les calculs de coût sur les sept ressources pour chaque encodage, les lemmes de préservation et de perte. Pour les grands théorèmes de la littérature — NP-complétude de SAT, borne de Haken, cadre de Cook-Reckhow — nous donnons l'idée de preuve, nous indiquons où se trouve la difficulté, et nous signalons explicitement que la démonstration complète n'est pas reproduite ici. Le statut CONNU marque ces passages.

Aucune formule n'est attribu��e à un auteur sous forme de citation entre guillemets. Les références sont données par le nom et l'année, conformément à la liste close des dix ouvrages et articles autorisés. Si un résultat n'appartient pas à cette liste, il n'est pas cité.

### Pourquoi maintenant ?

La correspondance de Curry-Howard a cinquante ans passés. Les solveurs SAT résolvent des instances industrielles à des millions de variables. Les assistants de preuve formalisent des théorèmes de mathématiques. Et pourtant, la question du *coût* de ces passages reste souvent traitée comme une note de bas de page, un « il est bien connu que la traduction est polynomiale », sans qu'on précise *quelle* ressource est polynomialement bornée et *laquelle* explose.

Le programme RTC, auquel ce tome contribue, propose de combler cette lacune non pas en produisant de nouveaux résultats de complexité — ce n'est pas l'objet — mais en *organisant* les résultats existants selon la grille des traductions à ressources. Ce livre est une contribution à cette organisation. Il ne découvre rien. Il *mesure*, il *classe*, il *rend visible*.

La question « que mesure la taille d'un terme de preuve ? » n'a pas de réponse unique. Elle a une réponse par traduction, par convention de mesure, par ressource considérée. Ce livre est l'atlas de ces réponses.

### Remerciements

Ce texte doit beaucoup aux formulations claires de Barendregt en 1984, à la pédagogie de Girard, Lafont et Taylor en 1989, et à l'exposition systématique de Pierce en 2002. La vision des solveurs comme moteurs de preuve doit à Pipatsrisawat et Darwiche en 2011 et au collectif de Biere, Heule, van Maaren et Walsh en 2009. Les bornes et les cadres sont ceux de Cook en 1971, Cook et Reckhow en 1979, Haken en 1985, Tseitin en 1968. Ce que j'espère avoir ajouté, c'est la grille de lecture qui les unifie : la traduction comme objet premier, la ressource comme mesure, le statut comme honnêteté.

— Oussama Ghorbel

### Mode d'emploi : comment lire ce livre

Avant de tourner la page vers le premier chapitre, quelques indications pratiques.

Ce livre peut se lire de trois manières. La première est linéaire : du chapitre 1 au chapitre 16, en suivant l'ordre dans lequel les modèles sont construits, les traductions définies, les coûts mesurés. C'est la lecture recommandée pour qui découvre le sujet. La seconde est thématique : un lecteur intéressé uniquement par la correspondance de Curry-Howard peut se limiter aux chapitres 2, 3 et 4 ; un lecteur intéressé par la complexité des preuves peut aller directement aux chapitres 9 à 13 ; un lecteur intéressé par les solveurs SAT peut ouvrir au chapitre 11. Chaque chapitre est conçu pour être lisible indépendamment, à condition d'accepter quelques renvois en amont. La troisième lecture est celle de l'atlas : le chapitre 15 fournit le tableau synoptique de toutes les traductions et de tous les coûts, et peut servir de point d'entrée ou de point de vérification.

Les conventions typographiques sont les suivantes. Les termes techniques sont en italique à leur première occurrence et définis dans le corps du texte ou dans la marge. Les formules mathématiques sont composées en LaTeX, entre simples dollars pour les expressions en ligne — par exemple $\lambda x. x$ — et entre doubles dollars pour les expressions détachées :

$$\frac{\Gamma \vdash M : A \to B \quad \Gamma \vdash N : A}{\Gamma \vdash M\, N : B}$$

Les statuts épistémiques apparaissent en petites capitales au début de l'énoncé qu'ils qualifient : PROUVÉ, CONNU, EXPÉRIMENTAL, CONJECTURE, RÉFUTÉ, OUVERT. Un énoncé sans statut est une définition ou une convention, qui n'appelle pas de justification externe.

Les exercices, en fin de section, sont de trois types. Les exercices de vérification demandent d'appliquer une définition ou de compléter un calcul ; ils sont accessibles dès la première lecture. Les exercices de traduction demandent de passer d'un modèle à l'autre en explicitant le coût ; ils supposent une compréhension active de la fiche RTC. Les exercices de réflexion posent une question ouverte ou demandent de construire un contre-exemple ; certains n'ont pas de solution connue, et nous le disons quand c'est le cas.

Les références sont données entre parenthèses, par le nom de l'auteur et l'année : (Cook 1971), (Tseitin 1968), (Haken 1985). La liste complète des dix références autorisées figure en tête d'ouvrage. Aucune autre source n'est citée. Si un fait mentionné dans ce livre n'appartient pas à cette liste, c'est qu'il relève de la définition ou du calcul interne, et non d'un résultat attribuable.

### Une dernière remarque : le choix du français

Ce livre est écrit en français. Ce choix n'est pas anodin dans un domaine où la quasi-totalité de la littérature technique est en anglais. Il ne s'agit pas de traduire les mathématiques — les formules restent les formules — mais de penser la pédagogie, l'argumentation et la métaphore dans une langue qui est celle de l'auteur et, nous l'espérons, celle d'une partie de ses lecteurs. Le mot « traduction » prend, dans ce contexte, une résonance particulière : nous écrivons un livre sur les traductions entre modèles de calcul, et nous l'écrivons dans une langue qui n'est pas la langue véhiculaire du domaine. C'est une manière de rappeler que toute transmission est un passage, et que tout passage a un coût et un gain.

Le lecteur qui souhaiterait vérifier un énoncé dans la littérature originale trouvera, pour chaque résultat marqué CONNU, la référence exacte. Le lecteur qui souhaiterait aller au-delà de ce tome trouvera, dans le chapitre 16, les questions que ce livre laisse ouvertes et la manière dont elles s'inscrivent dans le programme RTC.

Il est temps de commencer. Le chapitre 1 pose les fondations : qu'est-ce qu'un modèle de calcul, qu'est-ce qu'une traduction, qu'est-ce qu'une ressource, et comment fonctionne le registre des statuts. Tout le reste du livre s'appuiera sur ces trois définitions.

— Oussama Ghorbel