## Introduction

### Le grand malentendu de l'équivalence

L'année 1936 marque une césure définitive dans l'histoire de la pensée humaine. D'un côté, Alonzo Church publie ses travaux sur l'indécidabilité et introduit un système formel fondé sur la substitution de fonctions, le lambda-calcul (Church 1936). De l'autre, Alan Turing propose une modélisation mécanique du calcul à travers une machine abstraite manipulant des symboles sur une bande infinie (Turing 1936). Rapidement, la communauté mathématique fait un constat qui deviendra le socle de l'informatique théorique : ces deux modèles, bien que radicalement différents dans leur syntaxe et leur dynamique, capturent exactement la même classe de fonctions. C'est la thèse de Church-Turing, un pilier de notre discipline dont le statut épistémologique dépasse la simple preuve formelle pour toucher à la nature même du calcul effectif.

Pourtant, cette équivalence fondamentale a engendré un malentendu persistant, une illusion d'optique conceptuelle qui dure depuis près d'un siècle. Parce que le lambda-calcul et les machines de Turing définissent les mêmes frontières de la calculabilité, on a souvent conclu, à tort, qu'ils étaient interchangeables sans friction. On a cru que l'équivalence extensionnelle impliquait une équivalence structurelle. Or, il n'en est rien.

Mon objectif dans cet ouvrage est de dissiper cette illusion. La thèse centrale de ce livre est la suivante : le lambda-calcul et les machines de Turing définissent la même classe de fonctions calculables, mais les traductions qui les relient ne sont pas neutres. Elles conservent la calculabilité, certes, mais elles perdent, transforment ou dilatent des ressources structurelles fondamentales. Passer d'un modèle à l'autre n'est pas un simple changement de notation ; c'est une opération de physique de l'information qui possède un coût, qui génère de la résistance, et qui modifie la topologie du calcul.

Ce tome cartographie ces traductions dans les deux sens, mesure leur coût et identifie ce qui résiste, ce qui se dilate et ce qui disparaît lors du passage d'un modèle à l'autre. Nous n'allons pas seulement nous demander *si* une machine de Turing peut être encodée en lambda-terme, ou *si* une $\beta$-réduction peut être simulée par des transitions d'états. Nous allons mesurer l'anatomie de ces passages. Nous allons peser le coût de la traduction.

### Le cadre conceptuel : les traductions à ressources

Pour mener à bien cette cartographie, j'introduis un cadre conceptuel qui structurera l'intégralité de notre voyage : la théorie des **traductions à ressources**.

Une traduction entre deux modèles de calcul n'est pas un simple dictionnaire. C'est un compilateur qui doit allouer, transformer et parfois sacrifier des ressources. Pour analyser ces traductions, nous devons d'abord nous accorder sur ce qu'est une ressource dans le contexte du calcul abstrait. J'identifie sept ressources structurelles fondamentales qui seront le fil rouge de cet ouvrage :

1. **La taille** : le nombre de symboles ou de nœuds nécessaires pour écrire un programme ou représenter un état. C'est la mesure de l'encombrement syntaxique.
2. **Le temps** : le nombre d'étapes élémentaires (réductions ou transitions) pour atteindre un résultat. C'est la dynamique séquentielle du calcul.
3. **La mémoire** : l'espace requis pour stocker les données intermédiaires, qu'il s'agisse de cases sur une bande ou de fermetures (closures) dans un tas.
4. **La profondeur** : le degré d'imbrication des structures. Dans le lambda-calcul, c'est la profondeur des abstractions ; sur une machine de Turing, c'est la complexité des enchaînements d'états.
5. **La largeur** : la capacité du modèle à exposer des branchements ou des évaluations parallèles à un instant $t$.
6. **La précision** : la fidélité de la simulation. Une traduction est-elle exacte étape par étape, ou regroupe-t-elle plusieurs micro-étapes en une seule macro-transition ?
7. **Le partage** : la capacité à représenter des structures en graphe plutôt qu'en arbre, permettant à plusieurs parties d'un programme de faire référence à la même zone mémoire sans la dupliquer.

Chaque fois que nous établirons un pont entre le lambda-calcul et les machines de Turing, nous évaluerons la traduction selon ces sept axes. Nous verrons par exemple que la bande de Turing offre un accès mémoire séquentiel mais spatialement explicite, tandis que le lambda-calcul offre une mémoire structurelle implicitement gérée par la portée des variables, au prix d'une explosion potentielle de la taille lors de la substitution.

