## Conclusion : Le ternaire comme outil de conception, pas comme nouvelle puissance

### Synthèse des apports : ce que la base 3 conserve et ce qu'elle perd

Nous arrivons au terme de ce voyage à travers les bits et les trits. L'ambition de cet ouvrage n'était pas de vous vendre une révolution technologique, mais de vous offrir une boussole rigoureuse pour naviguer dans les promesses souvent exagérées du calcul non binaire. Le calcul ternaire équilibré a régulièrement été paré de vertus magiques par des enthousiastes oubliant les contraintes matérielles implacables de la conversion et de l'interfaçage. Notre thèse centrale, martelée dès l'introduction et démontrée chapitre après chapitre, est aujourd'hui sans appel : le ternaire équilibré est un changement de codage. Il rend gratuites certaines opérations arithmétiques et compacte la représentation des données, mais il ne modifie aucune classe de complexité fondamentale.

Pour ancrer cette réalité dans le marbre des mathématiques, il convient de rappeler le fondement même de l'économie de radix, un concept popularisé par Hayes (2001) et dont les racines remontent aux analyses de Knuth (1969). Cette métrique mesure le coût physique de représentation d'un nombre.

$$ E(b, N) = b \lfloor \log_b(N) + 1 \rfloor $$
**Énoncé** : Coût de représentation (nombre de symboles physiques ou de chiffres) requis pour encoder l'entier $N$ en base $b$.
**Conditions** : $b \ge 2$ (base entière), $N \ge 1$.
**Statut** : CONNU.
**Exemple numérique** : Pour $N = 27$ et $b = 3$, on calcule $E(3, 27) = 3 \times \lfloor \log_3(27) + 1 \rfloor = 3 \times \lfloor 3 + 1 \rfloor = 3 \times 4 = 12$ unités de coût.

Ce coût asymptotique nous mène directement au gain théorique maximal de la base 3 par rapport à la base 2. C'est un résultat classique, mais il constitue la pierre angulaire de notre honnêteté intellectuelle : le gain existe, mais il est borné.

$$ R_{3/2} = \lim_{N \to \infty} \frac{E(3, N)}{E(2, N)} = \frac{3 \ln 2}{2 \ln 3} \approx 0,946 $$
**Énoncé** : Ratio asymptotique de l'économie de radix entre la base 3 et la base 2.
**Conditions** : $N \to \infty$.
**Statut** : PROUVÉ.
**Exemple numérique** : Pour un très grand entier, la base 3 n'utilise que $94,6\,\%$ des ressources de la base 2, soit un gain d'économie de radix de $1 - 0,946 = 0,054$, c'est-à-dire $5,4\,\%$.

Ce gain de 5,4 % est réel, mais il faut le mettre en balance avec les propriétés structurelles du ternaire équilibré. L'ensemble des chiffres, que nous appelons trits, offre une symétrie parfaite autour de zéro, éliminant le besoin d'un bit de signe séparé.

$$ \mathbb{T} = \{-1, 0, 1\} \text{ noté } \{\bar{1}, 0, 1\} $$
**Énoncé** : Définition de l'ensemble des trits en base 3 équilibrée.
**Conditions** : Aucun.
**Statut** : CONNU.
**Exemple numérique** : L'entier $5$ s'écrit $1 \times 3^1 + \bar{1} \times 3^0$, soit la séquence $(1\bar{1})_3$.

Cette symétrie intrinsèque rend la négation arithmétique totalement gratuite au niveau matériel, une propriété élégante que le binaire complément à deux ne possède pas sans une coûteuse propagation de retenue à travers les portes logiques.

$$ - (t_n \dots t_0)_3 = (\bar{t}_n \dots \bar{t}_0)_3 $$
**Énoncé** : La négation d'un nombre ternaire équilibré s'obtient par inversion simple et parallèle de chaque trit.
**Conditions** : $t_i \in \{-1, 0, 1\}$ avec la règle d'inversion $\bar{1} = 1, \bar{0} = 0, \bar{1} = -1$.
**Statut** : PROUVÉ.
**Exemple numérique** : L'opposé de $(1\bar{1})_3$ (qui vaut $5$) est $(\bar{1}1)_3$ (qui vaut $-5$), obtenu instantanément en remplaçant $1$ par $\bar{1}$ et $\bar{1}$ par $1$.

