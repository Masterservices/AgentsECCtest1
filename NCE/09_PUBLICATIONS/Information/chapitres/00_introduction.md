## Introduction

### Le problème des traductions

Traduire, c'est transporter. Quand on traduit un texte d'une langue à une autre, on accepte qu'un résidu se perde, qu'une nuance s'altère, qu'une structure se réorganise. Les traductions entre modèles de calcul obéissent à une logique analogue, mais avec une rigueur que la langue naturelle ne connaît pas : traduire une machine de Turing en circuit booléen, un réseau de neurones en programme réversible, une représentation binaire en représentation ternaire, c'est transformer un objet computationnel en un autre tout en contrôlant — ou en subissant — ce qui se conserve, ce qui se dissipe, ce qui se dilate.

Ce livre est né d'une conviction que je formule ainsi : la théorie de l'information fournit le registre commun le plus naturel pour mesurer ces traductions. Non pas comme métaphore vague, mais comme instrument quantitatif. L'entropie de Shannon mesure l'incertitude qu'une source porte ; la complexité de Kolmogorov mesure l'information irréductible d'un objet ; le coût de Landauer mesure l'énergie minimale qu'une opération irréversible dissipe ; la complexité de communication de Yao mesure les bits qu'il faut échanger pour résoudre un problème distribué. Chacune de ces grandeurs capture une facette du coût d'une traduction. Mon propos est de les rassembler dans un cadre unique et de montrer comment elles s'articulent.

### L'information comme monnaie commune

Considérons une source discrète $X$ prenant ses valeurs dans un alphabet fini $\mathcal{X}$ selon une distribution $p$. L'entropie de Shannon, introduite en 1948, quantifie l'incertitude moyenne de cette source :

$$H(X) \;=\; -\sum_{x \in \mathcal{X}} p(x)\,\log_2 p(x).$$

**Énoncé en mots.** L'entropie est la quantité moyenne d'information, mesurée en bits, produite par un tirage de la source. **Conditions de validité.** $p$ est une distribution de probabilité sur un ensemble fini ; le logarithme est pris en base 2. **Statut.** PROUVÉ (Shannon 1948). **Exemple numérique.** Pour une source binaire équiprobable, $p(0)=p(1)=1/2$ : $H(X) = -2 \cdot \tfrac{1}{2}\log_2\tfrac{1}{2} = 1$ bit. Pour une source biaisée $p(0)=0{,}9$, $p(1)=0{,}1$ : $H(X) = -0{,}9\log_2 0{,}9 - 0{,}1\log_2 0{,}1 \approx 0{,}469$ bit.

Cette grandeur est la première « monnaie » du registre. Mais elle ne suffit pas. Quand on traduit un objet $x$ d'un modèle à un autre, la question n'est plus « quelle incertitude la source porte-t-elle ? » mais « quelle est la complexité intrinsèque de l'objet lui-même ? ». La complexité de Kolmogorov répond à cette question. Pour une machine de Turing universelle $U$, on définit :

$$K_U(x) \;=\; \min\bigl\{\,|p| \;:\; U(p) = x\,\bigr\},$$

où $|p|$ désigne la longueur du programme $p$ en bits. **Énoncé en mots.** $K_U(x)$ est la longueur du plus court programme qui, exécuté sur $U$, produit $x$ puis s'arrête. **Conditions de validité.** $U$ est une machine de Turing universelle fixée ; $x$ est une chaîne binaire finie. **Statut.** CONNU (Kolmogorov 1965, Solomonoff 1964, Chaitin 1966). **Exemple numérique.** La chaîne $x = 0^{1000}$ (mille zéros) admet un programme de l'ordre de $\log_2 1000 + O(1) \approx 10 + O(1)$ bits (« imprimer 1000 zéros »), tandis qu'une chaîne aléatoire de même longueur exige un programme de taille proche de 1000 bits.

Le miracle — et c'est le cœur de ce livre — est que cette grandeur est *invariante à une constante additive près* lorsqu'on change de machine universelle. Si $U$ et $V$ sont deux machines universelles :

$$K_U(x) \;\leq\; K_V(x) \;+\; c_{U,V},$$

où $c_{U,V}$ est une constante qui ne dépend que de $U$ et $V$, jamais de $x$. **Énoncé en mots.** La complexité de Kolmogorov est robuste au choix du modèle de calcul : la traduction d'une machine à l'autre ne coûte qu'un overhead constant. **Conditions de validité.** $U$ et $V$ sont des machines de Turing universelles ; $x$ est une chaîne finie arbitraire. **Statut.** PROUVÉ (Kolmogorov 1965). **Exemple numérique.** Si $c_{U,V} = 200$ bits, alors pour toute chaîne $x$ de longueur un million, la différence relative $c_{U,V}/|x| = 0{,}02\%$ est négligeable. C'est cette robustesse qui fait de $K$ un invariant de traduction au sens fort.

