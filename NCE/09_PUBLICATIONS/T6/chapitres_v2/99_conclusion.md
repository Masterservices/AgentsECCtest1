## Conclusion — Ce que traduire veut dire

### Le fil rouge : toute flèche a un prix

Au terme de ces seize chapitres, une conviction s'est installée, que j'ai voulu démontrer non par proclamation mais par construction : une traduction entre modèles de calcul n'est jamais un acte gratuit. Chaque flèche que nous avons tracée — de la machine de Turing au tableau, du tableau au circuit, du circuit à la CNF, puis en sens inverse — s'accompagne d'une facture précise, libellée en taille, en profondeur, en largeur, en variables auxiliaires, en perte d'équivalence ou en abandon de l'uniformité. Le programme RTC, *Les Traductions du Calcul*, n'est rien d'autre que la discipline de tenir cette comptabilité sans complaisance.

Ce tome a suivi la chaîne $M \xrightarrow{T_1} C \xrightarrow{T_4} \varphi_{\mathrm{SAT}}$, puis le chemin de retour $C \xrightarrow{T_7} M$ et la transversale des réductions $T_8$. Pour chaque flèche, une fiche de traduction a été remplie : sens, coûts, conservations, pertes, statut. Cette structure n'est pas un artifice éditorial ; elle est la thèse elle-même mise en formulaire. Tant qu'une case reste vide, la traduction n'est pas comprise.

### Ce que nous avons prouvé

Trois résultats portent le statut PROUVÉ dans ce volume, et je les rappelle ici comme les piliers de l'édifice.

**Le déroulé du tableau en circuit (T1, chapitre 5).** Étant donné une machine de Turing $M$ qui accepte en temps $t$ et espace $s$, le tableau de calcul $t \times s$ se traduit en un circuit booléen de taille $O(t \cdot s)$ et de profondeur $O(t)$, dont la sortie est vraie si et seulement si $M$ accepte l'entrée codée. La preuve est élémentaire — chaque cellule du tableau devient une porte locale — mais elle fixe le point de départ de toute la chaîne : le temps se paie en profondeur, l'espace se paie en largeur.

**Le lemme L-02 (chapitre 11).** C'est le résultat propre à ce tome. Le tableau d'une machine utilisant un espace $s$ admet une décomposition en chemin (*path decomposition*) dont les sacs contiennent quatre lignes consécutives plus un sommet de contrôle, soit au plus $4s + 1$ sommets. La largeur de chemin est donc bornée par $4s + 1$, indépendamment du nombre de pas $t$. La preuve, donnée intégralement au chapitre 11, procède par construction explicite des sacs, vérification de la couverture des arêtes, et comptage. Les contrôles expérimentaux pour $s \in \{4, 6, 8, 10\}$, soit les bornes 17, 25, 33, 41, confirment la construction (statut EXPÉRIMENTAL pour les mesures, PROUVÉ pour la lecture logique). L'écart observé avec les heuristiques de largeur — 255 là où la construction donne 41 — mesure la perte d'une traduction structure → heuristique, non un défaut du lemme.

**La décision par balayage (chapitre 11, corollaire).** Une fois la décomposition en chemin de largeur $w = 4s + 1$ établie, la décision par programmation dynamique sur les sacs coûte $2^{O(s)} \cdot \mathrm{poly}(t)$. C'est un énoncé PROUVÉ qui rejoint le comptage classique des configurations (CONNU, Papadimitriou 1994) sans le remplacer : il offre une lecture structurelle, géométrique, là où le comptage offre une lecture arithmétique. Aucune conséquence d'effondrement de classes n'est annoncée, et c'est voulu.

### Ce que nous avons transmis

Plusieurs théorèmes de la littérature ont été présentés avec l'idée de leur preuve, sans prétendre à une démonstration complète. Leur statut est CONNU, et je les ai toujours attribués explicitement.

La simulation en $O(t \log t)$ de Pippenger et Fischer (1979) montre que la première traduction $T_1$ n'est pas optimale en taille : en réorganisant le tableau par blocs, on comprime la profondeur au prix d'une factorisation logarithmique de la taille. Nous avons donné l'intuition de la construction par niveaux, sans reproduire la preuve intégrale.