De même, la réduction modulo 3, opération notoirement coûteuse et itérative en binaire, devient une simple lecture du trit de poids faible, sans aucun calcul.

$$ N \pmod 3 = t_0 $$
**Énoncé** : Le reste de la division euclidienne de $N$ par 3 est exactement le trit de poids faible.
**Conditions** : $N$ représenté en base 3 équilibrée.
**Statut** : PROUVÉ.
**Exemple numérique** : Pour $N = (1\bar{1}0)_3 = 1 \times 9 - 1 \times 3 + 0 = 6$, le trit de poids faible est $t_0 = 0$. On vérifie trivialement que $6 \pmod 3 = 0$.

### Le registre des statuts : bilan des traductions à ressources

Tout au long de ce livre, nous avons tenu un registre des statuts rigoureux. Chaque affirmation a été classée sans ambiguïté : PROUVÉ, CONNU, EXPÉRIMENTAL, CONJECTURE, RÉFUTÉ ou OUVERT. Cette discipline est la colonne vertébrale de notre approche des traductions à ressources. Le ternaire ne vit pas en vase clos ; il doit être traduit vers le binaire pour interagir avec nos machines actuelles. Le codage double rail est la traduction la plus directe, bien qu'elle impose une inflation de la mémoire.

$$ \text{Code}(t) = \begin{cases} (1,0) & \text{si } t = 1 \\ (0,0) & \text{si } t = 0 \\ (0,1) & \text{si } t = -1 \end{cases} $$
**Énoncé** : Encodage binaire d'un trit sur deux bits physiques (double rail).
**Conditions** : $t \in \{-1, 0, 1\}$, l'état $(1,1)$ est interdit.
**Statut** : CONNU.
**Exemple numérique** : Le trit $t = 0$ est encodé par la paire de bits $(0,0)$, utilisant exactement 2 bits de mémoire physique pour représenter 1 trit.

Cette traduction a un coût incompressible qui annule souvent le gain théorique de l'économie de radix. C'est ici qu'intervient le lemme L-T2, le cœur théorique et la preuve maîtresse de cet ouvrage.

$$ \text{Taille}(C_{bin}) \le k \cdot \text{Taille}(C_{tern}) $$
**Énoncé** : Lemme L-T2. Tout circuit ternaire peut être simulé par un circuit binaire avec un facteur multiplicatif constant $k$ en taille, profondeur et largeur.
**Conditions** : $k$ dépend de la base de portes choisie et du schéma d'encodage.
**Statut** : PROUVÉ.
**Exemple numérique** : Si un circuit ternaire $C_{tern}$ possède $100$ portes et que la constante de traduction est $k = 4$, le circuit binaire équivalent $C_{bin}$ aura au plus $400$ portes.

Cette traduction à coût constant a des implications philosophiques et pratiques directes sur la complexité algorithmique. Les classes de complexité sont des invariants de la machine de Turing, et le changement de base n'y échappe pas. Le ternaire ne résout pas le problème P vs NP.

$$ \text{P}_{tern} = \text{P}_{bin} \quad \text{et} \quad \text{NP}_{tern} = \text{NP}_{bin} $$
**Énoncé** : Les classes de complexité P et NP sont strictement invariantes par changement de base (binaire vers ternaire).
**Conditions** : Machines de Turing déterministes et non déterministes.
**Statut** : PROUVÉ.
**Exemple numérique** : Un algorithme s'exécutant en temps $O(n^2)$ sur une machine ternaire s'exécutera en temps $O((2n)^2) = O(4n^2) = O(n^2)$ sur une machine binaire.

Pour les problèmes de satisfaisabilité (SAT), l'encodage des variables ternaires impose une inflation linéaire du nombre de variables booléennes, ce qui impacte directement les performances des solveurs modernes.

$$ \text{Vars}(C_{SAT}) = 2 \cdot \text{Trits}(C_{tern}) $$
**Énoncé** : Nombre de variables booléennes requises pour encoder un problème ternaire en SAT via double rail.
**Conditions** : Encodage direct sans variables auxiliaires supplémentaires pour les états interdits.
**Statut** : PROUVÉ.
**Exemple numérique** : Un problème nécessitant $50$ trits de mémoire requiert exactement $100$ variables booléennes dans le solveur SAT.

