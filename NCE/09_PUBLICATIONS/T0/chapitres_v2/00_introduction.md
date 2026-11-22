## Introduction

### L'illusion de l'équivalence

Dans les années 1930, le monde des mathématiques et de la logique a été le théâtre d'une convergence intellectuelle sans précédent. Alonzo Church avec son lambda-calcul, Alan Turing avec ses machines automates, Kurt Gödel et Jacques Herbrand avec leurs fonctions récursives, Emil Post et Andreï Markov avec leurs systèmes de réécriture : tous cherchaient à capturer l'essence même de ce que signifie « calculer ». Lorsqu'il a été démontré que tous ces modèles, en apparence si dissemblables, définissaient exactement la même classe de fonctions, la communauté scientifique a cru avoir clos le chapitre. La thèse de Church-Turing était née. Elle affirmait, avec une robustesse que près d'un siècle de recherches n'a jamais démentie, que tout ce qui est intuitivement calculable peut être calculé par une machine de Turing, ou de manière équivalente, par n'importe quel autre de ces modèles formels.

Cette équivalence est l'un des plus grands triomphes de la pensée humaine. Mais elle est aussi, d'une certaine manière, un miroir déformant. En prouvant que les grands modèles de calcul sont équivalents au sens de la calculabilité, les pionniers ont résolu la question du « quoi » : si un problème peut être résolu dans un modèle, il peut l'être dans tous les autres. Cependant, cette équivalence existentielle et asymptotique a laissé dans l'ombre la question du « comment », et plus encore, celle du « à quel prix ».

Dire qu'une machine de Turing peut simuler un réseau de neurones, ou qu'un programme en lambda-calcul peut être compilé en un circuit booléen, est une vérité mathématique absolue. Mais cette vérité ne nous dit rien sur le coût de l'opération. Elle ne nous dit pas si la mémoire nécessaire explosera de manière exponentielle, si la profondeur du calcul deviendra insondable, ou si la structure parallèle de l'algorithme original sera irrémédiablement aplatie en une séquence linéaire et stérile. L'équivalence de calculabilité est un marteau conceptuel : elle écrase les différences subtiles entre les modèles pour ne conserver que le noyau dur de la computabilité. Or, pour quiconque s'intéresse à la nature profonde du calcul, à l'efficacité des algorithmes, ou à l'architecture physique des ordinateurs et des cerveaux, ces différences subtiles sont la seule chose qui importe.

### La thèse du programme RTC

C'est pour combler cette lacune qu'a été conçu le programme de recherche RTC. Ce livre, qui en constitue le Tome 0, pose les fondations d'une approche rigoureuse et systématique de ce que nous appelons les **traductions à ressources**.

La thèse centrale de cet ouvrage peut se résumer en une phrase : les grands modèles de calcul sont déjà équivalents au sens de la calculabilité ; la seule question ouverte et féconde est celle des ressources — taille, temps, mémoire, profondeur, largeur structurelle, précision des poids, partage — que chaque traduction entre modèles conserve, perd ou crée.

Nous ne cherchons pas à inventer un nouveau modèle de calcul. Nous ne cherchons pas à prouver que l'un d'entre eux est « meilleur » que les autres dans l'absolu. Notre ambition est à la fois plus modeste et, nous l'espérons, plus utile : fonder un programme de recherche rigoureux autour de la cartographie de ces traductions. Nous voulons comprendre ce qui se passe dans l'espace interstitiel entre les modèles. Quand vous traduisez un algorithme de lambda-calcul vers un circuit booléen, que perdez-vous ? Quand vous encodez un problème de satisfaction de contraintes (SAT) pour le soumettre à un réseau neuronal, quelle structure géométrique est détruite ? Ce tome présente les premiers résultats démontrés de notre programme, ainsi que ses premiers échecs, sans jamais confondre intuition, conjecture et théorème.

### Qu'est-ce qu'une traduction à ressources ?