### Traductions, coûts et contraintes

Une traduction entre modèles de calcul n'est jamais gratuite. Elle a un coût en temps, en espace, en profondeur de circuit, en énergie dissipée. Le coût énergétique minimal d'une opération irréversible — l'effacement d'un bit — est donné par la borne de Landauer :

$$E_{\min} \;=\; k_B\, T\, \ln 2,$$

où $k_B$ est la constante de Boltzmann et $T$ la température absolue du bain thermique. **Énoncé en mots.** Effacer un bit d'information dans un environnement à la température $T$ dissipe au moins $k_B T \ln 2$ joules de chaleur. **Conditions de validité.** Le processus est irréversible ; le système est en contact avec un réservoir thermique à l'équilibre. **Statut.** PROUVÉ (Landauer 1961). **Exemple numérique.** À température ambiante $T = 300$ K : $E_{\min} = 1{,}38 \times 10^{-23} \times 300 \times \ln 2 \approx 2{,}87 \times 10^{-21}$ J par bit effacé.

Bennett a montré en 1973 qu'un calcul *réversible* peut en principe contourner cette borne. L'idée est que si l'on conserve l'information au lieu de l'effacer, la dissipation peut être rendue arbitrairement faible :

$$Q_{\text{rev}} \;\to\; 0 \quad \text{(à vitesse de calcul fixée, en limite quasi-statique).}$$

**Énoncé en mots.** Un calcul logiquement réversible, exécuté de manière quasi-statique, peut dissiper une énergie tendant vers zéro. **Conditions de validité.** Le calcul est réversible (bijection sur les états) ; l'exécution est suffisamment lente. **Statut.** PROUVÉ (Bennett 1973). **Exemple numérique.** Un additionneur réversible de $n$ bits n'efface aucun bit intermédiaire ; la chaleur dissipée par porte logique peut être rendue inférieure à $10^{-3} \, k_B T \ln 2$ en ralentissant le calcul d'un facteur $10^3$.

Du côté de la communication, la complexité de Yao mesure le nombre minimal de bits que deux agents, Alice et Bob, doivent échanger pour calculer une fonction $f(x,y)$ :

$$D(f) \;=\; \min_{\Pi} \;\max_{(x,y)}\; |\Pi(x,y)|,$$

où $\Pi$ parcourt tous les protocoles déterministes corrects. **Énoncé en mots.** $D(f)$ est le nombre de bits échangés dans le pire cas par le meilleur protocole déterministe qui calcule $f$. **Conditions de validité.** $f : \{0,1\}^n \times \{0,1\}^n \to \{0,1\}$ ; Alice connaît $x$, Bob connaît $y$ ; le protocole est déterministe. **Statut.** CONNU (Yao 1979). **Exemple numérique.** Pour la fonction d'égalité $\text{EQ}(x,y) = \mathbf{1}[x=y]$, on montre $D(\text{EQ}) = n + 1$ : Alice doit envoyer sa chaîne entière (plus un bit de conclusion) dans le pire cas.

Enfin, la traduction d'une représentation numérique vers une autre pose la question de l'économie de radix. Pour représenter un entier parmi $n$ valeurs possibles dans une base $b$, le coût en « digits × valeurs de digit » est :

$$E(b,\, n) \;=\; b \cdot \lceil \log_b n \rceil.$$

**Énoncé en mots.** $E(b,n)$ est le produit du nombre de symboles de la base par le nombre de chiffres nécessaires pour coder $n$ valeurs distinctes. **Conditions de validité.** $b \geq 2$ entier, $n \geq 1$ entier. **Statut.** CONNU. **Exemple numérique.** Pour $n = 10^6$ : en base 2, $E(2, 10^6) = 2 \times 20 = 40$ ; en base 3, $E(3, 10^6) = 3 \times 13 = 39$ ; en base $e \approx 2{,}718$ (optimum continu), le coût est minimal. La traduction binaire $\to$ ternaire économise ici un coût relatif de $2{,}5\%$.

### L'information comme prisme : du canal au goulot

Entre la source et le destinataire d'une traduction se trouve un canal. La capacité de ce canal, notée $C$, est le débit maximal d'information fiable :

$$C \;=\; \max_{p(x)}\; I(X;\,Y),$$

