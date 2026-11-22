## Introduction

### Le noyau minimal du calcul

Qu'est-ce que calculer ? Avant même que les ordinateurs n'existent sous leur forme matérielle, avant que les circuits de silicium ne tracent des chemins pour les électrons, le calcul était une affaire de symboles, de règles et de substitutions. Si l'on cherche à isoler l'essence la plus pure de la computation fonctionnelle, on finit inévitablement par converger vers une structure d'une austérité et d'une puissance fascinantes : le lambda-calcul. Ce livre est une exploration anatomique de cette structure. Il ne s'agit pas d'un manuel d'apprentissage d'un langage de programmation parmi d'autres, mais d'une dissection minutieuse de la mécanique intime du calcul lui-même.

Le lambda-calcul nous enseigne que pour calculer, il faut extraordinairement peu de choses. Il ne requiert ni mémoire mutable, ni boucles de contrôle, ni types de données primitifs. Il se contente d'arbres syntaxiques, d'une équivalence de nommage (l'alpha-équivalence) et d'une unique règle de transformation (la bêta-réduction). Cette minimalité fondatrice a été établie comme socle de la calculabilité au milieu des années 1930. Alonzo Church a démontré en 1936, dans son travail sur les problèmes insolubles de la théorie des nombres, que certaines fonctions ne pouvaient être définies par ce calcul, posant ainsi les limites de la mécanique symbolique. Presque simultanément, Alan Turing a établi en 1937 l'équivalence profonde entre la définissabilité dans le lambda-calcul et le calcul sur ses propres machines abstraites. Ce rapprochement historique scelle un fait épistémologique majeur : le lambda-calcul n'est pas une simple curiosité mathématique, il est l'un des visages universels de l'algorithme (CONNU).

Pourtant, cette universalité et cette minimalité masquent une complexité redoutable. Si la règle de calcul s'écrit en une ligne sur le papier, son exécution physique ou même sa modélisation rigoureuse soulève des abîmes. Tout le coût du calcul fonctionnel est concentré dans une seule opération : la substitution. Remplacer une variable par un terme au sein d'un autre terme semble trivial pour l'esprit humain, mais c'est une opération destructrice et coûteuse pour la machine. C'est ici que commence l'anatomie fonctionnelle du calcul : comprendre non seulement ce qui est calculé, mais ce que coûte chaque pas de calcul.

### Le prix de la minimalité : une anatomie des ressources

La thèse centrale de cet ouvrage est que le lambda-calcul, dans sa forme pure, est une structure minimale dont la manipulation engendre un prix systématique. Ce prix n'est pas toujours visible dans les manuels d'introduction, qui traitent la substitution comme une réécriture gratuite. Or, le nombre de pas bêta n'est pas spontanément une mesure de temps physique. La taille des termes peut exploser de manière exponentielle au cours de la réduction, et le partage des sous-termes devient une ressource à part entière, une monnaie d'échange entre le temps et l'espace.

Chaque fois que nous traduisons le lambda-calcul pur vers un autre formalisme pour le rendre plus efficace, plus sûr ou plus compréhensible, nous effectuons un choix économique. Les termes vers les indices positionnels éliminent le coût de l'alpha-équivalence mais complexifient la substitution. Les termes vers les combinateurs suppriment les variables au prix d'une explosion de la taille des termes intermédiaires. Les termes vers les machines à fermetures (closures) déplacent le coût de la substitution vers la gestion de l'environnement d'évaluation. Les termes vers les graphes partagés transforment la duplication en pointeurs, achetant du temps au prix de la complexité structurelle. Enfin, les termes vers les preuves typées échangent de l'expressivité contre une garantie absolue : la terminaison.

Ces traductions conservent toutes la puissance de calcul originelle et la propriété de confluence, mais elles déplacent le coût entre la taille, le temps, la mémoire, la profondeur, la largeur, la précision et le partage. Le typage, en particulier, agit comme un contrat d'assurance : il restreint l'univers des programmes possibles pour garantir que l'évaluation ne divergera jamais. La normalisation forte du lambda-calcul simplement typé est le prix acheté par cette restriction (CONNU). Mon objectif est de cartographier ces échanges, de peser chaque traduction et de montrer qu'en informatique théorique, rien ne se perd, rien ne se crée, tout se paie.

### La démarche : traductions, statuts et reconstructions

Pour naviguer dans ce paysage, ce livre adopte une démarche rigoureuse, presque clinique. Je ne revendique ici aucun résultat nouveau. Le domaine de la calculabilité et de la sémantique des langages est riche de théorèmes profonds, et mon rôle n'est pas d'annoncer des découvertes, mais de reconstruire complètement les énoncés que je démontre. Pour les grands théorèmes fondateurs, je fournirai les idées de preuve en les annonçant explicitement comme telles, afin de ne jamais présenter une intuition comme une démonstration formelle.

Pour garantir cette honnêteté intellectuelle, chaque affirmation, chaque théorème et chaque observation empirique dans ce livre porte un statut explicite, tiré d'un registre strict :
- **PROUVÉ** : le résultat est entièrement démontré dans les pages de ce livre, avec tout le détail nécessaire.
- **CONNU** : le résultat est un théorème majeur de la littérature (comme la confluence ou l'équivalence de Turing) ; j'en donne l'idée de preuve et le contexte, sans alourdir le texte par des dizaines de pages de technique formelle.
- **EXPÉRIMENTAL** : l'affirmation repose sur des observations empiriques concernant les coûts de réduction ou le comportement des machines abstraites.
- **CONJECTURE** : une hypothèse structurante du domaine qui n'a pas encore reçu de preuve définitive.
- **RÉFUTÉ** : une intuition séduisante mais qui s'est heurtée à la réalité mathématique, souvent liée à des tentatives d'optimisation naive du partage.
- **OUVERT** : une question fondamentale qui demeure sans réponse et qui trace les frontières actuelles de notre compréhension.

Ce registre des statuts est une boussole pour le lecteur. Il permet de distinguer ce qui est gravé dans le marbre mathématique de ce qui relève de l'ingénierie, de la conjecture ou de la frontière de la recherche. Les références citées pour appuyer ces statuts sont strictement limitées aux textes fondateurs et structurants du domaine, de Church et Turing aux travaux contemporains sur l'invariance de la réduction et les machines abstraites.

### À qui s'adresse ce livre

Ce livre est conçu pour un lecteur cultivé non spécialiste. Vous n'avez pas besoin d'être un chercheur en sémantique formelle pour le lire, mais vous devez posséder une certaine maturité mathématique et une curiosit�� pour les fondements de l'informatique. Que vous soyez mathématicien, philosophe des sciences, physicien théoricien, ou programmeur cherchant à comprendre les fondations des langages fonctionnels que vous utilisez, cet ouvrage vous fournira les outils conceptuels pour penser le calcul.

Pour servir ce public, chaque chapitre suit une trame pédagogique immuable :
1. **Intuition** : une explication conceptuelle, souvent imagée, pour saisir le *pourquoi* avant le *comment*.
2. **Définition** : la formalisation rigoureuse des objets et des règles.
3. **Énoncé statuté** : le théorème ou la propriété, accompagné de son statut (PROUVÉ, CONNU, etc.).
4. **Exemple** : une manipulation concrète sur des termes pour ancrer l'abstraction.
5. **Exercice** : une invitation à tester soi-même les limites de sa compréhension.

Le format visé est celui d'un ouvrage d'environ 220 pages, structuré en 16 chapitres denses, complétés par des annexes de preuves et un index. L'ensemble est divisé en quatre grandes parties, traçant un chemin progressif de l'abstraction pure vers la réalité matérielle des machines.

### Le grand atlas des traductions

L'architecture de ce livre est conçue comme un voyage à travers les différentes couches de réalité du lambda-calcul. Nous partirons du noyau symbolique pour descendre progressivement vers les contraintes physiques de l'évaluation, avant de remonter vers les garanties logiques du typage, pour finir sur une cartographie globale des coûts.

#### Partie I — Le noyau : arbres, noms, substitution, confluence
Cette première partie pose les fondations. Il s'agit de définir l'univers minimal dans lequel nous allons évoluer.
- **Chapitre 1 – Pourquoi un calcul de fonctions pures** : Nous explorerons la genèse philosophique et mathématique du lambda-calcul. Pourquoi abandonner l'état, les effets de bord et les boucles ? Nous verrons comment Church 1936 et Turing 1937 ont convergé vers l'idée que la manipulation de symboles selon des règles de substitution suffit à capturer l'essence de l'algorithme.
- **Chapitre 2 – Termes, portée, alpha-équivalence** : Nous définirons la syntaxe abstraite. Les termes ne sont pas des chaînes de caractères, mais des arbres. Nous introduirons la notion cruciale de portée des variables et l'alpha-équivalence, qui nous enseigne que le nom d'une variable est un accident historique sans importance pour le calcul (CONNU). Barendregt 1984 servira de guide pour la rigueur de ces définitions.
- **Chapitre 3 – La substitution : définition honnête et coût réel** : C'est le cœur battant du livre. Nous définirons la substitution $M[x := N]$ avec le soin chirurgical qu'elle exige pour éviter la capture de variables. Nous mettrons en lumière le fait que la substitution n'est pas une opération atomique, mais un processus de copie qui porte en lui le germe de l'explosion de la taille des termes.
- **Chapitre 4 – Bêta-réduction et confluence : le théorème de Church-Rosser** : Nous introduirons la seule règle de calcul : $(\lambda x. M) N \rightarrow M[x := N]$. Nous énoncerons et donnerons l'idée de preuve du théorème de Church et Rosser 1936, qui garantit que l'ordre dans lequel nous effectuons les calculs ne change pas le résultat final, pourvu qu'il y en ait un. La confluence est la propriété qui rend le calcul fonctionnel déterministe dans son résultat, même s'il est non-déterministe dans son exécution (CONNU).

#### Partie II — Stratégies, données, récursion : le calcul sans types
Une fois le noyau défini, il faut apprendre à s'en servir pour exprimer des programmes réels et comprendre les pièges de l'évaluation.
- **Chapitre 5 – Stratégies d'évaluation : choisir l'ordre des redexes** : Puisque la confluence nous laisse le choix de l'ordre de réduction, quel chemin emprunter ? Nous comparerons l'appel par nom (call-by-name), l'appel par valeur (call-by-value) et la réduction de tête, en analysant comment chaque stratégie impacte la terminaison et le nombre de pas.
- **Chapitre 6 – Normalisation, divergence, limites** : Tous les termes ne se réduisent pas à une forme normale. Nous étudierons la divergence (les boucles infinies) et les théorèmes de normalisation, en montrant que l'indécidabilité de l'arrêt est une conséquence directe de la puissance du calcul pur.
- **Chapitre 7 – Encodages de Church : données et programmes dans le même univers** : Comment représenter les entiers, les booléens et les paires sans aucun type de données primitif ? Nous détaillerons les encodages de Church, démontrant que la fonction pure suffit àincarner la donnée. Le calcul contient sa propre ontologie.
- **Chapitre 8 – Combinateurs et récursion : S, K, Y** : Nous nous appuierons sur les travaux de Hindley et Seldin 2008 pour explorer la logique combinatoire. En supprimant les variables (et donc la substitution), nous paierons le prix de l'abstraction par l'explosion combinatoire. Nous introduirons le combinateur de point fixe Y, clé de voûte de la récursion dans un univers sans affectation.

#### Partie III — Types, preuves, machines : trois traductions du même calcul
Cette partie explore trois traductions majeures qui modifient radicalement la nature du lambda-calcul pour répondre à des besoins spécifiques : la sécurité, la vérité logique et l'exécution physique.
- **Chapitre 9 – Lambda-calcul simplement typé** : Nous introduirons les types comme une restriction syntaxique. En annotant les termes, nous limitons drastiquement l'expressivité du langage. Pierce 2002 nous guidera dans l'algèbre des types et les règles d'inférence.
- **Chapitre 10 – Normalisation forte : la terminaison comme ressource achetée** : Nous démontrerons que dans le lambda-calcul simplement typé, toute séquence de réduction termine (PROUVÉ). C'est le grand théorème de normalisation forte. Nous analyserons ce que nous avons perdu (la récursion générale, la Turing-complétude) pour acheter cette garantie absolue.
- **Chapitre 11 – Curry-Howard : réduire, c'est simplifier une preuve** : Nous exposerons la correspondance découverte par Howard 1980. Un programme est une preuve, un type est une proposition logique, et la bêta-réduction est la simplification de cette preuve. Cette traduction élève le calcul au rang de raisonnement mathématique constructif.
- **Chapitre 12 – Machines abstraites : SECD et Krivine** : Comment un tas de silicium exécute-t-il un arbre syntaxique ? Nous étudierons la machine SECD de Landin 1964, pionnière de l'évaluation par fermetures, puis la machine de Krivine 2007, chef-d'œuvre de minimalisme pour l'appel par nom. Nous verrons comment ces machines traduisent les termes en états, en piles et en environnements, déplaçant le coût de la substitution vers la gestion de la mémoire.

#### Partie IV — Coûts, partage, atlas des traductions, transfert RTC
La dernière partie est la synthèse économique et conceptuelle de l'ouvrage. Elle dresse le bilan des ressources et ouvre les perspectives vers des modèles de calcul plus fins.
- **Chapitre 13 – Le coût de la réduction : du nombre de pas au temps réel** : Le nombre de pas bêta est-il une bonne mesure de complexité ? Nous discuterons des résultats d'Accattoli et Dal Lago 2016, qui ont montré que la réduction leftmost-outermost est invariante, c'est-à-dire qu'elle fournit une mesure de temps robuste, à condition de comprendre comment la machine sous-jacente gère la taille des termes (CONNU).
- **Chapitre 14 – Partage et réduction optimale** : Pour éviter l'explosion de la taille des termes par la substitution, il faut partager. Nous étudierons l'algorithme de Lamping 1990 pour la réduction optimale, qui utilise des graphes de partage complexes pour ne dupliquer que ce qui doit l'être, au prix d'une overhead algorithmique fascinant.
- **Chapitre 15 – Atlas des traductions : ce qui est conservé, ce qui est perdu** : Ce chapitre sera une synthèse cartographique. Pour chaque traduction (indices, combinateurs, machines, graphes, types), nous résumerons dans un tableau ce qui est invariant (puissance, confluence) et ce qui est déplacé (taille, temps, mémoire, partage).
- **Chapitre 16 – Transfert vers le programme RTC** : Le chapitre final opère le transfert vers le programme RTC (Réseaux de Traductions et Calculs à ressources). Il synthétisera ce que ce tome apporte à l'étude des traductions à ressources : quelles ressources avons-nous identifiées ? Quelles traductions avons-nous cartographiées ? Quelles questions demeurent OUVERTES pour les tomes et recherches futurs ? Ce chapitre servira de pont entre la théorie classique du lambda-calcul et les modèles de calcul contemporains où la ressource (énergie, mémoire, qubits) est la contrainte première.

### Ouverture

Le lambda-calcul est un miroir. Quand on le regarde superficiellement, on n'y voit que des lettres grecques et des parenthèses. Mais quand on accepte de plonger dans son anatomie, on y découvre les lois de conservation de l'information et de l'énergie computationnelle. Chaque traduction que nous allons explorer dans ces pages est une lentille différente posée sur le même objet fondamental. Aucune lentille n'est parfaite ; chacune introduit une aberration, un coût, une distorsion. Mais c'est précisément dans l'étude de ces distorsions que réside la véritable compréhension de l'informatique théorique.

Nous n'allons pas apprendre à programmer en lambda-calcul pour écrire des applications web. Nous allons apprendre à penser le calcul pour comprendre ce qui se passe lorsque le symbole rencontre la machine, lorsque l'abstraction se heurte à la finitude de la mémoire, et lorsque la promesse de l'infini mathématique doit être payée en cycles d'horloge et en octets.

L'anatomie fonctionnelle du calcul commence ici. Tournons la page, et entrons dans le noyau.

## Chapitre 1 – Pourquoi un calcul de fonctions pures

### Intuition : L'effacement de la machine

Lorsque l'on prononce le mot « ordinateur », l'imaginaire collectif convoque aussitôt des circuits, des horloges, des registres mémoire et des flux d'électrons. Notre intuition moderne du calcul est profondément marquée par l'architecture de von Neumann : une unité de traitement qui lit des données dans une mémoire, les modifie, et les réécrit. Le temps y est une séquence d'états mutables. Calculer, dans ce paradigme, c'est faire évoluer un état vers un autre.

Mais que se passe-t-il si l'on retire la mémoire ? Que reste-t-il du calcul si l'on interdit la mutation, si l'on efface le temps physique, et si l'on refuse toute notion d'état global ? Il reste une structure d'une pureté absolue, où le calcul n'est plus la transformation d'un état, mais la simplification d'une expression. C'est le pari fondateur du lambda-calcul.

L'intuition de ce chapitre est la suivante : pour comprendre la véritable nature du calcul, il faut d'abord accepter de l'amputer de tout ce qui le rend matériellement commode. Il faut oublier les variables mutables, les boucles de contrôle, les pointeurs et les effets de bord. En nous imposant cette austérité, nous ne perdons rien de la puissance de calcul — c'est là le miracle — mais nous gagnons une visibilité parfaite sur la mécanique intime de l'évaluation. Le lambda-calcul pur est un microscope. En éliminant le bruit de la machine à états, il nous force à regarder la seule opération qui constitue véritablement le calcul fonctionnel : la substitution.

### Le refus de l'état et la transparence référentielle

Dans un langage de programmation classique, l'expression $f(x) + f(x)$ n'est pas toujours équivalente à $2 \times f(x)$. Si la fonction $f$ lit une horloge système, modifie une variable globale ou interagit avec un réseau, l'évaluer deux fois produira un résultat différent de l'évaluer une seule fois et doubler le résultat. L'état caché brise l'équivalence mathématique.

Le lambda-calcul pur impose la transparence référentielle absolue. Une expression ne dépend que de ses sous-expressions. Si deux termes sont structurellement identiques, ils sont interchangeables dans n'importe quel contexte sans altérer le sens ou le résultat du calcul. Cette propriété, qui semble aller de soi en mathématiques, est une contrainte redoutable en informatique. Elle signifie que le calcul est atemporel : un terme ne « s'exécute » pas, il se « réduit ». Il n'y a pas d'avant ni d'après, il n'y a que des relations de déduction entre des arbres syntaxiques.

Ce choix n'est pas seulement esthétique ; il est épistémologique. En 1936, lorsqu'Alonzo Church cherche à formaliser la notion de fonction effective, il ne part pas de la machine. Il part de la logique et des symboles. Son article fondateur, *An unsolvable problem of elementary number theory* (Church 1936), ne décrit pas un processeur, mais un système de réécriture. L'idée de Church est que la calculabilité n'a pas besoin de substrat physique pour être définie ; elle émerge de la seule manipulation syntaxique de symboles selon des règles de substitution rigoureuses.

### Définition : Les trois briques de l'univers

Pour construire cet univers sans état, nous n'avons besoin que de trois concepts. C'est là que la minimalité du lambda-calcul prend tout son sens. Tout terme, aussi complexe soit-il, est construit à partir de ces trois briques :

1. **La variable** : un simple nom, un symbole (comme $x$, $y$, $z$). Elle ne contient aucune valeur, elle n'est qu'un espace réservé, une promesse d'instanciation.
2. **L'abstraction** : la création d'une fonction. Si $M$ est un terme et $x$ une variable, alors $\lambda x. M$ est un terme. Cela se lit « la fonction qui, à $x$, associe $M$ ». C'est le seul moyen de créer une structure qui attend une donnée.
3. **L'application** : l'acte de calculer. Si $M$ et $N$ sont des termes, alors $(M \ N)$ est un terme. Cela signifie « appliquer la fonction $M$ à l'argument $N$ ».

C'est tout. Il n'y a pas de nombres entiers, pas de booléens, pas de structures de contrôle. Les nombres et les conditions seront des conquêtes ultérieures, des édifices bâtis sur ces trois fondations. La grammaire de notre univers tient en une ligne :
$$ M, N ::= x \mid \lambda x. M \mid (M \ N) $$

Cette définition inductive est d'une simplicité trompeuse. Elle cache le fait que l'abstraction lie la variable $x$ dans le terme $M$, créant ainsi une frontière, une « portée ». Comprendre comment cette portée interagit avec l'application sera l'objet de notre prochain chapitre. Mais pour l'heure, retenons que le lambda-calcul est un langage où la donnée et le programme sont faits de la même étoffe : des arbres syntaxiques.

### Énoncé statuté : L'équivalence des modèles de calcul

Pourquoi devrions-nous croire que ce jeu de réécriture symbolique, dépourvu de mémoire et de boucles, capture l'intégralité de ce qui est calculable ? C'est ici qu'intervient l'un des piliers de l'informatique théorique.

**Énoncé (CONNU) : Thèse de Church-Turing et équivalence des modèles.**
*La classe des fonctions définissables dans le lambda-calcul pur est exactement identique à la classe des fonctions calculables par une machine de Turing.*

**Statut : CONNU.**
Ce résultat n'est pas démontré dans ce livre, car il repose sur une double simulation fastidieuse qui n'éclaire pas l'anatomie des ressources. Voici cependant l'idée de la preuve, telle qu'elle a été établie historiquement.
D'un côté, Alan Turing, dans *Computability and lambda-definability* (Turing 1937), a montré que l'on pouvait encoder la machine de Turing (son ruban, sa tête de lecture, sa table de transitions) sous forme de termes du lambda-calcul. Chaque étape de la machine devient une réduction bêta.
De l'autre, Church et ses étudiants ont montré que l'on pouvait simuler la substitution du lambda-calcul sur une machine de Turing, en manipulant des chaînes de caractères et des symboles sur un ruban.
Puisque les deux modèles peuvent s'émuler mutuellement avec une perte de contrôle sur le temps et l'espace, ils définissent la même frontière de la calculabilité. Le lambda-calcul n'est donc pas un sous-ensemble de l'informatique ; il en est l'un des visages universels.

### Exemple : Le moindre programme

Pour ancrer cette abstraction, observons le terme le plus simple qui soit, celui qui incarne l'identité pure :
$$ I = \lambda x. x $$
Ce terme est une fonction qui prend un argument $x$ et le retourne tel quel. Il ne fait rien. Mais en informatique, « ne rien faire » est déjà une opération qui a un coût.

Appliquons cette fonction à elle-même. Le terme s'écrit :
$$ (I \ I) = ((\lambda x. x) \ (\lambda y. y)) $$
(Notez que j'ai renommé la variable de l'argument en $y$ pour la clarté, une opération que nous formaliserons sous le nom d'alpha-équivalence au chapitre 2).

Que se passe-t-il lorsque nous évaluons ce terme ? La règle de calcul, que nous détaillerons au chapitre 3, nous dit de prendre le corps de la fonction (ici, $x$) et d'y remplacer la variable liée ($x$) par l'argument fourni (ici, $\lambda y. y$).
Le résultat de cette substitution est :
$$ \lambda y. y $$
Nous avons effectué un pas de calcul. Nous avons consommé une application pour révéler que l'identité appliquée à l'identité n'est rien d'autre que l'identité. Le terme s'est simplifié. C'est cela, calculer en lambda-calcul : réduire la complexité syntaxique d'un arbre en y propageant des sous-arbres.

Considérons maintenant un terme légèrement plus complexe, le combinateur d'auto-application, souvent noté $\omega$ :
$$ \omega = \lambda x. (x \ x) $$
Que se passe-t-il si nous appliquons $\omega$ à lui-même ?
$$ (\omega \ \omega) = ((\lambda x. (x \ x)) \ (\lambda x. (x \ x))) $$
En appliquant la règle de substitution, nous remplaçons le $x$ du corps par l'argument entier. Le résultat est :
$$ ((\lambda x. (x \ x)) \ (\lambda x. (x \ x))) $$
Nous sommes revenus à notre point de départ. Le terme s'est réécrit en lui-même. C'est la naissance de la divergence, de la boucle infinie, non pas par un saut inconditionnel ou une instruction de boucle matérielle, mais par la pure géométrie de la substitution. L'auto-référence, et donc l'infini computationnel, émerge spontanément de l'application d'une fonction à elle-même.

### La pureté comme loupe sur les ressources

Revenons à la thèse de ce livre. Pourquoi s'imposer cette pureté ? Parce que dans un langage impératif, le coût du calcul est masqué par la machine. Lorsque vous faites une boucle, le coût est celui de l'incrémentation d'un registre et d'un saut d'instruction. Lorsque vous copiez un tableau, le coût est celui d'une allocation mémoire et d'un transfert de bus.

En lambda-calcul pur, il n'y a qu'une seule opération : la substitution $M[x := N]$.
Si le calcul explose en temps ou en espace, c'est exclusivement la faute de la substitution. Soit nous substituons un terme $N$ très grand dans de nombreux endroits de $M$ (explosion de la taille), soit nous substituons le même terme encore et encore dans une boucle infinie (divergence temporelle).

Cette minimalité transforme le lambda-calcul en un laboratoire idéal pour l'étude des ressources. Chaque traduction que nous explorerons dans ce livre — vers les indices positionnels, vers les combinateurs, vers les machines abstraites comme celle de Krivine 2007 — est une tentative de résoudre les pathologies de la substitution pure.
- Les machines à environnements (Landin 1964) retardent la substitution pour éviter de copier des termes inutilement.
- La réduction optimale (Lamping 1990) partage les sous-termes pour ne jamais dupliquer le travail.
- Le typage (Pierce 2002) restreint les termes autorisés pour interdire les boucles infinies comme $(\omega \ \omega)$.

En comprenant le noyau pur, nous comprenons la maladie. Les chapitres suivants seront les remèdes, avec leurs effets secondaires.

### Exercice : Penser sans effets de bord

Pour clore ce chapitre d'introduction au noyau, je vous propose un exercice de déconditionnement. Il ne s'agit pas de manipuler des formules, mais de rééduquer votre intuition.

**Exercice 1.1 (Conceptuel) :**
Considérez la fonction suivante, écrite dans un pseudo-code impératif familier :
```
compteur = 0
fonction f(x):
    compteur = compteur + 1
    return x * 2
```
Si j'évalue `f(3) + f(3)`, le résultat est `12`, et la variable globale `compteur` vaut `2`.
Si j'évalue `y = f(3)` puis `y + y`, le résultat est `12`, mais `compteur` vaut `1`.

1. Expliquez pourquoi la transparence référentielle est violée dans ce programme.
2. Proposez une réécriture de ce programme en utilisant uniquement des fonctions pures (où l'état du compteur doit être passé explicitement en argument et retourné).
3. Réfléchissez au coût de cette réécriture : combien de fois le terme représentant l'état du compteur doit-il être dupliqué ou propagé par rapport à la version impérative ?

**Exercice 1.2 (Syntaxique) :**
En utilisant uniquement les trois règles de formation (variable, abstraction, application), construisez un terme qui prend deux arguments $x$ et $y$ et qui retourne $x$ en ignorant $y$.
*Indice : L'abstraction peut être imbriquée. $\lambda x. \lambda y. M$ est une fonction qui attend un premier argument, puis un second.*

Ces exercices ne sont pas de simples jeux syntaxiques. Ils vous forcent à ressentir physiquement le poids de la propagation de l'information. Dans un monde sans mémoire globale, l'information doit voyager. Et faire voyager l'information, c'est substituer. C'est là le prix de la pureté, et le début de notre anatomie.