Pour que le lecteur saisisse immédiatement la nature de notre démarche, appliquons dès maintenant la méthode pédagogique qui structurera l'ensemble de ce livre : l'intuition d'abord, puis la définition, puis l'énoncé, et enfin l'exemple.

**Intuition.** Imaginez que vous deviez traduire un poème complexe d'une langue à une autre. Vous parvenez à préserver le sens global de l'œuvre (c'est l'équivalence de calculabilité). Mais pour y parvenir, vous êtes obligé d'ajouter de longues notes de bas de page, de détruire le rythme des vers, et de remplacer des métaphores culturellement denses par des descriptions littérales de plusieurs paragraphes. Le sens est conservé, mais les *ressources* de l'œuvre — sa concision, sa musicalité, sa profondeur implicite — ont été radicalement altérées. En informatique, traduire un programme d'un modèle à l'autre obéit à la même logique : le résultat du calcul est identique, mais l'empreinte structurelle de ce calcul subit des transformations drastiques.

**Définition.** Soient $M$ et $M'$ deux modèles de calcul. Une traduction $T$ de $M$ vers $M'$ est une fonction qui associe à tout programme $x \in M$ un programme $T(x) \in M'$ calculant la même fonction. Nous disons que cette traduction est $(f,g)$-bornée si la taille de la sortie est contrôlée par une fonction $f$ de la taille de l'entrée, c'est-à-dire $|T(x)| \le f(|x|)$, et si chaque ressource suivie $\rho$ vérifie une contrainte similaire $\rho'(T(x)) \le g(\rho(x))$, où $\rho$ et $\rho'$ désignent la mesure de la ressource dans les modèles respectifs.

**Énoncé.** Une ressource est dite *préservée à facteur $c$* si $\rho'(T(x)) \le c \cdot \rho(x) + O(1)$. Elle est dite *détruite* si elle peut rester bornée dans un sens de la traduction, mais exploser (par exemple, croître exponentiellement) dans l'autre sens, rendant la traduction inverse structurellement impossible sans un coût prohibitif.

**Exemple.** Prenons la traduction du lambda-calcul vers les machines de Turing. Le lambda-calcul permet le *partage* de termes (via des liaisons ou *let-bindings*), ce qui permet de représenter des structures de données immenses avec une très petite empreinte syntaxique. Si la traduction vers une machine de Turing se fait par substitution naïve (copie du terme à chaque utilisation), la ressource « taille du programme » est détruite : un terme de taille $n$ peut produire une machine de Turing de taille $2^n$. La calculabilité est sauve, mais la ressource mémoire est sacrifiée.

### Le registre des statuts : une méthode contre l'enthousiasme

Le domaine de l'informatique théorique, et plus encore celui de l'intelligence artificielle et de l'apprentissage automatique, est régulièrement secoué par des annonces prématurées, des généralisations abusives et des intuitions présentées comme des lois fondamentales. Un algorithme qui résout rapidement une instance particulière d'un problème est trop souvent présenté comme la preuve qu'une classe entière de complexité a été vaincue.

Pour nous prémunir contre ces découvertes fictives et maintenir une honnêteté intellectuelle absolue, chaque affirmation de ce livre porte un statut explicite, tiré de notre registre interne :

*   **PROUVÉ** : La preuve mathématique complète et vérifiable est donnée dans le texte ou en annexe.
*   **CONNU** : Le résultat est déjà publié et accepté par la communauté scientifique ; nous le rappelons pour les besoins de notre cadre conceptuel.
*   **EXPÉRIMENTAL** : Le phénomène a été mesuré de manière reproductible sur un ensemble de données ou d'instances précis, mais il n'a pas de valeur universelle.
*   **CONJECTURE** : Une hypothèse forte, soutenue par des indices théoriques ou expérimentaux, mais qui résiste encore à la démonstration formelle.
*   **RÉFUTÉ** : Une intuition répandue ou une hypothèse précédente que nos travaux ou ceux de la littérature ont démontrée comme fausse.
*   **OUVERT** : Une question fondamentale pour laquelle nous n'avons ni preuve, ni réfutation, ni même de conjecture solide, et qui constitue une direction de recherche pour l'avenir du programme RTC.

