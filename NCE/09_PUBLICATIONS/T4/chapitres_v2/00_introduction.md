## Introduction — La comptabilité des machines

### Une phrase, et pas une image

Un réseau de neurones, vu de près, tient dans une phrase : des nombres entrent, chaque unité forme une somme pondérée de ce qu'elle reçoit, compare cette somme à un seuil ou lui applique une fonction très simple, puis transmet le résultat à d'autres unités. Il n'y a rien d'autre. Pas de mystère, pas de fluide, pas d'étincelle : des portes, des couches, des boucles, des nombres.

Ce livre part de cette phrase et la prend au sérieux. Si un réseau est une machine, alors on peut tenir sa comptabilité comme on tient celle d'un circuit logique ou d'une machine de Turing : compter les unités, les étapes, les bits gardés en mémoire, les couches, les unités par couche, les bits des nombres, et la réutilisation des calculs intermédiaires. Sept colonnes, pas une de plus, pas une de moins. Et une question qui revient à chaque page : quand on traduit un modèle de calcul dans un autre, quelles colonnes restent identiques, lesquelles grossissent, lesquelles se vident — et où passe la différence ?

Car c'est là ma thèse. Une traduction entre modèles n'est jamais gratuite, et elle n'est jamais non plus un simple mur. Elle conserve certaines ressources, en perd ou en déplace d'autres. Le booléen vers le neurone à seuil est presque gratuit. Le graphe partagé vers l'arbre peut coûter un facteur exponentiel. La boucle vers le circuit sans boucle échange de la mémoire contre de la profondeur. Le seuil vers la fonction continue échange de la netteté contre de la précision numérique. Et le pivot de tous ces échanges, la monnaie dans laquelle les autres dettes finissent par être payées, c'est la précision des nombres : poids, seuils, activations.

### Le point de départ n'est pas une provocation

Lire les neurones comme des machines n'est pas une réaction récente contre une métaphore envahissante. C'est le point de départ historique. Le travail de McCulloch et Pitts 1943 est un calcul logique : des unités tout-ou-rien, des entrées excitatrices et inhibitrices, des seuils, et la question de savoir quelles propositions un tel assemblage peut calculer (CONNU). Rosenblatt 1958 introduit le perceptron comme une machine qui apprend ses poids, avec un théorème de convergence lorsque la séparation existe (CONNU). Minsky et Papert 1969 examinent ce qu'une seule couche de ce type ne peut pas calculer, et le font par des arguments de géométrie et de comptage, pas par des métaphores (CONNU).

La métaphore cérébrale a été féconde, et je ne vais pas passer trois cents pages à la critiquer. Je vais simplement faire autrement. Le mot « neurone » désignera ici une porte arithmétique ; le mot « apprentissage » désignera une procédure de modification de nombres ; le mot « profondeur » désignera un nombre de couches, pas une élévation de l'esprit. Ce déplacement de vocabulaire n'est pas une coquetterie : il rend les questions vérifiables. « Le cerveau fait-il mieux ? » n'a pas de réponse dans ce livre. « Combien de bits faut-il pour que cette traduction reste exacte ? » en a une, et nous la calculerons.

### Traduire, c'est payer

Voici la forme générale de l'objet que j'appelle une *traduction à ressources*. On se donne deux modèles de calcul $A$ et $B$, une famille de fonctions calculables dans $A$, et une application qui transforme toute machine de $A$ en une machine de $B$ calculant la même fonction — ou la même fonction à une erreur contrôlée près. On ne demande pas seulement : « est-ce possible ? » On demande : « à quel prix, et payé en quelle monnaie ? »

Quelques traductions traverseront tout le livre :

- circuit booléen vers neurones à seuil (chapitre 3, notre étalon) ;
- porte à seuil vers unités à activation continue, sigmoïde ou ReLU (chapitre 9) ;
- graphe partagé vers arbre, c'est-à-dire duplication des sous-calculs (chapitre 5) ;
- réseau récurrent vers réseau sans boucle, par dépliage du temps (chapitre 13) ;
- transformer vers circuit à seuil de profondeur bornée, sous hypothèse de précision (chapitre 15).

