## Conclusion : Transfert vers le programme RTC

Chère lectrice, cher lecteur, nous voici parvenus au terme de notre exploration. Dans ce livre, j'ai cherché à cartographier un territoire invisible mais fondamental : l'espace des traductions entre les modèles de calcul. De la machine de Turing au lambda-calcul, des circuits booléens aux réseaux de neurones, nous avons vu que toute traduction fidèle préserve un noyau dur d'invariants — calculabilité, temps et taille à un polynôme près, largeur arborescente, profondeur, précision et partage — tandis que d'autres ressources se dégradent inévitablement. Identifier ces invariants, démontrer leurs bornes et comprendre les barrières qui nous empêchent de les séparer constitue le cœur battant du programme RTC (Traductions à Ressources et Contraintes).

### Synthèse des invariants et des fragilités

Le voyage a commencé par l'invariant absolu : la calculabilité. Les travaux fondateurs de Church 1936 et Turing 1936 ont établi que la notion de fonction calculable est robuste, indépendante du formalisme choisi. Ce statut est CONNU et universellement accepté. Mais dès que l'on s'intéresse à l'efficacité, le paysage se complexifie. La thèse de Church-Turing étendue postule que les modèles raisonnables s'équivalent à un polynôme près. Les relations entre ces mesures de complexité, explorées en profondeur par Pippenger et Fischer 1979, forment le socle de notre cadre moderne, tel que synthétisé par Arora et Barak 2009.

$$T_{M_2}(x) \le (T_{M_1}(x))^c$$
*Énoncé en mots* : Le temps de calcul d'une machine $M_2$ simulant une machine $M_1$ est borné par une puissance polynomiale du temps de $M_1$.
*Conditions de validité* : Modèles de calcul raisonnables (machines de Turing, RAM, lambda-calcul).
*Statut* : CONNU.
*Exemple numérique* : Si $M_1$ termine en $T_{M_1}(x) = 10$ étapes et que l'exposant de simulation est $c=2$, alors $M_2$ termine en au plus $10^2 = 100$ étapes.

$$S_{M_2}(x) \le (S_{M_1}(x))^d$$
*Énoncé en mots* : La taille de la description ou de l'espace mémoire de la machine simulante est bornée polynomialement par rapport à celle de la machine simulée.
*Conditions de validité* : Modèles de calcul standards avec encodage efficace.
*Statut* : CONNU.
*Exemple numérique* : Si la taille de $M_1$ est $S_{M_1}(x) = 5$ unités et $d=3$, alors $S_{M_2}(x) \le 5^3 = 125$ unités.

Cette équivalence polynomiale trouve son point de bascule dans la réduction à la satisfaisabilité propositionnelle. Cook 1971 a démontré que SAT agit comme un pivot universel, capturant l'essence du calcul non déterministe.

$$|\phi_{Cook}| \le c \cdot T^2$$
*Énoncé en mots* : La taille de la formule propositionnelle générée par la réduction de Cook est quadratique par rapport au temps de calcul de la machine de Turing.
*Conditions de validité* : Réduction standard d'une machine de Turing non déterministe vers SAT.
*Statut* : CONNU.
*Exemple numérique* : Pour un temps de calcul $T=10$ et une constante $c=2$, la taille de la formule est $|\phi| \le 2 \times 10^2 = 200$ variables et clauses combinées.

Même dans le cadre fonctionnel du lambda-calcul, l'invariance polynomiale résiste. Accattoli et Dal Lago 2016 ont prouvé que la stratégie de réduction la plus naïve en apparence préserve cette borne, confirmant que le partage et le temps sont intimement liés.

$$T_{LO} \le c \cdot T_{mach}^2$$
*Énoncé en mots* : Le nombre d'étapes de réduction bêta dans la stratégie de gauche à droite (leftmost-outermost) est borné quadratiquement par le nombre d'étapes d'une machine abstraite.
*Conditions de validité* : Lambda-calcul et machines à environnements.
*Statut* : PROUVÉ.
*Exemple numérique* : Si la machine exécute $T_{mach} = 10$ étapes et $c=1$, la réduction bêta prend au plus $1 \times 10^2 = 100$ étapes.