où $I(X;Y)$ est l'information mutuelle entre l'entrée $X$ et la sortie $Y$ du canal. **Énoncé en mots.** La capacité est le supremum, sur toutes les distributions d'entrée, de l'information mutuelle entre entrée et sortie. **Conditions de validité.** Le canal est discret, sans mémoire, caractérisé par $p(y|x)$. **Statut.** PROUVÉ (Shannon 1948). **Exemple numérique.** Pour un canal binaire symétrique de probabilité d'erreur $\varepsilon = 0{,}1$ : $C = 1 - H(\varepsilon) = 1 - (-0{,}1\log_2 0{,}1 - 0{,}9\log_2 0{,}9) \approx 1 - 0{,}469 = 0{,}531$ bit par utilisation.

L'information mutuelle elle-même se définit à partir des entropies :

$$I(X;\,Y) \;=\; H(X) \;-\; H(X \mid Y) \;=\; H(Y) \;-\; H(Y \mid X).$$

**Énoncé en mots.** L'information mutuelle est la réduction d'incertitude sur $X$ apportée par la connaissance de $Y$ (et réciproquement). **Conditions de validité.** $X$ et $Y$ sont des variables aléatoires discrètes de distributions conjointes bien définies. **Statut.** PROUVÉ (Shannon 1948). **Exemple numérique.** Si $X$ est uniforme sur $\{0,1\}$ et $Y = X$ (canal parfait), $H(X|Y) = 0$ donc $I(X;Y) = 1$ bit. Si $Y$ est indépendant de $X$, $H(X|Y) = H(X)$ donc $I(X;Y) = 0$.

Une propriété fondamentale gouverne toute chaîne de traductions successives. Si $X \to Y \to Z$ forme une chaîne de Markov (la traduction de $X$ en $Y$, puis de $Y$ en $Z$), alors :

$$I(X;\,Z) \;\leq\; I(X;\,Y).$$

**Énoncé en mots.** L'inégalité de traitement des données affirme qu'une traduction supplémentaire ne peut jamais augmenter l'information sur la source : on ne crée pas d'information en post-traitant. **Conditions de validité.** $X \to Y \to Z$ est une chaîne de Markov, c'est-à-dire $p(z|x,y) = p(z|y)$. **Statut.** PROUVÉ (Cover et Thomas 1991). **Exemple numérique.** Si $I(X;Y) = 0{,}8$ bit et que $Z$ est obtenu de $Y$ par un canal binaire symétrique de bruit $\varepsilon = 0{,}2$, alors $I(X;Z) \leq 0{,}8$ bit ; en pratique $I(X;Z) \approx 0{,}8 \times (1 - H(0{,}2)) \approx 0{,}8 \times 0{,}278 \approx 0{,}222$ bit.

Cette inégalité est la clé de voûte du goulot d'information, formalisé par Tishby, Pereira et Bialek (1999) :

$$\min_{p(t|x)}\; \bigl[\, I(X;\,T) \;-\; \beta\, I(T;\,Y) \,\bigr],$$

où $T$ est une représentation intermédiaire, $\beta > 0$ un paramètre de compromis. **Énoncé en mots.** Le goulot d'information cherche la représentation $T$ qui comprime $X$ au maximum (premier terme minimal) tout en préservant l'information pertinente pour prédire $Y$ (second terme maximal). **Conditions de validité.** $X$, $Y$ sont des variables aléatoires conjointes ; $T$ est un canal stochastique de $X$. **Statut.** CONNU (Tishby, Pereira et Bialek 1999). **Exemple numérique.** Si $H(X) = 10$ bits, $I(X;Y) = 4$ bits et $\beta = 1$, une représentation $T$ avec $I(X;T) = 5$ bits et $I(T;Y) = 3{,}8$ bits donne un coût de $5 - 3{,}8 = 1{,}2$, tandis que $T = X$ donne $10 - 4 = 6$ : la compression est préférable.

### Démarche et méthode

La démarche de ce livre est triple. Premièrement, *exposer* : chaque outil informationnel est présenté avec sa définition, son intuition, ses preuves ou idées de preuve, ses conditions de validité. Deuxièmement, *relier* : je montre comment ces outils s'appliquent concrètement à des traductions entre modèles — machine de Turing vers circuit, représentation binaire vers ternaire, calcul irréversible vers réversible, réseau de neurones vers programme symbolique. Troisièmement, *transférer* : le dernier chapitre synthétise ce que ce registre informationnel apporte au programme RTC (Ressources, Traductions, Contraintes), qui classe les ressources computationnelles (taille, temps, mémoire, profondeur, largeur, précision, partage) et étudie les contraintes que l'information impose à leur manipulation.