### Le registre des statuts

La rigueur exige que nous distinguions clairement ce qui est établi de ce qui est spéculatif. L'informatique théorique est un domaine vivant, où certaines bornes de complexité restent hors de portée. C'est pourquoi chaque affirmation majeure, chaque théorème et chaque bilan de traduction dans ce livre sera affublé d'un statut explicite, tiré du **registre des statuts** suivant :

* **PROUVÉ** : Le résultat est démontré de manière complète et formelle dans les pages de ce livre.
* **CONNU** : Le résultat est un théorème classique ou établi dans la littérature scientifique ; j'en donnerai l'idée de la preuve et les intuitions fondamentales, sans alourdir le texte par des démonstrations formelles de plusieurs dizaines de pages.
* **EXPÉRIMENTAL** : L'affirmation repose sur des observations tirées d'implémentations ou de simulations, mais ne dispose pas encore de bornes formelles strictes.
* **CONJECTURE** : L'hypothèse est hautement plausible, soutenue par des faisceaux d'indices théoriques, mais reste non démontrée à ce jour.
* **RÉFUTÉ** : L'idée, parfois séduisante, a été formellement invalidée ; nous étudierons ces échecs pour comprendre les limites des modèles.
* **OUVERT** : La question demeure une zone d'ombre active de la recherche, un point de fuite vers lequel le programme de recherche contemporain se dirige.

Ce registre est un contrat de lecture. Il vous permet de savoir exactement sur quel sol vous marchez. Quand nous aborderons l'invariance de la $\beta$-réduction (Accattoli et Dal Lago 2016), le statut sera CONNU. Quand nous évaluerons les bornes exactes de la duplication lors de l'encodage de certaines machines, le statut pourra être PROUVÉ par nos soins.

### À qui s'adresse ce livre et comment le lire

J'ai conçu cet ouvrage pour un lecteur cultivé non spécialiste. Vous n'avez pas besoin d'être un chercheur en sémantique dénotationnelle ou en théorie de la complexité structurelle pour suivre ce voyage. Il suffit d'avoir une appétence pour la logique, une compréhension de base de ce qu'est un algorithme, et la curiosité de comprendre la mécanique intime des mathématiques du calcul.

La démarche pédagogique suit un rythme immuable en cinq temps, inspiré des meilleures traditions de l'enseignement mathématique :
1. **L'intuition** : une métaphore, une image ou un problème concret pour saisir l'enjeu avant les formules.
2. **La définition** : la pose rigoureuse des objets mathématiques manipulés.
3. **L'énoncé** : le théorème ou la propriété, dépouillé de sa preuve pour en apprécier la portée.
4. **L'exemple** : l'application de l'énoncé sur un cas concret, souvent minimaliste, pour en vérifier la mécanique.
5. **L'exercice** : une invitation à manipuler vous-même les concepts, avec des indications pour débloquer la réflexion.

Les formules seront présentes, car le langage mathématique est irremplaçable pour exprimer la précision des coûts de traduction, mais elles seront toujours enrobées dans leur signification physique. Le lambda-calcul n'est pas qu'une syntaxe, c'est une algèbre de l'espace et du temps ; la machine de Turing n'est pas qu'un automate, c'est une géométrie de la mémoire.

### Cartographie de l'ouvrage

Le livre est structuré en quatre grandes parties, progressant des fondations vers les frontières de la complexité, pour aboutir à une synthèse programmatique.

#### Partie I — Fondations : deux langages du calcul
Avant de traduire, il faut comprendre les langues en présence.
Le **Chapitre 1** présente le lambda-calcul comme langage de la substitution. Nous y définirons les termes, les variables libres et liées, et la $\beta$-réduction, en nous appuyant sur la sémantique classique (Barendregt 1984).
Le **Chapitre 2** déploie les machines de Turing comme langage de la bande. Nous y formaliserons les états, les transitions et la notion de ruban infini.
Le **Chapitre 3** abordera la thèse de Church-Turing, non comme un théorème, mais comme un postulat épistémologique sur la nature du calcul effectif.
Le **Chapitre 4** traitera de l'équivalence extensionnelle historique.
*Bilan de la traduction historique (Turing 1937)* : Sens : $\lambda \leftrightarrow$ TM. Coût : non évaluable à l'époque, focalisé sur la terminaison. Conservé : la classe des fonctions récursives. Perdu : la notion même de ressource, absente du cadre de 1937. Statut : CONNU.