Chacune se solde par un tableau de sept colonnes, avec des « conservé », « multiplié par », « échangé contre ». Aucune ne se solde par « équivalent », tout court. Ce mot, employé sans colonne derrière, est la source la plus constante de confusion dans la littérature de vulgarisation comme dans les conversations d'ingénieurs.

### Le registre à sept colonnes

Fixons les compteurs. Pour un réseau sans boucle, une *couche* est un ensemble d'unités calculables en parallèle ; la profondeur $d$ est le nombre de couches, la largeur $\ell$ le plus grand nombre d'unités dans une couche, la taille $s$ le nombre total d'unités.

1. **Taille** : nombre d'unités (variante : nombre de poids non nuls). C'est le travail total.
2. **Temps** : nombre d'étapes élémentaires. Pour un circuit sans boucle, c'est la profondeur ; pour une machine à boucle, c'est le nombre d'itérations, à distinguer soigneusement du travail total.
3. **Mémoire** : nombre de bits d'état conservés d'une étape à la suivante.
4. **Profondeur** : nombre de couches, ou longueur du plus long chemin de dépendance.
5. **Largeur** : maximum d'unités actives simultanément dans une couche.
6. **Précision** : nombre de bits des poids, des seuils, des activations — et, séparément, nombre de bits de l'accumulateur qui forme la somme. Ces trois précisions ne sont pas interchangeables, et le chapitre 6 montrera pourquoi.
7. **Partage** : le nombre de réutilisations d'un même résultat intermédiaire (le *fan-out*), et le fait que la structure soit un graphe ou un arbre.

Deux identités élémentaires servent de garde-fous (PROUVÉ, chapitre 5, par comptage direct) : $s \le d \cdot \ell$, et le dépliage d'un graphe en arbre peut multiplier la taille par un facteur exponentiel en la profondeur.

Voici le second point en chiffres, sur un exemple que nous retrouverons. La parité de huit bits se calcule par une chaîne : $p_1 = x_1$, puis $p_i = p_{i-1} \oplus x_i$. Chaque XOR coûte deux neurones à seuil, d'où $14$ neurones, une profondeur $14$, une largeur $2$. Mais chaque $p_{i-1}$ est utilisé *deux fois* dans l'étape suivante. Si l'on interdit le partage et que l'on recopie les sous-calculs, le nombre $T_i$ de neurones de l'arbre vérifie $T_i = 2T_{i-1} + 2$ avec $T_1 = 0$, donc $T_i = 2^i - 2$, et $T_8 = 254$ (PROUVÉ, chapitre 5). Quatorze contre deux cent cinquante-quatre : la septième colonne n'est pas décorative.

### Le registre des statuts

Chaque énoncé de ce livre porte une étiquette. C'est une contrainte de rédaction que je me suis imposée, et je la crois plus utile qu'un long discours de méthode.

- **PROUVÉ** : la preuve complète est écrite ici, en toutes lettres, avec les conventions fixées. Ce sont des résultats modestes : le lemme L-03, l'impossibilité du XOR à une porte, les identités de comptage, les coûts exacts de nos variantes compilées.
- **CONNU** : le résultat est établi dans la littérature citée. Je n'en donne que l'*idée de preuve*, et je le dis explicitement à chaque fois. Une idée de preuve n'est pas une preuve ; elle sert à comprendre pourquoi l'énoncé est plausible et où se trouve la difficulté.
- **EXPÉRIMENTAL** : valeur mesurée selon le protocole du chapitre 12. Ce n'est pas un théorème, cela ne fournit aucune borne inférieure, et les limites du protocole sont rappelées partout où le chiffre apparaît.
- **CONJECTURE** : énoncé que je formule, qui me paraît plausible, et que je ne démontre pas.
- **RÉFUTÉ** : énoncé faux, avec son contre-exemple. Exemple : « une seule porte à seuil calcule la parité de huit bits » (RÉFUTÉ, chapitre 4).
- **OUVERT** : question précise que je formule et que ce tome ne résout pas. Je ne prétends pas qu'elle soit ouverte au sens de la communauté scientifique ; je dis seulement qu'elle n'est pas résolue ici, dans le cadre de la bibliographie fermée que je me suis fixée.

