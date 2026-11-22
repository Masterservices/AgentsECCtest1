## Introduction

### Une discipline de la destruction contrôlée

La cryptographie, dans son acception la plus profonde, n'est pas l'art de cacher. C'est la science des traductions computationnelles conçues pour anéantir l'information exploitable par un adversaire borné en ressources. Cette phrase, qui constitue la thèse directrice de cet ouvrage, mérite d'être dépliée mot à mot.

Une *traduction*, d'abord. Tout acte cryptographique transforme un objet en un autre : un texte clair devient texte chiffré, une graine aléatoire de quelques bits engendre une suite pseudo-aléatoire de longueur arbitraire, un message produit une signature vérifiable mais infalsifiable. Dans chaque cas, on passe d'un espace à un autre, d'une représentation à une autre, d'un modèle de calcul à un autre. La structure syntaxique — la longueur, le format, la possibilité de vérifier — est préservée. La sémantique accessible, elle, est détruite.

*Détruire l'information exploitable*, ensuite. Il ne s'agit pas d'effacer toute trace d'information au sens de Shannon. Le texte chiffré contient, en un sens informationnel absolu, autant de bits que le texte clair. Mais l'adversaire, muni de ressources finies en temps, en mémoire, en profondeur de circuit, ne peut extraire de ces bits aucune connaissance actionnable. La destruction est relative à un modèle de calcul.

*Un adversaire borné en ressources*, enfin. C'est ici que la complexité computationnelle entre en scène. Sans borne sur les ressources de l'adversaire, aucune traduction n'est sûre : un attaquant disposant d'un temps illimité peut toujours énumérer toutes les clés possibles. La cryptographie moderne — depuis Shannon 1949 jusqu'aux constructions contemporaines — est une théorie conditionnelle : elle garantit la sécurité *tant que* certaines ressources restent hors de portée.

Ce livre étudie ces traductions destructrices à travers un prisme particulier : celui du programme que j'appelle le programme RTC, pour *Traductions à Ressources et Complexité*. L'idée directrice est la suivante : chaque primitive cryptographique est une traduction entre espaces de représentations, et toute traduction a un *coût*, un *gain* et une *perte* en ressources. Quelles ressources — taille de la description, temps de calcul, mémoire, profondeur de circuit, largeur, précision arithmétique, possibilité de partage — sont conservées, perdues ou gagnées lors du passage du clair au chiffré, de la graine au pseudo-aléa, du message à la signature ? Quelles barrières fondamentales limitent notre capacité à inverser ces traductions ?

### Le cadre conceptuel : traductions, ressources et statuts

Avant d'entrer dans la matière, je dois présenter le cadre formel qui irrigue chaque chapitre. Il repose sur deux piliers : la notion de *traduction à ressources* et le *registre des statuts*.

Une traduction à ressources est une application calculable

$$
T : \{0,1\}^n \longrightarrow \{0,1\}^{m(n)}
$$

accompagnée d'un vecteur de ressources $(R_1, R_2, \ldots, R_k)$ décrivant le coût de l'évaluation de $T$ et, le cas échéant, le coût de son inversion. Ici, $n$ désigne la taille de l'entrée, $m(n)$ la taille de la sortie, et chaque $R_i$ peut représenter le temps, la mémoire, la profondeur de circuit ou la largeur. **Énoncé en mots** : une traduction à ressources est une fonction binaire dont on comptabilise non seulement l'effet mais aussi le coût sous plusieurs dimensions simultanément. **Conditions de validité** : $T$ doit être calculable en temps polynomial pour être qualifiée de « traduction efficace » ; $m(n)$ doit être polynomial en $n$. **Statut** : définition propre à cet ouvrage. **Exemple numérique** : prenons $n = 4$ et la traduction $T(x) = x \oplus k$ où $k = 1011$. Pour $x = 0110$, on obtient $T(0110) = 0110 \oplus 1011 = 1101$. La taille est conservée ($m(n) = n = 4$), le temps est $O(n) = O(4)$ opérations bit à bit, la mémoire est $O(1)$ bit supplémentaire.

Le registre des statuts, ensuite, est une discipline épistémologique. Chaque affirmation de ce livre porte l'un des six statuts suivants :