### Le registre des statuts : ce que nous savons et ce qui nous résiste

Au-delà du temps et de la taille, la structure spatiale des calculs révèle des invariants paramétrés. La largeur arborescente, introduite par Robertson et Seymour 1986, mesure la proximité d'un graphe avec un arbre. Lorsque l'on traduit un circuit en formule SAT via la transformation de Tseitin 1968, cette largeur ne s'effondre pas, mais elle ne s'envole pas non plus de manière incontrôlée. C'est le résultat L-01 du programme RTC.

$$w_{Tseitin} \le (k+1)(w+1)-1$$
*Énoncé en mots* : La largeur arborescente de la formule de Tseitin obtenue à partir d'un circuit est bornée supérieurement par le produit du degré entrant maximal plus un et de la largeur du circuit plus un, moins un.
*Conditions de validité* : Circuit booléen de largeur arborescente $w$ et de degré entrant maximal $k$.
*Statut* : PROUVÉ (Résultat L-01).
*Exemple numérique* : Pour un circuit avec $k=2$ et $w=3$, le calcul pas à pas donne $(2+1) \times (3+1) - 1 = 3 \times 4 - 1 = 12 - 1 = 11$. La largeur arborescente de la formule SAT résultante est au plus 11.

*Démonstration courte* : La transformation de Tseitin introduit une variable par fil du circuit. Si le circuit a une largeur arborescente $w$, on peut construire une décomposition arborescente où chaque sac contient les variables des fils actifs. Pour un nœud de degré entrant $k$, le sac doit contenir les $k$ entrées et la sortie, soit $k+1$ variables. En combinant avec la largeur $w$, la taille maximale du sac est $(k+1)(w+1)$, d'où une largeur arborescente de $(k+1)(w+1)-1$.

Cette maîtrise structurelle culmine avec le théorème de Courcelle 1990, qui montre que la logique monadique du second ordre devient traitable sur des graphes de largeur bornée.

$$T_{Courcelle} \le f(w) \cdot n$$
*Énoncé en mots* : Le temps d'évaluation d'une formule de logique monadique du second ordre sur un graphe est linéaire en la taille du graphe, mais dépend exponentiellement de sa largeur arborescente.
*Conditions de validité* : Graphe de taille $n$ et de largeur arborescente $w$, formule MSO fixe.
*Statut* : CONNU.
*Exemple numérique* : Pour un graphe de $n=50$ sommets, une largeur $w=3$ et une fonction $f(3)=100$, le temps est $100 \times 50 = 5000$ opérations.

$$tw(G_{k,k}) = k$$
*Énoncé en mots* : La largeur arborescente d'une grille carrée de côté $k$ est exactement égale à $k$.
*Conditions de validité* : Grille $k \times k$ non orientée.
*Statut* : CONNU.
*Exemple numérique* : Pour une grille de $4 \times 4$ ($k=4$), la largeur arborescente est exactement $tw = 4$.

Cependant, notre quête de bornes inférieures absolues se heurte à des murs invisibles. Baker, Gill et Solovay 1975 ont démontré que la diagonalisation seule ne peut pas séparer $P$ et $NP$.

$$Q_B(n) = 2^n$$
*Énoncé en mots* : Le nombre de requêtes nécessaires pour une machine déterministe afin de décider le langage diagonal $L_B$ relativisé est exponentiel, illustrant la barrière de relativisation.
*Conditions de validité* : Oracle $B$ construit par diagonalisation contre les machines polynomiales.
*Statut* : PROUVÉ.
*Exemple numérique* : Pour une entrée de taille $n=3$, la machine déterministe doit explorer $2^3 = 8$ requêtes pour vérifier l'absence de chaîne acceptante, confirmant la séparation.

