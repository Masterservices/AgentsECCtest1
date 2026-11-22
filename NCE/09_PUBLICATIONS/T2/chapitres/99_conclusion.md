## Conclusion : Le grand livre de la comptabilité de l'exécution

### Ce que nous avons parcouru : l'invariant et le coût

Au terme de ce voyage à travers les états, les rubans et les configurations, il est temps de refermer le grand livre de la comptabilité de l'exécution. Lorsque j'ai entrepris la rédaction de cet ouvrage, mon objectif n'était pas de proposer une énième introduction à la calculabilité, ni de répéter ce qui a été magistralement établi par Turing 1936 concernant les nombres calculables et le problème de la décision. Ma thèse, qui a servi de fil conducteur à chacun des seize chapitres, est d'une autre nature : une machine de Turing n'est pas seulement un critère absolu de calculabilité. C'est avant tout un système de comptabilité de l'exécution.

Tout au long de ces pages, nous avons observé que toutes les variantes de ce modèle — qu'il s'agisse de multiplier les rubans, d'élargir l'alphabet, d'introduire le non-déterminisme, de restreindre l'espace à une constante, ou de traduire le calcul en circuits booléens — calculent fondamentalement les mêmes fonctions. L'invariant sémantique, c'est-à-dire la fonction mathématique ou le langage formel reconnu, est farouchement conservé. Cependant, et c'est là le cœur battant de notre démarche, aucune traduction n'est gratuite. Chaque fois que nous modifions la syntaxe de la machine pour la plier à une nouvelle contrainte physique ou théorique, les ressources sont déplacées. Le temps, l'espace, la taille de la description, la profondeur, la largeur, la précision et le partage deviennent les monnaies d'échange de cette économie computationnelle.

Nous avons commencé par poser les fondations. Dans la première partie, nous avons défini la machine non pas comme une boîte noire, mais comme une syntaxe stricte où la configuration $C$ évolue vers $C'$ par des règles de transition locales. Nous avons vu que programmer une machine, c'est tenir un registre rigoureux de ces déplacements de têtes de lecture. Ensuite, la deuxième partie nous a confrontés à la robustesse du modèle. Nous avons traduit des machines multi-rubans en machines à un seul ruban, des machines non-déterministes en machines déterministes, et nous avons construit la machine universelle, démontrant que l'interprétation est elle-même une traduction dont le coût doit être soldé. La troisième partie a tracé les frontières de l'incompressible et de l'indécidable, rappelant que le temps et l'espace ne sont pas de simples métriques, mais des ressources hiérarchiques qui structurent la réalité du calcul. Enfin, la quatrième partie a achevé la traduction vers les circuits booléens et les classes de complexité, préparant le terrain pour le programme RTC.

### Le registre des statuts : une épistémologie de la traduction

Pour mener à bien cette entreprise, il nous fallait un outil épistémologique capable de distinguer l'intuition de la certitude, et l'asymptotique grossière de la borne fine. C'est pourquoi j'ai imposé, pour chaque affirmation de ce livre, l'usage du registre des statuts. Ce cadre de travail n'est pas une simple coquetterie de présentation ; c'est une nécessité méthodologique pour quiconque s'intéresse aux traductions à ressources.

Rappelons la signification de ces étiquettes, qui ont rythmé notre lecture. Le statut PROUVÉ a été réservé aux résultats dont la preuve complète et détaillée figure dans le tome. Par exemple, la simulation d'une machine à $k$ rubans par une machine à un seul ruban avec un coût en temps quadratique est PROUVÉ, en s'appuyant sur les techniques de Hennie et Stearns 1966 et la formalisation de Hopcroft et Ullman 1979. Le statut CONNU a été appliqué aux grands théorèmes dont nous avons donné l'énoncé et l'idée de la preuve, en le disant explicitement. C'est le cas du théorème de Savitch 1970, qui établit que l'espace non-déterministe peut être déterminisé au prix d'une élévation au carré de l'espace, ou encore de la hiérarchie en temps de Hartmanis et Stearns 1965.