- **PROUVÉ** : une démonstration complète est fournie dans le texte.
- **CONNU** : le résultat est établi dans la littérature autorisée ; l'idée de la preuve est donnée.
- **EXPÉRIMENTAL** : le résultat repose sur des calculs ou des simulations.
- **CONJECTURE** : l'énoncé est plausible mais non démontré.
- **RÉFUTÉ** : l'énoncé a été montré faux.
- **OUVERT** : la question est posée, aucune réponse n'est connue.

Ce registre n'est pas un ornement. Il est la colonne vertébrale honnête du livre. Le lecteur saura toujours, à chaque ligne, s'il lit une certitude, une intuition ou un mystère.

### La cryptographie comme théorie des traductions

Pour ancrer la perspective, considérons les cinq primitives fondamentales que ce livre dissèque :

**Le masque jetable.** La traduction est

$$
C = M \oplus K, \quad |K| = |M|
$$

où $M$ est le message, $K$ la clé tirée uniformément, et $C$ le chiffré. Shannon 1949 a démontré que cette traduction est *parfaitement sûre* : la distribution de $C$ est indépendante de $M$. **Énoncé en mots** : si la clé est aussi longue que le message et parfaitement aléatoire, le chiffré ne révèle absolument rien. **Conditions de validité** : $K$ est uniforme sur $\{0,1\}^{|M|}$ et utilisée une seule fois. **Statut** : PROUVÉ (Shannon 1949). **Exemple** : $M = 1010$, $K = 0111$, alors $C = 1010 \oplus 0111 = 1101$. L'entropie conditionnelle $H(M|C) = H(M) = 4$ bits : aucune information n'a fuité.

**La fonction à sens unique.** Une fonction $f : \{0,1\}^n \to \{0,1\}^n$ est à sens unique si elle est calculable en temps polynomial mais si, pour tout adversaire probabiliste polynomial $\mathcal{A}$,

$$
\Pr_{x \leftarrow \{0,1\}^n}\bigl[\mathcal{A}(f(x)) \in f^{-1}(f(x))\bigr] \leq \text{negl}(n)
$$

où $\text{negl}(n)$ désigne une fonction négligeable : pour tout polynôme $p$, $\text{negl}(n) < 1/p(n)$ pour $n$ assez grand. **Énoncé en mots** : on peut calculer $f$ facilement, mais retrouver une préimage est au-delà de toute capacité polynomiale. **Conditions de validité** : l'adversaire est probabiliste, polynomial, et la probabilité est prise sur le tirage uniforme de $x$ et la randomisation interne de $\mathcal{A}$. **Statut** : CONJECTURE (l'existence de fonctions à sens unique est un problème ouvert ; elle impliquerait $\text{P} \neq \text{NP}$). **Exemple numérique** : pour $n = 8$, si $f(x) = x^2 \mod 257$, alors $f(13) = 169 \mod 257 = 169$. Inverser (trouver $x$ tel que $x^2 \equiv 169 \mod 257$) est facile ici par exhaustivité, mais la conjecture porte sur le comportement asymptotique quand $n \to \infty$.

**Le générateur pseudo-aléatoire.** Le théorème de Håstad, Impagliazzo, Levin et Luby 1999 établit que toute fonction à sens unique $f$ permet de construire un générateur pseudo-aléatoire $G : \{0,1\}^s \to \{0,1\}^{\ell(s)}$ avec $\ell(s) > s$. La traduction va d'une graine courte vers une suite longue indiscernable du hasard uniforme. **Énoncé en mots** : le pseudo-aléa est une amplification de complexité — on traduit $s$ bits de « vraie » aléa en $\ell(s)$ bits d'aléa computationnel. **Conditions de validité** : $f$ est à sens unique ; $\ell(s)$ est polynomial en $s$. **Statut** : PROUVÉ (Håstad, Impagliazzo, Levin et Luby 1999). **Exemple** : avec $s = 3$ bits de graine, un générateur pourrait produire $\ell(3) = 6$ bits pseudo-aléatoires ; la traduction « gagne » 3 bits de longueur apparente, mais cette extension est illusoire pour un observateur non borné.

**Le chiffrement probabiliste.** Goldwasser et Micali 1984 ont montré que la sécurité sémantique — l'impossibilité de calculer *tout* bit d'information sur le clair à partir du chiffré — exige l'introduction de randomisation dans la traduction de chiffrement :