La transformation de Tseitin (1968), cœur du chapitre 9, établit que tout circuit de taille $m$ se traduit en une CNF équisatisfiable de $O(m)$ clauses, au prix de $O(m)$ variables auxiliaires. Le statut est CONNU ; la preuve est courte et je l'ai esquissée : chaque porte devient une petite clause, et la variable d'extension nomme le fil de sortie. Ce qui est conservé : l'équisatisfiabilité, la taille linéaire. Ce qui est perdu : l'équivalence logique littérale (RÉFUTÉ au chapitre 9 — un contre-exemple explicite sur la porte XOR montre que les modèles ne coïncident plus une fois les variables auxiliaires oubliées).

Le théorème de Cook (1971) et Levin (1973), présenté au chapitre 10, est la flèche $T_5$ : le tableau entier devient une CNF en $O(t^2)$ variables et clauses. L'idée de la preuve a été donnée ; la construction complète des clauses de transition, d'acceptation et d'unicité est laissée en exercice dirigé.

Enfin, la relation entre espace déterministe et non-déterministe de Savitch (1970) apparaît en filigrane au chapitre 15 : la largeur du tableau, lorsqu'on autorise le non-déterminisme, se comporte comme $s^2$ plutôt que $s$, et cette quadrature est le prix structurel du passage de NTM à DTM.

### Ce qui est perdu et ce qui résiste

Le sous-titre du livre promet de dire *ce qu'elles conservent, ce qu'elles perdent*. Le bilan est le suivant.