Chaque affirmation est étiquetée par un statut explicite : PROUVÉ, CONNU, EXPÉRIMENTAL, CONJECTURE, RÉFUTÉ ou OUVERT. Ce choix reflète une exigence épistémologique : le lecteur doit toujours savoir s'il lit un théorème démontré, un résultat classique accepté, une observation empirique, une hypothèse raisonnable ou une question sans réponse. Je m'interdis toute annonce de découverte et toute présentation d'une intuition comme preuve.

### À qui s'adresse ce livre

Ce livre s'adresse à un lecteur cultivé, curieux, disposant d'une familiarité avec les mathématiques de niveau licence (probabilités élémentaires, logique, algorithmique de base) mais n'étant pas nécessairement spécialiste en théorie de l'information ou en théorie de la calculabilité. Chaque concept est accompagné d'une intuition, d'une définition formelle, d'un énoncé, d'un exemple numérique calculé pas à pas et, lorsque c'est pertinent, d'un exercice. Le chercheur en informatique théorique y trouvera une synthèse organisée autour d'un fil conducteur original ; l'étudiant en master y trouvera un chemin progressif ; l'ingénieur curieux y trouvera des ordres de grandeur concrets et des liens entre des domaines souvent enseignés séparément.

### Plan de l'ouvrage

Le livre se compose de quatre parties et seize chapitres.

**Partie I — Entropie, codage et canaux : la grammaire informationnelle.** Les chapitres 1 à 4 posent les fondations : entropie de Shannon et mesure de l'incertitude (chapitre 1), information mutuelle et inégalité de traitement des données (chapitre 2), codage de source et compression optimale (chapitre 3), codage de canal, capacité et fiabilité (chapitre 4). Cette partie fournit le vocabulaire et les premières bornes.

**Partie II — Complexité de Kolmogorov : l'invariant de traduction.** Les chapitres 5 à 8 développent l'outil central : définition et premières propriétés de $K$ (chapitre 5), théorème d'invariance et signification de la constante additive (chapitre 6), non-calculabilité et indécidabilité (chapitre 7), lien avec l'induction de Solomonoff et l'information algorithmique (chapitre 8). Cette partie établit que $K$ est l'invariant de traduction le plus robuste dont on dispose.

**Partie III — Communication, énergie et représentation : coûts de traduction.** Les chapitres 9 à 12 quantifient les coûts : complexité de communication de Yao (chapitre 9), jeux de Karchmer-Wigderson et profondeur des formules (chapitre 10), coût énergétique de Landauer et réversibilité de Bennett (chapitre 11), économie de radix et coût de représentation (chapitre 12). Cette partie montre que toute traduction a un prix mesurable.

**Partie IV — Goulots d'information, synthèse et transfert vers RTC.** Les chapitres 13 à 16 culminent : le goulot d'information dans les réseaux de neurones (chapitre 13), la synthèse unificatrice (chapitre 14), les questions ouvertes et conjectures (chapitre 15), et enfin le transfert vers le programme RTC — quelles ressources sont gouvernées par quelles contraintes informationnelles, quelles traductions restent à analyser (chapitre 16).

### Conventions typographiques et notations

Les formules sont composées en LaTeX. Les logarithmes sont en base 2 sauf mention explicite contraire. Les chaînes binaires sont notées $x \in \{0,1\}^*$, leur longueur $|x|$. La notation $O(1)$ désigne une constante indépendante de la taille de l'entrée. Le symbole $\triangleq$ signale une définition. Les statuts épistémiques apparaissent en petites capitales : PROUVÉ, CONNU, EXPÉRIMENTAL, CONJECTURE, RÉFUTÉ, OUVERT.

Une dernière remarque avant d'entrer dans le vif. Ce livre ne prétend pas clore le sujet. La théorie de l'information offre un *registre*, non une théorie complète de toutes les traductions computationnelles. Des questions restent ouvertes — la caractérisation exacte des surcoûts de traduction entre certains modèles, l'extension du goulot d'information à des architectures profondes arbitraires, la quantification fine du partage de sous-calculs dans les circuits. Le chapitre 15 les recense sans fausse modestie. Le chapitre 16 trace les directions que le programme RTC permet d'envisager. Mon ambition est plus modeste et, je l'espère, plus utile : donner au lecteur une carte cohérente, honnête sur ses lacunes, riche en formules et en exemples, pour naviguer dans le paysage des traductions computationnelles à travers le prisme de l'information.

Commençons par la source de toute mesure : l'entropie.