$$
\text{Enc}(pk, m; r) \longrightarrow c
$$

où $r$ est la randomisation tirée uniformément. **Énoncé en mots** : la traduction du clair vers le chiffré n'est plus une fonction mais une relation ; un même message admet une exponentielle de chiffrés possibles. **Conditions de validité** : le schéma doit satisfaire l'indistinguabilité IND-CPA. **Statut** : PROUVÉ (Goldwasser et Micali 1984 pour la définition et la première construction). **Exemple** : si $m = 1$ et $r$ est tiré dans $\{0,1\}^{4}$, alors il existe $2^4 = 16$ chiffrés distincts possibles pour le même bit de message.

**La fonction à trappe.** Yao 1982 formalise la notion : une fonction à sens unique $f$ munie d'un piège $t$ tel que, connaissant $t$, l'inversion devient polynomiale. RSA, introduit par Rivest, Shamir et Adleman 1978, en est l'archétype : la traduction $x \mapsto x^e \mod N$ est facile à évaluer, difficile à inverser sans la factorisation de $N$, triviale avec elle.

$$
f(x) = x^e \mod N, \quad f^{-1}(y) = y^d \mod N \text{ si } ed \equiv 1 \pmod{\varphi(N)}
$$

**Énoncé en mots** : l'exponentiation modulaire est une traduction à sens unique munie d'une trappe arithmétique. **Conditions de validité** : $N = pq$ avec $p, q$ premiers grands ; $\gcd(e, \varphi(N)) = 1$. **Statut** : CONNU (Rivest, Shamir et Adleman 1978 ; la sécurité repose sur la conjecture de la difficulté de la factorisation). **Exemple** : $p = 5$, $q = 11$, $N = 55$, $\varphi(N) = 40$, $e = 3$, $d = 27$ (car $3 \times 27 = 81 \equiv 1 \mod 40$). Pour $x = 7$ : $f(7) = 7^3 \mod 55 = 343 \mod 55 = 13$. Inversion : $13^{27} \mod 55 = 7$.

### À qui s'adresse ce livre ?

Ce livre s'adresse à un lecteur cultivé, curieux, disposant d'une formation mathématique de premier cycle universitaire (algèbre linéaire, probabilités élémentaires, logique propositionnelle) mais qui n'est pas nécessairement spécialiste en cryptographie ni en théorie de la complexité. Chaque notion est introduite par une intuition, suivie d'une définition formelle, d'un énoncé, d'un exemple numérique calculé pas à pas et d'un exercice. Le lecteur peut être un étudiant en informatique ou en mathématiques, un ingénieur souhaitant comprendre les fondements théoriques des outils qu'il emploie, ou un chercheur d'une discipline voisine cherchant une entrée structurée dans ce paysage.

Je n'ai pas cherché à écrire un manuel de mise en œuvre. Aucun protocole TLS, aucune bibliothèque logicielle, aucun benchmark industriel n'est discuté ici. L'objet est la *structure* : pourquoi ces traductions fonctionnent, ce qu'elles conservent, ce qu'elles détruisent, et quelles limites fondamentales bornent notre capacité à les comprendre et à les inverser.

### Méthodologie et honnêteté épistémique

La cryptographie est un domaine où l'on manipule des conjectures avec la même aisance que des théorèmes. L'existence de fonctions à sens unique n'est pas prouvée. La sécurité de RSA repose sur la difficulté présumée de la factorisation. La séparation $\text{P} \neq \text{NP}$ reste ouverte. Impagliazzo 1995 a cartographié cinq « mondes » possibles selon que ces conjectures sont vraies ou fausses, et nous ne savons pas dans lequel nous vivons.

Face à cette incertitude structurelle, j'ai choisi la transparence totale. Le registre des statuts n'est pas une coquetterie : il est un engagement. Quand j'écris une preuve, elle est complète et vérifiable ligne à ligne. Quand je cite un grand résultat, je donne l'idée de la preuve en signalant clairement que la démonstration intégrale excède le cadre de cet ouvrage. Quand j'énonce une conjecture, je le dis. Quand une question est ouverte, je la pose comme telle, sans fausse résolution.

