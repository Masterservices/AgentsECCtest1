## Introduction

J'écris ce livre parce que le calcul ternaire équilibré m'a d'abord séduit, puis déçu, puis reconquis — et que je souhaite au lecteur de parcourir exactement ce chemin, dans cet ordre.

La séduction est immédiate. Là où le binaire impose deux états, $0$ et $1$, le ternaire équilibré en propose trois : $-1$, $0$, $+1$. La négation devient gratuite, la symétrie est inscrite dans le codage lui-même, et l'on pressent qu'une base plus proche du nombre $e \approx 2{,}718$ devrait, d'une certaine manière, être plus « naturelle » que la base $2$. Cette intuition a une histoire longue, de Łukasiewicz (1920) qui introduit une logique à trois valeurs pour échapper au tiers exclu, jusqu'aux travaux récents sur la quantification ternaire des poids de réseaux de neurones (Li, Zhang et Liu 2016 ; Zhu, Han, Mao et Dally 2017 ; Ma et al. 2024). Entre ces deux pôles, un siècle de tentatives, de machines expérimentales, de promesses et de renoncements.

La déception vient ensuite, et elle est nécessaire. Le ternaire équilibré ne change **aucune** classe de complexité. Tout problème décidable en temps polynomial par une machine de Turing binaire l'est, à facteur constant près, par une machine ternaire, et réciproquement. Il n'existe pas de problème qui devient soudainement facile parce qu'on a changé de base. Ce fait, que j'établis formellement sous la forme du lemme L-T2 (PROUVÉ), est le cœur honnête de ce livre. Quiconque cherche dans le ternaire une « nouvelle puissance de calcul » sera déçu, et il vaut mieux que cette déception survienne dès l'introduction plutôt qu'au chapitre 15.

La reconquête, enfin, est celle de l'ingénieur et du concepteur. Si le ternaire ne change pas *ce qui est calculable*, il change *comment certaines opérations se présentent*. La négation d'un nombre est une simple inversion de signe trit à trit ; la réduction modulo $3$ est la lecture du trit de poids faible ; la quantification des poids d'un réseau de neurones en $\{-1, 0, +1\}$ réduit la mémoire d'un facteur $\log_2 3 \approx 1{,}585$ par rapport au binaire signé. Ces gains sont réels, mesurables, mais ils sont *locaux* et *asymptotiquement négligeables* face aux coûts de conversion. Le ternaire est un outil de conception, pas une révolution.

Ce livre est la démonstration patiente de cette triple affirmation : séduction, déception, reconquête.

### Le sujet : qu'est-ce que le ternaire équilibré ?

En représentation positionnelle classique, un entier $n$ s'écrit en base $b$ comme

$$n = \sum_{k=0}^{m} d_k \, b^k, \quad d_k \in \{0, 1, \dots, b-1\}.$$

En base $b = 3$ *équilibrée*, on remplace l'alphabet $\{0, 1, 2\}$ par l'alphabet symétrique $\{-1, 0, +1\}$, que l'on note traditionnellement $\{\bar{1}, 0, 1\}$ :

$$n = \sum_{k=0}^{m} t_k \, 3^k, \quad t_k \in \{-1, 0, +1\}.$$

Cette écriture est unique pour tout entier relatif. Le nombre $5$, par exemple, s'écrit $1\bar{1}1$ car

$$5 = 1 \cdot 3^2 + (-1) \cdot 3^1 + 1 \cdot 3^0 = 9 - 3 + 1.$$

Le nombre $-5$ s'obtient en inversant chaque trit : $\bar{1}1\bar{1}$. Cette propriété — la négation par inversion composante par composante — est le premier gain « gratuit » du codage. En binaire, la négation exige un complément à deux, une addition, une retenue. En ternaire équilibré, elle est une permutation de l'alphabet :

$$\forall k, \quad t_k \mapsto -t_k.$$

Le deuxième gain gratuit est la réduction modulo $3$ : il suffit de lire $t_0$, le trit de poids faible, pour obtenir $n \bmod 3$ sans division.