Les statuts EXPÉRIMENTAL, CONJECTURE, RÉFUTÉ et OUVERT ont servi à baliser les terres inconnues ou contestées du programme RTC. Trop souvent, dans la littérature de vulgarisation ou même dans certains manuels avancés, une intuition sur le comportement d'un algorithme est présentée comme une vérité établie. En étiquetant CONJECTURE les lois candidates sur la conservation des ressources, et OUVERT les questions non tranchées, nous avons tracé une ligne de démarcation nette entre ce que la science des machines a démontré et ce qu'elle espère. Ce registre est la garantie que le lecteur cultivé, même non spécialiste, ne confondra jamais la beauté d'une hypothèse avec la solidité d'une démonstration. C'est cette honnêteté intellectuelle qui fait la valeur d'un traité sur la complexité.

### Les grandes traductions et leurs coûts : un bilan synthétique

Si nous devons tirer un bilan de ces deux cents pages, c'est celui de l'universalité des coûts cachés. Prenons le temps de synthétiser les traductions majeures que nous avons opérées, en gardant à l'esprit la fiche de traduction : source, cible, invariant préservé, et coûts multiples.

La traduction du multi-ruban vers le mono-ruban est l'exemple parfait du déplacement de ressources. L'invariant préservé est le langage reconnu. La cible est une machine à un seul ruban. Le coût en temps est quadratique, le coût en espace est linéaire, et la taille de la description augmente d'un facteur constant dépendant du nombre de rubans et de la taille de l'alphabet. Ce résultat, PROUVÉ, nous enseigne que la parallélisation spatiale (plusieurs rubans) s'achète au prix d'une perte de temps lors de la sérialisation sur un support unique.

La traduction du non-déterminisme vers le déterminisme est encore plus vertigineuse. L'arbre de calcul non-déterministe, exploré en largeur ou en profondeur, doit être aplati. L'invariant est la classe des langages acceptés. Mais le coût en temps est exponentiel dans le pire des cas, tandis que le coût en espace, grâce à l'ingéniosité de la construction de Savitch 1970, n'est que quadratique. Ici, la ressource "espace" est privilégiée au détriment de la ressource "temps". C'est une leçon fondamentale de comptabilité : on peut compresser l'espace de vérification, mais le temps d'exploration s'étire inéluctablement.