Aucune annonce de découverte, donc. Le lemme L-03 est un exercice de compilation, connu dans son principe depuis McCulloch et Pitts 1943. Je le démontre intégralement parce qu'il me sert d'*étalon* : c'est la traduction dont je connais le prix exact, et à laquelle je comparerai toutes les autres.

### L'étalon : le lemme L-03

Convention, fixée une fois pour toutes : un neurone à seuil reçoit $u_1, \dots, u_k \in \{0,1\}$, des poids entiers $w_i$ et un seuil entier $\theta$, et produit
$$y = \mathbf{1}\Big[\sum_{i=1}^{k} w_i u_i \ \ge\ \theta\Big].$$
Remarquons tout de suite qu'avec des entiers, $\sum w_i u_i \ge \theta$ équivaut à $\sum w_i u_i > \theta - 1$ : la convention « large » ou « stricte » est ici sans effet. Ce genre de détail est exactement ce que la colonne *précision* sert à surveiller.

**Lemme L-03 (PROUVÉ).** *Soit $C$ un circuit booléen acyclique sur la base $\{\mathrm{ET}, \mathrm{OU}, \mathrm{NON}\}$, à $s$ portes, de profondeur $d$, de largeur $\ell$, avec réutilisation arbitraire des sorties de portes. Il existe un réseau de neurones à seuil $N$ à $s$ neurones, de profondeur $d$, de largeur $\ell$, de même graphe de connexions, tel que $N(x) = C(x)$ pour tout $x \in \{0,1\}^n$, avec des poids entiers dans $\{-1, 1\}$ et des seuils entiers compris entre $0$ et le nombre d'entrées de la porte. Si $C$ contient des portes XOR à deux entrées, chacune est remplacée par trois neurones de poids dans $\{-2, -1, 1\}$, au prix de deux couches supplémentaires par XOR.*

*Preuve.* On associe à chaque porte $g$ un neurone $\nu(g)$ recevant exactement les mêmes fils que $g$. Trois cas.

- $g = \mathrm{ET}(u_1, \dots, u_k)$ : prendre $w_i = 1$ et $\theta = k$. La somme vaut le nombre d'entrées égales à $1$ ; elle est $\ge k$ si et seulement si toutes valent $1$.
- $g = \mathrm{OU}(u_1, \dots, u_k)$, $k \ge 1$ : prendre $w_i = 1$ et $\theta = 1$. La somme est $\ge 1$ si et seulement si au moins une entrée vaut $1$.
- $g = \mathrm{NON}(u)$ : prendre $w = -1$ et $\theta = 0$. La somme vaut $-u \in \{0, -1\}$ ; elle est $\ge 0$ si et seulement si $u = 0$.

Dans les trois cas, les poids sont dans $\{-1,1\}$ et le seuil est un entier entre $0$ et $k$. On conclut par induction sur un ordre topologique des portes : les fils d'entrée portent $x$ ; si tous les fils d'une porte portent la valeur du fil correspondant dans $C$, le neurone produit la valeur de la porte, d'après les trois cas. Toutes les valeurs coïncident donc, en particulier aux sorties. Comme $g \mapsto \nu(g)$ est une bijection qui préserve les connexions, elle préserve les niveaux, donc la profondeur, la largeur, la taille et le partage.

Pour XOR, poser $h = \mathbf{1}[u_1 + u_2 \ge 2]$ puis $y = \mathbf{1}[u_1 + u_2 - 2h \ge 1]$. Les quatre cas donnent : $(0,0) \mapsto h=0, y=\mathbf{1}[0 \ge 1]=0$ ; $(0,1)$ et $(1,0) \mapsto h=0, y=\mathbf{1}[1\ge1]=1$ ; $(1,1) \mapsto h=1, y=\mathbf{1}[-1\ge1]=0$. C'est bien XOR, avec trois neurones, deux couches, et un poids $-2$. $\square$

Le registre de L-03 est donc : taille $\times 1$, profondeur $\times 1$, largeur $\times 1$, partage conservé, temps identique, mémoire nulle, précision minuscule — trois bits signés suffisent pour les poids, $\lceil \log_2(k+1) \rceil$ pour les seuils, un bit pour les activations.