## Chapitre 1 — Entropie de Shannon : mesurer l'incertitude d'une source

### Pourquoi mesurer l'incertitude ?

Avant de traduire, il faut savoir ce que l'on transporte. Une source qui produit toujours le même symbole ne porte aucune information : sa traduction est triviale, son coût nul. Une source qui tire ses symboles au hasard, sans structure exploitable, porte un maximum d'information : toute traduction fidèle doit en préserver la totalité. Entre ces deux extrêmes se situe le territoire que ce chapitre explore.

L'entropie de Shannon, introduite en 1948, est la grandeur qui quantifie cette incertitude. Elle répond à une question simple en apparence, profonde en réalité : *combien de bits faut-il, en moyenne, pour décrire le résultat d'un tirage de la source ?* Cette question est la première brique de notre registre informationnel. Sans elle, aucune mesure de coût de traduction n'a de point d'ancrage.

### L'information propre d'un événement

Considérons une source discrète $X$ prenant ses valeurs dans un alphabet fini $\mathcal{X} = \{x_1, x_2, \ldots, x_n\}$ selon une distribution de probabilité $p$. Avant de définir l'entropie, définissons l'information portée par un événement individuel.

$$\iota(x) \;\triangleq\; -\log_2 p(x).$$

**Énoncé en mots.** L'information propre (ou surprisal) d'un événement $x$ est le logarithme en base 2 de l'inverse de sa probabilité. Plus l'événement est rare, plus il « surprend », plus il porte d'information. **Conditions de validité.** $p(x) > 0$ ; si $p(x) = 0$, on pose par convention $\iota(x) = +\infty$. **Statut.** PROUVÉ (Shannon 1948). **Exemple numérique.** Si $p(x) = 1/8$, alors $\iota(x) = -\log_2(1/8) = 3$ bits. Si $p(x) = 1$, alors $\iota(x) = 0$ : un événement certain ne surprend pas.

Cette définition n'est pas arbitraire. Elle est la seule fonction $f : (0,1] \to \mathbb{R}^+$ satisfaisant simultanément trois exigences : (i) $f$ est continue ; (ii) $f$ est décroissante ; (iii) $f(pq) = f(p) + f(q)$ pour tout $p, q \in (0,1]$ (l'information de deux événements indépendants s'additionne). Ces trois axiomes caractérisent $f(p) = -\log_2 p$ à un facteur multiplicatif près, fixé par le choix de la base.

### Définition de l'entropie

L'entropie est l'espérance de l'information propre :

$$H(X) \;\triangleq\; \mathbb{E}[\iota(X)] \;=\; -\sum_{x \in \mathcal{X}} p(x)\,\log_2 p(x).$$

**Énoncé en mots.** L'entropie de $X$ est la quantité moyenne d'information, en bits, produite par un tirage de la source. **Conditions de validité.** $\mathcal{X}$ est fini ; $p$ est une distribution de probabilité ; on adopte la convention $0 \log_2 0 = 0$. **Statut.** PROUVÉ (Shannon 1948). **Exemple numérique.** Source ternaire $\mathcal{X} = \{a, b, c\}$ avec $p(a) = 1/2$, $p(b) = 1/4$, $p(c) = 1/4$. Calcul : $H(X) = -\tfrac{1}{2}\log_2\tfrac{1}{2} - \tfrac{1}{4}\log_2\tfrac{1}{4} - \tfrac{1}{4}\log_2\tfrac{1}{4} = \tfrac{1}{2} + \tfrac{1}{2} + \tfrac{1}{2} = 1{,}5$ bit.

On peut réécrire cette définition en termes d'espérance, ce qui sera utile pour les manipulations ultérieures :

$$H(X) \;=\; \sum_{x \in \mathcal{X}} p(x)\,\iota(x) \;=\; \sum_{x \in \mathcal{X}} p(x)\,\log_2 \frac{1}{p(x)}.$$

**Énoncé en mots.** L'entropie est la moyenne pondérée des surprisals, les poids étant les probabilités elles-mêmes. **Statut.** PROUVÉ (Shannon 1948). Cette reformulation est une identité immédiate.

### Entropie binaire : le cas à un paramètre

Le cas le plus fréquent est celui d'une source binaire $X \in \{0, 1\}$ avec $p(1) = p$ et $p(0) = 1 - p$. On note :

$$h(p) \;\triangleq\; -p\,\log_2 p \;-\; (1-p)\,\log_2(1-p).$$

