## Introduction

### Traduire un calcul, c'est payer une ressource

Depuis les travaux fondateurs d'Alan Turing (Turing 1936), la communauté scientifique vit avec une certitude à la fois profonde et trompeuse : tous les modèles de calcul raisonnables sont équivalents. Qu'il s'agisse d'une machine à ruban, d'un réseau de portes logiques ou d'une formule propositionnelle, la classe des fonctions calculables reste la même. Cette thèse, pilier de l'informatique théorique, nous a permis de bâtir une théorie robuste de la calculabilité. Mais elle a aussi engendré une illusion tenace. En nous habituant à l'équivalence des modèles, nous avons fini par oublier que cette équivalence n'est valable que pour l'existence du calcul, et non pour son coût.

Dans ce livre, je vous propose de rompre avec cette illusion. Ma thèse centrale est la suivante : une traduction entre modèles de calcul n'est jamais gratuite ; c'est un échange de ressources. Passer d'une machine de Turing à un circuit booléen, puis de ce circuit à une formule du problème de satisfiabilité propositionnelle (SAT), n'est pas un simple changement de notation. C'est une opération physique et mathématique qui transforme le temps en taille, l'espace en largeur, et la séquentialité en profondeur. Chaque flèche de traduction possède un prix exact, et ce tome est consacré à la comptabilité rigoureuse de ces échanges.

Pour mener à bien cette entreprise, il faut abandonner l'idée que les modèles de calcul sont des vases communicants parfaits. Lorsqu'on traduit un algorithme séquentiel en un circuit parallèle, on gagne en profondeur ce que l'on perd en taille. Lorsqu'on encode ce circuit en clauses logiques pour le soumettre à un solveur SAT, on gagne en universalité de résolution ce que l'on perd en précision sémantique. Ce livre suit la chaîne complète de ces traductions : machines de Turing $\rightarrow$ circuits $\rightarrow$ SAT, puis le sens inverse. Pour chaque flèche, pour chaque traduction, nous tiendrons une fiche obligatoire qui détaillera le sens de la traduction, son coût en ressources, ce qu'elle conserve et ce qu'elle perd irrémédiablement.

### Le programme RTC et le registre des statuts

Pour structurer cette comptabilité, ce livre s'inscrit dans un cadre conceptuel précis : le programme de recherche RTC, pour « Les Traductions du Calcul ». L'objectif de RTC est d'étudier quelles ressources — taille, temps, mémoire, profondeur, largeur, précision, partage — chaque traduction entre modèles de calcul conserve, transforme ou détruit. Ce volume est le tome de TRADUCTION par excellence, celui qui lie les modèles dynamiques (les machines) aux modèles statiques (les circuits) et déclaratifs (les clauses).

Le programme RTC repose sur sept ressources fondamentales qui seront nos unités de mesure tout au long de ces pages :
1. **La taille** : le nombre d'états, de portes logiques ou de clauses nécessaires pour décrire le calcul.
2. **Le temps** : le nombre d'étapes de calcul, de transitions ou de résolutions.
3. **La mémoire** (ou espace) : la quantité de ruban, de fils ou de variables actives simultanément.
4. **La profondeur** : la plus longue chaîne de dépendances causales, du début à la fin du calcul.
5. **La largeur** : la mesure de la complexité structurelle, comme la largeur de chemin (*pathwidth*) ou la largeur d'arbre (*treewidth*), qui dicte comment le calcul peut être découpé.
6. **La précision** : la fidélité de la correspondance entre le modèle source et le modèle cible. Dans notre cadre booléen, cela désigne l'équivalence logique, l'équisatisfiabilité, ou la projection des modèles.
7. **Le partage** : la capacité à réutiliser un même sous-calcul, mesurée par le fan-out d'un circuit ou les variables d'extension d'une forme normale conjonctive (CNF).

