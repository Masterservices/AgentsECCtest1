## Conclusion

### Ce que nous avons parcouru ensemble

Cher lecteur, nous voici arrivés au terme de ce voyage à travers les traductions entre modèles de calcul. Depuis les premières pages où nous avons rencontré le lambda-calcul de Church jusqu'aux architectures profondes d'attention qui animent aujourd'hui nos systèmes d'intelligence artificielle, un fil rouge n'a cessé de nous guider : **toute traduction conserve ou perd des ressources mesurables**.

Ce formulaire n'était pas un simple catalogue. C'était une invitation à regarder autrement les ponts que nous jetons entre les formalismes. Quand nous traduisons un terme lambda en machine de Turing, un circuit en formule SAT, ou un réseau de neurones en fonction ReLU par morceaux, nous ne faisons pas que changer de langage. Nous payons un prix — en taille, en temps, en mémoire, en profondeur, en précision — et ce prix obéit à des lois mathématiques précises.

Permettez-moi de reprendre avec vous les moments clés de notre parcours, non pour répéter ce que vous avez lu, mais pour en extraire la substance et voir ce qu'elle nous enseigne sur la nature même du calcul.

---

### Les fondations : lambda-calcul et machines de Turing

Tout a commencé par la substitution. La règle de bêta-réduction, dans sa simplicité trompeuse, cache une complexité que nous avons mesurée pas à pas. Rappelez-vous cette formule qui quantifie le coût d'une substitution complète :

$$|t[x := u]| \leq |t| \cdot |u|$$

**Énoncé** : La taille du terme résultant d'une substitution est bornée par le produit des tailles du terme receveur et du terme substitué.
**Conditions de validité** : Termes du lambda-calcul pur, mesure de taille par le nombre de nœuds de l'arbre syntaxique.
**Statut** : PROUVÉ.
**Exemple** : Si $t = (\lambda y. x\ x\ x)$ avec $|t| = 6$ et $u = \lambda z. z$ avec $|u| = 2$, alors $|t[x := u]| \leq 6 \times 2 = 12$. En pratique, $t[x := u] = (\lambda y. (\lambda z. z)\ (\lambda z. z)\ (\lambda z. z))$ qui a pour taille 12, atteignant la borne.

Cette borne, anodine en apparence, est le premier signal d'alarme : la substitution peut provoquer une explosion exponentielle si elle est itérée. C'est exactement ce qui se produit avec les entiers de Church. Le successeur appliqué $n$ fois à $\overline{0}$ donne $\overline{n}$, dont la taille croît linéairement, mais l'addition de Church $\text{plus} = \lambda m.\lambda n.\lambda f.\lambda x. m\ f\ (n\ f\ x)$ appliquée à $\overline{m}$ et $\overline{n}$ produit un terme de taille proportionnelle à $m + n$, tandis que la multiplication peut engendrer des termes de taille $O(m \cdot n)$.

Nous avons ensuite vu comment ces encodages, bien qu'élégants, masquent des coûts de réduction redoutables. Le théorème fondamental qui lie le lambda-calcul aux machines de Turing s'énonce ainsi :

$$\text{TM}(t) \leq O(|t| \cdot \text{steps}_\beta(t)^2)$$

**Énoncé** : Le temps de simulation d'une réduction lambda sur une machine de Turing multi-ruban est borné par le produit de la taille initiale du terme et du carré du nombre d'étapes de bêta-réduction.
**Conditions de validité** : Stratégie de réduction normalisante (leftmost-outermost), machine de Turing multi-ruban.
**Statut** : CONNU.
**Exemple** : Un terme de taille 100 nécessitant 50 étapes de réduction sera simulé en au plus $100 \times 50^2 = 250\,000$ étapes de machine de Turing.

Ce résultat, classique depuis les travaux de Church (1936) et Turing (1936), nous rappelle que l'équivalence computationnelle ne signifie pas équivalence de coût. Deux modèles peuvent calculer exactement les mêmes fonctions, mais l'un peut exiger un temps quadratiquement supérieur à l'autre pour y parvenir.

---

### Le cœur du livre : complexité, circuits et SAT

La partie centrale de notre parcours nous a conduits au cœur de la théorie de la complexité. Le théorème de hiérarchie en temps, démontré par Hartmanis et Stearns (1965), établit qu'accorder plus de temps à une machine de Turing lui permet strictement de résoudre davantage de problèmes :

$$\text{DTIME}(f(n)) \subsetneq \text{DTIME}(f(n) \log f(n))$$