Ce que L-03 ne dit pas est aussi important que ce qu'il dit. Il ne dit rien de l'*apprentissage* : les poids sont écrits à la main, pas trouvés par descente de gradient. Il ne dit rien des activations continues. Il ne dit rien du sens inverse : la majorité de huit bits est un seul neurone à seuil, mais demande un petit circuit de comptage sur la base booléenne. L'asymétrie est réelle, et elle dépend de la base choisie.

**Exercice 0.1.** Montrer que XOR n'est pas calculable par une seule porte à seuil. *Indication :* écrire les quatre inégalités imposées par la table de vérité, en tirer $\theta > 0$, $w_1 \ge \theta$, $w_2 \ge \theta$, puis additionner les deux dernières et comparer à la quatrième. (PROUVÉ au chapitre 4 ; l'exercice est la preuve.)

### Trois fonctions-tests

Trois tâches minuscules serviront de banc d'essai, du chapitre 2 au chapitre 16. Elles ont une propriété précieuse : leurs domaines d'entrée sont finis et petits, donc *exhaustifs*.

- **Parité 8** : $\mathrm{PAR}(x) = x_1 \oplus \cdots \oplus x_8$, sur $256$ entrées.
- **Majorité 8** : $\mathrm{MAJ}(x) = 1$ si au moins cinq des huit bits valent $1$ (convention de majorité stricte, choisie pour éviter les égalités), sur $256$ entrées.
- **Addition 3+3** : deux entiers de trois bits, somme sur quatre bits, $64$ couples d'entrées.

Leurs coûts compilés, vérifiés porte par porte au chapitre 8 :

| Fonction | Variante | Taille | Profondeur | Largeur | Poids |
|---|---|---|---|---|---|
| Majorité 8 | porte unique $\mathbf{1}[\sum x_i \ge 5]$ | 1 | 1 | 1 | $1$, seuil $5$ |
| Parité 8 | chaîne de XOR | 14 | 14 | 2 | $\{1,-2\}$ |
| Parité 8 | comptage en deux couches | 9 | 2 | 8 | $\{-1,1\}$ |
| Addition 3+3 | retenue propagée | 10 | 4 | 4 | $\{-2,-1,1\}$ |

La variante « comptage » mérite un mot, car elle montre que la profondeur achète quelque chose. Poser $z_k = \mathbf{1}[\sum_i x_i \ge k]$ pour $k = 1, \dots, 8$, puis sortir $\mathbf{1}[z_1 - z_2 + z_3 - z_4 + z_5 - z_6 + z_7 - z_8 \ge 1]$. Si $m$ bits valent $1$, la somme alternée vaut $\lceil m/2 \rceil - \lfloor m/2 \rfloor = m \bmod 2$. Neuf neurones, deux couches (PROUVÉ, chapitre 8).

**Exercice 0.2.** Vérifier cette identité pour $m = 0, 3, 4, 8$, puis expliquer pourquoi elle échoue si l'on remplace la somme alternée par une somme ordinaire.

Ces quatre lignes sont le cœur du livre : *la même fonction*, quatre registres différents. Laquelle est « la meilleure » ? La question n'a pas de sens sans préciser la colonne qu'on veut économiser.

### Une mesure, et ce qu'elle ne dit pas

Le chapitre 12 décrit un protocole : pour chacune des trois tâches, entraîner un réseau à deux couches cachées de seize unités chacune — noté 16-16 — par rétropropagation (Rumelhart, Hinton et Williams 1986), puis élaguer grossièrement : retirer des unités une par une tant que la fonction calculée sur la table exhaustive reste inchangée.

Résultat (EXPÉRIMENTAL) : les réseaux élagués conservent une largeur d'au moins $11$ à $14$ selon la tâche et le déroulement, là où les variantes compilées économes en largeur du tableau ci-dessus tiennent dans $1$ à $3$ unités de large.