Parce que la rigueur est la condition sine qua non de ce programme, chaque affirmation de ce livre porte un statut épistémologique clair, tiré d'un registre de six statuts. Il n'y a pas de place pour l'ambiguïté entre ce qui est démontré, ce qui est observé et ce qui est supposé :
- **PROUVÉ** : l'énoncé est démontré intégralement dans ce tome, avec une preuve écrite, complète et vérifiable (construction, comptage, bornes).
- **CONNU** : l'énoncé est un théorème de la littérature citée. Ce tome en donne l'idée de la preuve et l'intuition, en le disant explicitement, sans prétendre à l'originalité.
- **EXPÉRIMENTAL** : l'énoncé est un constat mesuré selon un protocole décrit. Il n'est pas généralisable sans preuve formelle.
- **CONJECTURE** : l'énoncé est cru vrai, soutenu par des indices, mais non démontré.
- **RÉFUTÉ** : l'énoncé est faux, et le tome fournit un contre-exemple explicite ou une contradiction avec un énoncé PROUVÉ.
- **OUVERT** : la question n'est résolue ni dans ce tome ni dans les références citées.

Ce registre des statuts n'est pas une simple précaution de style ; c'est l'ossature intellectuelle du livre. Il nous permettra, par exemple, de séparer nettement la preuve du lemme L-02 sur la largeur des tableaux de calcul (PROUVÉ) des écarts observés avec les heuristiques modernes d'évaluation de largeur (EXPÉRIMENTAL).

### Les trois modèles : Machines, Circuits, SAT

Le voyage de ce tome s'articule autour de trois modèles de calcul qui forment la colonne vertébrale de la théorie de la complexité.

Le premier modèle est la **machine de Turing**. Introduite pour formaliser la notion d'algorithme (Turing 1936), elle est le modèle de la séquentialité et du temps. Une machine de Turing déroule son calcul pas à pas, modifiant son état et son ruban. Son tableau de calcul, qui fige l'histoire complète de l'exécution dans une grille à deux dimensions, sera notre objet central pour observer comment le temps se spatialise.

Le deuxième modèle est le **circuit booléen**. Contrairement à la machine, le circuit n'a pas de notion de temps qui s'écoule ; il est une structure spatiale, un graphe acyclique dirigé où l'information circule des entrées vers les sorties (Jukna 2012). Le circuit est le modèle du parallélisme et de la profondeur. Traduire une machine en circuit, c'est accepter de déployer toute l'histoire du calcul dans l'espace, en payant la taille du circuit pour acheter la faible profondeur de l'évaluation.

Le troisième modèle est le **problème de satisfiabilité propositionnelle (SAT)**. C'est le modèle déclaratif par excellence. Au lieu de décrire *comment* calculer, une formule SAT décrit *quelles conditions* doivent être remplies pour qu'une solution soit valide (Cook 1971 ; Levin 1973). SAT est le réceptacle universel des problèmes de décision (Biere, Heule, van Maaren et Walsh 2009). Traduire un circuit ou un tableau en clauses SAT, c'est abandonner la structure algorithmique pour ne conserver que la contrainte logique, un échange qui se paie en variables auxiliaires et en perte de précision sémantique.

### Les grandes leçons du voyage

Au fil des traductions que nous allons décortiquer, trois grandes leçons émergent, structurant la thèse de ce livre. Aucune de ces leçons n'annonce un effondrement miraculeux des classes de complexité ; elles révèlent au contraire la rigidité implacable de la comptabilité des ressources.

**Première leçon : le temps se paie en taille et en profondeur.**
Lorsqu'on déroule le tableau de calcul d'une machine de Turing pour en faire un circuit, la taille du circuit croît linéairement avec le temps de calcul $t$. Cependant, en exploitant la structure des opérations, on peut optimiser cette traduction. La simulation en $O(t \log t)$, un résultat classique de Pippenger et Fischer (Pippenger et Fischer 1979), montre que le temps peut être compressé en taille et en profondeur au prix d'une complexité structurelle accrue. Ce résultat est CONNU, et nous en explorerons l'idée de la preuve et les implications sur le partage des sous-calculs.

