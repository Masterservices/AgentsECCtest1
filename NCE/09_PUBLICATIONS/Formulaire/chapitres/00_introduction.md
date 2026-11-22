## Introduction — Traduire, c'est payer

### Un même calcul, cinq costumes

Additionner trois et quatre semble un geste unique. Il ne l'est pas. Dans le lambda-calcul, j'écris deux numéraux de Church, je leur applique un terme d'addition, et six réductions bêta plus tard j'obtiens le numéral de sept. Sur une machine de Turing, le même résultat exige de déplacer une tête de lecture, de réécrire des symboles, de boucler sur un ruban. Dans un circuit booléen, il faut des portes, des fils, une profondeur. En logique propositionnelle, il faut des variables auxiliaires et des clauses qui contraignent chaque porte. Dans un réseau de neurones, il faut des poids, des biais, une fonction d'activation, et une décision sur la précision numérique.

Cinq costumes pour le même nombre. Cinq factures différentes.

Ce livre est né d'une remarque têtue : nous savons depuis longtemps que ces modèles calculent la même chose, et nous enseignons cette équivalence comme si elle épuisait la question. Elle ne l'épuise pas. Elle ouvre la question. Ce qui change d'un modèle à l'autre, ce n'est pas le *quoi*, c'est le *combien*. Et ce combien est mesurable, comparable, parfois borné par un théorème, parfois seulement constaté sur des machines.

J'ai donc rassemblé, classé et illustré les formules qui gouvernent ces passages. C'est un formulaire, au sens où un formulaire de physique est un formulaire : un répertoire d'énoncés utilisables, chacun muni de ses conditions d'emploi.

### La thèse

La thèse tient en une phrase : **toute traduction entre modèles de calcul conserve ou perd des ressources mesurables — taille, temps, mémoire, profondeur, largeur, précision, partage — et cette perte obéit à des formules.**

Le versant « conservation » est ancien et solide : le lambda-calcul définissable et la calculabilité par machine de Turing coïncident (CONNU ; Church 1936 ; Turing 1936). Le versant « perte » est le nôtre. Un terme de trente-neuf nœuds peut avoir une forme normale de cent trente mille nœuds. Une machine qui tourne en un million de pas se traduit en un circuit d'environ vingt millions de portes (CONNU ; Pippenger et Fischer 1979). Un circuit de trois portes se traduit en neuf clauses. Un réseau profond à vingt unités peut exiger mille unités pour être aplani.

Ces nombres ne sont pas des détails d'implémentation. Ce sont les prix. Et un prix qu'on ne sait pas chiffrer est un prix qu'on paie sans le savoir.

### Ce que j'appelle une traduction à ressources

Fixons le vocabulaire, car le reste du livre en dépend. Un modèle de calcul est un triplet : un domaine d'objets, une sémantique qui dit ce que chaque objet calcule, et une fonction de coût qui dit ce que chaque objet consomme. Le coût n'est pas un scalaire mais un vecteur :

$$\rho_A(x) \;=\; \bigl(\,|x|,\ \tau_A(x),\ \mathrm{es}_A(x),\ \delta_A(x),\ \omega_A(x),\ \pi_A(x),\ \mathrm{pa}_A(x)\,\bigr)$$

En mots : taille, temps, espace, profondeur, largeur, précision, partage. Définition, donc hors registre des statuts : une définition ne se prouve pas, elle se juge à ce qu'elle permet de dire. Une traduction de $A$ vers $B$ est un triplet $T=(\mathrm{enc},\mathrm{sim},\mathrm{dec})$ correct au sens où

$$\mathrm{dec}\bigl(\mathrm{sim}(\mathrm{enc}(x))\bigr) \;=\; \llbracket x \rrbracket_A \qquad \text{pour tout } x \text{ du domaine.}$$

Cette égalité est la correction *fonctionnelle*. Elle ne dit rien du coût. Le coût s'écrit séparément, ressource par ressource, sous la forme d'une majoration monotone :