Trois avertissements, que je répéterai chaque fois que ce chiffre apparaîtra. Premièrement, ce n'est **pas une borne inférieure** : l'élagage est glouton, dépendant de l'ordre, et ne certifie aucune minimalité. Deuxièmement, la comparaison n'est pas colonne par colonne : nos variantes étroites paient en profondeur — la chaîne de parité a largeur $2$ mais profondeur $14$. Troisièmement, huit bits, trois tâches, un protocole : rien de tout cela ne se transpose tel quel à des réseaux de grande taille.

La conclusion permise est donc modeste et précise : *la procédure d'entraînement et d'élagage employée ne trouve pas les solutions économes en largeur que la compilation exhibe*. C'est un fait sur une procédure, pas un fait sur les réseaux. La conclusion interdite serait : « les réseaux entraînés ont besoin de largeur $11$ ». Cette phrase, je ne l'écrirai nulle part.

### La précision comme pivot

Pourquoi la sixième colonne est-elle le pivot ? Parce que c'est elle qui paie les dettes des autres, silencieusement.

Quand on remplace un seuil par une sigmoïde très raide pour retrouver le comportement booléen, la pente — donc la magnitude des poids — doit croître comme l'inverse de la tolérance d'erreur. Quand on déplie une boucle en couches, la mémoire disparaît, mais l'état doit voyager *exactement* dans les activations, sous peine de dérive. Quand on partage un sous-calcul, on économise la taille, mais on augmente la profondeur de lecture et les exigences de fidélité du fil partagé.

La littérature citée fournit les grands repères, tous marqués CONNU, tous accompagnés seulement d'une idée de preuve. Les théorèmes d'approximation universelle (Cybenko 1989 ; Hornik, Stinchcombe et White 1989) disent qu'une couche cachée suffit à approcher une fonction continue sur un compact ; ils ne disent ni la taille, ni la précision, ni la facilité d'entraînement. Les bénéfices de la profondeur (Telgarsky 2016) exhibent des fonctions qu'une architecture profonde calcule avec peu d'unités et qu'une architecture peu profonde ne peut approcher qu'avec beaucoup plus d'unités. Les circuits à seuil de profondeur bornée (Hajnal, Maass, Pudlák, Szegedy et Turán 1993) montrent que la profondeur deux ne suffit pas à tout, certaines fonctions explicites y exigeant une taille exponentielle. La taille des poids (Håstad 1994) montre qu'une porte à seuil unique peut exiger des poids de magnitude exponentielle en le nombre d'entrées. Les réseaux récurrents à poids rationnels ou réels (Siegelmann et Sontag 1995 ; Pérez, Marinković et Barceló 2019) séparent deux régimes de puissance selon ce qu'on autorise dans les nombres. Enfin, les transformers à précision logarithmique se ramènent à des circuits à seuil de profondeur constante (Merrill et Sabharwal 2023) : l'idée est que chaque opération d'attention, avec $O(\log n)$ bits, se réalise en profondeur constante par des portes de comptage et de comparaison, et que l'empilement d'un nombre constant de telles couches reste de profondeur constante.

Cette dernière référence est le modèle du raisonnement que je veux transmettre : une affirmation sur un modèle moderne, formulée comme un énoncé de comptabilité, avec une hypothèse de précision explicite. Retirez l'hypothèse, l'énoncé change de vérité.

**Exercice 0.3.** Pour un circuit de fan-in maximal $4$, combien de bits faut-il pour les poids et les seuils issus de L-03 ? Comparez au nombre de bits nécessaires pour stocker l'état d'une chaîne de parité de longueur $8$ déplieée en arbre.

### Pour qui, et comment lire

Ce livre s'adresse à un lecteur cultivé non spécialiste. Il faut savoir compter, manipuler des inégalités, lire une formule avec un $\sum$, et accepter de vérifier une table de vérité à quatre lignes. Il ne faut aucune connaissance en neurosciences, aucun logiciel, aucun cadre d'apprentissage automatique. Les notions sont introduites dans l'ordre : intuition, définition, énoncé, exemple, exercice. Les preuves complètes sont courtes et ne demandent rien d'autre que de l'arithmétique ; les grands théorèmes sont énoncés avec leur statut et leur idée de preuve, sans démonstration.