**Conservé :** la décidabilité de l'acceptation ; l'équisatisfiabilité (Tseitin) ; la borne supérieure $2^{O(s)}$ sur la complexité en espace (L-02 + balayage) ; la structure locale du tableau (chaque cellule dépend d'un voisinage borné).

**Perdu :** l'équivalence logique littérale dès qu'on introduit des variables d'extension (RÉFUTÉ, chapitre 9) ; l'uniformité de la famille de circuits (chapitre 7 — la traduction $T_1$ produit une famille non uniforme ; reconstruire la machine à partir du circuit exige une description de la famille, ce que la flèche $T_7$ ne fait qu'en partie) ; la précision du partage (le fan-out d'un circuit n'a pas d'analogue direct en CNF sans duplication de clauses) ; la profondeur exacte (le passage circuit → CNF aplati la structure en niveaux).

**Résistant :** les bornes inférieures. Ce tome n'établit aucune borne inférieure non triviale pour la taille des circuits. La question $\mathrm{P}$ vs $\mathrm{NP}$ reste OUVERTE, et je n'ai pas cherché à la contourner. Les heuristiques de largeur, malgré leur utilité pratique, restent des bornes supérieures EXPÉRIMENTALES ; l'écart 255 contre 41 n'est ni une réfutation ni une confirmation, c'est une mesure de la perte de fidélité d'une traduction structure → algorithme glouton.

### Les huit flèches, en un tableau

Pour clore le registre, je résume les huit traductions en une phrase chacune.

- **T1** (machine → tableau → circuit) : taille $O(ts)$, profondeur $O(t)$, largeur $O(s)$. PROUVÉ.
- **T2** (Pippenger–Fischer) : taille $O(t \log t)$, profondeur $O(t)$. CONNU.
- **T3** (uniformité) : la traduction oublie la machine ; la famille de circuits ne porte pas, en général, de programme de reconstruction. PROUVÉ (obstruction).
- **T4** (Tseitin, circuit → CNF) : $O(m)$ clauses, $O(m)$ variables auxiliaires, équisatisfiabilité. CONNU.
- **T5** (Cook–Levin, tableau → CNF) : $O(t^2)$ variables, $O(t^2)$ clauses. CONNU.
- **T6** (prix du format) : le passage à la CNF impose des variables d'extension et détruit l'équivalence littérale. PROUVÉ / RÉFUTÉ.
- **T7** (circuit → machine, sens inverse) : évaluation séquentielle en temps $O(m)$, espace $O(\log m)$ pour stocker les valeurs. PROUVÉ.
- **T8** (réductions) : traduire un problème plutôt qu'une machine ; la réduction many-one compose les flèches. CONNU.

### Ouvertures vers le programme RTC

Le chapitre 16, *Transfert vers le programme RTC*, esquisse les prolongements. Ce tome n'est qu'une chaîne linéaire : $M \to C \to \mathrm{SAT} \to M$. Le programme RTC envisage un graphe de modèles plus riche : machines à oracle, circuits non uniformes de profondeur bornée ($\mathrm{AC}^0$, $\mathrm{NC}^1$), systèmes de preuve propositionnelle, automates à pile, circuits arithmétiques. Chaque arête de ce graphe appellera sa propre fiche de traduction.

Trois questions, au moins, restent ouvertes à l'issue de ce volume.

**Q1.** La borne $4s + 1$ du lemme L-02 est-elle serrée ? Pour $s = 4$, la construction donne 17 ; existe-t-il un tableau d'espace 4 dont toute décomposition en chemin exige un sac de 17 sommets, ou peut-on descendre ? Statut : OUVERT.

**Q2.** Peut-on raffiner la traduction $T_4$ pour conserver davantage de structure — par exemple, préserver la largeur de chemin du circuit dans la structure d'incidence de la CNF ? Les travaux de Biere, Heule, van Maaren et Walsh (2009) suggèrent que la structure du graphe d'incidence influence les solveurs, mais la traduction exacte largeur → treewidth de la CNF reste, à ma connaissance, OUVERTE.

**Q3.** Le partage (fan-out, variables d'extension) est une ressource que ce tome a identifiée sans la quantifier finement. Quelle est la perte minimale de taille lorsqu'on interdit le fan-out supérieur à 2 dans un circuit avant traduction en CNF ? Jukna (2012) pose des questions voisines sur la complexité des fonctions booléennes ; la réponse précise pour notre chaîne reste OUVERTE.

Ces trois questions, et d'autres, constituent le cahier de charges du tome suivant du programme RTC.

### Sur la méthode

Un mot sur la manière. J'ai voulu que chaque affirmation porte un statut. Ce n'est pas une coquetterie : c'est une hygiène. Trop de textes de complexité mélangent, dans une même phrase, un lemme démontré, une intuition heuristique et une conjecture vieille de cinquante ans. Le lecteur perd alors le fil de ce qu'il peut utiliser comme outil et de ce qu'il doit encore prouver. Le registre PROUVÉ / CONNU / EXPÉRIMENTAL / CONJECTURE / RÉFUTÉ / OUVERT est ma tentative modeste pour rendre ce fil visible. Il est imparfait — certains énoncés sont à la lisière de deux statuts — mais il a l'avantage de forcer l'auteur à se demander, à chaque ligne : *qu'est-ce que je sais, et comment le sais-je ?*

De même, la fiche de traduction à huit cases n'est pas un formulaire administratif. C'est un rappel que traduire, c'est choisir : choisir ce qu'on garde, accepter ce qu'on lâche, et le dire. Un ingénieur qui encode un problème en SAT pour le soumettre à un solveur fait exactement ce geste, souvent sans le formaliser. J'espère que ce livre lui donne les mots.

### Au lecteur

Ce livre a été écrit pour un lecteur cultivé, curieux, non nécessairement spécialiste. Si vous êtes arrivé jusqu'ici, c'est que vous avez accepté de suivre une chaîne d'abstractions — machine, tableau, circuit, clause — sans perdre de vue la question concrète : *combien ça coûte ?* Cette question, je crois, est plus honnête que « est-ce possible ? ». La calculabilité, depuis Turing (1936), est acquise pour l'essentiel des modèles raisonnables. La complexité, elle, est une comptabilité fine, et c'est dans cette finesse que vivent les difficultés réelles.

Je n'ai pas cherché à vous éblouir. Aucun résultat de ce tome ne prétend au titre de découverte. Le lemme L-02 est un énoncé borné, démontré, modeste : il dit que la largeur d'un tableau d'espace $s$ est en $4s + 1$. C'est peu, et c'est suffisant pour ouvrir une lecture géométrique de l'espace. Les contrôles expérimentaux sont des vérifications, pas des preuves. Les théorèmes de Pippenger et Fischer, de Tseitin, de Cook et Levin, de Savitch, sont cités, expliqués, transmis — non revendiqués.

Si ce livre vous a donné envie de prendre un crayon et de vérifier une preuve, de lancer un solveur SAT sur un petit tableau pour voir les clauses, de dessiner la décomposition en chemin d'un tableau $4 \times 6$ à la main, alors il a rempli son office. La complexité computationnelle n'est pas une galerie de théorèmes à contempler ; c'est une discipline de la main et du brouillon, où l'on compte les portes, les clauses, les sommets d'un sac, un par un.

### Dernier mot

Traduire, c'est payer. Mais c'est aussi *choisir* ce qu'on veut emporter de l'autre côté. La machine de Turing emporte sa décidabilité dans le circuit ; le circuit emporte son équisatisfiabilité dans la CNF ; la CNF, résolue, emporte un certificat que la machine peut vérifier. À chaque étape, quelque chose reste sur le quai : l'uniformité, l'équivalence littérale, la profondeur, le partage. Ce tome a dressé l'inventaire de ces bagages perdus.

Le programme RTC continuera d'étendre cet inventaire à d'autres modèles, d'autres flèches, d'autres ressources. Mais le principe restera celui que j'ai voulu inscrire dans chaque page : tenir la fiche, dire le statut, compter le coût. Rien de plus. Rien de moins.

Je vous remercie d'avoir lu jusqu'au bout de cette chaîne. Elle est, à sa manière, une preuve que la patience — $O(t)$ pas, un à un — finit par accepter.

*Oussama Ghorbel*
*Novembre 2026*

### Post-scriptum — deux précisions de comptabilité

Tenir le registre jusqu'au bout, c'est aussi le retourner contre sa propre prose. Deux formulations de cette conclusion méritent d'être resserrées, et je préfère les corriger ici plutôt que de laisser le lecteur emporter une fiche mal remplie.

Première précision, sur T2. La simulation de Pippenger et Fischer (1979) gagne sur la **taille** : $O(t \log t)$ portes au lieu du déroulé brut. Elle ne promet aucune profondeur plus petite. Rien dans l'énoncé ne garantit que les chemins entrée–sortie raccourcissent ; la case « profondeur » de la fiche T2 doit donc porter la mention *non améliorée par cet argument*, et non *compressée* (CONNU pour la borne de taille ; la lecture « la profondeur diminue » n'est pas une conséquence du théorème, et je la retire). Le fil conducteur du livre reste exact tel qu'il a été formulé au chapitre 1 : le temps se paie en taille **et** en profondeur, et une économie sur l'une des deux ressources n'est pas une économie sur l'autre.

Seconde précision, sur T7. Évaluer un circuit de $m$ portes en séquentiel coûte un temps linéaire à facteurs de gestion près, mais l'espace $O(\log m)$ que j'ai mentionné ne suffit que pour les index et les compteurs, pas pour les **valeurs**. Si l'on mémorise tous les fils, il faut $m$ bits (PROUVÉ, comptage immédiat : un bit par fil, et la famille exhibée ci-dessous montre que l'oubli se paie). La fiche T7 se lit donc ainsi : temps $O(m)$ à facteurs polylogarithmiques près sur une machine de Turing, espace $O(m)$ bits en évaluation mémoïsée ; ou bien espace $O(d \log m)$ bits en évaluation par profondeur d'abord sans mémoire, où $d$ est la profondeur, au prix d'un temps qui peut exploser. C'est exactement le genre d'échange que le programme RTC exige d'écrire noir sur blanc plutôt que de le sous-entendre.