Les références sont limitées à un corpus restreint et explicite, de Shannon 1949 à Soos, Nohl et Castelluccia 2009. Chaque référence citée l'est avec son auteur et son année. Je n'invente aucune attribution, aucun numéro de page, aucune citation entre guillemets que je ne puisse garantir.

### Le plan du livre

L'ouvrage est organisé en quatre parties de quatre chapitres, suivant une progression qui va des fondements informationnels aux obstacles structurels, puis au transfert vers le programme RTC.

**Partie I — Fondements : information, secret et sens unique.** Le chapitre 1 pose le décor shannonien : entropie, information mutuelle, la traduction qui préserve tout (le masque jetable). Le chapitre 2 introduit les fonctions à sens unique et la traduction qu'on ne peut pas inverser. Le chapitre 3 présente le théorème HILL (Håstad, Impagliazzo, Levin et Luby 1999) : de toute fonction à sens unique naît le pseudo-aléa. Le chapitre 4 installe le décor computationnel : classes P, NP, BPP, les hiérarchies, la complexité en circuit.

**Partie II — Chiffrement probabiliste, sécurité sémantique et mondes d'Impagliazzo.** Le chapitre 5 étudie le passage du déterminisme au probabilisme. Le chapitre 6 explore la résiduosité quadratique et les constructions à clé publique élémentaires. Le chapitre 7 développe RSA et les fonctions à trappe. Le chapitre 8 cartographie les cinq mondes d'Impagliazzo 1995.

**Partie III — Cryptanalyse logique et algébrique : traduire le chiffrement en formules.** Le chapitre 9 détaille la traduction de Tseitin 1968, du circuit vers la forme normale conjonctive. Le chapitre 10 montre comment le chiffrement devient une instance SAT (Massacci et Marraro 2000 ; Soos, Nohl et Castelluccia 2009). Le chapitre 11 aborde la cryptanalyse algébrique et les systèmes surdéterminés (Courtois et Pieprzyk 2002). Le chapitre 12 introduit la largeur structurelle et la difficulté des formules cryptographiques.

**Partie IV — Obstacles, limites et transfert vers le programme RTC.** Le chapitre 13 présente les preuves naturelles de Razborov et Rudich 1997 : quand la cryptographie bloque la complexité. Le chapitre 14 développe la méthodologie des réductions et de la sécurité prouvée. Le chapitre 15 opère la synthèse : la cryptographie comme théorie des traductions destructrices. Le chapitre 16, enfin, réalise le transfert vers le programme RTC : quelles ressources sont en jeu, quelles traductions restent à explorer, quelles questions ouvertes ce tome lègue à l'étude générale des traductions à ressources.

### Une lecture active

Ce livre est conçu pour être lu un crayon à la main. Les exercices ne sont pas des suppléments décoratifs : ils sont le lieu où le lecteur vérifie qu'il a compris, en refaisant. Les exemples numériques sont calculés pas à pas, non pas pour leur intérêt intrinsèque, mais pour montrer que les objets abstraits — entropie, négligeabilité, réduction — ont un contenu calculable, vérifiable, tangible.

Je formule un vœu : qu'à la dernière page, le lecteur perçoive la cryptographie non plus comme une collection de recettes ou de protocoles, mais comme une théorie cohérente des traductions entre mondes computationnels — une théorie où chaque théorème est une affirmation sur ce qu'on peut ou ne peut pas traduire, sur ce qui survit et ce qui est irrémédiablement perdu dans le passage d'une représentation à une autre.

La complexité est la gardienne du secret. La traduction est le mécanisme. La destruction de l'information exploitable est l'objectif. Ce livre est l'étude de cette mécanique.

$$
\boxed{\text{Traduire, c'est choisir ce qu'on conserve. Chiffrer, c'est choisir ce qu'on détruit.}}
$$

**Énoncé en mots** : toute traduction sélectionne une structure à préserver ; la traduction cryptographique sélectionne une sémantique à anéantir. **Conditions de validité** : métaphore structurante du livre, non un théorème. **Statut** : principe directeur de l'ouvrage. **Exemple** : dans le masque jetable, on conserve la longueur ($n$ bits $\to$ $n$ bits) et l'opération $\oplus$ ; on détruit toute information sur $M$ pour qui ne possède pas $K$.

Bienvenue dans la science des traductions qui détruisent.