**Énoncé** : Pour toute fonction $f$ croissante et constructible en temps, la classe des problèmes résolubles en temps $f(n)$ est strictement incluse dans celle des problèmes résolubles en temps $f(n) \log f(n)$.
**Conditions de validité** : $f(n)$ constructible en temps, $f(n) \geq n$.
**Statut** : PROUVÉ.
**Exemple** : $\text{DTIME}(n^2) \subsetneq \text{DTIME}(n^2 \log n^2) = \text{DTIME}(2n^2 \log n)$. Il existe des problèmes solubles en temps $2n^2 \log n$ mais pas en temps $n^2$.

Ce théorème est la pierre angulaire de notre compréhension des classes de complexité. Il justifie que P, NP, PSPACE et les autres ne sont pas de simples étiquettes, mais correspondent à des sauts quantitatifs réels dans les ressources disponibles.

Le théorème de Savitch (1970) nous a offert l'une des traductions les plus surprenantes du livre :

$$\text{NSPACE}(s(n)) \subseteq \text{DSPACE}(s(n)^2)$$

**Énoncé** : Tout problème résoluble par une machine de Turing non déterministe en espace $s(n)$ est résoluble par une machine déterministe en espace $s(n)^2$.
**Conditions de validité** : $s(n) \geq \log n$, $s(n)$ constructible en espace.
**Statut** : PROUVÉ.
**Exemple** : Si un algorithme non déterministe utilise $s(n) = \sqrt{n}$ d'espace, il peut être simulé déterministement en espace $(\sqrt{n})^2 = n$. Ainsi, $\text{NSPACE}(\sqrt{n}) \subseteq \text{DSPACE}(n)$.

La conséquence la plus célèbre est que $\text{NPSPACE} = \text{PSPACE}$, ce qui contraste sharply avec la question ouverte $\text{P} \stackrel{?}{=} \text{NP}$. L'espace, contrairement au temps, semble absorber le non-déterminisme sans explosion exponentielle.

Puis vint le théorème de Cook-Levin (Cook 1971), que j'ai placé au centre du livre car il incarne parfaitement la thèse des traductions à ressources :

$$L \in \text{NP} \implies \exists \text{ réduction polynomiale } f : L \to \text{SAT} \text{ avec } |f(x)| = O(|x|^k)$$

**Énoncé** : Tout langage de NP se réduit à SAT par une réduction polynomiale qui transforme une instance de taille $n$ en une formule de taille $O(n^k)$ pour un $k$ fixé.
**Conditions de validité** : Machine de Turing non déterministe polynomiale, encodage standard.
**Statut** : PROUVÉ.
**Exemple** : Un problème NP vérifié par une machine non déterministe en temps $n^3$ se traduit en une formule SAT de taille $O((n^3)^2) = O(n^6)$ (car la construction de Cook-Levin produit une formule de taille quadratique en le temps de calcul).

Cette traduction est universelle : elle fonctionne pour n'importe quel problème de NP. Mais elle a un coût. La formule SAT résultante est souvent bien plus grande que l'instance d'origine, et cette inflation est inévitable dans le cadre général.

L'encodage de Tseitin (1968) nous a ensuite montré comment traduire un circuit booléen en formule CNF de manière bien plus économique :

$$|\text{CNF}(C)| = O(|C|)$$

**Énoncé** : La taille de la formule CNF produite par l'encodage de Tseitin à partir d'un circuit $C$ est linéaire en la taille du circuit.
**Conditions de validité** : Circuit booléen acyclique, introduction de variables auxiliaires pour chaque porte.
**Statut** : PROUVÉ.
**Exemple** : Un circuit de 1000 portes (ET, OU, NON) sera traduit en une formule CNF d'environ 3000 à 4000 clauses (chaque porte ET ou OU engendrant 3 clauses), soit une taille de l'ordre de 4000, linéaire en 1000.

Cette linéarité est remarquable. Elle contraste avec la construction de Cook-Levin et explique pourquoi les solveurs SAT modernes travaillent sur des encodages Tseitin plutôt que sur la construction directe.

Nous avons également exploré la transition de phase du 3-SAT aléatoire, un phénomène expérimental fascinant :

$$\alpha_c \approx 4.267$$