Les résultats présentés dans ce tome sont modestes. Nous ne prétendons pas avoir révolutionné la théorie de la complexité. Nous prétendons seulement avoir nettoyé un petit coin de la fenêtre à travers laquelle nous observons les modèles de calcul, et avoir fourni les outils pour que d'autres puissent faire de même.

### Avertissement sur la notion de « ressources »

Le terme « ressources » est central dans cet ouvrage et dans le programme RTC. Il est toutefois nécessaire de lever toute ambiguïté sémantique dès ces premières pages : les ressources dont il est question ici sont exclusivement computationnelles et structurelles (temps de calcul, espace mémoire, largeur d'un circuit, profondeur d'un graphe, précision des poids synaptiques). Bien que l'optimisation de ces ressources algorithmiques ait des répercussions économiques majeures dans l'industrie technologique et la finance quantitative, ce contenu est strictement informatif, théorique et mathématique. Il ne constitue en aucun cas un conseil financier personnalisé, une recommandation d'investissement dans des entreprises technologiques, ni une promesse de rendement économique. L'analyse des coûts dont nous parlons est mesurée en bits, en portes logiques et en cycles d'horloge, jamais en devises.

### À qui s'adresse ce livre

Ce livre a été écrit pour un lecteur cultivé non spécialiste. Vous n'avez pas besoin d'être chercheur en théorie de la complexité pour le lire, mais vous devez posséder une certaine familiarité avec le raisonnement formel et l'abstraction mathématique.

Il s'adresse à l'ingénieur qui conçoit des architectures matérielles et qui se demande pourquoi certaines fonctions logiques sont si coûteuses à câbler ; au chercheur en neurosciences computationnelles qui cherche à comprendre ce qui distingue fondamentalement un cerveau biologique d'un réseau de neurones artificiel ; au philosophe des sciences qui s'interroge sur la nature de l'information et de sa transformation ; et, bien sûr, à l'étudiant en informatique qui souhaite voir au-delà des recettes algorithmiques pour contempler la géométrie profonde du calcul.

Notre engagement envers ce lecteur est la clarté. Nous suivrons invariablement la règle en quatre temps évoquée plus haut : nous partirons toujours d'une intuition tangible, nous la formaliserons par une définition rigoureuse, nous en tirerons un énoncé ou un lemme, et nous l'ancrerons dans la réalité par un exemple concret. Les formules mathématiques, écrites en LaTeX, ne sont pas là pour intimider, mais pour servir de squelette à la pensée.

### Plan de l'ouvrage

Pour guider le lecteur dans cette exploration, l'ouvrage est structuré en quatre parties, progressant de la remise en contexte historique et conceptuelle jusqu'aux résultats spécifiques de notre programme, avant d'esquisser l'avenir.