Ces deux observations, triviales en apparence, structurent une grande partie de l'attrait du ternaire. Mais elles ont un prix : chaque addition, chaque multiplication, chaque comparaison doit gérer trois états au lieu de deux, et les tables de vérité passent de $2^2 = 4$ entrées possibles à $3^2 = 9$. Le coût se déplace, il ne disparaît pas.

### La démarche : traductions à ressources et registre des statuts

Ce livre est organisé autour d'un cadre conceptuel que j'appelle les **traductions à ressources**. L'idée est la suivante : passer d'un circuit binaire à un circuit ternaire (ou l'inverse) n'est jamais gratuit. Toute traduction consomme des *ressources* — taille (nombre de portes), profondeur (nombre de niveaux), largeur (nombre de fils). La question centrale n'est pas « le ternaire est-il meilleur ? », mais « combien coûte la traduction, et que gagne-t-on en échange ? ».

Formellement, si $C_B$ est un circuit binaire de taille $S_B$ et de profondeur $D_B$, et $C_T$ un circuit ternaire équivalent, le lemme L-T2 (PROUVÉ, chapitre 12) affirme qu'il existe des constantes $c_1, c_2 > 0$ indépendantes de la taille du circuit telles que

$$S_T \leq c_1 \cdot S_B \quad \text{et} \quad D_T \leq c_2 \cdot D_B,$$

et réciproquement. La traduction est à *facteur constant*. Aucune classe de complexité — $\mathbf{P}$, $\mathbf{NP}$, $\mathbf{PSPACE}$, $\mathbf{EXP}$ — n'est modifiée.

Pour que le lecteur puisse à chaque instant situer le degré de certitude d'une affirmation, j'emploie tout au long du livre un **registre des statuts**. Chaque énoncé mathématique, chaque résultat expérimental, chaque intuition est étiqueté :

- **PROUVÉ** : démonstration complète donnée dans le texte ;
- **CONNU** : résultat établi dans la littérature, idée de la preuve fournie ;
- **EXPÉRIMENTAL** : observation numérique reproductible, sans preuve formelle ;
- **CONJECTURE** : énoncé que je crois vrai mais que je ne sais pas démontrer ;
- **RÉFUTÉ** : énoncé faux, accompagné d'un contre-exemple ;
- **OUVERT** : question à laquelle je ne connais pas de réponse.

Ce registre est une dette envers la rigueur. Le lecteur cultivé mais non spécialiste que je vise doit pouvoir distinguer, ligne à ligne, ce qui est acquis de ce qui reste à faire.

### L'économie de radix : un gain réel mais modeste

Une question classique, posée notamment par Hayes (2001), est celle du *radix optimal*. Si l'on mesure le coût d'un chiffre par le nombre d'états qu'il doit distinguer, le coût total d'un registre représentant un entier $N$ en base $b$ est proportionnel à

$$\text{coût}(b) = b \cdot \log_b N = \frac{b \cdot \ln N}{\ln b}.$$

Minimiser cette expression par rapport à $b$ conduit à $b^* = e \approx 2{,}718$. La base entière la plus proche est $b = 3$. Le gain par rapport à la base $2$ se calcule :

$$\frac{\text{coût}(2)}{\text{coût}(3)} = \frac{2 / \ln 2}{3 / \ln 3} = \frac{2 \ln 3}{3 \ln 2} \approx \frac{2 \times 1{,}0986}{3 \times 0{,}6931} \approx 1{,}054.$$

Le gain est de $5{,}4\%$. Il est réel. Il est aussi, dans la pratique des circuits intégrés modernes, largement absorbé par les coûts de conversion entre interfaces binaires et internes ternaires. Ce livre ne cache ni le gain ni son caractère asymptotiquement négligeable.

### Le public visé

J'écris pour un lecteur cultivé, curieux, disposant d'une formation scientifique de niveau licence — mathématiques, informatique, physique ou ingénierie — mais qui n'est pas nécessairement spécialiste de théorie de la complexité, de conception de circuits ou d'apprentissage profond. Chaque notion est introduite par une intuition, puis définie formellement, puis illustrée par un exemple numérique calculé pas à pas, puis consolidée par un exercice. Les formules sont nombreuses — c'est un choix assumé — mais toujours accompagnées d'un commentaire en langue naturelle qui dit *ce qu'elles signifient* avant de dire *ce qu'elles prouvent*.

Le spécialiste, lui, trouvera les énoncés précis, les preuves complètes des lemmes L-T1 et L-T2, les tables de vérité ternaires exhaustives, et les références exactes (et uniquement celles-ci) vers les travaux de Łukasiewicz (1920), Shannon (1948), McCulloch et Pitts (1943), Kleene (1952), Tseitin (1968), Knuth (1969), Hayes (2001), Bogdanov et al. (2007), Courbariaux, Bengio et David (2015), Li, Zhang et Liu (2016), Zhu, Han, Mao et Dally (2017), et Ma et al. (2024). Je n'invente aucune référence. Je n'attribue aucune citation entre guillemets. Je n'annonce aucune découverte.

### Ce que ce livre n'est pas

Il n'est pas un manifeste pour l'ordinateur ternaire. Il n'est pas une promesse de rendements miraculeux. Il ne prétend pas que la base $3$ résoudra $\mathbf{P}$ vs $\mathbf{NP}$, ni qu'elle rendra obsolètes les architectures binaires. Il ne contient aucune spéculation financière ni aucune recommandation d'investissement : les considérations économiques sur le coût des portes logiques sont strictement techniques et informatives.

Il est, en revanche, un exercice d'honnêteté intellectuelle appliqué à un objet mathématique et ingénierial fascinant. Le ternaire équilibré mérite mieux que l'enthousiasme sans preuve et mieux que le dédain sans examen. Il mérite d'être compris.

### Le plan du livre

Le livre est organisé en quatre parties et seize chapitres.

**Partie I — Fondements : le trit, l'arithmétique et les logiques à trois valeurs** pose les définitions. Le chapitre 1 introduit la représentation en base $3$ équilibrée, l'unicité de l'écriture, la conversion depuis et vers le binaire. Le chapitre 2 développe l'arithmétique élémentaire : addition, soustraction, multiplication, division, avec les tables de retenue ternaires complètes. Le chapitre 3 présente les logiques à trois valeurs de Łukasiewicz (1920) et de Kleene (1952), leurs connecteurs, leurs tables de vérité, leurs différences. Le chapitre 4 en déduit les portes logiques ternaires fondamentales : MIN, MAX, complément, littéral, et leurs tables de vérité à $9$ entrées.

**Partie II — Économie de radix, circuits et traductions matérielles** entre dans le vif de l'ingénierie. Le chapitre 5 développe l'économie de radix, le calcul du gain de $5{,}4\%$, et ses limites pratiques. Le chapitre 6 présente les additionneurs et multiplieurs ternaires, avec des comptages de portes natives (statut EXPÉRIMENTAL). Le chapitre 7 étudie les traductions ternaire $\leftrightarrow$ binaire : codage double rail, convertisseurs, coût en fils et en portes. Le chapitre 8 montre comment obtenir des circuits binaires minimaux pour les portes ternaires par encodage SAT (statut EXPÉRIMENTAL).

**Partie III — Réseaux de neurones, SAT et classes de complexité** aborde les applications modernes et la théorie. Le chapitre 9 énonce et prouve le lemme L-T1 : tout neurone à seuil binaire peut être simulé par un neurone à poids ternaires avec un facteur constant sur le nombre d'entrées. Le chapitre 10 retrace la trajectoire de BinaryConnect (Courbariaux, Bengio et David 2015) aux Ternary Weight Networks (Li, Zhang et Liu 2016), à Trained Ternary Quantization (Zhu, Han, Mao et Dally 2017), jusqu'à BitNet b1.58 (Ma et al. 2024), en passant par le contexte de la cryptographie légère (Bogdanov et al. 2007). Le chapitre 11 analyse les encodages SAT en variables ternaires, les conflits, et le lien avec l'information au sens de Shannon (1948). Le chapitre 12 contient la preuve complète du lemme L-T2 : les traductions à coût constant entre circuits binaires et ternaires préservent toutes les classes de complexité usuelles.

**Partie IV — Verdict, honnêteté et transfert vers le programme RTC** conclut. Le chapitre 13 recense les domaines où le ternaire gagne effectivement : négation, réduction modulaire, quantification compacte. Le chapitre 14 recense ceux où il perd : conversion d'interface, profondeur des circuits, compatibilité avec l'écosystème binaire existant. Le chapitre 15 est le chapitre d'honnêteté : le ternaire ne change aucune classe de complexité, et ce fait est irréductible. Le chapitre 16, enfin, opère le transfert vers le programme RTC (Traductions à Ressources et Complexité) : quelles ressources sont pertinentes, quelles traductions restent à étudier, quelles questions demeurent ouvertes.

### Une note sur les formules

Ce livre est riche en formules. Chaque chapitre en contient au moins quinze, en notation $\LaTeX$, avec énoncé, conditions d'application, statut et exemple numérique. J'ai fait ce choix parce que je crois qu'une formule bien commentée est plus honnête qu'une métaphore : elle dit exactement ce qu'elle dit, ni plus ni moins. Le lecteur qui souhaite sauter une démonstration peut lire l'énoncé et l'exemple ; celui qui souhaite vérifier peut suivre la preuve pas à pas. Les deux lectures sont légitimes.

### Un dernier mot

Le calcul ternaire équilibré est, je le crois, un magnifique objet pédagogique. Il oblige à repenser des habitudes binaires si profondes qu'on les confond avec la nature du calcul. Il montre que le choix d'une base est un *codage*, pas une ontologie. Il montre aussi, et c'est peut-être sa leçon la plus précieuse, que changer de codage ne change pas la difficulté intrinsèque des problèmes. La complexité est plus profonde que la représentation.

J'espère que ce livre transmettra à la fois la beauté de l'objet et la lucidité sur ses limites. Le ternaire équilibré ne sauvera pas le monde. Mais il éclairera, je l'espère, la manière dont nous pensons le calcul, la représentation et la traduction.

C'est, au fond, tout ce qu'on peut honnêtement demander à un livre de mathématiques appliquées.

— Oussama Ghorbel

### Post-scriptum : la méthode à l'épreuve

J'ajoute à cette introduction une note de méthode, car un livre qui prêche l'honnêteté doit la pratiquer jusque dans ses propres pages. Plus haut, en présentant la négation, j'ai affirmé que $5$ s'écrit $1\bar{1}1$. Vérifions, comme le registre des statuts nous y oblige :

$$1\bar{1}1 = 1\cdot 9 + (-1)\cdot 3 + 1\cdot 1 = 9 - 3 + 1 = 7 \neq 5.$$

Statut : **RÉFUTÉ**. Et l'écriture $\bar{1}1\bar{1}$ que j'en avais déduite pour $-5$ vaut en réalité

$$\bar{1}1\bar{1} = -9 + 3 - 1 = -7.$$

Les écritures correctes sont

$$5 = 1\bar{1}\bar{1} = 9 - 3 - 1, \qquad -5 = \bar{1}11 = -9 + 3 + 1,$$

et c'est $7$, non $5$, qui s'écrit $1\bar{1}1$. Je laisse cette correction visible plutôt que de la faire disparaître : elle montre pourquoi chaque affirmation de ce livre porte un statut et un exemple numérique vérifiable. Une erreur de calcul n'est pas une honte ; une erreur qu'aucun lecteur ne peut détecter en est une. Le contrat de lecture que je propose est là : reprenez-moi chaque fois qu'un exemple vous paraît douteux, la vérification est toujours à portée de main.

### Conventions et notations

Quelques conventions, valables pour tout le livre. L'alphabet ternaire équilibré est $\mathbb{T} = \{-1, 0, +1\}$, et je note $\bar{1}$ le trit $-1$. Les mots s'écrivent du trit le plus significatif au plus faible, comme nos nombres décimaux ; le mot vide représente $0$. Cette représentation est classique, et Knuth (1969) en donne un traitement de référence (statut : **CONNU**).

Avec $m+1$ trits ($m \geq 0$), les entiers représentables sont exactement ceux de l'intervalle

$$-\frac{3^{m+1}-1}{2} \;\leq\; n \;\leq\; \frac{3^{m+1}-1}{2}.$$

Statut : **PROUVÉ** (chapitre 1). Idée de la preuve : le mot maximal $11\ldots1$ vaut la somme géométrique

$$\sum_{k=0}^{m} 3^k = \frac{3^{m+1}-1}{2},$$

le mot minimal vaut son opposé, et l'intervalle contient exactement

$$\frac{3^{m+1}-1}{2} - \left(-\frac{3^{m+1}-1}{2}\right) + 1 = 3^{m+1}$$

entiers — autant que de mots de longueur $m+1$. L'algorithme de division centrée du chapitre 1 montre que chacun est atteint ; le comptage force alors l'unicité.

Il en découle le nombre de trits nécessaires :

$$m+1 = \left\lceil \log_3\!\left(2|n|+1\right) \right\rceil.$$

Exemple calculé : $n = 14$. On forme $2|n|+1 = 29$, puis $\log_3 29 = \ln 29 / \ln 3 \approx 3{,}3673 / 1{,}0986 \approx 3{,}065$, d'où $4$ trits ; et de fait $14 = 1\bar{1}\bar{1}\bar{1} = 27 - 9 - 3 - 1$. Pour $n = 0$, la formule donne $0$ trit : le mot vide, conformément à la convention.

Enfin, un trit transporte une information de

$$\log_2 3 \approx 1{,}585 \text{ bits}$$

(statut : **CONNU**, Shannon 1948). Huit trits valent $8 \times 1{,}585 \approx 12{,}68$ bits, et l'encadrement

$$2^{12} = 4096 \;<\; 3^8 = 6561 \;<\; 8192 = 2^{13}$$

montre qu'il faut $13$ bits pour couvrir ce que $8$ trits expriment. Ce chiffre de $1{,}585$ est celui qui donne son nom au BitNet b1.58 de Ma et al. (2024) ; le chapitre 10 en fera le tour complet.

### Un premier calcul pas à pas

Avant d'ouvrir le chapitre 1, je veux donner au lecteur le plaisir d'un calcul complet. Additionnons $7$ et $-5$, avec $7 = 1\bar{1}1$ et $-5 = \bar{1}11$. La règle est locale : à chaque position $k$, on forme la somme des deux trits et de la retenue entrante, puis on la décompose :

$$a_k + b_k + c_k = t_k + 3\,c_{k+1}, \qquad t_k, c_{k+1} \in \{-1, 0, +1\}.$$

**Lemme (division centrée).** Pour tout entier $s$, il existe un unique couple $(t, c) \in \{-1,0,1\} \times \mathbb{Z}$ tel que $s = t + 3c$. Statut : **PROUVÉ**. Preuve : posons $c = \lfloor (s+1)/3 \rfloor$ et écrivons $s + 1 = 3c + r$ avec $r \in \{0,1,2\}$ ; alors $t = s - 3c = r - 1 \in \{-1,0,1\}$, ce qui donne l'existence. Pour l'unicité, si $t + 3c = t' + 3c'$, alors $t - t' = 3(c' - c)$ ; or $|t - t'| \leq 2 < 3$, donc $c = c'$ et $t = t'$. $\square$