**Énoncé** : Pour le 3-SAT aléatoire avec $n$ variables et $m = \alpha n$ clauses, la probabilité de satisfaisabilité passe brusquement de proche de 1 à proche de 0 lorsque $\alpha$ franchit le seuil critique $\alpha_c \approx 4.267$.
**Conditions de validité** : Clauses tirées uniformément au hasard, $n \to \infty$.
**Statut** : EXPÉRIMENTAL (fortement soutenu par des preuves partielles).
**Exemple** : Avec $n = 1000$ variables, le seuil se situe autour de $m = 4267$ clauses. En dessous, presque toutes les instances sont satisfaisables ; au-dessus, presque aucune.

Ce seuil n'est pas seulement une curiosité mathématique. Il marque la région où les solveurs SAT peinent le plus, car les instances y sont à la fois rares en solutions et difficiles à prouver insatisfaisables.

La borne de Schöning (1999) pour le k-SAT nous a offert un algorithme probabiliste élégant :

$$\Pr[\text{succès}] \geq \left(\frac{k}{2(k-1)}\right)^n \cdot \text{poly}(n)$$

**Énoncé** : L'algorithme de marche aléatoire de Schöning résout le k-SAT avec une probabilité de succès au moins $\left(\frac{k}{2(k-1)}\right)^n$ multipliée par un facteur polynomial.
**Conditions de validité** : Formule k-SAT satisfaisable, $k \geq 3$.
**Statut** : PROUVÉ.
**Exemple** : Pour le 3-SAT avec $n = 50$ variables, la probabilité de succès par essai est au moins $(3/4)^{50} \approx 5.66 \times 10^{-7}$. En répétant $10^7$ fois, on obtient une probabilité de succès globale proche de $1 - e^{-5.66} \approx 0.9966$.