**Énoncé en mots.** $h(p)$ est l'entropie d'une source binaire de paramètre $p$. **Conditions de validité.** $p \in [0,1]$, convention $0\log_2 0 = 0$. **Statut.** PROUVÉ (Shannon 1948). **Exemple numérique.** Pour $p = 0{,}3$ : $h(0{,}3) = -0{,}3\log_2 0{,}3 - 0{,}7\log_2 0{,}7$. On calcule : $\log_2 0{,}3 = \ln 0{,}3 / \ln 2 \approx -1{,}204/0{,}693 \approx -1{,}737$, donc $-0{,}3 \times (-1{,}737) \approx 0{,}521$. De même $\log_2 0{,}7 \approx -0{,}515$, donc $-0{,}7 \times (-0{,}515) \approx 0{,}360$. Total : $h(0{,}3) \approx 0{,}881$ bit.

La fonction $h$ est symétrique ($h(p) = h(1-p)$), concave, nulle en $p = 0$ et $p = 1$, et maximale en $p = 1/2$ où $h(1/2) = 1$ bit.

### Propriétés fondamentales

**Non-négativité.** Pour toute source discrète :

$$H(X) \;\geq\; 0,$$

avec égalité si et seulement si $X$ est déterministe (un seul symbole de probabilité 1). **Statut.** PROUVÉ (Shannon 1948). **Preuve.** Chaque terme $-p(x)\log_2 p(x) \geq 0$ car $p(x) \in [0,1]$ implique $\log_2 p(x) \leq 0$. La somme de termes positifs est positive. L'égalité exige $p(x) \in \{0, 1\}$ pour tout $x$. $\square$

**Borne supérieure.** Pour une source à $n$ symboles :

$$H(X) \;\leq\; \log_2 n,$$

avec égalité si et seulement si la distribution est uniforme : $p(x_i) = 1/n$ pour tout $i$. **Conditions de validité.** $|\mathcal{X}| = n < \infty$. **Statut.** PROUVÉ (Shannon 1948). **Idée de preuve.** On applique l'inégalité de Gibbs (ou l'inégalité de Jensen à la fonction concave $\log$) à la divergence de Kullback-Leibler entre $p$ et la distribution uniforme. **Exemple numérique.** Pour $n = 8$ : $H(X) \leq \log_2 8 = 3$ bits, atteint quand chaque symbole a probabilité $1/8$.

**Concavité.** Pour deux distributions $p$ et $q$ sur $\mathcal{X}$ et tout $\lambda \in [0,1]$ :

$$H(\lambda p + (1-\lambda)q) \;\geq\; \lambda\, H(p) \;+\; (1-\lambda)\, H(q).$$

**Énoncé en mots.** L'entropie est une fonction concave de la distribution. Mélanger deux sources ne peut que maintenir ou augmenter l'incertitude moyenne. **Conditions de validité.** $p$, $q$ distributions sur le même alphabet ; $\lambda \in [0,1]$. **Statut.** PROUVÉ (Shannon 1948 ; Cover et Thomas 1991). **Exemple numérique.** $p = (1, 0)$ donne $H(p) = 0$ ; $q = (0, 1)$ donne $H(q) = 0$. Le mélange $\lambda = 1/2$ donne $(1/2, 1/2)$, d'entropie $1$ bit $\geq 0$.

### Entropie conjointe et entropie conditionnelle

Quand deux sources $X$ et $Y$ sont observées simultanément, l'incertitude totale est mesurée par l'entropie conjointe :

$$H(X, Y) \;\triangleq\; -\sum_{x \in \mathcal{X}} \sum_{y \in \mathcal{Y}} p(x, y)\,\log_2 p(x, y).$$

**Énoncé en mots.** $H(X,Y)$ est l'information moyenne du couple $(X,Y)$. **Conditions de validité.** $p(x,y)$ est une distribution conjointe sur $\mathcal{X} \times \mathcal{Y}$. **Statut.** PROUVÉ (Shannon 1948). **Exemple numérique.** Si $X$ et $Y$ sont indépendants, uniformes sur $\{0,1\}$ : $p(x,y) = 1/4$ pour chaque paire, $H(X,Y) = -4 \times \tfrac{1}{4}\log_2\tfrac{1}{4} = 2$ bits.

L'entropie conditionnelle mesure l'incertitude résiduelle sur $X$ une fois $Y$ connu :

$$H(X \mid Y) \;\triangleq\; -\sum_{y \in \mathcal{Y}} p(y) \sum_{x \in \mathcal{X}} p(x \mid y)\,\log_2 p(x \mid y).$$