Razborov et Rudich 1997 ont ensuite érigé la barrière des preuves naturelles, montrant que nos outils combinatoires standards s'effondrent face à la pseudo-aléatoire.

$$P_{nat} \le 2^{-n}$$
*Énoncé en mots* : La probabilité qu'une fonction booléenne aléatoire possède une propriété constructive et large (condition des preuves naturelles) est exponentiellement petite.
*Conditions de validité* : Fonctions booléennes sur $n$ variables, propriété de complexité de circuit.
*Statut* : PROUVÉ.
*Exemple numérique* : Pour $n=3$ variables, la probabilité qu'une fonction aléatoire satisfasse une telle propriété spécifique est au plus $2^{-3} = 0.125$.

Enfin, Aaronson et Wigderson 2009 ont scellé le paysage avec l'algébrisation, prouvant que même l'arithmétisation ne suffit pas à franchir le fossé entre $P$ et $NP$.

$$\tilde{A}(x) = A(x) \text{ pour } x \in \{0,1\}^n$$
*Énoncé en mots* : L'extension multilinéaire $\tilde{A}$ d'une fonction booléenne $A$ coïncide avec $A$ sur le domaine booléen, formant la base de l'algébrisation qui bloque les preuves arithmétiques.
*Conditions de validité* : Oracle $A$ et son extension algébrique $\tilde{A}$ sur un corps fini.
*Statut* : CONNU.
*Exemple numérique* : Pour $A(x_1, x_2) = x_1 \land x_2$, l'extension est $\tilde{A}(x_1, x_2) = x_1 x_2$. Pour l'entrée $(1,1)$, $\tilde{A}(1,1) = 1 \times 1 = 1$, ce qui est égal à $A(1,1) = 1$.

### Les réseaux de neurones, la compilation et les résultats RTC

Lorsque nous quittons le silicium pour la biologie inspirée, les invariants mutent. Siegelmann et Sontag 1995 ont révélé que la précision des poids synaptiques est une ressource fragile mais surpuissante.

$$\text{RN}(\mathbb{Q}) \equiv \text{Turing}$$
*Énoncé en mots* : Les réseaux de neurones récurrents à temps discret avec des poids rationnels sont équivalents en puissance de calcul aux machines de Turing.
*Conditions de validité* : Architecture récurrente, activation par seuil, poids dans $\mathbb{Q}$.
*Statut* : CONNU.
*Exemple numérique* : Un réseau avec un poids rationnel $p = 1/2$ peut simuler un décalage de bits. Pour l'entrée $x=1$, l'état interne devient $1/2$. À l'étape suivante, avec $x=1$, l'état devient $1/2 + 1/4 = 3/4$, encodant ainsi la séquence binaire de manière exacte.

À l'ère moderne, Merrill et Sabharwal 2023 ont montré que les transformeurs, malgré leur parallélisme massif, sont contraints par leur profondeur lorsqu'ils opèrent avec une précision réaliste.

$$D \ge c \log_2(n)$$
*Énoncé en mots* : La profondeur minimale d'un transformeur opérant avec une précision logarithmique pour résoudre des tâches de dépendance globale est logarithmique en la taille de l'entrée.
*Conditions de validité* : Transformeurs avec précision numérique limitée à $O(\log n)$ bits.
*Statut* : CONNU.
*Exemple numérique* : Pour une séquence de longueur $n=1024$ et une constante $c=1$, la profondeur minimale requise est $D \ge 1 \times \log_2(1024) = 10$ couches d'attention.

Le programme RTC a permis de formaliser ces contraintes via des résultats de compilation. Le résultat L-02 borne la largeur de chemin du tableau d'une machine, une étape clé pour compiler l'espace vers la structure.

$$pw_{tableau} \le 4s+1$$
*Énoncé en mots* : La largeur de chemin du graphe de tableau d'une machine de Turing est bornée par une fonction linéaire de l'espace utilisé.
*Conditions de validité* : Machine de Turing déterministe utilisant au plus $s$ cellules de ruban.
*Statut* : PROUVÉ (Résultat L-02).
*Exemple numérique* : Si la machine utilise $s=5$ cellules, la borne est $4 \times 5 + 1 = 20 + 1 = 21$. La largeur de chemin du tableau est au plus 21.