### Le registre des ressources : sept colonnes pour une même traduction

Le programme RTC exige qu'on tienne les comptes. Pour chaque traduction étudiée, je remplis un registre à sept colonnes, que je note

$$
\mathrm{Res}(T,n) \;=\; \bigl(\,\mathrm{sortie},\ \mathrm{portes},\ \mathrm{travail},\ \mathrm{profondeur},\ \mathrm{largeur},\ \mathrm{précision},\ \mathrm{secret}\,\bigr).
$$

**Énoncé en mots** : une traduction est décrite par la longueur de sa sortie, le nombre de portes de son circuit, les bits de mémoire auxiliaire, le nombre de couches du circuit, le nombre maximal de portes par couche, le nombre de bits de précision arithmétique nécessaires, et le nombre de bits de secret qui doivent avoir été partagés au préalable. **Conditions de validité** : $T$ est realised par un circuit boolien fini, sans boucle ; les unités sont fixées une fois pour toutes comme ci-dessus. **Statut** : convention de comptabilité propre à l'ouvrage ; les inégalités qui suivent sont PROUVÉES. **Exemple numérique** : pour le masque jetable sur $n=4$ bits en version parallèle, $\mathrm{Res} = (4,\,4,\,0,\,1,\,4,\,1,\,4)$ : quatre bits de sortie, quatre portes XOR, aucun registre auxiliaire, une seule couche, quatre portes simultanées, arithmétique sur un bit, quatre bits de clé pré-partagés.

Deux inégalités élémentaires gouvernent ce registre et méritent d'être démontrées immédiatement, car elles reviendront dans tous les chapitres.

$$
\mathrm{profondeur}(C) \;\le\; \mathrm{portes}(C) \;=\; \mathrm{temps}_{\mathrm{séquentiel}}(C),
\qquad
\mathrm{temps}_{\mathrm{parallèle}}(C) \;=\; \mathrm{profondeur}(C).
$$

**Énoncé en mots** : le temps parallèle d'un circuit est sa profondeur, son temps séquentiel est son nombre de portes, et la profondeur ne dépasse jamais le nombre de portes. **Conditions de validité** : circuit acyclique, une porte évaluée par pas de temps, portes d'une même couche mutuellement indépendantes. **Statut** : PROUVÉ. **Démonstration complète** : un chemin orienté du circuit ne visite jamais deux fois la même porte, puisqu'il n'y a pas de cycle ; sa longueur est donc au plus le nombre total de portes, d'où $\mathrm{profondeur} \le \mathrm{portes}$. Une machine séquentielle évalue une porte par pas et doit toutes les évaluer : son temps est exactement le nombre de portes. Une machine parallèle peut évaluer chaque couche en un pas, d'où un temps égal à la profondeur ; elle ne peut faire mieux, car les portes d'un chemin maximal doivent être évaluées dans l'ordre, ce qui impose autant de pas que la longueur du chemin. $\square$ **Exemple numérique** : soit $y=(x_1\oplus x_2)\wedge(x_3\oplus x_4)$. Le circuit a $3$ portes, une profondeur de $2$ (couche 1 : deux XOR ; couche 2 : un AND). Temps séquentiel $=3$, temps parallèle $=2$, et $2\le 3$ comme annoncé.

$$
\mathrm{portes}(C) \;\le\; \mathrm{largeur}(C)\times \mathrm{profondeur}(C).
$$

**Énoncé en mots** : le nombre de portes est borné par le produit de la largeur et de la profondeur ; on peut donc échanger du temps contre de l'espace de calcul. **Conditions de validité** : circuit organisé en couches, largeur définie comme le maximum de portes par couche. **Statut** : PROUVÉ. **Démonstration complète** : chaque couche contient au plus $\mathrm{largeur}(C)$ portes, et il y a $\mathrm{profondeur}(C)$ couches ; la somme est donc au plus le produit. $\square$ **Exemple numérique** : pour le circuit précédent, $3 \le 2\times 2 = 4$. Pour le masque jetable sur $4$ bits, la version parallèle donne $4 \le 4\times 1 = 4$ ; la version séquentielle, qui traite un bit à la fois, donne $4 \le 1\times 4 = 4$. Même traduction, même nombre de portes, deux profils de ressources opposés : c'est exactement le genre de phénomène que le registre doit rendre visible.