**Deuxième leçon : l'espace se lit en largeur.**
C'est le cœur battant de la partie III de ce livre. Si le temps se déploie en taille, la mémoire (l'espace $s$) utilisée par une machine dicte la largeur structurelle de son tableau de calcul. Le lemme L-02, qui est PROUVÉ intégralement au chapitre 11, établit que le tableau d'une machine utilisant un espace $s$ admet une décomposition en chemin de sacs d'au plus $4s+1$ sommets. La largeur de chemin est donc bornée par $4s+1$, et ce, de manière totalement indépendante du nombre de pas $t$. Ce lemme est borné, précis, et ne prétend pas résoudre les grandes conjectures de la complexité, car la décision par balayage de cette structure coûte tout de même $2^{O(s)}\,\mathrm{poly}(t)$ (PROUVÉ), ce qui rejoint parfaitement le comptage classique des configurations (CONNU). Nous verrons également, par des contrôles pour les bornes 17, 25, 33, 41 (EXPÉRIMENTAL), comment les heuristiques modernes peuvent surestimer cette largeur (observant par exemple un écart de 255 là où la construction donne 41), mesurant ainsi la perte d'une traduction structure $\rightarrow$ heuristique.

**Troisième leçon : le format propositionnel se paie en variables et clauses auxiliaires.**
La traduction de Tseitin (Tseitin 1968) permet de convertir n'importe quel circuit en une formule CNF équisatisfiable avec une croissance linéaire de la taille. C'est un résultat PROUVÉ et fondamental pour les solveurs SAT modernes. Cependant, l'équivalence logique littérale, elle, est perdue : la formule CNF admet des modèles qui ne correspondent pas directement aux modèles du circuit original sans projection. Cette affirmation d'équivalence stricte est donc RÉFUTÉE. Le format propositionnel exige un sacrifice : la précision sémantique contre l'efficacité de la résolution (Papadimitriou 1994 ; Arora et Barak 2009).

### À qui s'adresse ce livre et comment le lire

Ce livre s'adresse à un lecteur cultivé, possédant une base en mathématiques discrètes et en algorithmique, mais qui n'est pas nécessairement un spécialiste de la théorie de la complexité structurelle. L'objectif est de rendre tangibles des concepts souvent noyés sous le formalisme.

Pour y parvenir, chaque chapitre suit un rythme pédagogique immuable en cinq temps :
1. **Intuition** : une métaphore ou une explication conceptuelle pour saisir l'enjeu avant les formules.
2. **Définition** : le cadre formel, posé avec rigueur mais sans lourdeur inutile.
3. **Énoncé** : le théorème, le lemme ou la propriété, accompagné de son statut (PROUVÉ, CONNU, etc.).
4. **Exemple** : une application concrète sur un petit cas, pour vérifier la mécanique de la preuve ou de la traduction.
5. **Exercice** : une mise en pratique pour le lecteur, avec des corrigés détaillés en fin de volume.

Les formules mathématiques sont rédigées en LaTeX, intégrées naturellement au texte pour faciliter la lecture. Les fiches de traduction, quant à elles, sont présentées comme des tableaux de bord synthétiques à la fin de chaque grande étape de traduction.

### Plan détaillé de l'ouvrage

L'ouvrage est structuré en quatre parties et seize chapitres, couvrant environ 220 pages. Le plan suit le flux des traductions, de la machine vers les clauses, puis le retour vers les machines et les réductions, avant de s'ouvrir sur les perspectives du programme RTC.

**Partie I — Le contrat de traduction : modèles, ressources, statuts (Chapitres 1 à 4)**
Cette partie pose les fondations. Le **Chapitre 1** introduit la philosophie des traductions à ressources et le programme RTC. Le **Chapitre 2** formalise les machines de Turing et construit l'objet central du livre : le tableau de calcul. Le **Chapitre 3** présente les circuits booléens, en définissant rigoureusement la taille, la profondeur, la largeur et le partage. Le **Chapitre 4** clôt cette partie avec le monde de SAT, explorant les clauses, la résolution, et les graphes d'incidence qui relient la logique à la structure.

**Partie II — Sens aller, première cible : des machines aux circuits (Chapitres 5 à 8)**
Nous entrons dans le vif des traductions. Le **Chapitre 5** détaille la traduction **T1** : le déroulement brut du tableau de calcul en un circuit booléen, évaluant le coût linéaire en taille. Le **Chapitre 6** aborde la traduction **T2**, consacrée au résultat de Pippenger et Fischer (Pippenger et Fischer 1979), montrant comment atteindre une taille en $O(t \log t)$ grâce au partage et aux réseaux de tri. Le **Chapitre 7** traite de la traduction **T3**, une traduction souvent oubliée mais cruciale : l'uniformité, ou comment un algorithme peut générer le circuit, et ce que cette exigence fait perdre en liberté structurelle. Le **Chapitre 8** dresse le bilan du sens aller vers les circuits, remplissant la fiche de traduction synthétique et analysant les conservations et les pertes.

