## Introduction — Compter deux fois

### Une réduction n'est jamais gratuite

On dit couramment : « on réduit le problème à SAT ». Le verbe est commode, et il est trompeur. Il suggère un déplacement sans frais, comme si l'on changeait simplement de notation pour poser la même question dans une autre écriture. Or une traduction est un calcul. Elle prend du temps, produit de la matière, introduit des objets qui n'existaient pas dans le problème source, et détruit parfois de l'information que l'on croyait accessoire. Réduire, c'est payer.

Ce volume part d'un constat de comptabilité. Lorsqu'un problème est formulé comme un circuit booléen, toutes les ressources du calcul se lisent sur le même objet : le nombre de portes, la longueur du plus long chemin, l'épaisseur des étages, la réutilisation des résultats intermédiaires. Lorsqu'on traduit ce circuit vers une formule en forme normale conjonctive — l'entrée des solveurs SAT — ces ressources sont payées une seconde fois, et pas nécessairement dans la même monnaie. Certaines se conservent à un facteur près. Certaines se perdent. Certaines n'ont plus de correspondant dans le langage cible et doivent être redéfinies pour rester mesurables.

La thèse que je défends ici est méthodologique, et je le dis d'emblée pour éviter tout malentendu : ce livre n'annonce aucune découverte. Il soutient qu'une traduction entre modèles de calcul ne devrait jamais être publiée sans deux documents annexes. Le premier est un **contrat de fidélité** : que garantit-on sur les solutions — équivalence, équisatisfiabilité, préservation des modèles ? Le second est une **fiche de ressources** : que devient chaque budget — taille, temps, mémoire, profondeur, largeur, précision, partage ? Le reste est de la littérature utile, mais incomplète.

Ce programme, que j'appelle RTC, s'inscrit dans la collection « Les Traductions du Calcul ». Le présent tome en est le cas d'étude le plus concret : le triangle circuits / formes normales / solveurs, avec une illustration centrale démontrée intégralement, le lemme L-01 sur la largeur arborescente.

### Le circuit, objet pivot

Un circuit booléen est un graphe orienté acyclique dont les sources sont des variables ou des constantes, dont les nœuds internes sont des portes ($\wedge$, $\vee$, $\neg$, parfois $\oplus$), et dont un nœud distinguished est la sortie. Quatre nombres s'y lisent immédiatement :

- la **taille** : le nombre de portes ;
- la **profondeur** : la longueur du plus long chemin d'une entrée à la sortie ;
- la **largeur** : le nombre maximal de portes sur un même étage, quand on organise le circuit en niveaux ;
- le **partage** : le degré de réutilisation, c'est-à-dire le fait qu'une porte puisse alimenter plusieurs portes aval.

Attention au mot « largeur » : il désignera dans ce livre trois choses différentes, et cette polysémie est une source constante de confusion. Largeur d'un circuit (épaisseur d'un étage), largeur d'une clause (nombre de littéraux), largeur arborescente (ressemblance d'un graphe à un arbre). Le chapitre 4 fixe le vocabulaire, le chapitre 7 s'occupe de la deuxième, le chapitre 13 de la troisième.