### Une dernière fiche : le partage se paie deux fois

Puisque je viens d'ouvrir cette case, autant la remplir complètement. Rien ici n'est une découverte : c'est le folklore de l'évaluation, que j'écris parce qu'une fiche exige des cases pleines et une preuve écrite.

**Énoncé (PROUVÉ).** Soit la famille de circuits $C_d$ définie par $g_0 = x$ et $g_i = g_{i-1} \wedge g_{i-1}$ pour $1 \le i \le d$, de sortie $g_d$. Alors $C_d$ a $d+1$ nœuds, profondeur $d$, fan-out $2$ sur chaque $g_i$ avec $i < d$, et calcule la fonction identité $x \mapsto x$. Deux stratégies d'évaluation donnent :

1. *Mémoïsée* : chaque nœud est évalué une fois, donc $\Theta(d)$ opérations élémentaires et $d+1$ bits de valeurs stockées.
2. *Récursive sans mémoire* : le temps vérifie $T(d) = 2T(d-1) + O(1)$, donc $T(d) = \Theta(2^d)$, tandis que la pile d'appels contient au plus $d+1$ cadres de $O(\log d)$ bits, soit $O(d \log d)$ bits.

**Preuve.** Le comptage des nœuds et de la profondeur est immédiat par construction. Pour (1), il suffit d'ordonner les nœuds par indice croissant : chaque $g_i$ n'a qu'un seul prédécesseur, déjà évalué, et l'on écrit un bit par nœud ; l'ordre est valide car le graphe est acyclique, ce qui est vérifié puisque tout arc va d'un indice vers l'indice suivant. Pour (2), l'appel sur $g_i$ déclenche deux appels indépendants sur $g_{i-1}$, aucune valeur n'étant conservée entre eux ; d'où la récurrence, et $T(d) + c = 2(T(d-1) + c)$ pour une constante $c$ convenable, donc $T(d) = \Theta(2^d)$. La pile ne contient jamais qu'une branche de la racine vers une feuille, soit $d+1$ cadres, chacun portant un indice de nœud sur $O(\log d)$ bits. $\square$