**Partie III — Sens aller, seconde cible : des circuits et des tableaux aux clauses (Chapitres 9 à 12)**
Cette partie traite du passage au format propositionnel. Le **Chapitre 9** présente la traduction **T4**, l'art de nommer les fils selon la méthode de Tseitin (Tseitin 1968), et prouve la croissance linéaire et l'équisatisfiabilité. Le **Chapitre 10** détaille la traduction **T5**, le théorème de Cook-Levin (Cook 1971 ; Levin 1973), qui encode le tableau de calcul entier directement en CNF, fondant ainsi la NP-complétude. Le **Chapitre 11** est le cœur technique de l'ouvrage : il énonce et prouve intégralement le lemme L-02 sur la largeur du tableau (largeur de chemin $\le 4s+1$), et présente les contrôles expérimentaux pour $s = 4, 6, 8, 10$. Le **Chapitre 12** synthétise ces approches dans la traduction **T6**, évaluant le prix exact du format propositionnel en termes de variables et de clauses.

**Partie IV — Sens inverse, réductions et transfert vers RTC (Chapitres 13 à 16)**
Le voyage s'inverse et s'élargit. Le **Chapitre 13** explore la traduction **T7**, le sens inverse : comment évaluer un circuit ou résoudre une formule SAT à l'aide d'une machine de Turing, et quel est le coût en temps et en mémoire de cette évaluation. Le **Chapitre 14** aborde la traduction **T8**, qui change d'échelle : les réductions entre problèmes plutôt qu'entre machines, montrant comment les ressources se transmettent d'un problème à un autre (Savitch 1970). Le **Chapitre 15** examine ce qui résiste à la traduction : les bornes inférieures, les limites des heuristiques de largeur, et les statuts mal tenus dans la littérature, séparant le CONNU du CONJECTURE. Enfin, le **Chapitre 16**, « Transfert vers le programme RTC », conclut l'ouvrage en dressant le bilan de ce que ce tome apporte à l'étude globale des traductions à ressources, en listant les questions ouvertes et en traçant la voie pour les tomes futurs.

En refermant ce livre, le lecteur ne verra plus une machine de Turing, un circuit et une formule SAT comme trois visages interchangeables d'une même réalité. Il y verra trois états de la matière computationnelle, séparés par des frontières franchissables, mais dont le droit de passage se paie toujours, invariablement, en ressources. C'est à la lecture de ce ticket de caisse que commence la véritable compréhension du calcul.

## Chapitre 1 — Traduire un calcul, c'est payer une ressource

### 1.1 Intuition : le changement de devise computationnelle

Imaginez que vous voyagez d'un pays à l'autre. À la frontière, vous devez échanger votre monnaie contre celle du pays de destination. Le bureau de change vous propose un taux, mais il prend aussi une commission. Vous ne repartirez jamais avec exactement la même valeur réelle ; une partie de votre richesse s'est évaporée dans le mécanisme de l'échange. En informatique théorique, nous avons longtemps fait comme si les frontières entre les modèles de calcul n'existaient pas, ou du moins, comme si les bureaux de change étaient parfaitement gratuits.

Prenons un algorithme simple, comme la multiplication de deux entiers. Nous pouvons l'écrire pour une machine de Turing (Turing 1936), qui va déplacer sa tête de lecture sur un ruban, étape par étape. Nous pouvons aussi le dessiner sous la forme d'un circuit booléen (Jukna 2012), où des portes logiques reçoivent les bits des deux entiers et produisent le résultat en une seule vague parallèle. Enfin, nous pouvons le formuler comme un problème de satisfiabilité (Cook 1971), où l'on cherche une affectation de variables qui rend vraies une série de clauses logiques. La théorie classique nous dit : « Ces trois descriptions sont équivalentes. » C'est vrai, au sens où elles calculent la même fonction. Mais cette équivalence est une illusion d'optique. Elle masque le coût de la traduction.