### Détruire sans perdre : le paradoxe fondateur

Voici le point que je veux installer avant toute technique. Une traduction cryptographique ne détruit pas l'information au sens absolu ; elle la rend inaccessible. Pour le masque jetable $C=M\oplus K$ avec $K$ uniforme et indépendant de $M$ :

$$
I(M;C)=0,\qquad H(M\mid C)=H(M),\qquad H(M\mid C,K)=0.
$$

**Énoncé en mots** : le chiffré seul n'apprend rien sur le clair ; le chiffré accompagné de la clé révèle tout. **Conditions de validité** : $|K|=|M|=n$, $K$ uniforme sur $\{0,1\}^n$, indépendant de $M$, utilisé une seule fois. **Statut** : PROUVÉ (Shannon 1949 ; démonstration élémentaire donnée ici en entier). **Démonstration complète** : pour tous $m,c$, $\Pr[C=c\mid M=m]=\Pr[K=m\oplus c]=2^{-n}$, quantité indépendante de $m$ ; donc $M$ et $C$ sont indépendants, ce qui donne $I(M;C)=0$ et $H(M\mid C)=H(M)$. Enfin $M=C\oplus K$ est une fonction déterministe de $(C,K)$, donc $H(M\mid C,K)=0$. $\square$ **Exemple numérique** : $n=2$, $M$ uniforme sur $\{00,11\}$, donc $H(M)=1$ bit. $K$ uniforme sur les quatre valeurs. Alors $C$ est uniforme sur les quatre valeurs, $H(C)=2$ bits, $H(M\mid C)=1$ bit, et $H(M\mid C,K)=0$.

$$
I(M;C,K) \;=\; H(M)-H(M\mid C,K) \;=\; H(M).
$$

**Énoncé en mots** : l'information n'a pas disparu, elle a été déplacée dans la clé ; la traduction est une redistribution, non une annihilation. **Conditions de validité** : mêmes hypothèses que ci-dessus. **Statut** : PROUVÉ (conséquence immédiate du calcul précédent). **Exemple numérique** : avec $H(M)=1$ bit et $H(M\mid C,K)=0$, on obtient $I(M;C,K)=1-0=1$ bit. Le bilan est exact : zéro bit accessible sans clé, un bit accessible avec clé.

### L'écart entre information et calcul

Le pseudo-aléa pousse ce paradoxe à l'extrême. Soit $G:\{0,1\}^s\to\{0,1\}^{\ell(s)}$ un générateur efficace, et $U_s$ la loi uniforme sur les graines.

$$
H\bigl(G(U_s)\bigr) \;\le\; \log_2\bigl|\mathrm{Im}(G)\bigr| \;\le\; s \;<\; \ell(s).
$$

**Énoncé en mots** : la sortie d'un générateur ne contient jamais plus d'entropie véritable que sa graine, même si elle est plus longue. **Conditions de validité** : $G$ déterministe, graine uniforme, $\ell(s)>s$. **Statut** : PROUVÉ. **Démonstration complète** : pour une loi $p$ supported par un ensemble fini $S$, la concavité du logarithme donne $H(p)-\log_2|S| = \sum_i p_i\log_2\frac{1}{p_i|S|} \le \log_2\Bigl(\sum_i p_i\frac{1}{p_i|S|}\Bigr)=\log_2 1 = 0$. Appliqué à $S=\mathrm{Im}(G)$, cela donne la première inégalité ; la seconde vient de $|\mathrm{Im}(G)|\le 2^s$. $\square$ **Exemple numérique** : $s=3$, $\ell(3)=6$, $G$ injectif. L'image a $8$ éléments, donc $H(G(U_3))=3$ bits exactement, pour une sortie de $6$ bits. Le déficit informationnel est de $6-3=3$ bits.

Ce déficit se mesure. La distance statistique entre deux lois $X,Y$ sur un même ensemble est

$$
\Delta(X,Y)\;=\;\frac12\sum_z\bigl|\Pr[X=z]-\Pr[Y=z]\bigr|\;=\;\max_{D}\bigl|\Pr[D(X)=1]-\Pr[D(Y)=1]\bigr|.
$$