Enfin, le coût de conversion entre les bases n'est pas nul. Il nécessite des arbres d'additionneurs binaires qui pèsent lourd dans le bilan énergétique global.

$$ C_{conv} = O(N) \text{ portes pour convertir } N \text{ trits} $$
**Énoncé** : Complexité en nombre de portes logiques pour convertir un mot de $N$ trits en binaire.
**Conditions** : Architecture à additionneurs à propagation de retenue ou à anticipation.
**Statut** : PROUVÉ.
**Exemple numérique** : Convertir un mot de $32$ trits nécessite un circuit de conversion dont la taille est proportionnelle à $32$, soit $O(32)$ portes logiques.

### Réseaux de neurones et quantification : le verdict de l'expérience

Si le ternaire ne change pas la complexité fondamentale du calcul booléen, il trouve un terrain d'application exceptionnel et inattendu dans l'apprentissage profond. La quantification des poids des réseaux de neurones est le domaine où le ternaire brille aujourd'hui, non pas par sa logique propositionnelle, mais par sa compacité mémoire et sa régularisation implicite. Le lemme L-T1 établit la base des neurones à seuil, héritiers directs des travaux de McCulloch et Pitts (1943).

$$ y = \text{sgn}\left( \sum_{i=1}^n w_i x_i - \theta \right), \quad w_i \in \{-1, 0, 1\} $$
**Énoncé** : Lemme L-T1. Sortie d'un neurone à seuil à poids ternaires.
**Conditions** : $x_i \in \{-1, 1\}$, $\theta$ est le seuil d'activation.
**Statut** : CONNU.
**Exemple numérique** : Pour $w = (1, -1)$, $x = (1, 1)$ et $\theta = 0$, on a $\sum w_i x_i = 1 - 1 = 0$. Donc $y = \text{sgn}(0) = 0$.

Les réseaux à poids ternaires (TWN) ont montr�� que l'on pouvait contraindre les poids pendant la propagation avant sans effondrement catastrophique de la précision, ouvrant la voie à l'inférence sur dispositifs embarqués.

$$ W^t = \begin{cases} 1 & \text{si } W > \Delta \\ 0 & \text{si } |W| \le \Delta \\ -1 & \text{si } W < -\Delta \end{cases} $$
**Énoncé** : Fonction de quantification des poids dans les réseaux TWN.
**Conditions** : $W$ est le poids flottant sous-jacent, $\Delta$ est le seuil d'apprentissage.
**Statut** : EXPÉRIMENTAL (Li, Zhang et Liu 2016).
**Exemple numérique** : Si $W = 0,5$ et $\Delta = 0,6$, alors $|W| \le \Delta$, donc le poids quantifié utilisé pour l'inférence est $W^t = 0$.

Plus récemment, l'ère des grands modèles de langage (LLM) à 1 bit, initiée par des travaux comme BinaryConnect (Courbariaux, Bengio et David 2015), a évolué vers 1,58 bit, prouvant que le ternaire est optimal pour remplacer la multiplication par de simples additions.