#### Partie I — La question
Cette première partie plante le décor et déconstruit les idées reçues.
Le **Chapitre 1 (Quatre manières de calculer)** présente les grands paradigmes que nous étudierons : le lambda-calcul (la fonction et la substitution), les machines de Turing (le temps séquentiel et la mémoire), les circuits booléens (l'espace, la profondeur et la largeur) et les réseaux neuronaux (l'approximation continue et les poids).
Le **Chapitre 2 (L'équivalence est déjà démontrée)** explique pourquoi la question de la calculabilité est close et pourquoi s'y attarder encore est une perte de temps pour qui cherche à comprendre la mécanique fine du calcul.
Le **Chapitre 3 (SAT n'est pas un modèle de calcul)** s'attaque à une confusion fréquente. Le problème de la satisfaisabilité booléenne (SAT) est un problème, pas un modèle. Pourtant, les solveurs SAT agissent comme un pivot universel de l'ingénierie moderne. Nous clarifierons ce statut hybride.
Enfin, le **Chapitre 4 (Les limites que personne ne franchit)** rappelle les barrières infranchissables de l'indécidabilité et de la complexité, qui s'appliquent à tous les modèles, quelle que soit l'élégance de la traduction.

#### Partie II — Le cadre
Ici, nous forgeons les outils du programme RTC.
Le **Chapitre 5 (Qu'est-ce qu'une traduction à ressources ?)** développe formellement le cadre des traductions $(f,g)$-bornées.
Le **Chapitre 6 (Les ressources du calcul)** établit une taxonomie précise des ressources : quelles sont-elles, comment les mesure-t-on, et pourquoi des notions comme la « largeur » ou le « partage » sont-elles aussi importantes que le temps et l'espace ?
Le **Chapitre 7 (La carte des traductions connues)** dresse un état de l'art de ce que la littérature scientifique a déjà établi, en pointant les zones d'ombre.
Le **Chapitre 8 (Une méthode contre les découvertes fictives)** expose notre épistémologie interne : comment éviter les biais de mesure, les illusions d'optique algorithmiques et les généralisations hâtives.

#### Partie III — Premiers résultats : la largeur
C'est le cœur technique et inédit de ce tome. Nous nous concentrons sur une ressource spécifique, souvent négligée au profit du temps et de la mémoire, mais qui s'avère être le véritable goulot d'étranglement des traductions modernes : la largeur structurelle d'un calcul.
Le **Chapitre 9 (La largeur d'un calcul)** définit ce concept, de la largeur d'arbre (*treewidth*) à la largeur d'un circuit ou d'un réseau.
Le **Chapitre 10 (Ce que Cook-Levin conserve)** analyse la réduction fondatrice de la théorie de la NP-complétude. Nous montrons ce qui survit et ce qui est perdu lorsqu'on réduit un calcul non déterministe à une formule booléenne.
Le **Chapitre 11 (Tseitin préserve la largeur)** examine la transformation qui permet de convertir n'importe quel circuit en forme normale conjonctive (CNF) sans explosion exponentielle de la taille, et nous démontrons dans quelles conditions exactes elle préserve la largeur structurelle.
Le **Chapitre 12 (Du circuit au neurone)** aborde la traduction la plus fascinante et la plus mal comprise : comment encoder une logique discrète et symbolique dans les poids continus d'un réseau de neurones, et quelle largeur cachée cela impose-t-il au réseau ?
Le **Chapitre 13 (La largeur prédit-elle la difficulté ?)** confronte nos mesures à la réalité empirique. Une grande largeur structurelle est-elle toujours le signe d'un calcul difficile ?
Le **Chapitre 14 (Quand l'outil de mesure ment)** explore les limites de nos propres outils. Les heuristiques des solveurs SAT et les métriques de complexité nous induisent parfois en erreur sur la véritable nature de l'instance traitée.
Le **Chapitre 15 (L'apprentissage oublie la structure)** conclut cette partie par une observation fondamentale sur les réseaux neuronaux : en apprenant à approximer une fonction, l'apprentissage profond tend à détruire la structure symbolique et la largeur du calcul original, le remplaçant par une interpolation statistique massive.

#### Partie IV — La suite du programme
Le **Chapitre 16 (La bibliothèque à venir)** esquisse les directions futures du programme RTC. Nous y détaillons les traductions qui restent à explorer, les ressources que nous ne savons pas encore mesurer, et la construction progressive d'une bibliothèque ouverte de traductions à ressources bornées, qui servira de socle aux tomes suivants.

### Le point de départ

L'étude du calcul a longtemps été obsédée par l'universalité. Nous avons voulu des machines capables de tout calculer, des langages capables de tout exprimer. Cette quête est accomplie. L'ordinateur sur lequel vous lisez ces mots, le serveur qui a peut-être aidé à les formater, et le réseau neuronal qui pourrait un jour en analyser la sémantique, sont tous, au fond, la même machine de Turing.

Mais savoir que deux chemins mènent au même sommet ne nous dit pas lequel est une promenade et lequel est une escalade mortelle. Il est temps d'arrêter de contempler l'universalité pour commencer à mesurer le paysage. Il est temps de parler de ressources.

Tournons la page, et entrons dans le vif du calcul.