#### Partie II — Traduction des machines de Turing vers le lambda-calcul
Comment plier une géométrie linéaire (la bande) pour la faire entrer dans une algèbre arborescente (les lambda-termes) ?
Le **Chapitre 5** posera les bases de l'encodage des données : entiers de Church, booléens et listes.
Le **Chapitre 6** détaillera l'encodage complet d'une machine de Turing en un seul lambda-terme, en utilisant un point fixe pour simuler la boucle d'exécution.
Le **Chapitre 7** révélera le coût caché de cette opération : l'explosion de taille et la duplication des termes. Nous verrons comment la substitution aveugle du lambda-calcul force la copie de la bande entière à chaque étape.
Le **Chapitre 8** dressera le bilan de cette première direction.
*Bilan de la traduction (Chapitres 5 à 7)* : Sens : TM $\to$ $\lambda$. Coût : dilatation exponentielle de la taille et du temps due à la duplication de la bande lors de la substitution ; mémoire implicite mais non partagée. Conservé : la calculabilité et la terminaison. Perdu : l'accès en temps constant à une case mémoire et la compacité spatiale. Statut : CONNU.

#### Partie III — Traduction du lambda-calcul vers les machines de Turing
Le voyage de retour est tout aussi accidenté. Comment évaluer un programme fonctionnel sur une machine impérative et séquentielle ?
Le **Chapitre 9** explorera l'idée fondatrice de Landin (Landin 1964) et la naissance de la machine abstraite SECD, qui introduit la notion d'environnement pour retarder la substitution.
Le **Chapitre 10** se penchera sur la machine de Krivine (Krivine 2007), un modèle d'une élégance extrême pour l'appel par nom, utilisant une pile pour gérer les fermetures.
Le **Chapitre 11** est crucial : il aborde le coût de la $\beta$-réduction et le modèle de coût invariant. Longtemps, on a cru que la $\beta$-réduction était un modèle de coût irréaliste car une seule réduction pouvait dupliquer un terme de taille exponentielle. Les travaux d'Accattoli et Dal Lago (2016) ont prouvé que, sous certaines stratégies, la $\beta$-réduction est invariante par rapport aux machines de Turing.
Le **Chapitre 12** synthétisera ces acquis.
*Bilan de la traduction (Chapitres 9 à 11)* : Sens : $\lambda \to$ TM. Coût : mémoire linéaire pour la pile et l'environnement ; temps polynomial par rapport à la stratégie de réduction. Conservé : la sémantique d'évaluation (appel par nom ou par valeur). Perdu : la pureté mathématique du terme au profit d'une machinerie d'états. Statut : PROUVÉ (pour l'invariance de la stratégie leftmost-outermost).

#### Partie IV — Partage, optimalité et transfert vers le programme RTC
La dernière partie s'attaque à la ressource la plus subtile et la plus coûteuse à traduire : le partage.
Le **Chapitre 13** expliquera pourquoi le partage est une ressource perdue dans les traductions naïves. Le lambda-calcul syntaxique décrit des arbres, mais l'évaluation efficace nécessite des graphes.
Le **Chapitre 14** présentera la réduction optimale de Lamping (Lamping 1990), une tentative magistrale et complexe de préserver le partage à l'aide de fan-in et fan-out, en repoussant les limites de la duplication.
Le **Chapitre 15** élargira la perspective vers la complexité computationnelle. En nous appuyant sur les fondations de Hartmanis et Stearns (1965) et les synthèses modernes (Arora et Barak 2009), nous définirons ce qu'est une simulation raisonnable entre modèles et comment les classes de complexité (P, NP, PSPACE) survivent ou s'effondrent selon les ressources allouées.
Enfin, le **Chapitre 16**, intitulé **Transfert vers le programme RTC**, servira de conclusion programmatique. Le programme RTC (Traductions à Ressources et Calculabilité) est le cadre de recherche que ce tome appelle et structure. Nous y listerons les questions ouvertes, les ressources qui résistent encore à l'analyse, et les ponts qu'il reste à bâtir vers d'autres modèles (réseaux de preuve, calcul quantique, automates cellulaires).

### L'horizon du calcul

Pourquoi consacrer un livre entier à la mesure de ces coûts de traduction ? Parce que l'informatique n'est pas seulement la science de ce qui est calculable. C'est la science de ce qui est calculable *dans les limites de notre univers physique*.

Le temps et l'espace sont des contraintes impitoyables. Quand nous disons qu'un algorithme est polynomial, nous parlons une langue qui dépend intimement du modèle de calcul sous-jacent. Si la traduction d'une machine de Turing vers le lambda-calcul engendre une dilatation exponentielle de la taille, alors un algorithme polynomial sur machine de Turing pourrait devenir exponentiel en temps d'évaluation lambda si l'on n'y prend pas garde. C'est précisément pour résoudre ce paradoxe que la notion de modèle de coût invariant a été développée. Comprendre ces traductions, c'est comprendre la relativité du temps de calcul.

Au fil des pages, vous constaterez que le lambda-calcul et les machines de Turing sont comme deux facettes d'un même cristal. L'une reflète la composition, l'abstraction et la génération de structures fractales ; l'autre reflète la séquentialité, la mémoire localisée et l'usure du temps pas à pas. Les faire dialoguer exige de la précision, de l'humilité face à l'explosion combinatoire, et une attention de tous les instants aux ressources qui se dérobent.

Le registre des statuts sera votre boussole. Les sept ressources seront votre vocabulaire. Les traductions seront notre terrain d'expérimentation.

Il est temps à présent de laisser de côté les considérations historiques et philosophiques pour entrer dans la matière. Il est temps de définir les premiers symboles, de tracer les premières règles, et de comprendre comment l'acte même de substituer une variable par un terme contient, en germe, toute la complexité du monde computationnel.

Tournez la page, et entrons dans le lambda-calcul.

### Conventions de notation et typographie du calcul

Avant d'entrer dans le vif des définitions, il convient de fixer quelques conventions typographiques qui nous accompagneront tout au long des seize chapitres. Le lambda-calcul possède une syntaxe économe, presque austère, et la moindre ambiguïté de parenthèsage peut transformer un terme bien formé en une expression illisible. Voici les règles que j'adopte.

Les variables du lambda-calcul seront notées $x, y, z, u, v$, éventuellement indicées. L'application sera notée par simple juxtaposition : $M\, N$ signifie que le terme $M$ est appliqué au terme $N$. L'abstraction sera écrite $\lambda x.\, M$, avec un point séparant la variable liée du corps. La convention d'association à gauche pour l'application sera systématique : $M\, N\, P$ se lit $(M\, N)\, P$. L'abstraction, quant à elle, s'étend aussi loin à droite que possible : $\lambda x.\, M\, N$ se lit $\lambda x.\, (M\, N)$.

Pour les machines de Turing, je noterai une configuration instantanée sous la forme $q\, \alpha\, \underline{a}\, \beta$, où $q$ est l'état courant, $\alpha$ le contenu de la bande à gauche de la tête, $a$ le symbole lu, et $\beta$ le contenu à droite. Le soulignement marque la position de la tête de lecture. Les transitions seront écrites $\delta(q, a) = (q', b, D)$, où $D \in \{L, R\}$ indique la direction du déplacement.