*Démonstration courte* : Le tableau d'une machine de Turing sur $s$ cellules et $T$ étapes forme une grille de largeur $s$. Une décomposition en chemin peut être construite en prenant des tranches verticales de 4 colonnes adjacentes pour couvrir les transitions d'état et les mouvements de tête. Chaque tranche contient au plus $4s$ nœuds, plus un nœud de liaison, donnant une largeur de chemin de $4s+1$.

Le résultat L-03 démontre que la compilation de fonctions symétriques vers des réseaux à seuil préserve une extrême parcimonie des poids.

$$W_{max} \le 2$$
*Énoncé en mots* : Dans la compilation de fonctions symétriques vers des réseaux de neurones à seuil, le poids maximal des connexions synaptiques ne dépasse pas 2.
*Conditions de validité* : Compilation de fonctions booléennes symétriques standard.
*Statut* : PROUVÉ (Résultat L-03).
*Exemple numérique* : Pour la compilation de la fonction majorité à 3 entrées, les poids synaptiques sont tous de 1. Le maximum est $1 \le 2$. Pour une fonction symétrique spécifique à 4 entrées nécessitant un seuil complexe, la construction garantit que le poids maximal atteint exactement $2 \le 2$.

Enfin, le résultat E-01b met en lumière le fossé entre l'apprentissage statistique et la compilation algorithmique.

$$w_{train} \in [11, 14], w_{compile} \in [1, 3]$$
*Énoncé en mots* : La largeur des couches cachées des réseaux de neurones entraînés par descente de gradient est significativement supérieure à celle des réseaux compilés algorithmiquement pour la même tâche.
*Conditions de validité* : Tâches de classification booléenne, architectures feed-forward.
*Statut* : EXPÉRIMENTAL (Résultat E-01b).
*Exemple numérique* : Pour la tâche de parité sur 8 bits, le réseau entraîné converge vers une largeur $w_{train} = 12$, tandis que le réseau compilé par seuil atteint une largeur $w_{compile} = 2$. L'écart est de $12 - 2 = 10$ unités.

### Transfert vers le programme RTC : ressources, traductions et questions ouvertes

Ce que ce tome apporte à l'étude des traductions à ressources est une cartographie claire. Nous avons identifié les ressources qui survivent au changement de paradigme (calculabilité, temps polynomial, largeur arborescente) et celles qui se brisent (précision réelle, largeur entraînée, profondeur logarithmique). Les traductions étudiées — de Turing vers SAT, de circuits vers Tseitin, de fonctions booléennes vers réseaux à seuil — révèlent que l'optimisation d'une ressource se paie souvent par la dégradation d'une autre.

Plusieurs questions demeurent OUVERTES. Existe-t-il une traduction qui préserve simultanément la largeur arborescente et la profondeur sans explosion exponentielle de la taille ? L'écart expérimental E-01b est-il une limitation fondamentale de la descente de gradient face à la complexité structurelle, ou peut-il être comblé par de nouveaux paysages d'optimisation ? Ces questions définiront les prochains tomes de notre programme.

### Mot final au lecteur

La complexité n'est pas une prison, mais une géographie. Comprendre ce qui se conserve et ce qui se perd lorsque nous traduisons un problème d'un langage à un autre est l'essence même de l'informatique théorique. J'espère que ce livre vous aura armé pour naviguer dans ce paysage avec rigueur et intuition.

*Exercice* : Considérez une machine de Turing utilisant $s=10$ cellules d'espace. Calculez la largeur de chemin de son tableau (L-02). Si cette machine est traduite en circuit booléen de largeur $w=5$ et de degré entrant $k=2$, calculez la largeur arborescente de la formule de Tseitin correspondante (L-01). Comparez les deux largeurs et concluez sur la ressource la plus fragile lors de cette double traduction.