**Énoncé en mots** : la distance statistique est exactement le meilleur avantage d'un testeur, sans limite de ressources. **Conditions de validité** : lois sur un ensemble fini, maximum pris sur tous les testeurs booléens. **Statut** : CONNU (notion standard ; Goldreich 2001 ; Katz et Lindell 2007), et l'égalité est PROUVÉE ici. **Démonstration complète de l'égalité** : les différences $\Pr[X=z]-\Pr[Y=z]$ somment à zéro, donc leur partie positive et leur partie négative valent chacune $\Delta$. Le testeur qui répond $1$ exactement sur l'ensemble des $z$ à différence positive atteint l'avantage $\Delta$ ; aucun testeur ne peut faire mieux, puisqu'il sélectionne une sous-partie de ces différences. $\square$ **Exemple numérique** : $X$ uniforme sur $\{00,11\}$, $Y$ uniforme sur les quatre mots de deux bits. $\Delta=\frac12\bigl(\tfrac14+\tfrac14+\tfrac14+\tfrac14\bigr)=\tfrac12$. Le testeur « les deux bits sont égaux » réussit avec probabilité $1$ sur $X$ et $1/2$ sur $Y$ : avantage $1/2$, optimal.

La sécurité computationnelle, elle, se définit en bornant le testeur :

$$
\bigl|\Pr[D(X_n)=1]-\Pr[D(Y_n)=1]\bigr|\;\le\;\varepsilon(n)
\quad\text{pour tout } D \text{ de taille } \le t(n).
$$

**Énoncé en mots** : deux familles de lois sont indiscernables si aucun testeur de taille bornée ne les sépare notablement. **Conditions de validité** : $t(n)$ polynomial, $\varepsilon(n)$ négligeable, familles indexées par $n$. **Statut** : CONNU (Yao 1982 ; Goldwasser et Micali 1984). **Exemple numérique** : reprenons $G$ avec $s=3$, $\ell=6$, image de taille $8$, sortie uniforme sur cette image. Alors $\Delta\bigl(G(U_3),U_6\bigr)=\frac12\bigl(8\cdot\tfrac{7}{64}+56\cdot\tfrac1{64}\bigr)=\frac12\cdot\frac{112}{64}=\frac78$. Statistiquement, l'écart est énorme : $7/8$. Computationnellement, on conjecture qu'il est invisible pour tout testeur polynomial quand $s$ grandit. Tout le livre tient dans cet écart entre $7/8$ et « invisible ».

### Le paramètre de sécurité : l'asymétrie quantifiée

La borne « négligeable » n'est pas une commodité de style ; elle fixe le régime où la destruction devient operative.

$$
\forall c>0,\ \exists n_0,\ \forall n\ge n_0:\quad \mu(n) < n^{-c}.
$$

**Énoncé en mots** : une fonction négligeable décroît plus vite que toute inverse de polynôme. **Conditions de validité** : $\mu$ positive, $n$ entier tendant vers l'infini. **Statut** : PROUVÉ pour $\mu(n)=2^{-n}$ (croissance exponentielle contre polynomiale). **Exemple numérique** : $n=128$, $c=3$. On a $2^{-128}\approx 2{,}94\times 10^{-39}$ et $128^{-3}=1/2\,097\,152\approx 4{,}77\times 10^{-7}$. Le rapport vaut environ $6\times 10^{-33}$ : la borne exponentielle est écrasée.

$$
\mathrm{temps}_{\text{légitime}}(\lambda)=O(\lambda^{3})
\qquad\text{contre}\qquad
\mathrm{temps}_{\text{exhaustif}}(\lambda)=2^{\lambda}.
$$

**Énoncé en mots** : l'utilisateur légitime paie un coût polynomial, l'attaquant par force brute un coût exponentiel ; c'est cette asymétrie, et elle seule, qui rend la traduction utilisable. **Conditions de validité** : espace de clés de $\lambda$ bits, aucune attaque meilleure que l'énumération, opérations comptées à l'unité. **Statut** : le calcul est PROUVÉ ; l'absence d'attaque meilleure est une CONJECTURE, et l'existence d'une borne inférieure prouvée est OUVERTE. **Exemple numérique** : $\lambda=128$. Côté légitime, $128^{3}=2\,097\,152$ opérations. Côté attaquant, $2^{128}\approx 3{,}4\times 10^{38}$ opérations ; à $10^{12}$ opérations par seconde, cela représente $3{,}4\times 10^{26}$ secondes, soit environ $1{,}1\times 10^{19}$ années. Le même objet, deux coûts : voilà la matière première de la cryptographie.