Trois chemins de lecture sont possibles. Le chemin rapide : chapitres 1, 2, 3, 5, 8, 16 — on y voit l'étalon, le registre et le transfert. Le chemin des ressources : chapitres 6, 7, 10, 11, 14, 15 — on y suit la précision et la profondeur. Le chemin de la pratique : chapitres 9, 12, 13, 15 — on y trouve le protocole, les mesures et leurs limites. Un manuel général comme Goodfellow, Bengio et Courville 2016 reste le complément naturel pour tout ce qui touche à l'usage ; les réseaux à boucle et à états stables, dont je ne traiterai qu'un aspect au chapitre 13, ont leur point d'entrée dans Hopfield 1982.

La bibliographie est courte et volontairement fermée : quinze titres, tous cités dans le texte avec auteur et année. Je ne donne ni numéro de page, ni identifiant numérique, ni citation entre guillemets attribuée à un chercheur. Quand je résume un résultat, c'est mon résumé, avec le statut qui convient.

### Le plan

**Partie I — Le neurone comme porte : le socle booléen.** Chapitre 1 : modèles, ressources, traductions, et la règle du jeu. Chapitre 2 : le neurone à seuil comme porte logique, conventions et premiers exemples. Chapitre 3 : la compilation porte par porte, avec la preuve complète de L-03 et ses variantes. Chapitre 4 : le perceptron, XOR, parité, et ce que l'apprentissage peut et ne peut pas trouver.

**Partie II — Circuits à seuil : la comptabilité des ressources.** Chapitre 5 : les sept compteurs, leurs inégalités, le partage et le dépliage en arbre. Chapitre 6 : la précision des poids, jusqu'où il faut compter. Chapitre 7 : la profondeur bornée, ce que ces circuits savent faire. Chapitre 8 : les trois fonctions-tests et le détail de leurs coûts compilés.

**Partie III — Approximer : activations continues, profondeur, apprentissage.** Chapitre 9 : du seuil à la sigmoïde et à la ReLU, ce que la continuité coûte en bits. Chapitre 10 : les théorèmes d'approximation universelle, ce qu'ils disent et ne disent pas. Chapitre 11 : les bénéfices de la profondeur. Chapitre 12 : rétropropagation, entraînement, élagage — protocole, mesures, limites.

**Partie IV — Mémoire, précision, machines modernes et transfert.** Chapitre 13 : les réseaux récurrents, le temps et la mémoire comme ressources, le dépliage. Chapitre 14 : rationnels contre réels, précision et Turing-complétude. Chapitre 15 : transformers, attention, parallélisme, précision bornée. Chapitre 16 : transfert vers le programme RTC.

### Ce que ce livre ne promet pas, et ce qu'il transmet

Je ne promets ni performance, ni recette, ni raccourci vers des systèmes plus puissants. Je ne présente aucun résultat comme une découverte. Je ne prétends pas que la lecture-machine épuise ce qu'on peut dire d'un réseau ; je soutiens qu'elle est la seule à permettre une comptabilité vérifiable, et qu'elle est étonnamment sous-utilisée dans les discussions ordinaires.

Le dernier chapitre tire le bilan pour le programme RTC, consacré aux traductions à ressources. Il répond à trois questions. *Quelles ressources ?* Les sept colonnes, avec la précision dédoublée en poids, activations et accumulation. *Quelles traductions ?* Cinq familles, dont une entièrement démontrée ici, et quatre documentées par des énoncés CONNU accompagnés de leur idée de preuve. *Quelles questions ouvertes ?* Principalement celle-ci, que je formule sans la résoudre (OUVERT) : existe-t-il une traduction générale des réseaux à seuil de profondeur $d$ vers des réseaux à activation continue, qui préserve la taille à un facteur polynomial tout en gardant une précision logarithmique en la taille ? Et sa variante pratique (CONJECTURE) : les solutions économes en largeur que la compilation produit-elles sont-elles atteignables par une procédure d'entraînement et d'élagage raisonnable, ou faut-il les injecter ?

Entre ces deux questions se tient tout le livre. Une machine ne se contente pas d'être équivalente à une autre : elle l'est à un prix, dans une monnaie, avec une facture. Apprendre à lire cette facture, colonne par colonne, est le seul objectif de ces pages.