$$\rho_B^{(r)}\bigl(T(x)\bigr) \;\le\; g_r\bigl(\rho_A^{(r')}(x)\bigr), \qquad g_r \text{ croissante.}$$

La fonction $g_r$ est le **surcoût** de la traduction pour la ressource $r$. Tout le formulaire est un catalogue de $g_r$. Et la règle la plus utile du livre est immédiate :

$$\rho_C^{(r)}\bigl(T'(T(x))\bigr) \;\le\; h_r\bigl(g_r(\rho_A(x))\bigr)$$

En mots : les surcoûts monotones se composent par composition. Conditions : $g_r$ et $h_r$ croissantes, traductions correctes, mêmes conventions de mesure. Statut : PROUVÉ — la preuve est l'inégalité $T'(T(x)) \le h_r(\rho_B(T(x))) \le h_r(g_r(\rho_A(x)))$, où la seconde étape utilise la monotonie de $h_r$. Exemple chiffré : si $g(u)=u\log_2 u$ et $h(v)=4v$, pour $u=10^6$ on calcule $\log_2 10^6 = 6\times 3{,}3219 = 19{,}93$, puis $g(u)=1{,}993\times 10^7$, puis $h(g(u)) = 7{,}97\times 10^7$. Le pipeline complet coûte environ quatre-vingts millions d'unités, pas quatre millions.

Cette règle a un verso, tout aussi élémentaire et tout aussi utile : une borne inférieure dans le modèle cible remonte au modèle source par $g_r^{-1}$. C'est le mécanisme de transfert que le dernier chapitre exploite.

### Le registre des statuts

Je m'impose une discipline : aucune affirmation sans étiquette. Six étiquettes, pas une de plus.

**PROUVÉ** : la démonstration est écrite en entier dans ce livre, et elle est courte. Exemple : la formule de taille d'une substitution, ou l'impossibilité pour un neurone à seuil de calculer le ou exclusif.

**CONNU** : le résultat est établi dans la littérature ; je donne l'idée de la preuve, en disant explicitement que c'est une idée. Exemple : $\mathrm{NSPACE}(s)\subseteq \mathrm{DSPACE}(s^2)$ (CONNU ; Savitch 1970), dont l'idée est la recherche récursive de point milieu.

**EXPÉRIMENTAL** : le constat vient de mesures ou de simulations, sans démonstration. Exemple : la localisation numérique du seuil du 3-SAT aléatoire autour du rapport $4{,}26$.

**CONJECTURE** : énoncé plausible, non démontré, que je signale comme tel. Exemple : $\mathrm{P}\neq\mathrm{NP}$.

**RÉFUTÉ** : énoncé faux, avec contre-exemple ou preuve du contraire. Exemple : « un pas bêta coûte un travail constant » — faux, la duplication peut faire exploser la taille.

**OUVERT** : question que personne n'a tranchée et que je laisse ouverte. Exemple : $\mathrm{P}=\mathrm{NP}$ ?

Ce registre n'est pas une coquetterie. Il est la différence entre un formulaire et un catalogue de promesses. Quand je lis « approximation universelle » (CONNU ; Cybenko 1989), je note aussi ce que le théorème ne dit pas : il garantit l'existence d'un réseau approchant, il ne garantit ni sa taille, ni sa profondeur, ni qu'on le trouve par descente de gradient. L'écart entre existence et construction est exactement l'espace où vivent les ressources.

### Pour qui, et comment lire

Ce livre s'adresse au lecteur cultivé non spécialiste : quelqu'un qui sait manipuler un logarithme, une récurrence, une somme, et qui n'a jamais suivi de cours de complexité. Je n'exige aucun prérequis en lambda-calcul, en logique propositionnelle ni en apprentissage. Chaque notion est introduite par une intuition, puis une définition, puis un énoncé, puis un exemple chiffré, puis un exercice.

Chaque formule du livre est présentée en fiche, avec cinq champs : ce qu'elle dit en français, l'égalité ou l'inégalité, ses conditions de validité, son statut, et un exemple numérique calculé pas à pas. Les démonstrations courtes sont écrites en entier ; les grandes sont esquissées et l'esquisse est annoncée comme telle. Je ne présente jamais une intuition comme une preuve, et je n'annonce aucune découverte : ce tome rassemble et organise, il ne revendique pas de résultat nouveau.

Voici quinze fiches d'ouverture. Elles traversent tout le livre et donnent le ton.

### Le formulaire en miniature

**F01 — Le prix d'une substitution.** En mots : remplacer une variable par un terme coûte exactement le nombre d'occurrences fois la taille du terme inséré, moins ce qu'on retire. Avec $|x|=1$, $|MN|=|M|+|N|+1$, $|\lambda x.M|=|M|+1$ :

$$|M[x:=N]| \;=\; |M| + \nu_x(M)\,\bigl(|N|-1\bigr)$$

Conditions : substitution sans capture, $\nu_x(M)$ occurrences libres de $x$, renommage gratuit en taille. Statut : PROUVÉ — induction sur $M$ ; cas variable immédiat ; cas application par additivité ; cas abstraction, le renommage d'un lieur ne change pas la taille. Exemple : $M=\lambda y.\,x\,(x\,y)$ a $6$ nœuds, $\nu_x=2$ ; $N=\lambda z.z$ a $2$ nœuds ; $6+2\times(2-1)=8$, et le terme $\lambda y.(\lambda z.z)((\lambda z.z)y)$ a bien $8$ nœuds.

**F02 — L'explosion de taille.** En mots : la forme normale peut être exponentiellement plus grosse que le terme de départ.

$$\mathrm{nf}(M_k)=\overline{2^{2^{k-1}}}, \qquad |M_k| = 8k-1, \qquad |\overline{n}| = 2n+3$$

Conditions : $M_k$ est $k$ copies du numéral $\overline{2}$ imbriquées à droite. Statut : PROUVÉ (calcul explicite, chapitre 2). Exemple : $\overline{2}\,\overline{2}=\overline{4}$, puis $\overline{2}\,\overline{4}=\overline{16}$, puis $\overline{256}$, puis $\overline{65536}$. Pour $k=5$ : source $8\times5-1=39$ nœuds, forme normale $2\times65536+3=131\,075$ nœuds, rapport $\approx 3361$. Corollaire : « chaque pas bêta coûte un travail constant » est RÉFUTÉ.

**F03 — Six pas, deux factures.** En mots : l'addition de Church se normalise en six pas bêta, quels que soient les entiers.

$$\#\beta\bigl(\mathrm{ADD}\,\overline{m}\,\overline{n} \twoheadrightarrow \overline{m+n}\bigr) = 6, \qquad |\overline{m+n}| = 2(m+n)+3$$

Conditions : ordre normal, $\mathrm{ADD}=\lambda m\lambda n\lambda f\lambda x.\,m\,f\,(n\,f\,x)$. Statut : PROUVÉ — deux pas pour les deux arguments externes, deux pour $\overline{m}\,f$ puis son application, deux pour $\overline{n}\,f\,x$. Exemple : $3+4$ donne $|\overline{7}|=17$ nœuds ; $1000+1000$ donne $|\overline{2000}|=4003$ nœuds. Six pas dans les deux cas. Le nombre de pas n'est donc pas le coût.

**F04 — Le déroulement de Y.** En mots : le combinateur de point fixe grossit linéairement à chaque tour.

$$Y\,g \twoheadrightarrow_\beta g\,(W_g W_g), \qquad |g(W_gW_g)| = 3|g|+12$$

Conditions : $Y=\lambda f.(\lambda x.f(xx))(\lambda x.f(xx))$, $W_g=\lambda x.g(xx)$, deux pas bêta. Statut : PROUVÉ pour le compte ; CONNU pour la non-terminaison en général (Barendregt 1984). Exemple : $|Y|=14$, $|g|=5$ donne $|Yg|=20$, puis $27$ après deux pas, puis $33$, puis $39$ : six nœuds de plus par déroulement.

**F05 — Le temps se hiérarchise.** En mots : donner plus de temps permet strictement de calculer plus.

$$f(n)\log f(n) = o\bigl(g(n)\bigr) \;\Longrightarrow\; \mathrm{DTIME}(f) \subsetneq \mathrm{DTIME}(g)$$

Conditions : fonctions constructibles en temps, modèle multi-ruban. Statut : CONNU (Hartmanis et Stearns 1965 ; Arora et Barak 2009) ; idée de preuve : diagonalisation contre une simulation universelle, avec rembourrage. Exemple : $f(n)=n$, $g(n)=n^2$ ; à $n=10^6$, $n\log_2 n \approx 1{,}99\times10^7$ contre $10^{12}$, rapport $\approx 5\times10^4$.

**F06 — Le carré de Savitch.** En mots : le non-déterminisme en espace se paie au carré, pas exponentiellement.

$$\mathrm{NSPACE}\bigl(s(n)\bigr) \subseteq \mathrm{DSPACE}\bigl(s(n)^2\bigr)$$

Conditions : $s(n)\ge \log n$, constructible. Statut : CONNU (Savitch 1970) ; idée : atteindre une configuration en $2^k$ pas se réduit à chercher un point milieu, profondeur $k$, une configuration par niveau de pile. Exemple : $s=20$, $5$ états, $2$ symboles donnent au plus $5\times20\times2^{20}=1{,}05\times10^8$ configurations, donc $k=27$ niveaux, donc $27\times20=540$ cellules, à comparer à $s^2=400$.

**F07 — Le tableau de Cook–Levin.** En mots : un calcul de longueur $t$ se code en une formule de taille quadratique en $t$.

$$|\varphi_{M,x}| = O\bigl(t(n)^2\bigr)$$

Conditions : encodage par cases et fenêtres locales, une variable par paire (case, symbole). Statut : CONNU (Cook 1971 ; Arora et Barak 2009) ; idée : le tableau espace-temps est contraint par des fenêtres $2\times3$. Exemple : $t=100$ donne $101^2=10\,201$ cases ; avec $8$ symboles de case, $81\,608$ variables ; les fenêtres donnent de l'ordre de $10^5$ clauses, constantes fixées au chapitre 7.

**F08 — Le surcoût des circuits.** En mots : simuler $t$ pas par un circuit coûte $t\log t$ portes, pas $t^2$.

$$\mathrm{DTIME}\bigl(t(n)\bigr) \subseteq \mathrm{SIZE}\bigl(O(t(n)\log t(n))\bigr)$$

Conditions : machine multi-ruban, simulation oblivieuse, famille de circuits non uniforme. Statut : CONNU (Pippenger et Fischer 1979) ; idée : rendre la simulation oblivieuse puis router par un réseau de commutation diviser-pour-régner. Exemple : $t=10^6$, $\log_2 t = 19{,}93$, produit $1{,}99\times10^7$ portes à constante près, contre $10^{12}$ pour l'encodage naïf.

**F09 — Tseitin, porte par porte.** En mots : chaque porte se traduit en au plus quatre clauses de trois littéraux, avec une variable auxiliaire.

$$\#\text{clauses} \le 4g+1, \qquad \#\text{variables} = n+g$$

Conditions : portes d'arité $\le 2$, équ satisfiabilité et non équivalence logique, clause unitaire forçant la sortie. Statut : PROUVÉ pour l'équ satisfiabilité (chapitre 9) ; CONNU pour l'encodage (Tseitin 1968). Exemple : $y_1=x_1\wedge x_2$, $y_2=y_1\vee x_3$, $y_3=\neg y_2$ donne $3+3+2=8$ clauses, plus $(y_3)$, soit $9$ clauses, $6$ variables, $19$ littéraux.

**F10 — Le seuil du 3-SAT.** En mots : le premier moment borne le seuil par le haut ; la valeur observée est plus basse.

$$\mathbb{E}[Z] = 2^n\bigl(1-2^{-k}\bigr)^m, \qquad \alpha_{\text{1er moment}} = \frac{1}{\log_2(8/7)} \approx 5{,}19$$

Conditions : tirage uniforme à $k$ littéraux par clause, $Z$ nombre d'affectations satisfaisantes. Statut : PROUVÉ pour la borne ; EXPÉRIMENTAL pour $\alpha_c\approx 4{,}26$ ; OUVERT pour l'existence d'un seuil net démontré à $k=3$. Exemple : $n=100$, $m=600$ ; $\log_2(7/8)=-0{,}19265$ ; exposant $100-115{,}59=-15{,}59$ ; $\mathbb{E}[Z]\approx 2{,}0\times10^{-5}$, donc $\Pr[\text{SAT}]\le 2{,}0\times10^{-5}$ par Markov.

**F11 — La marche de Schöning.** En mots : le 3-SAT se résout en temps de base $4/3$ par variable.

$$T(n) = O^*\!\left(\bigl(2(k-1)/k\bigr)^n\right) \;\xrightarrow{\;k=3\;}\; O^*\!\left((4/3)^n\right)$$

Conditions : algorithme randomisé, redémarrages, $3n$ pas de marche par essai. Statut : CONNU (Schöning 1999) ; idée : la distance de Hamming à une solution fixée diminue avec probabilité au moins $1/3$ par pas. Exemple : $n=100$ ; $100\ln(4/3)=28{,}77$ ; $e^{28{,}77}\approx 3{,}1\times10^{12}$, contre $2^{100}\approx 1{,}27\times10^{30}$ : facteur $\approx 4\times10^{17}$.

**F12 — La largeur qui sauve.** En mots : une décomposition arborescente étroite rend SAT polynomial.

$$T_{\text{SAT}} = O\bigl(2^{w}\cdot n\bigr)$$

Conditions : décomposition jolie de largeur $w$ du graphe primal fournie, chaque clause contenue dans un sac. Statut : PROUVÉ au chapitre 12 via les lemmes L-01 et L-02 ; idée : programmation dynamique sur les sacs, table de $2^{w}$ affectations. Exemple : $n=1000$, $w=10$ donne $1024\times1000=1{,}02\times10^6$ opérations, contre $2^{1000}\approx 10^{301}$.

**F13 — Le mur du neurone unique.** En mots : un neurone à seuil ne calcule pas le ou exclusif.

$$\mathrm{XOR}(x_1,x_2) \neq \mathbb{1}\bigl[w_1x_1+w_2x_2+b \ge 0\bigr] \quad \text{pour tous } w_1,w_2,b$$

Conditions : entrées binaires, seuil dur. Statut : PROUVÉ ; l'énoncé « un neurone suffit » est RÉFUTÉ (contexte : McCulloch et Pitts 1943). Preuve complète : $(0,0)\mapsto 0$ impose $b<0$ ; $(1,0)\mapsto 1$ impose $w_1+b\ge 0$ ; $(0,1)\mapsto 1$ impose $w_2+b\ge 0$ ; en sommant les deux dernières, $w_1+w_2+b \ge -b > 0$, ce qui contredit $(1,1)\mapsto 0$. Deux unités ReLU suffisent : $\mathrm{XOR}=\mathrm{ReLU}(x_1+x_2)-2\,\mathrm{ReLU}(x_1+x_2-1)$, valant $0,1,1,0$ sur $(0,0),(0,1),(1,0),(1,1)$.

**F14 — La profondeur multiplie les plis.** En mots : composer des dents de scie multiplie les morceaux linéaires ; une couche cachée ne fait que les additionner.

$$N(f\circ g) \le N(f)\,N(g), \qquad N(t^{\circ k}) = 2^k, \qquad N_{\text{1 couche}}(w) \le w+1$$

Conditions : fonctions affines par morceaux sur un intervalle, $t$ la tente à deux pans, ReLU. Statut : PROUVÉ pour les comptes ; CONNU pour la séparation en approximation (Telgarsky 2016). Exemple : $k=10$ donne $1024$ morceaux avec $20$ unités ReLU sur $10$ couches ; une représentation exacte à une couche exige $w\ge 1023$.

**F15 — Le coût de l'attention.** En mots : l'attention complète est quadratique en longueur de séquence.

$$\mathrm{Att}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V, \qquad \Theta(n^2 d) \text{ opérations}, \ \Theta(n^2) \text{ mémoire}$$

Conditions : attention dense, une tête, implantation naïve. Statut : CONNU (Vaswani et al. 2017). Exemple : $n=1024$, $d=64$ ; $n^2=1\,048\,576$ ; $n^2d=67\,108\,864$ produits-accumulations pour $QK^\top$, autant pour le produit par $V$, soit $1{,}34\times10^8$ ; la matrice des scores occupe $1\,048\,576\times4 = 4$ Mio. À $n=2048$ : $16$ Mio.

### Le plan

Le livre forme une seule partie, **Partie I — Lambda-calcul : syntaxe, encodages et coûts de traduction**, parce que le lambda-calcul y sert d'étalon : c'est le modèle le plus pauvre en structure, donc le plus révélateur de ce qu'une traduction doit ajouter.

Les chapitres 1 à 4 posent l'étalon. **Chapitre 1, Substitution et bêta-réduction : les règles primitives**, fixe les conventions de taille et prouve F01. **Chapitre 2, Encodages de Church : entiers, booléens et paires**, chiffre le coût des données. **Chapitre 3, Combinateur Y, types simples et terminaison**, sépare ce qui termine de ce qui ne termine pas. **Chapitre 4, Coût de réduction et simulation du lambda-calcul**, explique pourquoi compter les pas ne suffit pas et ce que le partage économise.

Les chapitres 5 à 9 franchissent vers les machines et la logique. **Chapitre 5, Machines de Turing et classes de complexité : définitions**, installe le vocabulaire. **Chapitre 6, Hiérarchies de temps et d'espace, théorème de Savitch**, donne F05 et F06. **Chapitre 7, Cook-Levin : SAT comme traduction universelle de NP**, déroule F07. **Chapitre 8, Simulation par circuits : le surcoût $O(t\log t)$**, détaille F08. **Chapitre 9, Encodage de Tseitin : circuit → CNF clause par clause**, écrit F09 porte par porte.

Les chapitres 10 à 12 regardent SAT du côté des algorithmes et de la structure. **Chapitre 10, Transition de phase du 3-SAT aléatoire**, distingue soigneusement le calculé du constaté. **Chapitre 11, Borne de Schöning : marche aléatoire et $(4/3)^n$**, donne la preuve de F11 dans ses grandes lignes. **Chapitre 12, Largeur arborescente, largeur de chemin et lemmes L-01, L-02**, démontre F12 en entier.

Les chapitres 13 à 15 passent aux neurones. **Chapitre 13, Neurone à seuil, portes logiques et ReLU**, traduit les portes en unités et réciproquement. **Chapitre 14, Approximation universelle, rétropropagation et attention**, confronte l'existence garantie (CONNU ; Cybenko 1989) au coût d'apprentissage (CONNU ; Rumelhart, Hinton et Williams 1986) et à la facture mémoire de F15. **Chapitre 15, Profondeur, régions linéaires et séparation ReLU**, développe F14.

Le **chapitre 16, Transfert vers le programme RTC : tables de correspondance et questions ouvertes**, referme le formulaire sur lui-même : quelles ressources ce tome a su chiffrer, quelles traductions il a couvertes, lesquelles restent sans formule, et sous quelle forme ces manques deviennent des questions de travail.

### Ce que ce livre ne promet pas

Il ne promet pas de rendre la complexité facile. Il ne promet aucun algorithme nouveau, aucune amélioration de borne, aucune résolution de question ouverte. Il promet un instrument : savoir, avant d'écrire une traduction, quel ordre de grandeur elle va coûter, et savoir si ce coût est démontré, mesuré, ou seulement espéré.

Trois angles morts sont assumés d'emblée. La précision numérique, d'abord : les énoncés d'approximation supposent des réels exacts, alors qu'une implantation tronque, et l'écart entre les deux n'est pas toujours chiffré ici. Le partage, ensuite : ressource réelle, mal normalisée, dont je donne des comptes explicites plutôt qu'une théorie. La précision des constantes, enfin : beaucoup de formules sont asymptotiques, et le lecteur qui veut un nombre exact devra descendre dans la preuve.

C'est peu, et c'est voulu. Un formulaire utile n'est pas un formulaire exhaustif : c'est un formulaire dont chaque ligne indique honnêtement jusqu'où on peut s'y fier.