Deux conséquences méritent d'être notées. D'abord, si $|s| \leq 3$, alors $|c| \leq (|s| + |t|)/3 \leq 4/3 < 2$, donc la retenue reste elle-même un trit : c'est l'invariant qui rend l'additionneur possible. Ensuite, la table de décomposition est complète et tient en sept lignes :

| $s$ | trit $t$ | retenue $c$ |
|---|---|---|
| $-3$ | $0$ | $\bar{1}$ |
| $-2$ | $1$ | $\bar{1}$ |
| $-1$ | $\bar{1}$ | $0$ |
| $0$ | $0$ | $0$ |
| $+1$ | $1$ | $0$ |
| $+2$ | $\bar{1}$ | $1$ |
| $+3$ | $0$ | $1$ |

Déroulons le calcul, position par position, en partant de $c_0 = 0$.

Position $0$ : les trits de poids faible de $7$ et de $-5$ valent tous deux $1$, donc

$$s_0 = 1 + 1 + 0 = 2 = (-1) + 3 \cdot 1 \quad\Rightarrow\quad t_0 = \bar{1},\; c_1 = 1.$$

Position $1$ :

$$s_1 = (-1) + 1 + 1 = 1 = 1 + 3 \cdot 0 \quad\Rightarrow\quad t_1 = 1,\; c_2 = 0.$$