Passer de la machine au circuit, c'est convertir du temps en espace. La machine prend $t$ étapes ; le circuit, lui, doit être construit avec un nombre de portes qui dépend de $t$. Passer du circuit à la formule SAT, c'est convertir de la structure en variables auxiliaires. Chaque traduction est un changement de devise computationnelle. Et comme dans toute transaction, il y a un taux de change, une commission, et parfois, une perte sèche d'information. Ce chapitre pose les bases de cette comptabilité. Nous allons définir ce qu'est une traduction, quelles sont les ressources qui servent de monnaie d'échange, et comment nous allons noter rigoureusement ce qui est conservé et ce qui est perdu.

### 1.2 Définition : modèles, traductions et ressources

Pour formaliser cette intuition, nous devons d'abord définir notre vocabulaire. Un **modèle de calcul** est un cadre formel qui spécifie comment une entrée est transformée en une sortie. Dans ce tome, nos trois modèles principaux sont la machine de Turing (séquentielle, dynamique), le circuit booléen (parallèle, spatial) et la formule propositionnelle, en particulier sous forme normale conjonctive ou CNF (déclarative, contraignante).

Une **traduction** $T$ est une fonction effective qui, à partir de la description d'un calcul dans un modèle source $M_1$, produit la description d'un calcul dans un modèle cible $M_2$, de telle sorte que le comportement observable (la fonction calculée ou la réponse au problème de décision) soit préservé d'une manière que nous préciserons à chaque fois.

Mais comment mesurer le coût de $T$ ? C'est ici qu'interviennent les sept ressources du programme RTC (« Les Traductions du Calcul »). Chaque traduction sera évaluée selon l'impact qu'elle a sur ces sept dimensions :