Les ressources seront notées de manière uniforme. La taille d'un terme $M$ sera $|M|$, le temps d'une computation sera $T(n)$, l'espace sera $S(n)$, la profondeur sera $\mathrm{prof}(M)$, la largeur sera $\mathrm{larg}(M)$. Le partage sera quantifié par le nombre de nœuds distincts dans la représentation en graphe, noté $|\mathrm{graph}(M)|$, par opposition à la taille arborescente $|M|$.

Enfin, les traductions elles-mêmes recevront une notation fonctionnelle. La traduction d'une machine de Turing $\mathcal{M}$ vers le lambda-calcul sera notée $\llbracket \mathcal{M} \rrbracket_{\mathrm{TM} \to \lambda}$, et la traduction inverse d'un lambda-terme $M$ vers une machine de Turing sera $\llbracket M \rrbracket_{\lambda \to \mathrm{TM}}$. Le coût d'une traduction $\tau$ sera systématiquement résumé dans un tableau à sept entrées correspondant à nos sept ressources.

### Les exercices : votre atelier de traduction

Ce livre n'est pas un traité que l'on parcourt passivement. La compréhension profonde des traductions entre modèles de calcul exige de mettre les mains dans la syntaxe, de construire soi-même les encodages, de sentir sous ses doigts la résistance de la duplication ou la fluidité du partage. C'est pourquoi chaque chapitre se clôture par une série d'exercices gradués.