**Énoncé en mots.** $H(X|Y)$ est l'incertitude moyenne restante sur $X$ après observation de $Y$. **Conditions de validité.** $p(x|y)$ bien définie pour tout $y$ avec $p(y) > 0$. **Statut.** PROUVÉ (Shannon 1948). **Exemple numérique.** Si $Y = X$ (connaissance parfaite), $p(x|y) \in \{0,1\}$, donc $H(X|Y) = 0$. Si $Y$ est indépendant de $X$, $H(X|Y) = H(X)$.

Ces deux grandeurs sont reliées par la règle de la chaîne :

$$H(X, Y) \;=\; H(Y) \;+\; H(X \mid Y) \;=\; H(X) \;+\; H(Y \mid X).$$

**Énoncé en mots.** L'incertitude du couple se décompose en l'incertitude sur l'une des variables plus l'incertitude résiduelle sur l'autre. **Conditions de validité.** Distribution conjointe bien définie. **Statut.** PROUVÉ (Shannon 1948). **Preuve.** On écrit $p(x,y) = p(y)\,p(x|y)$, on prend $-\log_2$ des deux côtés : $-\log_2 p(x,y) = -\log_2 p(y) - \log_2 p(x|y)$, puis on somme sur $(x,y)$ pondéré par $p(x,y)$. $\square$ **Exemple numérique.** $H(X) = 1$ bit (source binaire uniforme), $H(Y|X) = 0{,}5$ bit. Alors $H(X,Y) = 1 + 0{,}5 = 1{,}5$ bit.

### Additivité pour les sources indépendantes

Si $X$ et $Y$ sont indépendantes :

$$H(X, Y) \;=\; H(X) \;+\; H(Y).$$

**Énoncé en mots.** L'entropie de deux sources indépendantes est la somme de leurs entropies. **Conditions de validité.** $p(x,y) = p(x)\,p(y)$ pour tout $(x,y)$. **Statut.** PROUVÉ (Shannon 1948). **Preuve.** L'indépendance donne $H(X|Y) = H(X)$ ; on applique la règle de la chaîne. $\square$ **Exemple numérique.** Deux dés équitables indépendants à 6 faces : $H = \log_2 6 + \log_2 6 = 2\log_2 6 \approx 5{,}17$ bits.

Plus généralement, pour $n$ variables indépendantes $X_1, \ldots, X_n$ :

$$H(X_1, X_2, \ldots, X_n) \;=\; \sum_{i=1}^{n} H(X_i).$$

**Statut.** PROUVÉ. La preuve se fait par récurrence sur $n$ à partir du cas $n = 2$.

### Changement de base et unités

L'entropie dépend du logarithme choisi. En base $b$ :

$$H_b(X) \;=\; -\sum_{x} p(x)\,\log_b p(x) \;=\; \frac{H_2(X)}{\log_2 b}.$$

**Énoncé en mots.** Passer de la base 2 à la base $b$ divise l'entropie par $\log_2 b$. **Conditions de validité.** $b > 1$. **Statut.** PROUVÉ (Cover et Thomas 1991). **Exemple numérique.** $H_2(X) = 3$ bits. En base $e$ (nats) : $H_e(X) = 3/\log_2 e = 3/1{,}4427 \approx 2{,}079$ nats. En base 10 (hartleys) : $H_{10}(X) = 3/\log_2 10 \approx 3/3{,}3219 \approx 0{,}903$ hartley.

Dans tout ce livre, sauf mention contraire, le logarithme est en base 2 et l'unité est le bit. Ce choix est cohérent avec la représentation binaire qui domine les modèles de calcul étudiés ; le chapitre 12 examinera ce qu'il advient quand on traduit vers d'autres bases.

### Entropie d'un mélange de sources

Soit $Z$ une variable qui vaut $X$ avec probabilité $\lambda$ et $Y$ avec probabilité $1 - \lambda$, où $X$ et $Y$ sont des sources sur le même alphabet. L'entropie du mélange satisfait :

$$H(Z) \;=\; \lambda\, H(X) + (1-\lambda)\, H(Y) + h(\lambda),$$

où $h(\lambda) = -\lambda\log_2\lambda - (1-\lambda)\log_2(1-\lambda)$ est l'entropie binaire du choix. **Énoncé en mots.** L'entropie du mélange est la moyenne pondérée des entropies plus l'incertitude sur le choix de la source. **Conditions de validité.** $X$ et $Y$ sur le même alphabet ; $\lambda \in (0,1)$. **Statut.** PROUVÉ (Cover et Thomas 1991). **Exemple numérique.** $H(X) = 0$ (source déterministe « a »), $H(Y) = 1$ bit (source binaire uniforme), $\lambda = 1/2$. Alors $H(Z) = 0 + 0{,}5 + 1 = 1{,}5$ bit. Le bit supplémentaire vient de l'incertitude « quelle source a été choisie ? ».