Un exemple, élémentaire, pour sentir que ces ressources sont indépendantes. La parité $x_1 \oplus x_2 \oplus \cdots \oplus x_n$ se calcule par une chaîne de $n-1$ portes $\oplus$, de profondeur $n-1$ ; ou par un arbre équilibré, de même taille $n-1$, mais de profondeur $\lceil \log_2 n \rceil$. Même taille, profondeurs radicalement différentes (calcul immédiat ; PROUVÉ au chapitre 4 sous forme d'énoncé général).

Le partage, lui, est la ressource la plus discrète et la plus décisive. Les $n$ parités préfixes $p_i = x_1 \oplus \cdots \oplus x_i$ se calculent avec $n-1$ portes si l'on réutilise $p_{i-1}$ pour produire $p_i$. Si l'on interdit le partage et que l'on recopie un arbre par sortie, on écrit $\sum_{i=1}^{n} (i-1) = n(n-1)/2$ portes. Le même résultat, deux factures. Une formule — un arbre — n'a pas de mécanisme de partage ; une CNF non plus. C'est exactement pour cette raison que l'encodage de Tseitin, qui consiste à *nommer les fils*, est autre chose qu'un détail technique : il réintroduit dans un langage sans partage la possibilité de désigner un résultat intermédiaire.

### Trois contrats de fidélité

Fixons le vocabulaire, car toute la méthode repose sur ces distinctions.

Soit $F$ une formule sur un ensemble de variables $X$, et $G$ une formule sur un ensemble $Y \supseteq X$.

1. **Équivalence** : $X = Y$ et $F$, $G$ ont exactement les mêmes modèles.
2. **Préservation des modèles par extension unique** : toute affectation de $X$ satisfaisant $F$ se prolonge en exactement une affectation de $Y$ satisfaisant $G$, et réciproquement toute affectation satisfaisant $G$ restreinte à $X$ satisfait $F$. La projection est une bijection entre modèles.
3. **Équisatisfiabilité** : $F$ est satisfaisable si et seulement si $G$ l'est. Rien de plus.

Ces contrats sont de force décroissante, et le troisième est presque vide. L'affirmation « l'équisatisfiabilité suffit dès qu'on veut compter ou énumérer les solutions » est **RÉFUTÉ** : sur $X = \{x,y\}$, les formules $F = (x \vee y)$ et $G = (x)$ sont toutes deux satisfaisables, mais $F$ a trois modèles et $G$ en a deux. Un solveur qui répond « SAT » ne distingue pas les deux situations ; un compteur, si.

Le choix du contrat n'est donc pas cosmétique : il détermine ce qu'on a le droit de faire du résultat. C'est le premier item de toute fiche de traduction, et je le répéterai dans chacun des seize chapitres.

### Une porte, et trois lignes de preuve

Entrons en matière par le plus petit calcul possible, pour que le lecteur voie immédiatement le niveau d'exigence du livre. Prenons une porte $g = a \wedge b$. Son encodage de Tseitin est la CNF à trois clauses
$$T = (\neg g \vee a) \wedge (\neg g \vee b) \wedge (g \vee \neg a \vee \neg b).$$

**Énoncé.** Les modèles de $T$ sont exactement les affectations de $(a,b,g)$ vérifiant $g = a \wedge b$. En particulier, chacune des quatre affectations de $(a,b)$ se prolonge en exactement un modèle de $T$. **Statut : PROUVÉ** (cas élémentaire du théorème général démontré au chapitre 5).

**Preuve.** Soit une affectation satisfaisant $T$. Si $g = 1$, les clauses $(\neg g \vee a)$ et $(\neg g \vee b)$ imposent $a = 1$ et $b = 1$, donc $g = a \wedge b$. Si $g = 0$, la clause $(g \vee \neg a \vee \neg b)$ impose $a = 0$ ou $b = 0$, donc $a \wedge b = 0 = g$. Réciproquement, si $g = a \wedge b$, les trois clauses sont satisfaites : les deux premières parce que $g=1$ entraîne $a=b=1$, la troisième parce que $g=0$ entraîne qu'un des deux littéraux $\neg a, \neg b$ vaut $1$. L'existence et l'unicité de l'extension follows : pour $(a,b)$ fixé, la valeur de $g$ est déterminée. $\square$

Trois lignes, aucune intuition déguisée en argument. Le chapitre 5 obtient le cas général par composition de ces extensions, porte après porte, dans un ordre topologique : c'est le même raisonnement, itéré.

### Le prix de la forme normale

Voici maintenant le contrepoint, et la première vraie facture. Une CNF est une conjonction de clauses ; une DNF une disjonction de termes. Convertir sans introduire de variables nouvelles peut coûter exponentiellement cher, et la parité le montre de la manière la plus nette.

**Énoncé.** Toute CNF équivalente à $x_1 \oplus \cdots \oplus x_n$ sur les seules variables $x_1,\dots,x_n$ contient exactement $2^{n-1}$ clauses, et chacune mentionne les $n$ variables. **Statut : PROUVÉ** (chapitre 3, borne de normalisation pour la parité).

**Preuve.** Une clause non satisfaite par une affectation exclut un sous-cube : si elle omet la variable $x_i$, elle est falsifiée par deux affectations ne différant que sur $x_i$. Or deux affectations qui diffèrent sur une seule coordonnée ont des parités opposées ; elles ne peuvent donc pas être toutes deux falsifiantes pour la parité. Aucune clause d'une CNF équivalente à la parité n'omet de variable : chacune est pleine et exclut exactement une affectation. Comme la parité est fausse sur exactement $2^{n-1}$ affectations, il faut et il suffit de $2^{n-1}$ telles clauses. $\square$

Le même argument vaut pour la DNF, par symétrie. Comparons alors les deux traductions disponibles pour un circuit de parité :

- normalisation **sans** variables nouvelles, contrat d'**équivalence**, taille $2^{n-1}$ ;
- encodage **avec** variables nouvelles, contrat d'**extension unique**, taille linéaire.

On n'achète pas la même chose. La deuxième traduction est linéaire *parce qu'elle accepte un contrat plus faible*. Voilà, en miniature, toute la thèse du livre : le prix d'une traduction est indexé sur le contrat de fidélité qu'elle signe.

### Nommer les fils : la fiche de ressources de Tseitin

L'encodage que l'on appelle aujourd'hui encodage de Tseitin, d'après le travail de Tseitin 1968, associe à chaque porte une variable fraîche et écrit la contrainte qui lie cette variable à ses entrées. Dressons sa fiche, telle qu'elle sera établie puis utilisée.

**Taille.** Une porte de degré d'entrée $j \le k$ donne exactement $2^j$ clauses pleines de longueur $j+1$ : une par affectation falsifiante de sa table de vérité. La taille est donc conservée à un facteur dépendant uniquement de $k$ (PROUVÉ, chapitre 5). Pour les portes usuelles, on remplace ce bloc par des jeux de $j+1$ clauses, équivalents et plus courts.

**Modèles.** Conservés par extension unique (PROUVÉ, chapitre 5, théorème général dont la preuve élémentaire est donnée plus haut).

**Partage.** Rendu exprimable : c'est le rôle même des variables de nommage. Une CNF ne sait pas réutiliser un sous-calcul ; elle sait réutiliser un *nom*.

**Profondeur.** Ici, une perte de nature différente : la CNF n'a pas de profondeur. La ressource n'a pas d'image directe dans le langage cible. Il faut la transporter indirectement — par la structure du graphe primal, par la profondeur des preuves de résolution — ou renoncer à la suivre. Le chapitre 8 est consacré à ce phénomène, que j'appelle *ressource sans correspondant*.

**Brièveté des preuves.** Non garantie. Les bornes inférieures connues en théorie de la preuve montrent que de petites formules peuvent exiger de très longues réfutations ; les tautologies issues de parités sur graphes, dans le travail de Tseitin 1968, fournissent les premières familles difficiles pour la résolution régulière (CONNU ; idée de preuve annoncée comme telle au chapitre 10, panorama dans Biere, Heule, van Maaren et Walsh 2009).

**Facilité pratique.** Non garantie, et non réductible à une propriété de l'encodage seul : le comportement des solveurs est un constat de mesure (EXPÉRIMENTAL), toujours accompagné dans ce volume de son protocole et de ses limites.

### Le lemme L-01, annoncé

La largeur arborescente mesure à quel point un graphe ressemble à un arbre. On découpe le graphe en *sacs* de sommets, organisés en arbre, de sorte que chaque arête tienne dans un sac et que les sacs contenant un sommet donné forment une partie connexe de l'arbre ; la largeur est la taille du plus grand sac moins un. Un arbre a largeur $1$ ; une clique sur $n$ sommets, largeur $n-1$.

Cette ressource est algorithmiquement précieuse : par programmation dynamique sur les sacs, on décide la satisfiabilité d'une CNF dont le graphe primal a largeur $w$ en temps $2^{O(w)} \cdot \mathrm{poly}(n+m)$ (PROUVÉ, chapitre 13, algorithme et analyse complets).

Le graphe primal d'une CNF a pour sommets les variables, deux variables étant reliées si elles apparaissent ensemble dans une clause. La question RTC est alors immédiate : l'encodage de Tseitin, qui ajoute des variables et des clauses, abîme-t-il cette structure ?

**Lemme L-01.** Soit $C$ un circuit dont chaque porte a au plus $k$ entrées, et soit $w$ la largeur arborescente du graphe non orienté sous-jacent à $C$. Alors le graphe primal de la CNF de Tseitin de $C$ a largeur arborescente au plus
$$(k+1)(w+1)-1.$$
**Statut : PROUVÉ** (chapitre 13, preuve intégrale).

L'idée — et je souligne qu'il s'agit ici d'une idée, la preuve complète occupant le chapitre 13 — est de partir d'une décomposition arborescente du circuit et de remplacer, dans chaque sac, chaque sommet par le petit paquet de variables CNF qui le concernent : lui-même et les noms des portes incidentes, au plus $k+1$ variables par sommet. Un sac de taille au plus $w+1$ devient un sac de taille au plus $(k+1)(w+1)$, et l'on vérifie que les deux conditions de décomposition survivent à cette substitution.

L-01 n'est pas une découverte : c'est un lemme structurel élémentaire du programme RTC, démontré pour être utilisé. Ce qu'il dit est modeste et utile : la structure est conservée à un facteur $k+1$ près. Ce qu'il ne dit pas est tout aussi important : il ne promet rien sur le temps que mettra un solveur CDCL sur cette instance. Le lien entre largeur bornée et comportement pratique des solveurs reste, à ma connaissance, une question à formuler proprement (OUVERT, chapitre 16).

### Le registre des statuts

Chaque affirmation de ce livre porte une étiquette. Ce n'est pas une coquetterie de style : c'est l'instrument central de la méthode, et la seule manière que je connaisse d'écrire sur SAT sans mélanger ce qui est démontré, ce qui est mesuré et ce qui est espéré.

- **PROUVÉ** : la preuve complète est imprimée dans le volume. Exemples : le lemme L-01, la borne de normalisation pour la parité, l'équisatisfiabilité et l'extension unique pour Tseitin, la correction de la propagation unitaire, le fait qu'une clause apprise est une résolvante, l'algorithme de programmation dynamique sur les sacs.
- **CONNU** : résultat établi ailleurs, énoncé avec son idée de preuve, explicitement annoncée comme idée. Exemples : la NP-complétude de SAT (Cook 1971 ; Levin 1973), dont l'idée est de décrire le tableau de calcul d'une machine par une formule ; les bornes inférieures de résolution ; la simulation de la résolution par CDCL avec redémarrages (Pipatsrisawat et Darwiche 2011) ; l'algorithme randomisé de Schöning 1999 pour $k$-SAT, en $(4/3)^n$ pour $k=3$ à facteurs polynomiaux près ; les encadrements du seuil aléatoire.
- **EXPÉRIMENTAL** : constat de mesure, avec protocole et limites. Exemple : le pic de difficulté observé autour d'un ratio clauses/variables voisin de $4{,}26$ pour le 3-SAT aléatoire uniforme — une mesure sur des tailles accessibles, non un théorème (chapitre 14).
- **CONJECTURE** : hypothèse de travail. L'hypothèse ETH et sa version forte SETH, dans le cadre de Impagliazzo et Paturi 2001 ; la conjecture du seuil pour le 3-SAT aléatoire.
- **RÉFUTÉ** : affirmation fausse, avec contre-exemple explicite. Exemple : « la propagation unitaire décide la satisfiabilité ». Contre-exemple : $(x \vee y) \wedge (\neg x \vee \neg y)$ est satisfaisable, $(x\vee y)\wedge(\neg x \vee y)\wedge(x \vee \neg y)\wedge(\neg x \vee \neg y)$ est insatisfaisable, et aucune des deux ne contient de clause unitaire : la propagation n'y fait rien.
- **OUVERT** : question non résolue, formulée assez précisément pour être transmise. Exemple : $P = NP$ ? Exemple plus modeste, propre au programme : peut-on remplacer le facteur $k+1$ de L-01 par une constante indépendante du degré d'entrée, sous des hypothèses structurelles raisonnables ?

Ce registre a une conséquence de lecture : lorsqu'un chapitre dit CONNU, il ne démontre pas ; il explique l'idée et renvoie. Lorsqu'il dit PROUVÉ, il démontre, et le lecteur est en droit d'exiger la preuve entière.

### Ce que ce volume ne promet pas

Je ne promets pas de rendre les solveurs rapides. Je ne promets aucun algorithme sous-exponentiel : sous ETH, un tel algorithme pour 3-SAT est exclu, mais ETH est une conjecture, et son statut ne se transfère pas magiquement en théorème (CONJECTURE). Je ne promets pas davantage qu'un encodage « bien structuré » sera bien traité en pratique : c'est une question de mesure, et la mesure est capricieuse (EXPÉRIMENTAL).

Je promets l'inverse d'une promesse de performance : une grille de lecture. À la fin du volume, le lecteur saura poser trois questions devant n'importe quelle traduction — quel contrat ? quelle fiche ? quel statut ? — et saura reconnaître les endroits où la littérature répond, et ceux où elle se tait. Environ deux cent vingt pages, quatre parties, seize chapitres, un même rythme : intuition, définition, énoncé statué, exemple, exercices.

### À qui je m'adresse

Je m'adresse à un lecteur cultivé non spécialiste. Il faut savoir ce qu'est une fonction, un ensemble, une récurrence, et accepter de lire une formule avec des $\wedge$ et des $\neg$. Il ne faut aucune familiarité préalable avec la théorie de la complexité, la théorie de la preuve ou les solveurs SAT : tout est défini au moment où c'est utilisé.

Trois publics, en pratique. L'étudiant qui veut comprendre pourquoi SAT est à la fois un problème « difficile » et un outil industriel qui fonctionne. L'ingénieur qui encode des contraintes — planification, vérification, configuration — et souhaite savoir ce que son encodage lui coûte, plutôt que de le découvrir en production. Le lecteur curieux de la notion de ressource, qui trouvera ici un cas où l'on peut *compter* au lieu de gloser.

On peut lire ce livre à trois profondeurs : les intuitions et les énoncés ; les exemples et les fiches ; les preuves et les exercices. Les chapitres 1, 8 et 16 forment l'ossature méthodologique ; les chapitres 5 et 13 en sont le cœur technique ; les chapitres 11, 12, 14 et 15 en sont la partie la plus proche des machines réelles.

### Le plan, partie par partie

**Partie I — Objets et budgets.** Le chapitre 1 installe le cadre : ressources, traductions, statuts. Le chapitre 2 fixe syntaxe, sémantique et problèmes de décision (SAT, TAUT, conséquence). Le chapitre 3 mesure le prix de la normalisation, avec la borne de parité démontrée plus haut. Le chapitre 4 définit les circuits et leurs quatre budgets, en s'appuyant sur le paysage des bornes inférieures (CONNU ; Jukna 2012).

**Partie II — Traduire vers SAT.** Le chapitre 5 démontre l'encodage de Tseitin : nommer les fils, contrat d'extension unique, fiche de taille. Le chapitre 6 expose Cook–Levin (CONNU ; Cook 1971 ; Levin 1973) : la machine comme tableau, le tableau comme formule, avec l'idée de la preuve et le coût du tableau. Le chapitre 7 borne la largeur des clauses et passe à 3-SAT, en distinguant soigneusement ce que la réduction garantit de ce qu'elle ne garantit pas. Le chapitre 8 dresse l'anatomie d'une traduction et le registre des ressources conservées, perdues, ou sans correspondant.

**Partie III — Raisonner.** Le chapitre 9 présente la résolution : une règle, des preuves, une géométrie. Le chapitre 10 examine les familles difficiles — tiroirs, parités sur graphes — et la longueur des preuves (CONNU pour les bornes inférieures ; Tseitin 1968 ; panorama dans Biere, Heule, van Maaren et Walsh 2009). Le chapitre 11 démonte DPLL, depuis les procédures de Davis et Putnam 1960 et Davis, Logemann et Loveland 1962, avec correction de la propagation unitaire démontrée. Le chapitre 12 passe à CDCL : apprentissage de clauses, retours arrière non chronologiques (Marques-Silva et Sakallah 1999), preuve que toute clause apprise est une résolvante (PROUVÉ), et simulation de la résolution (CONNU ; Pipatsrisawat et Darwiche 2011).

**Partie IV — Structures, hasard, applications, transfert.** Le chapitre 13 définit la largeur arborescente, démontre L-01 et l'algorithme sur les sacs. Le chapitre 14 traite le 3-SAT aléatoire : transition de phase, encadrements connus (CONNU), conjecture du seuil (CONJECTURE), difficulté typique mesurée (EXPÉRIMENTAL). Le chapitre 15 encode le réel : planification en