Les exercices marqués d'une étoile ($\star$) sont des vérifications directes : appliquer une définition, dérouler une réduction sur un petit exemple, confirmer qu'un encodage produit bien le résultat attendu. Ils sont accessibles dès la première lecture.

Les exercices marqués de deux étoiles ($\star\star$) demandent une construction : écrire l'encodage d'une machine à deux états, simuler trois étapes de la machine de Krivine sur un terme donné, estimer la taille d'un terme après $n$ substitutions. Ils nécessitent une feuille de papier et une bonne heure de concentration.

Les exercices marqués de trois étoiles ($\star\star\star$) sont des invitations à la recherche. Ils pointent vers des questions où les bornes exactes ne sont pas connues, où la conjecture rôde. Je les ai inclus non pas pour vous piéger, mais pour vous montrer que la frontière du savoir est proche, tangible, accessible à quiconque maîtrise les outils de base. Certains de ces exercices correspondent à des problèmes OUVERTS au sens du registre des statuts ; je le signalerai explicitement.

### Une dette intellectuelle

Ce livre n'aurait pas existé sans les travaux que je cite et auxquels je rends hommage à chaque page. La syntaxe et la sémantique du lambda-calcul que j'utilise sont celles que Barendregt a patiemment édifiées dans son traité de référence (Barendregt 1984). L'intuition fondatrice selon laquelle une machine peut évaluer mécaniquement une expression fonctionnelle remonte à Landin (1964) et à sa machine SECD, premier pont explicite entre l'abstraction lambda et l'exécution séquentielle. La machine de Krivine (Krivine 2007) offre une formalisation d'une pureté remarquable pour l'appel par nom, et c'est elle qui servira de fil conducteur à notre traduction $\lambda \to$ TM.

La question du coût de la $\beta$-réduction, longtemps considérée comme un obstacle insurmontable à toute comparaison raisonnable entre mod��les, a trouvé une résolution élégante dans les travaux d'Accattoli et Dal Lago (2016), qui ont établi que la stratégie leftmost-outermost constitue un modèle de coût invariant. Leur résultat, de statut CONNU dans notre registre, irrigue les chapitres 11 et 15.

La réduction optimale de Lamping (1990) représente quant à elle un sommet technique que nous aborderons avec humilité au chapitre 14. Lamping a montré qu'il est possible de réduire un lambda-terme en un nombre de pas proportionnel à la taille du résultat, à condition de gérer le partage par un mécanisme de jetons et de crochets. Cette prouesse algorithmique illustre parfaitement notre thèse : le partage est une ressource qui, si on la préserve, change radicalement le coût de la traduction.

Les fondations de la théorie de la complexité, posées par Hartmanis et Stearns (1965) et synthétisées avec clarté par Arora et Barak (2009), fournissent le cadre dans lequel nous évaluerons si une simulation est « raisonnable » ou non. Sans ces outils, la notion même de coût polynomial n'aurait pas de sens indépendant du modèle.

Enfin, les textes fondateurs de Church (1936), Turing (1936) et Turing (1937) restent la source première. C'est Turing qui, en 1937, a établi formellement l'équivalence entre $\lambda$-définissabilité et calculabilité par machine, fermant ainsi la boucle ouverte par Church un an plus tôt. Ce geste de 1937 est le point de départ de notre enquête ; tout le reste du livre en est, en un sens, le commentaire approfondi.

### Le seuil

Nous voici au seuil. Derrière cette porte, il n'y a plus de métaphores, plus de promesses, plus de survols. Il y a des termes, des règles, des réductions. Il y a une bande infinie et une tête qui se déplace. Il y a la substitution, cet acte apparemment anodin qui consiste à remplacer une variable par un terme, et qui contient en puissance toute la complexité computationnelle.

Je vous invite à lire ce livre comme on explore une carte ancienne : en acceptant que certaines zones soient encore vierges, en notant les distances avec soin, en sachant que le territoire résiste toujours un peu à la représentation. Les traductions entre le lambda-calcul et les machines de Turing sont un territoire vaste, accidenté, parfois contre-intuitif. Mais c'est précisément cette résistance qui les rend fascinantes.

Le premier chapitre commence maintenant. Nous allons définir, symbole par symbole, le langage de la substitution. Et vous verrez que dans la simplicité apparente de $\lambda x.\, x$, il y a déjà, en miniature, tout ce qui rendra nos traductions si coûteuses et si belles.