### Entropie et traduction : première connexion

Quel lien avec les traductions entre modèles de calcul ? Considérons une source $X$ dont les sorties sont des programmes pour une machine $M_1$. Traduire ces programmes vers une machine $M_2$ revient à appliquer une fonction (éventuellement stochastique) $T$ :

$$Y \;=\; T(X).$$

Si $T$ est déterministe, la chaîne $X \to Y$ est une chaîne de Markov triviale, et l'inégalité de traitement des données (que nous développerons au chapitre 2) impose :

$$H(Y) \;\leq\; H(X).$$

**Énoncé en mots.** Une traduction déterministe ne peut pas augmenter l'entropie de la source. Elle peut la préserver (si $T$ est injective) ou la réduire (si $T$ fusionne des symboles). **Conditions de validité.** $T$ est une fonction mesurable ; $X$ est une variable aléatoire discrète. **Statut.** PROUVÉ (Cover et Thomas 1991). **Exemple numérique.** Si $X$ est uniforme sur $\{0,1\}^3$ ($H(X) = 3$ bits) et $T$ extrait le premier bit, $Y \in \{0,1\}$ uniforme, $H(Y) = 1$ bit. La traduction a perdu 2 bits d'entropie.

Cette observation est la première manifestation d'un principe que le livre déclinera sous toutes ses formes : *une traduction ne crée pas d'information ; elle la préserve, la comprime ou la dissipe.*

### Entropie et longueur de description

L'entropie possède une interprétation opérationnelle que le chapitre 3 développera : elle est la limite inférieure du nombre moyen de bits par symbole pour tout code sans perte. Formellement, pour tout code prefixe $C$ :

$$\mathbb{E}[|C(X)|] \;\geq\; H(X),$$

où $|C(x)|$ est la longueur du mot de code associé à $x$. **Énoncé en mots.** Aucun code prefixe ne peut encoder la source en moins de $H(X)$ bits par symbole en moyenne. **Conditions de validité.** Le code est prefixe (aucun mot n'est préfixe d'un autre). **Statut.** PROUVÉ (Shannon 1948). **Exemple numérique.** Pour la source $\{a, b, c\}$ avec $p = (1/2, 1/4, 1/4)$, $H = 1{,}5$ bit. Le code $a \mapsto 0$, $b \mapsto 10$, $c \mapsto 11$ donne une longueur moyenne $0{,}5 \times 1 + 0{,}25 \times 2 + 0{,}25 \times 2 = 1{,}5$ bit : la borne est atteinte.

### Exercices

**Exercice 1.1.** Calculer l'entropie d'un dé équilibré à 6 faces. Puis calculer l'entropie d'un dé pipé avec $p(1) = 1/2$ et $p(2) = p(3) = p(4) = p(5) = p(6) = 1/8$. Comparer.

**Exercice 1.2.** Montrer que $h(p) \leq 1$ pour tout $p \in [0,1]$, avec égalité ssi $p = 1/2$. (Indication : utiliser la concavité de $\log$ ou la borne supérieure avec $n = 2$.)

**Exercice 1.3.** Soit $X$ uniforme sur $\{1, 2, \ldots, n\}$ et $Y = X \mod 2$. Calculer $H(X)$, $H(Y)$, $H(X|Y)$. Vérifier la règle de la chaîne.

**Exercice 1.4.** Montrer que si $H(X|Y) = H(X)$, alors $X$ et $Y$ sont indépendantes. (Indication : utiliser la définition de l'entropie conditionnelle et l'unicité de la décomposition.)

### Ce que ce chapitre apporte au registre

L'entropie de Shannon est la première grandeur du registre informationnel. Elle mesure l'incertitude d'une source avant toute traduction. Dans les chapitres suivants, nous verrons comment cette mesure se raffine (information mutuelle, chapitre 2), comment elle borne la compression (chapitre 3), comment elle gouverne la fiabilité sur un canal (chapitre 4). Mais surtout, nous garderons en mémoire la leçon de ce chapitre : une traduction déterministe ne crée pas d'entropie. Ce principe, apparemment modeste, est la première contrainte que l'information impose à toute traduction entre modèles de calcul. Il sera renforcé, généralisé, quantifié tout au long de ce livre.

La source est mesurée. Il reste à comprendre ce que deux sources partagent, ce que l'une révèle de l'autre. C'est l'objet du chapitre suivant : l'information mutuelle.