La traduction vers les circuits booléens, abordée dans la quatrième partie, change radicalement de paradigme. Nous passons d'un modèle séquentiel et infini (la machine de Turing) à un modèle parallèle, fini et acyclique. L'invariant préservé est la fonction booléenne calculée sur des entrées de taille bornée $n$. Les travaux de Pippenger et Fischer 1979 nous ont permis d'établir, avec le statut CONNU, qu'une machine de Turing fonctionnant en temps $t$ peut être simulée par un circuit de taille $O(t \log t)$. Mais cette traduction fait émerger de nouvelles ressources : la profondeur du circuit (qui correspond au temps parallèle), la largeur (qui correspond à l'espace), et le partage des sous-circuits. Nous avons vu que la traduction d'un calcul en formule logique, au sens de Cook 1971, préserve la satisfiabilité mais explose la taille de la description, créant ainsi le pont vers la classe NP.

Enfin, la traduction vers les automates finis, lorsque l'espace est borné par une constante, nous ramène aux origines de la théorie des langages formels avec Kleene 1956. L'invariant est la régularité du langage. Le coût est l'effondrement de la mémoire : la machine perd sa capacité à compter au-delà d'un seuil fini, et la ressource "espace" est figée, ne laissant que le "temps" et la "taille de description" (le nombre d'états) comme variables d'ajustement.

### Perspectives et questions ouvertes : le programme RTC

Ce livre n'est pas un point d'arrivée ; c'est le manifeste fondateur du programme RTC, l'étude systématique des Traductions à Ressources et de leur Conservation. Si les chapitres précédents ont soldé les comptes du vingtième siècle, le programme RTC ouvre des chantiers pour les décennies à venir.

Plusieurs questions demeurent étiquetées OUVERT. La plus célèbre, bien sûr, concerne la traduction entre les classes P et NP. Depuis Cook 1971, nous savons que la traduction d'un calcul non-déterministe polynomial en un problème de satisfiabilité booléenne est possible et préserve l'invariant de décision. Mais la question de savoir si cette traduction peut être inversée sans coût exponentiel en temps reste le grand OUVERT de notre discipline. Si P = NP, cela signifierait qu'il existe une traduction qui conserve l'invariant sémantique tout en annulant le surcoût temporel du déterminisme. Mais le programme RTC nous pousse à poser une question plus fine : même si P = NP, quel serait le coût de cette traduction en termes de taille de description, de profondeur de circuit, ou de précision arithmétique ? L'effondrement du temps entraînerait-il une explosion inévitable d'une autre ressource ?

C'est ici qu'interviennent nos CONJECTURE. L'une des lois candidates du programme RTC, que j'ai formulée au chapitre 16, postule une conservation stricte du volume computationnel. CONJECTURE : Pour toute traduction non triviale entre un modèle séquentiel et un modèle parallèle (circuits), toute réduction de la profondeur (temps parallèle) d'un facteur polynomial exige une augmentation de la largeur (espace ou nombre de portes) d'un facteur au moins polynomial, et ce, indépendamment de la classe de complexité. Cette conjecture suggère qu'il existe une "masse" computationnelle invariante, produit de la profondeur et de la largeur, qui résiste à toute tentative d'optimisation simultanée.

Une autre perspective ouverte par le programme RTC concerne la ressource de "partage". Dans les modèles de calcul modernes, la capacité à partager des sous-calculs modifie radicalement la taille de la description. Comment traduire une machine de Turing universelle, au sens de Papadimitriou 1994 et Arora et Barak 2009, dans un modèle où le partage est interdit ? Quel est le coût exact en précision lorsque l'on traduit des calculs réels ou continus vers des rubans discrets ? Ces questions, actuellement OUVERT, nécessitent de nouvelles fiches de traduction, où la précision et le partage rejoindront le temps et l'espace dans le grand livre de la comptabilité.

### Mot final au lecteur : la machine comme miroir

Au moment de poser la plume, je m'adresse à vous, lecteur, qui avez accepté de me suivre dans les méandres des configurations et des réductions. Vous n'êtes peut-être pas un spécialiste de la théorie de la complexité, mais vous avez désormais en main les outils pour décortiquer les promesses des algorithmes qui façonnent notre monde.

La machine de Turing, dans sa nudité originelle — un ruban infini, une tête de lecture, et une table de transitions —, peut sembler déconnectée des réalités technologiques contemporaines. Pourtant, c'est précisément cette abstraction qui fait sa puissance. En étudiant les traductions à ressources, nous n'avons pas seulement analysé des modèles mathématiques ; nous avons exploré les limites physiques et logiques de la pensée computationnelle. Chaque fois qu'un ingénieur vous promet qu'un nouveau paradigme de calcul résoudra un problème complexe en un instant, votre esprit, formé par le registre des statuts, devra immédiatement s'interroger : quel est l'invariant préservé ? Et surtout, quelle ressource a été déplacée dans l'ombre ? L'espace a-t-il été sacrifié ? La taille de la description a-t-elle explosé ? La précision a-t-elle été tronquée ?

Les machines que nous avons décrites sont des miroirs. Elles reflètent notre propre capacité à structurer l'information, à vérifier des preuves, et à accepter les compromis. L'indécidabilité de l'arrêt n'est pas une faille de nos ordinateurs ; c'est la preuve formelle que la création et l'analyse ne peuvent être entièrement mécanisées sans heurter un mur logique. Les hiérarchies en temps et en espace nous rappellent que l'univers de l'information est vaste, et que certains problèmes requièrent intrinsèquement plus de réalité physique — plus de temps, plus de matière — pour être résolus.

Ce livre a tenu le registre de ces déplacements. Il a refusé de présenter l'intuition comme une preuve, et a exigé que chaque coût soit explicitement soldé. En refermant cet ouvrage, je forme le vœu que vous emportiez avec vous cette rigueur de la comptabilité de l'exécution. Que vous soyez étudiant, chercheur, ou simplement un esprit curieux des fondements du numérique, puissiez-vous ne jamais accepter une traduction sans en examiner le prix.

Le ruban de la machine de Turing est infini, et les configurations possibles sont innombrables. Le programme RTC ne fait que commencer, et les fiches de traduction de demain restent à écrire. Mais désormais, vous savez comment les lire, comment les contester, et comment les prouver. La machine s'arrête ici, mais l'exécution de votre propre réflexion, elle, ne fait que commencer.

Toutefois, avant de vous abandonner à cette exécution personnelle, il me reste un devoir d'auteur : vous fournir les instruments de navigation qui structurent l'appareil critique de ce tome. Un traité de comptabilité ne saurait se refermer sans laisser à son lecteur le grand livre des comptes, la table des conversions et le glossaire des monnaies d'échange. Ces annexes conceptuelles, trop souvent reléguées à de simples index alphabétiques dans la littérature classique, sont ici élevées au rang de synthèse méthodologique. Elles constituent la boîte à outils du programme RTC.

### Le glossaire des ressources : anatomie des monnaies d'échange

Dans le cadre des traductions à ressources, l'ambiguïté sémantique est l'ennemie de la preuve. Chaque ressource doit être définie opérationnellement avant d'être échangée. Voici les définitions qui doivent guider votre lecture des fiches de traduction, qu'elles s'appliquent aux machines de Turing, aux circuits ou aux automates.

**Temps ($T$)** : Le nombre d'étapes de transition locales effectuées par la machine depuis la configuration initiale jusqu'à la configuration d'acceptation ou de rejet. Dans les circuits, le temps est assimilé à la profondeur.
**Espace ($S$)** : Le nombre de cases distinctes du ruban visitées par au moins une tête de lecture au cours de l'exécution.
**Taille de description ($D$)** : La longueur de l'encodage binaire de la machine (nombre d'états, taille de l'alphabet, table de transitions) ou la taille du circuit (nombre total de portes logiques).
**Profondeur ($P$)** et **Largeur ($L$)** : Ressources natives des circuits booléens. La profondeur est la longueur du plus long chemin dirigé de l'entrée vers la sortie (temps parallèle) ; la largeur est le nombre maximal de portes sur une même couche (espace parallèle).
**Partage ($\Sigma$)** : La capacité d'un modèle à réutiliser le résultat d'un sous-calcul sans le dupliquer. Les circuits permettent le partage (un graphe acyclique orienté), tandis que les formules booléennes l'interdisent (ce sont des arbres), ce qui provoque une explosion de la taille de description.
**Précision ($\Pi$)** : Le nombre de bits ou de symboles nécessaires pour représenter une donnée, particulièrement cruciale lorsqu'on traduit des modèles continus ou probabilistes vers le ruban discret de Turing 1936.

**Exemple** : Considérons la traduction d'un algorithme de tri sur un ruban. L'invariant est la permutation correcte de l'entrée. Si nous traduisons cet algorithme vers un automate fini (Kleene 1956), la ressource "espace" s'effondre à une constante, mais l'invariant ne peut être préservé pour des entrées de taille arbitraire. L'automate ne peut "compter" ni "mémoriser" les éléments, ce qui démontre que la mémoire (l'espace non borné) est une ressource indispensable pour cette classe de fonctions.

**Exercice** : Soit un langage $L$ reconnu par une machine non-déterministe en espace $S(n)$. Selon le théorème de Savitch 1970, nous savons qu'il existe une machine déterministe le reconnaissant en espace $O(S(n)^2)$. Si l'on tente de traduire cette machine déterministe en un circuit booléen de profondeur $O(S(n)^2)$, quelle ressource subit une inflation incontrôlée ?
*Réponse* : La largeur du circuit (et donc sa taille totale). La simulation d'un espace mémoire réutilisable sur $T$ étapes de temps exige un déroulement temporel qui fait exploser le nombre de portes, une limitation fondamentale étudiée par Papadimitriou 1994. Statut de l'analyse : CONNU.

### La table des traductions : trois fiches canoniques

Pour illustrer la rigueur exigée par le registre des statuts, voici trois fiches de traduction canoniques qui résument l'économie computationnelle de notre discipline. Elles servent de matrice pour toute analyse future.

**Fiche A : La sérialisation spatiale**
*Source* : Machine de Turing à $k$ rubans ($k \geq 2$).
*Cible* : Machine de Turing à 2 rubans.
*Invariant préservé* : Langage formel reconnu.
*Coût en temps* : $O(t \log t)$ où $t$ est le temps de la machine source.
*Coût en espace* : $O(s)$ où $s$ est l'espace source.
*Statut de l'énoncé* : PROUVÉ (Hennie et Stearns 1966).
*Statut de l'optimalité* : CONNU. L'optimalité de la borne inférieure pour le cas général reste un sujet d'étude, bien que Hopcroft et Ullman 1979 en détaillent les mécanismes de simulation par entrelacement des rubans.

**Fiche B : La déterminisation de l'espace**
*Source* : Machine non-déterministe en espace $S(n)$.
*Cible* : Machine déterministe.
*Invariant préservé* : Langage reconnu.
*Coût en temps* : Exponentiel en $S(n)$ dans le pire cas.
*Coût en espace* : $O(S(n)^2)$.
*Statut de l'énoncé* : PROUVÉ (Savitch 1970).
*Statut de l'optimalité* : OUVERT. Nous ne savons pas à ce jour si l'exposant $2$ peut être amélioré de manière générale pour toutes les classes d'espace, ce qui constitue l'une des énigmes majeures de la complexité structurelle.

**Fiche C : L'extraction vers le circuit**
*Source* : Calcul d'une machine de Turing en temps $t$.
*Cible* : Circuit booléen.
*Invariant préservé* : Fonction calculée sur une entrée de taille $n$.
*Coût en taille de description* : $O(t \log t)$.
*Coût en profondeur* : $O(t)$.
*Statut de l'énoncé* : CONNU (Pippenger et Fischer 1979).
*Statut de l'optimalité* : CONJECTURE. Nous conjecturons que la borne $O(t \log t)$ est strictement optimale pour la simulation de machines à un seul ruban par des circuits, en raison du coût incompressible du routage de l'information sur le ruban.

### Postface : L'Entscheidungsproblem et l'horizon du programme RTC

En 1936, lorsqu'Alan Turing a formulé sa machine abstraite pour répondre à l'Entscheidungsproblem, il ne cherchait pas à optimiser le temps d'exécution ni à minimiser l'espace mémoire. Son objectif était d'une tout autre ampleur : définir l'essence même du calcul, tracer la frontière entre ce qui peut être mécanisé et ce qui échappe à toute procédure finie. L'indécidabilité de l'arrêt, que nous avons longuement auscultée au chapitre 9, demeure la cicatrice originelle de notre discipline. Elle nous rappelle que la machine, aussi puissante soit-elle, bute inévitablement sur son propre reflet.

Pourtant, en refermant ce livre, vous avez compris que l'héritage de Turing 1936 ne se limite pas à cette frontière absolue. En descendant dans les couches de la complexité, en suivant les pas de Cook 1971 sur la réductibilité polynomiale et de Hartmanis et Stearns 1965 sur les hiérarchies temporelles, nous avons découvert que l'univers du calculable est lui-même structuré par une gravité implacable. Les ressources ne se créent pas, elles ne se perdent pas : elles se déplacent.

Le programme RTC, dont ce tome pose les fondations, est l'héritier direct de cette intuition. Il postule que l'étude des modèles de calcul ne doit plus se contenter de l'équivalence asymptotique grossière, mais doit plonger dans la micro-structure des coûts. Quand Arora et Barak 2009 ou Sipser 1997 exposent les grands théorèmes de la complexité moderne, ils nous offrent la carte des territoires. Le programme RTC, lui, vous donne la boussole et le carnet de comptable pour en explorer les sentiers cachés.

Les questions étiquetées OUVERT, au premier rang desquelles la séparation des classes P et NP, ne sont pas des échecs de la théorie. Ce sont les moteurs de la comptabilité. Si un jour une preuve venait à établir que P = NP, le programme RTC ne s'effondrerait pas ; il se déplacerait. Il exigerait alors de connaître le coût exact de cette translation en termes de taille de description, de profondeur de circuit, et de constantes cachées. L'invariant sémantique serait sauvé, mais la facture des ressources devrait tout de même être payée.

Voici donc le grand livre refermé. Les états sont figés, les rubans rembobinés, les configurations archivées. Mais la machine de Turing, dans son abstraction implacable, continuera de tourner en arrière-plan de chaque algorithme, de chaque circuit, de chaque preuve. À vous, désormais, de tenir les comptes.