**Lecture RTC.** Le même objet, le même calcul exact, deux traductions vers le modèle séquentiel : l'une échange de la mémoire contre du temps, l'autre du temps contre de la mémoire. La ressource qui les sépare est le **partage**. Si le fan-out est partout au plus $1$ — si le circuit est une formule, un arbre — les deux stratégies coïncident : chaque nœud a un unique chemin depuis la sortie, donc n'est jamais réévalué, et l'on obtient temps $\Theta(\text{taille})$ et espace $O(\text{profondeur} \cdot \log \text{taille})$ (PROUVÉ, même argument).

Le même $2^d$ réapparaît ailleurs dans le tome, et c'est ce qui fait l'unité de la chaîne : déplier $C_d$ en formule coûte $2^d$ feuilles, alors que la traduction de Tseitin (1968) produit $O(d)$ clauses en nommant chaque fil par une variable d'extension (CONNU). Nommer, c'est partager ; partager, c'est refuser de recopier. Les variables auxiliaires du chapitre 9 et le fan-out du chapitre 3 sont la même ressource vue depuis deux modèles.

### Dernier exercice, et son corrigé

**Exercice.** (a) Pour $s = 8$, donner la borne du lemme L-02 et expliquer en une phrase pourquoi le nombre de pas $t$ n'y apparaît pas. (b) Un logiciel de décomposition rend la valeur $255$ sur une instance où la construction donne $41$. Cet écart réfute-t-il L-02 ? Que mesure-t-il, et sous quel statut ? (c) Reprendre $C_d$ et donner le nombre de clauses obtenues par Tseitin, puis la taille de la formule dépliée.

**Corrigé.** (a) $4 \cdot 8 + 1 = 33$. Les sacs contiennent quatre lignes consécutives du tableau plus un sommet de contrôle ; le nombre de pas ne fait qu'allonger le chemin, il ne grossit aucun sac (PROUVÉ, chapitre 11). (b) Non. Une heuristique qui rend $255$ exhibe une décomposition de largeur $255$, donc une borne supérieure *plus faible*, parfaitement compatible avec $\text{largeur} \le 41$ : l'inégalité $41 \le 255$ va dans le bon sens. La mesure de l'écart est EXPÉRIMENTALE ; sa lecture logique — une borne supérieure ne réfute pas une borne supérieure meilleure — est PROUVÉE. (c) Une variable d'extension par porte et un nombre constant de clauses par porte, soit $O(d)$ clauses (CONNU, Tseitin 1968) ; la formule dépliée a $2^d$ occurrences de $x$, par la même récurrence que ci-dessus (PROUVÉ).

### Envoi

Je referme ce tome sans annonce. Aucune classe ne s'effondre, aucune borne inférieure nouvelle n'apparaît, et la question de la netteté de $4s+1$ reste OUVERTE, comme les deux autres questions du chapitre 16. Le balayage en $2^{O(s)}\,\mathrm{poly}(t)$ rejoint le comptage des configurations (CONNU, Papadimitriou 1994 ; Arora et Barak 2009) ; il en propose une lecture géométrique, non un remplacement. Ce que ce volume apporte est plus modeste et, je crois, plus durable : une manière de lire les traductions, une fiche à huit cases, six statuts, et l'habitude de demander *quelle ressource a payé* avant de demander *si c'est possible*.

Au lecteur qui a suivi la chaîne jusqu'ici, je laisse trois gestes simples. Compter les sommets d'un sac à la main, pour $s = 4$, et vérifier $17$. Écrire les clauses de Tseitin pour une seule porte XOR, et constater de ses yeux que l'équivalence littérale y reste sur le quai. Puis choisir un circuit, l'évaluer deux fois — avec mémoire, sans mémoire — et regarder le temps et l'espace changer de main. Ces trois gestes contiennent tout le livre ; le reste n'est que mise en forme.

Les traductions ne sont pas des ponts gratuits jetés entre des îles toutes équivalentes. Ce sont des passages payants, avec un tarif affiché, des bagages autorisés et des bagages abandonnés. Savoir lire le tarif, c'est déjà calculer autrement.

*Oussama Ghorbel*