$$ w_{ij} \in \{-1, 0, 1\} $$
**Énoncé** : Ensemble des poids de la matrice de transformation dans l'architecture BitNet b1.58.
**Conditions** : Multiplication matrice-vecteur sans multiplications matérielles.
**Statut** : EXPÉRIMENTAL (Ma et al. 2024).
**Exemple numérique** : Un poids de $-1$ inverse le signe de l'activation, un poids de $0$ l'annule (économie d'énergie majeure), et $1$ la conserve intacte.

D'un point de vue informationnel, ce choix de 3 états correspond à une quantité d'information précise par poids, reliant l'algèbre linéaire à la théorie de l'information de Shannon (1948).

$$ H(T) = - \sum_{i \in \{-1, 0, 1\}} p_i \log_2(p_i) $$
**Énoncé** : Entropie de Shannon d'un trit.
**Conditions** : $p_i$ est la probabilité de l'état $i$, avec $\sum p_i = 1$.
**Statut** : CONNU.
**Exemple numérique** : Pour une distribution uniforme $p_i = 1/3$, $H(T) = -3 \times (1/3 \log_2(1/3)) = \log_2(3) \approx 1,58$ bits.

### Perspectives et questions ouvertes vers le programme RTC

Ce tome apporte une pierre essentielle à l'étude des traductions à ressources, le programme RTC (Resource Translation Calculus). Nous avons montré que les ressources (portes, profondeur, énergie) se traduisent par des facteurs constants. Mais des questions demeurent OUVERTES. Comment optimiser la constante $k$ du lemme L-T2 pour des topologies de puces neuromorphiques spécifiques ? Comment intégrer le coût énergétique de la mémoire SRAM face aux registres ternaires dans des environnements à très faible consommation ? Le programme RTC doit désormais s'emparer de ces variables physiques pour affiner nos modèles théoriques.

Pour clore ce bilan, il faut peser le gain théorique face au surcoût pratique de la conversion dans une architecture hybride.

$$ \text{Gain}_{net} = \underbrace{0,054 \cdot S}_{\text{économie de radix}} - \underbrace{C_{conv}}_{\text{surcoût de conversion}} $$
**Énoncé** : Équation de synthèse du gain net d'une architecture ternaire par rapport au binaire.
**Conditions** : $S$ est la taille de la structure de données, $C_{conv}$ est le coût des interfaces de conversion.
**Statut** : PROUVÉ.
**Exemple numérique** : Si la structure contient $S = 1000$ éléments (gain de $54$ unités) mais que l'interface de conversion coûte $C_{conv} = 100$ portes, alors $\text{Gain}_{net} = 54 - 100 = -46$. Dans ce cas, le ternaire perd.

### Mot final au lecteur

Cher lecteur, nous avons exploré ensemble les recoins de la base 3 équilibrée, de l'arithmétique de Łukasiewicz (1920) et Kleene (1952) jusqu'aux quantifications modernes des réseaux de neurones. J'espère que cet ouvrage vous a convaincu d'une vérité fondamentale : l'élégance mathématique ne se traduit pas toujours par une supériorité engineering. Le ternaire équilibré est un outil de conception magnifique, un prisme intellectuel qui simplifie l'écriture de certains algorithmes et qui trouve aujourd'hui une renaissance spectaculaire dans l'intelligence artificielle quantifiée.

Cependant, il ne faut jamais céder à l'illusion qu'une simple changement de base pourrait contourner les limites fondamentales de la calculabilité ou de la complexité. Le lemme L-T2 est là pour nous le rappeler avec la froideur d'une preuve formelle : toute traduction entre circuits binaires et ternaires coûte un facteur constant. Ce que la base 3 conserve en symétrie, elle le perd souvent en compatibilité avec un monde bâti, couche par couche, sur le silicium binaire.

Gardez ce livre comme un rappel que la rigueur est la plus belle des curiosités. Que vous soyez ingénieur matériel, chercheur en apprentissage automatique ou simplement un esprit curieux fasciné par les logiques alternatives, j'espère que ces pages vous auront armé pour distinguer le signal du bruit, la preuve de la conjecture, et l'outil de la magie. Le calcul ternaire n'est pas une nouvelle puissance de calcul ; c'est une autre façon, parfois plus belle, de poser les questions à la machine. Et c'est déjà, en soi, une raison suffisante pour l'étudier.

### Épilogue : Le registre des statuts comme boussole pour le programme RTC

Avant de refermer définitivement ces pages, il est de notre devoir de consolider l'héritage méthodologique de cet ouvrage. Le registre des statuts — cette discipline consistant à étiqueter chaque affirmation comme PROUVÉ, CONNU, EXPÉRIMENTAL, CONJECTURE, RÉFUTÉ ou OUVERT — n'est pas une simple coquetterie rhétorique. C'est le fondement même du programme RTC (Resource Translation Calculus) vers lequel nous transférons désormais nos travaux. Dans un domaine où l'enthousiasme pour les architectures non binaires a souvent devancé la preuve formelle, ce registre impose une hygiène intellectuelle stricte.

Pour formaliser cette démarche, nous pouvons définir la fonction d'évaluation d'une affirmation $A$ dans le cadre du programme RTC.

$$ \Sigma(A) \in \{\text{PROUVÉ}, \text{CONNU}, \text{EXPÉRIMENTAL}, \text{CONJECTURE}, \text{RÉFUTÉ}, \text{OUVERT}\} $$
**Énoncé** : Fonction de statut $\Sigma$ attribuant à toute proposition du cadre RTC un statut épistémique strict et exclusif.
**Conditions** : $\Sigma(A)$ ne peut être PROUVÉ que si une démonstration formelle ou une réduction polynomiale complète est fournie ; il ne peut être EXPÉRIMENTAL que si des résultats empiriques reproductibles sont publiés.
**Statut** : PROUVÉ (par construction méthodologique).
**Exemple numérique** : Pour l'affirmation $A =$ « Le lemme L-T2 borne la traduction des circuits », $\Sigma(A) = \text{PROUVÉ}$. Pour $B =$ « Le ternaire réduit la consommation énergétique des SRAM de 20 % », $\Sigma(B) = \text{EXPÉRIMENTAL}$.

Ce transfert vers le programme RTC soulève des questions qui dépassent le simple cadre de la base 3. Si le ternaire équilibré nous a servi de terrain d'expérimentation, les leçons apprises sur les traductions à ressources s'appliquent à toute architecture hétérogène. Qu'il s'agisse de calculateurs quantiques, de puces neuromorphiques ou de processeurs probabilistes, le coût de la traduction vers le binaire classique reste le goulot d'étranglement ultime.

La loi de conservation des ressources de traduction peut s'exprimer ainsi :

$$ R_{total} = R_{natif} + R_{traduction} + R_{interfaçage} $$
**Énoncé** : Décomposition du coût total en ressources $R_{total}$ d'un système de calcul hétérogène.
**Conditions** : $R_{natif}$ est le coût du calcul dans la base ou le paradigme d'origine, $R_{traduction}$ est le coût algorithmique de la conversion, et $R_{interfaçage}$ est le coût physique (E/S, mémoire tampon).
**Statut** : CONNU (principe général d'architecture des ordinateurs).
**Exemple numérique** : Si un calcul ternaire natif coûte $R_{natif} = 50$ portes, mais que la traduction et l'interfaçage coûtent respectivement $R_{traduction} = 120$ et $R_{interfaçage} = 80$ portes, alors $R_{total} = 250$ portes. Le gain natif est noyé dans le coût de la frontière.

C'est exactement cette frontière que le programme RTC devra cartographier pour d'autres bases, d'autres logiques, et d'autres paradigmes. Le ternaire équilibré n'était que le premier chapitre d'une théorie plus vaste : celle de l'économie de la traduction informationnelle.

Nous laissons aux chercheurs de demain un cadre clair, débarrassé des illusions magiques. Les portes ternaires de Łukasiewicz (1920) et les réseaux de neurones quantifiés de Ma et al. (2024) partagent une même vérité : l'information ne se crée pas par un simple changement de dictionnaire. Elle se compresse, se translate, se code, mais son entropie fondamentale, telle que définie par Shannon (1948), demeure inaltérée par le choix de la base.

$$ I(X; Y) \le \min(H(X), H(Y)) $$
**Énoncé** : L'information mutuelle entre l'entrée et la sortie d'un système de traduction est bornée par l'entropie de la représentation la plus pauvre.
**Conditions** : $X$ et $Y$ sont les variables aléatoires représentant les états dans deux bases différentes.
**Statut** : CONNU (Shannon 1948).
**Exemple numérique** : Si $X$ est un mot binaire de 16 bits ($H(X) = 16$) et $Y$ son équivalent ternaire sur 11 trits ($H(Y) \approx 11 \times 1,58 = 17,38$), l'information mutuelle maximale transmise sans perte est $\min(16 ; 17,38) = 16$ bits. Le ternaire n'a pas créé d'information supplémentaire.

En définitive, ce livre se veut un manifeste pour la lucidité en informatique théorique et appliquée. Nous avons construit, formule après formule, table de vérité après table de vérité, un édifice où l'élégance du ternaire équilibré peut être admirée sans être idolâtrée. Le gain de 5,4 % de l'économie de radix restera à jamais une belle curiosité mathématique, un rappel que la nature préfère parfois la base $e$, mais que l'humanité a choisi la base 2 pour des raisons de bruit thermique et de marge de sécurité, et non par manque d'imagination.

Que ce registre des statuts vous accompagne. Qu'il vous protège des annonces prématurées de suprématie technologique. Et qu'il vous rappelle, à chaque fois que vous concevrez un circuit, un réseau de neurones ou un encodeur SAT, que la véritable ingénierie consiste à connaître le prix exact de chaque translation.

Le voyage en base 3 s'achève ici. Le programme RTC, lui, ne fait que commencer.