Cet algorithme, bien que théorique, illustre comment une traduction astucieuse du problème (voir le k-SAT comme une marche aléatoire sur l'hypercube) peut conduire à des bornes non triviales.

---

### Réseaux de neurones : profondeur, approximation et attention

La dernière partie de notre parcours nous a menés vers les réseaux de neurones, où les traductions prennent une forme différente mais obéissent toujours à des lois de conservation des ressources.

Le théorème d'approximation universelle de Cybenko (1989) établit qu'un réseau à une couche cachée suffit pour approximer toute fonction continue :

$$\forall f \in C([0,1]^d), \forall \epsilon > 0, \exists N, \exists w_i, a_i, b_i : \sup_{x} \left| f(x) - \sum_{i=1}^{N} w_i \sigma(a_i \cdot x + b_i) \right| < \epsilon$$

**Énoncé** : Pour toute fonction continue sur le cube unité et toute précision $\epsilon$, il existe un réseau à une couche cachée avec $N$ neurones à sigmoïde qui approxime $f$ à $\epsilon$ près.
**Conditions de validité** : $\sigma$ sigmoïde continue non constante, $f$ continue sur un compact.
**Statut** : PROUVÉ.
**Exemple** : Pour approximer $f(x) = \sin(2\pi x)$ sur $[0,1]$ à $\epsilon = 0.01$ près, un réseau sigmoïde nécessite typiquement $N \approx 50$ à $100$ neurones cachés (valeur expérimentale, la borne théorique de Cybenko n'est pas constructive).

Mais ce théorème ne dit rien sur la taille de $N$. Et c'est ici que les résultats de Telgarsky (2016) sur la profondeur interviennent :

$$\exists f : \text{profondeur } k \text{ nécessite } O(n) \text{ neurones, profondeur } 2 \text{ nécessite } 2^{\Omega(n)}$$

**Énoncé** : Il existe des fonctions calculables par un réseau de profondeur $k$ avec un nombre linéaire de neurones, mais qui exigent un nombre exponentiel de neurones si la profondeur est bornée à 2.
**Conditions de validité** : Fonctions ReLU, profondeur mesurée en nombre de couches cachées.
**Statut** : PROUVÉ.
**Exemple** : La fonction « dents de scie » itérée $k$ fois, $f(x) = \underbrace{g \circ g \circ \cdots \circ g}_{k}(x)$ où $g(x) = |2x - 1|$, se calcule avec $O(k)$ neurones ReLU de profondeur $k$, mais nécessite $2^k$ neurones en profondeur 2. Pour $k = 20$, cela donne $O(20)$ contre $2^{20} \approx 10^6$.

Cette séparation est profonde. Elle montre que la profondeur n'est pas un simple paramètre d'optimisation, mais une ressource computationnelle à part entière, au même titre que le temps ou l'espace pour les machines de Turing.

L'architecture Transformer, introduite par Vaswani et al. (2017), a apporté une nouvelle forme de traduction : l'attention. La complexité de l'attention multi-tête s'exprime ainsi :

$$\text{Coût}(\text{Attention}) = O(n^2 \cdot d)$$

**Énoncé** : Le calcul de l'attention auto-référente sur une séquence de longueur $n$ avec des embeddings de dimension $d$ coûte $O(n^2 d)$ opérations.
**Conditions de validité** : Attention dense (non éparse), séquence de longueur fixe.
**Statut** : CONNU.
**Exemple** : Pour une séquence de $n = 512$ tokens et $d = 768$, le coût est de l'ordre de $512^2 \times 768 \approx 2 \times 10^8$ opérations par couche d'attention.

Ce coût quadratique en la longueur de séquence est la raison pour laquelle les Transformers peinent sur les très longues séquences et pourquoi tant de recherches actuelles visent à le réduire (attention éparse, attention linéaire, etc.).

---

### Les formules qui résument tout

Permettez-moi de rassembler ici les formules qui, à mes yeux, capturent l'essence du livre. Chacune exprime une loi de conservation ou de perte lors d'une traduction :

**1. Substitution lambda** :
$$|t[x := u]| \leq |t| \cdot |u|$$
Statut : PROUVÉ. La substitution peut multiplier la taille.

**2. Simulation Turing du lambda-calcul** :
$$\text{TM}(t) \leq O(|t| \cdot \text{steps}_\beta(t)^2)$$
Statut : CONNU. Le temps de simulation est quadratique en le nombre de réductions.

**3. Théorème de Savitch** :
$$\text{NSPACE}(s(n)) \subseteq \text{DSPACE}(s(n)^2)$$
Statut : PROUVÉ. Le non-déterminisme spatial se simule avec un coût quadratique.

**4. Cook-Levin** :
$$L \in \text{NP} \implies |f(x)| = O(|x|^k)$$
Statut : PROUVÉ. La réduction à SAT est polynomiale mais potentiellement de haut degré.

**5. Tseitin** :
$$|\text{CNF}(C)| = O(|C|)$$
Statut : PROUVÉ. L'encodage circuit-vers-CNF est linéaire.

**6. Transition de phase 3-SAT** :
$$\alpha_c \approx 4.267$$
Statut : EXPÉRIMENTAL. Le seuil critique sépare les phases satisfaisable et insatisfaisable.

**7. Schöning** :
$$\Pr[\text{succès}] \geq \left(\frac{k}{2(k-1)}\right)^n$$
Statut : PROUVÉ. La marche aléatoire donne une borne exponentielle mais non triviale.

**8. Cybenko** :
$$\sup_{x} \left| f(x) - \sum_{i=1}^{N} w_i \sigma(a_i \cdot x + b_i) \right| < \epsilon$$
Statut : PROUVÉ. L'approximation universelle existe, mais $N$ peut être énorme.

**9. Séparation de profondeur (Telgarsky)** :
$$\text{profondeur } k : O(n) \quad \text{vs} \quad \text{profondeur } 2 : 2^{\Omega(n)}$$
Statut : PROUVÉ. La profondeur est une ressource exponentiellement puissante.

**10. Attention Transformer** :
$$\text{Coût} = O(n^2 \cdot d)$$
Statut : CONNU. L'attention dense est quadratique en la longueur de séquence.

Ces dix formules ne sont pas un résumé exhaustif, mais elles tracent les contours d'un paysage où chaque traduction a un prix, et où ce prix est mesurable, borné, et souvent surprenant.

---

### Perspectives et questions ouvertes

Ce formulaire n'est pas un point d'arrivée. C'est une carte, et comme toute carte, elle montre autant de territoires inexplorés que de chemins balisés. Voici quelques-unes des questions qui, à mes yeux, méritent d'être poursuivies :

**La question P vs NP** reste le Graal de la théorie de la complexité. Si $\text{P} = \text{NP}$, alors toute vérification polynomiale peut être transformée en recherche polynomiale, et le coût de la traduction SAT s'effondrerait. Si $\text{P} \neq \text{NP}$, alors il existe des traductions intrinsèquement coûteuses, et nous devons apprendre à vivre avec. Statut : OUVERT.

**La largeur arborescente et les algorithmes FPT** (Fixed-Parameter Tractable) offrent une voie prometteuse pour contourner l'explosion exponentielle sur des instances structurées. Quand un graphe de contraintes a une largeur arborescente bornée $w$, de nombreux problèmes NP-complets deviennent solubles en temps $O(f(w) \cdot n)$. Explorer systématiquement les traductions qui préservent ou exploitent la largeur arborescente est un programme de recherche fertile. Statut : OUVERT.

**L'approximation par réseaux de neurones** manque encore de bornes constructives. Le théorème de Cybenko garantit l'existence d'un réseau approximant, mais ne dit pas comment le trouver ni quelle taille il aura. Développer des bornes explicites reliant la régularité de la fonction cible, la dimension de l'entrée et la précision requise à la taille du réseau est un défi majeur. Statut : OUVERT.

**L'attention efficace** cherche à réduire le coût quadratique de l'attention dense. Des approches comme l'attention éparse, l'attention linéaire par noyaux, ou les architectures hybrides (mélangeant convolution et attention) sont activement explorées. Mais nous manquons encore de théorèmes de séparation clairs : existe-t-il des tâches pour lesquelles l'attention dense est strictement nécessaire, ou peut-on toujours s'en passer moyennant un surcoût polynomial ? Statut : OUVERT.

**Les traductions entre modèles quantiques et classiques** ouvrent un nouveau chapitre que ce livre n'a fait qu'effleurer. La classe BQP (Bounded-error Quantum Polynomial time) se situe-t-elle strictement entre P et PSPACE ? Quelles ressources sont perdues quand on simule un circuit quantique par un circuit classique ? Ces questions, à la frontière de la physique et de l'informatique, redéfinissent le paysage des traductions à ressources. Statut : OUVERT.

---

### Transfert vers le programme RTC

Ce tome apporte au programme des **Traductions à Ressources entre Modèles de Calcul** (RTC) plusieurs contributions structurantes :

**1. Un registre des statuts** : Chaque affirmation du livre porte un statut clair (PROUVÉ, CONNU, EXPÉRIMENTAL, CONJECTURE, RÉFUTÉ, OUVERT). Ce registre permet de distinguer ce qui est établi de ce qui reste à prouver, et d'éviter les confusions entre intuitions et théorèmes.

**2. Des tables de correspondance** : Les formules présentées peuvent être organisées en tables reliant les modèles sources (lambda-calcul, machines de Turing, circuits, réseaux de neurones) aux modèles cibles, avec pour chaque traduction les ressources préservées, les ressources perdues et le facteur de surcoût.

**3. Des questions ouvertes identifiées** : Les statuts OUVERT et CONJECTURE pointent vers les zones où le programme RTC doit concentrer ses efforts. Chaque question ouverte est une invitation à produire de nouveaux théorèmes, à raffiner des bornes, ou à réfuter des conjectures.

**4. Une méthodologie reproductible** : Chaque formule est accompagnée de ses conditions de validité et d'un exemple numérique. Cela permet au lecteur de vérifier, de tester, et d'étendre les résultats. Le programme RTC doit maintenir cette exigence de reproductibilité.

**5. Des ponts inter-disciplines** : En reliant la théorie de la complexité classique (Cook, Levin, Savitch) aux architectures modernes de deep learning (Vaswani, Telgarsky), ce livre montre que les traductions à ressources ne sont pas un sujet confiné à la logique mathématique. Elles irriguent l'informatique pratique, de la compilation à l'apprentissage automatique.

---

### Mot final

Cher lecteur, si vous êtes arrivé jusqu'ici, c'est que vous avez accepté de suivre un chemin exigeant. Vous avez manipulé des termes lambda, simulé des machines de Turing, encodé des circuits en formules SAT, et calculé des gradients dans des réseaux profonds. Vous avez vu que derrière chaque traduction se cache un coût, et que ce coût n'est pas arbitraire : il obéit à des lois mathématiques que nous avons patiemment déchiffrées.

Ce livre n'a pas prétendu tout dire. La théorie du calcul est vaste, et les traductions entre modèles sont innombrables. Mais j'espère vous avoir donné les outils pour aborder ces traductions avec un regard critique, pour demander systématiquement : **quelles ressources sont préservées ? Quelles ressources sont perdues ? Quel est le facteur de surcoût ? Et ce surcoût est-il inévitable ?**

Ces questions sont au cœur de l'informatique théorique, mais elles sont aussi au cœur de la pratique. Quand vous choisissez un langage de programmation, un compilateur, une architecture matérielle, ou un modèle d'apprentissage, vous effectuez une traduction. Et cette traduction a un coût. Le savoir, c'est pouvoir choisir en connaissance de cause.

Je vous remercie d'avoir parcouru ce formulaire avec moi. Puissent ces formules vous servir de boussole dans vos propres explorations du calcul, de ses modèles, et de ses traductions.

— **Oussama Ghorbel**