1. **La taille** : le nombre d'éléments de base du modèle. Pour une machine, c'est le nombre d'états et de symboles ; pour un circuit, le nombre de portes ; pour une CNF, le nombre de clauses et de littéraux.
2. **Le temps** : le nombre d'étapes d'exécution. Pour une machine, c'est le nombre de transitions ; pour un circuit, c'est le temps d'évaluation (souvent lié à la profondeur) ; pour SAT, c'est le temps de résolution, bien que cette ressource soit souvent externalisée au solveur.
3. **La mémoire** (ou espace) : la quantité de support nécessaire à un instant donné. C'est la portion de ruban utilisée par la machine, ou le nombre de fils actifs simultanément dans un circuit.
4. **La profondeur** : la longueur du plus long chemin de dépendance causale. C'est le temps de propagation du signal dans un circuit, ou le nombre de pas de temps dans le tableau d'une machine.
5. **La largeur** : une mesure de la complexité topologique du graphe sous-jacent, comme la largeur de chemin (*pathwidth*) ou la largeur d'arbre (*treewidth*). Elle dicte la capacité à découper le calcul en morceaux indépendants.
6. **La précision** : la nature exacte de la préservation sémantique. La traduction produit-elle une fonction strictement identique (équivalence), une formule équisatisfiable (équisatisfiabilité), ou une structure dont il faut extraire la réponse par projection ?
7. **Le partage** : la capacité du modèle cible à réutiliser un sous-calcul. Un circuit permet le partage (une porte peut alimenter plusieurs autres portes, c'est le *fan-out*), tandis qu'une formule arborescente ne le permet pas.

Ces sept ressources forment le vecteur de coût d'une traduction. Lorsque nous dirons que le temps se paie en taille, nous voudrons dire que la composante de taille du modèle cible croît en fonction de la composante de temps du modèle source.

### 1.3 Énoncé : le principe de conservation et de perte

Avant d'entrer dans les preuves complexes des chapitres suivants, il nous faut un énoncé fondateur, une boussole pour le voyage. Ce principe n'est pas un théorème unique avec une preuve de dix lignes, mais plutôt une méta-propriété qui émerge de l'ensemble de la théorie de la complexité (Papadimitriou 1994 ; Arora et Barak 2009).

**Énoncé 1.1 (Principe d'échange de ressources).**
*Soit $T$ une traduction effective d'un modèle de calcul $M_1$ vers un modèle de calcul $M_2$. Si $M_2$ restreint structurellement une ressource $r_1$ par rapport à $M_1$ (par exemple, l'absence de boucle temporelle dans un circuit, ou l'absence de partage dans une formule), alors la traduction $T$ doit compenser cette restriction par une inflation d'au moins une autre ressource $r_2$ (taille, profondeur, variables auxiliaires). De plus, la précision sémantique de la traduction (équivalence stricte contre équisatisfiabilité avec projection) détermine l'ampleur de cette inflation.*
**Statut : CONNU.**

L'idée de la preuve de ce principe repose sur l'argument de la diagonalisation et le comptage des configurations. Si un modèle cible pouvait simuler un modèle source sans payer aucune ressource supplémentaire tout en conservant toutes les propriétés structurelles, on pourrait comprimer l'information computationnelle au-delà des bornes de l'entropie, ou résoudre des problèmes indécidables. Par exemple, la machine de Turing peut réutiliser la même case du ruban à l'étape $t$ et à l'étape $t+1$ (partage temporel). Le circuit, étant un graphe acyclique, ne peut pas réutiliser une porte pour deux pas de temps différents ; il doit dupliquer la porte (inflation de la taille). C'est ce que nous explorerons en détail avec le déroulé du tableau de calcul.

Ce principe nous force à être honnêtes. Il n'y a pas de magie. Si un solveur SAT résout rapidement un problème encodé en CNF, ce n'est pas parce que la CNF a rendu le problème intrinsèquement plus facile, mais parce que la traduction a payé le prix de la structure en variables auxiliaires (Tseitin 1968), et que le solveur exploite cette nouvelle structure.

### 1.4 Exemple : l'addition, de la machine au circuit

Pour rendre ces concepts tangibles, prenons l'exemple le plus simple qui soit : l'addition de deux entiers de $n$ bits.

**Dans le modèle machine de Turing :**
Nous avons un ruban contenant les deux nombres, séparés par un symbole spécial. La machine parcourt les bits de droite à gauche, maintient une retenue dans son état interne (qui ne coûte que $O(1)$ en mémoire, soit 2 états pour la retenue), et écrit le résultat.
- Temps : $O(n)$ étapes.
- Mémoire : $O(n)$ cases de ruban.
- Partage : la tête de lecture et l'état interne sont réutilisés à chaque étape.

**Dans le modèle circuit booléen :**
Nous construisons un additionneur à propagation de retenue (*ripple-carry adder*). Pour chaque bit $i$ de $0$ à $n-1$, nous avons un bloc de portes logiques qui prend les bits $a_i$, $b_i$ et la retenue $c_i$, et produit la somme $s_i$ et la retenue $c_{i+1}$.
- Taille : $O(n)$ portes.
- Profondeur : $O(n)$ portes (la retenue doit se propager de $0$ à $n-1$).
- Partage : le circuit ne réutilise pas les portes d'un bit pour un autre ; il les duplique.

**La traduction (Machine $\rightarrow$ Circuit) :**
Si nous voulons traduire le comportement de la machine en un circuit, nous pourrions être tentés de dire que la taille du circuit est $O(n)$, tout comme le temps de la machine. Mais attention à la précision ! Le circuit de taille $O(n)$ ne calcule que pour une entrée de taille fixe $n$. La machine, elle, possède un nombre d'états fixe et peut traiter n'importe quelle entrée, quelle que soit sa longueur $n$.
Pour capturer le calcul de la machine pour *toute* entrée de taille jusqu'à $N$, le circuit doit être déroulé. Le tableau de calcul de la machine pour $t$ étapes et un espace $s$ aura une taille de $t \times s$. Si on le traduit en circuit, la taille du circuit sera $O(t \times s)$. Ici, le temps $t$ de la machine s'est transformé en taille (nombre de portes) dans le circuit. Le partage temporel de l'état de la machine a été payé par une duplication spatiale des portes à chaque pas de temps.

Cet exemple simple illustre parfaitement l'Énoncé 1.1. La restriction du circuit (pas de réutilisation temporelle, graphe acyclique) nous oblige à payer en taille (inflation spatiale) pour conserver la précision du calcul sur $t$ étapes.

### 1.5 La fiche de traduction : notre tableau de bord

Pour ne jamais perdre le fil de ce que nous payons et de ce que nous gagnons, chaque traduction majeure de ce livre (de T1 à T8) se conclura par une **fiche de traduction**. Cette fiche est un contrat de lecture. Elle vous garantit que je ne laisserai aucun coût dans l'ombre.

Voici le format type de la fiche que nous remplirons ensemble :

| Ressource / Dimension | Description et Coût | Statut |
| :--- | :--- | :--- |
| **Sens** | Source $\rightarrow$ Cible, effectivité de la traduction | - |
| **Taille** | Coût en éléments du modèle cible | PROUVÉ / CONNU |
| **Temps** | Impact sur le temps d'exécution ou d'évaluation | PROUVÉ / CONNU |
| **Mémoire** | Impact sur l'espace ou les variables actives | PROUVÉ / CONNU |
| **Profondeur** | Longueur du chemin critique | PROUVÉ / CONNU |
| **Largeur** | Complexité topologique (pathwidth/treewidth) | PROUVÉ / EXPÉRIMENTAL |
| **Précision** | Équivalence, équisatisfiabilité, projection | PROUVÉ / RÉFUTÉ |
| **Partage** | Capacité de réutilisation des sous-calculs | PROUVÉ / CONNU |
| **Conservations** | Ce qui est préservé intact | - |
| **Pertes** | Ce qui est détruit ou oublié | - |

Cette fiche n'est pas un simple résumé ; c'est l'application stricte du programme RTC. Lorsque nous évaluerons la traduction de Tseitin (T4) au chapitre 9, la case « Précision » portera la mention « Équisatisfiabilité (PROUVÉ) » et la case « Pertes » mentionnera « Équivalence logique littérale (RÉFUTÉ) ». Nous ne tricherons pas avec les mots. Une formule de Tseitin n'est pas logiquement équivalente au circuit d'origine ; elle est équisatisfiable sous projection. Cette nuance est la différence entre une ingénierie robuste et une approximation dangereuse.

### 1.6 Exercices

Pour clore ce chapitre fondateur, je vous propose deux exercices. Ils ne demandent pas de mathématiques avancées, mais exigent que vous commenciez à penser en termes de ressources et de traductions. Les corrigés détaillés se trouvent à la fin du volume, mais je vous encourage vivement à les chercher par vous-même.

**Exercice 1.1 : Le coût de l'oubli.**
Considérez une machine de Turing qui, sur une entrée de taille $n$, se déplace vers la droite jusqu'à trouver un marqueur de fin, puis revient à sa position initiale. Le temps de calcul est $t = 2n$.
1. Si l'on traduit cette machine en un circuit booléen qui prend $n$ bits en entrée et produit $n$ bits en sortie (la sortie étant identique à l'entrée, puisque la machine ne modifie rien), quelle est la taille minimale du circuit ?
2. Où est passée la ressource « temps » de la machine ($2n$ étapes) dans le modèle circuit ? Qu'a-t-on perdu dans la traduction ?

**Exercice 1.2 : Précision et projection.**
Soit un circuit $C$ avec deux entrées $x_1, x_2$ et une sortie $y = x_1 \lor x_2$.
On traduit ce circuit en une formule CNF $F$ en introduisant une variable auxiliaire $v$ pour la sortie, et en ajoutant des clauses pour forcer $v \leftrightarrow (x_1 \lor x_2)$.
1. Écrivez les clauses de $F$.
2. La formule $F$ est-elle logiquement équivalente à $y = x_1 \lor x_2$ ? (Autrement dit, ont-elles exactement les mêmes modèles sur les mêmes variables ?)
3. Expliquez pourquoi la précision de cette traduction est l'équisatisfiabilité par projection et non l'équivalence stricte. Quel statut du registre RTC s'applique à l'affirmation « $F$ et $C$ sont logiquement équivalents » ?

***

En refermant ce premier chapitre, vous avez en main les outils conceptuels qui nous accompagneront jusqu'à la dernière page. Nous avons défini les modèles, nous avons identifié les sept ressources du programme RTC, et nous avons compris que toute traduction est un échange où rien ne se crée, rien ne se perd sans compensation. Dans le chapitre suivant, nous allons plonger dans les entrailles de notre premier modèle : la machine de Turing, et nous allons apprendre à figer son mouvement dans l'objet qui rendra toutes nos traductions possibles : le tableau de calcul.