Position $2$ :

$$s_2 = 1 + (-1) + 0 = 0 \quad\Rightarrow\quad t_2 = 0,\; c_3 = 0.$$

Le résultat se lit $(t_2\,t_1\,t_0) = 0\,1\,\bar{1}$, soit

$$7 + (-5) = (0\,1\,\bar{1})_3 = 0\cdot 9 + 1\cdot 3 - 1 = 2.$$

Le fait notable est à la position $0$ : une somme *positive* ($2$) produit un trit *négatif* ($\bar{1}$) et une retenue positive. Le codage équilibré n'a pas de bit de signe séparé ; le signe est distribué dans chaque trit. C'est exactement ce qui rend la négation gratuite — et ce qui déroute l'intuition binaire. Le chapitre 2 donnera les tables complètes à neuf entrées et traitera les mots de longueur quelconque.

### Trois chemins de lecture

Ce livre se lit de trois manières, et j'ai voulu qu'aucune ne soit frustrante.

- **Le lecteur curieux** prendra les chapitres 1, 3 et 5, puis les chapitres 13, 14 et 15 : il verra l'objet, les logiques à trois valeurs, l'économie de radix et le verdict, sans entrer dans la mécanique des circuits.
- **Le praticien** — concepteur de circuits ou ingénieur en apprentissage — suivra les chapitres 1, 2, 4, 6, 7, 8, puis 10 : codage, arithmétique, portes natives, additionneurs, conversions, minimisation par SAT, quantification des poids.
- **Le théoricien** ira aux chapitres 9, 11, 12, 15 et 16 : lemmes L-T1 et L-T2, encodages SAT, classes de complexité, transfert vers le programme RTC.

Chaque chapitre suit la même pente : intuition, définition, énoncé, exemple calculé, exercice. Les formules sont nombreuses, mais chacune dit ce qu'elle signifie avant de dire ce qu'elle prouve ; le lecteur pressé peut lire les énoncés et les exemples, le lecteur exigeant peut tout vérifier.

### Avant-goût du programme RTC

Le dernier chapitre transfère les acquis vers le programme RTC — traductions à ressources et complexité. On y mesurera une traduction par un vecteur de ressources, par exemple

$$R(C) = \bigl(S(C),\; D(C),\; W(C)\bigr)$$

pour la taille, la profondeur et la largeur d'un circuit $C$, et l'on demandera : quelles sont les constantes optimales dans L-T2 ? quelle profondeur minimale pour un convertisseur double rail ? quel jeu de portes natives ternaires minimise le coût de traduction ? Statut : **OUVERT** — ce livre ne résout pas ces questions ; il les formule proprement, ce qui est déjà une manière de progresser.

Le reste du livre n'est que l'application patiente de la discipline annoncée dans cette introduction : énoncer avec un statut, compter avec des formules, vérifier avec des exemples, et dire clairement ce que l'on ne sait pas. Le trit, lui, attend au chapitre 1.