### Conventions de notation

J'écris $\lambda$ pour le paramètre de sécurité, $U_n$ pour la loi uniforme sur $\{0,1\}^n$, $\oplus$ pour l'ou exclusif bit à bit, $\log$ pour le logarithme en base $2$ (les entropies sont donc en bits), $X\approx_c Y$ pour l'indiscernabilité computationnelle, et PPT pour « probabiliste polynomial ». Une réduction s'écrit $A \le_{\mathrm{poly}} B$ : résoudre $A$ efficacement si l'on dispose d'un moyen efficace de résoudre $B$. Les énoncés asymptotiques portent sur des familles indexées par $\lambda$ ; les exemples numériques portent sur de très petites instances, choisies pour être vérifiables à la main, et ne prétendent jamais illustrer une sécurité réelle.

### Trois parcours de lecture

Un lecteur curieux de la thèse peut suivre les chapitres 1, 2, 5, 8 puis 15 : il obtiendra l'arc complet, de l'entropie aux mondes d'Impagliazzo 1995, puis à la synthèse. Un lecteur venu de la complexité peut entrer par 4, puis 9, 12, 13 et 16 : traduction de Tseitin 1968, largeur structurelle, barrière des preuves naturelles de Razborov et Rudich 1997, transfert vers RTC. Un lecteur soucieux de sécurité prouvée lira 3, 6, 7 et 14, où les réductions sont explicitées avec leurs pertes de paramètres. Les quatre parties restent ordonnées : chaque chapitre n'utilise que ce qui le précède.

### Ce que ce tome ne fait pas

Il ne propose aucune attaque nouvelle, aucune implémentation, aucune recommandation de paramétrage opérationnel. Il n'annonce aucune découverte. Les résultats étiquetés CONNU appartiennent au corpus cité ; les démonstrations complètes fournies ici sont élémentaires et données pour l'autonomie du lecteur ; les questions étiquetées OUVERTES le restent à la dernière page.

### Exercices d'entrée

**Exercice 1.** Avec $M=1101$ et $K=0110$, calculer $C$, puis vérifier que $C\oplus K=M$. Combien de bits de secret pré-partagé le registre exige-t-il ?

**Exercice 2.** Soit $X$ uniforme sur $\{000,111\}$ et $Y$ uniforme sur les huit mots de trois bits. Calculer $\Delta(X,Y)$ et exhiber un testeur optimal. *Indication* : compter les mots de poids $0$ ou $3$.

**Exercice 3.** Vérifier une traduction à trappe sur de petits paramètres : $p=3$, $q=11$, $N=33$, $\varphi(N)=20$, $e=3$, $d=7$, $x=5$.

$$
5^{3}\bmod 33 = 26,
\qquad
26^{7}\bmod 33 = 5.
$$

**Énoncé en mots** : chiffrer puis déchiffrer rend le message initial. **Conditions de validité** : $ed\equiv 1 \pmod{\varphi(N)}$ — ici $3\times 7=21\equiv 1 \pmod{20}$ — et $\gcd(x,N)=1$, ici $\gcd(5,33)=1$. **Statut** : PROUVÉ pour ces instances par calcul direct ; CONNU en général (Rivest, Shamir et Adleman 1978). **Exemple numérique pas à pas** : $5^3=125$ et $125-3\times 33=125-99=26$. Puis $26^2=676$ et $676-20\times 33=676-660=16$ ; $26^4=16^2=256$ et $256-7\times 33=256-231=25$ ; enfin $26^7=26^4\cdot 26^2\cdot 26$, soit $25\times 16=400\equiv 400-12\times 33=4$, puis $4\times 26=104\equiv 104-3\times 33=5$. Le cycle est fermé : la trappe a rendu l'inversion aussi coûteuse que l'évaluation.

### Ouverture

Le premier chapitre commence là où ces calculs s'arrêtent : par la question de savoir ce qu'est une quantité d'information, et pourquoi une traduction peut préserver tous les bits tout en ne laissant rien à comprendre.