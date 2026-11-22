## Introduction

### Le grand malentendu : calculer, est-ce penser ou transformer ?

Depuis les prémices de l'informatique théorique, une fracture conceptuelle divise la manière dont nous concevons le traitement de l'information. D'un côté, le calcul symbolique, incarné par la machine de Turing (Turing 1936), repose sur la manipulation discrète, séquentielle et exacte de symboles sur un ruban infiniment long. De l'autre, le calcul neuronal, initié par le modèle de McCulloch et Pitts (1943), propose une vision où le calcul émerge de l'activation parallèle et continue d'un vaste réseau d'unités interconnectées. Pendant des décennies, ces deux paradigmes ont été perçus comme des mondes étanches, voire rivaux : l'intelligence artificielle symbolique cherchait à expliciter les règles de la logique, tandis que le connexionnisme tentait d'imiter l'apprentissage statistique du cerveau biologique.

Aujourd'hui, à l'ère des grands modèles de langage et de l'architecture transformer (Vaswani et al. 2017), ce clivage historique a engendré un grand malentendu. Parce que les réseaux de neurones modernes accomplissent des tâches d'une complexité apparente inouïe — rédiger du code, traduire des langues, résoudre des problèmes mathématiques — une illusion tenace s'est installée : celle selon laquelle les réseaux de neurones constitueraient un nouveau paradigme de *calculabilité*, une rupture fondamentale avec les limites théoriques établies au vingtième siècle.

Ce livre est né de la nécessité de dissiper ce malentendu. Les réseaux de neurones ne calculent pas *autre chose* que les machines de Turing ; ils calculent *autrement*, sous des contraintes de ressources radicalement différentes. Comprendre l'intelligence artificielle moderne ne consiste pas à opposer le symbolique au neuronal, mais à étudier rigoureusement les ponts qui les relient. Ces ponts, je les nomme des **traductions**.

Traduire un algorithme symbolique en un réseau de neurones, ou extraire un automate fini d'un réseau entraîné, n'est pas une simple équivalence mathématique. C'est une opération de transformation qui, à l'instar de la traduction entre deux langues naturelles, altère la structure profonde du message. Une traduction computationnelle a un coût, elle préserve certaines propriétés, en sacrifie d'autres, et exige des compromis inévitables. L'objet de cet ouvrage est de cartographier ces compromis, de les quantifier et d'en révéler les limites fondamentales.

### La thèse du livre : les traductions à ressources

La thèse centrale de ce livre peut s'énoncer ainsi : toute traduction entre un modèle de calcul symbolique (machine de Turing, automate fini, circuit booléen) et un modèle neuronal (réseau de McCulloch-Pitts, réseau récurrent rationnel, transformer) peut être intégralement caractérisée par un septuplet de coûts et par un bilan de conservation et de perte de propriétés structurelles.

Lorsque nous compilons une machine de Turing en un réseau récurrent, nous ne nous contentons pas de prouver que les deux modèles reconnaissent les mêmes langages formels. Nous devons évaluer le coût de cette opération selon sept dimensions fondamentales :
1. **La taille** : quel est le rapport entre le nombre d'états de la machine et le nombre de neurones ou de poids synaptiques requis ?
2. **Le temps** : combien de pas de calcul discrets de la machine correspondent-ils à une itération (ou *forward pass*) dans le réseau ?
3. **La mémoire** : comment la bande infinie de la machine de Turing est-elle encodée dans un vecteur d'activation de dimension fixe ou variable ?
4. **La profondeur** : quelle est la complexité en profondeur du circuit équivalent, une notion cruciale héritée de la théorie de la complexité (Arora et Barak 2009) ?
5. **La largeur** : quelle dimension cachée est nécessaire pour représenter l'alphabet de la machine sans collision d'information ?
6. **La précision** : combien de bits sont nécessaires pour représenter les poids et les activations sans que le bruit arithmétique ne détruise le calcul ?
7. **Le partage** : dans quelle mesure les poids sont-ils réutilisés à travers le temps (réseaux récurrents) ou l'espace (transformers) ?

À ce septuplet de coûts s'ajoute un bilan qualitatif. Que conserve-t-on lors de la traduction ? La **Turing-complétude** (la capacité à simuler toute fonction calculable) est-elle maintenue ? Le **déterminisme** strict de la machine survit-il à la nature distribuée des représentations neuronales ? Le **parallélisme** massif des architectures modernes (Vaswani et al. 2017) compense-t-il la perte de séquentialité explicite ? Enfin, la **robustesse** face aux perturbations est-elle acquise ou perdue ? Chaque chapitre de ce livre se consacre à l'analyse minutieuse de ces bilans pour une traduction spécifique.

### La précision arithmétique : la ressource pivot

Parmi toutes les ressources du septuplet, l'une d'elles joue un rôle absolument central, agissant comme le point de bascule entre la théorie idéalisée et la réalité computationnelle : la **précision arithmétique**. C'est la ressource pivot de notre enquête.

Dans le modèle symbolique de Turing (1936), la précision est intrinsèquement infinie et parfaite. Un symbole sur le ruban est un symbole ; il n'y a pas d'erreur d'arrondi, pas de bruit de quantification. L'information est discrète et absolue. À l'inverse, les réseaux de neurones opèrent sur des valeurs numériques. La nature de ces valeurs détermine la puissance même du modèle.

L'histoire de cette ressource pivot est fascinante. En 1995, Siegelmann et Sontag ont démontré que les réseaux de neurones récurrents dotés de poids rationnels étaient Turing-complets. Cependant, cette preuve repose sur une hypothèse d'une exigence redoutable : la **précision arbitraire**. Pour simuler un ruban de Turing infini, le réseau doit encoder l'information dans les décimales de nombres rationnels dont le dénominateur croît indéfiniment. À chaque pas de temps, la précision requise augmente. Mathématiquement, le résultat est d'une grande beauté ; physiquement et informationnellement, il est inatteignable.

Que se passe-t-il lorsque nous restreignons cette précision à ce qui est matériellement réalisable ? C'est ici que le paysage théorique s'effondre et se reconfigure. Des travaux récents, notamment ceux de Merrill et Sabharwal (2023), ont établi que les transformers opérant avec une précision logarithmique — c'est-à-dire utilisant $O(\log n)$ bits pour traiter une séquence de longueur $n$, ce qui correspond aux standards du matériel informatique actuel — perdent la Turing-complétude. Sous cette contrainte de précision, le transformer ne peut plus simuler une machine de Turing universelle ; il se réduit à un circuit de faible profondeur, appartenant à des classes de complexité strictes comme $\mathsf{TC}^0$.

Ce résultat est l'un des piliers de notre réflexion. Il prouve que la puissance algorithmique des architectures modernes n'est pas une propriété absolue de leur topologie, mais le produit fragile d'une interaction entre leur structure et la précision arithmétique qui leur est allouée. La précision est le goulot d'étranglement par lequel le calcul neuronal retrouve les limites du calcul symbolique.

### Le registre des statuts et les règles du programme RTC

L'étude des capacités computationnelles de l'intelligence artificielle est trop souvent polluée par une confusion entre l'intuition empirique et la démonstration mathématique. On lit fréquemment que « les transformers comprennent la logique » ou que « les réseaux récurrents sont équivalents aux machines de Turing », sans que les conditions de ces affirmations ne soient précisées.

Pour garantir la rigueur de cet ouvrage, j'adopte et j'applique le cadre conceptuel du programme **RTC (Ressources, Traductions, Calculs)**. Ce programme impose des règles absolues qui structurent chaque page de ce livre :

1. **L'intuition ne tient pas lieu de preuve.** Lorsqu'un résultat est démontré dans ces pages, la preuve complète est fournie. Lorsqu'il s'agit d'un grand théorème classique (comme la caractérisation des langages réguliers par Kleene 1956), l'idée de la preuve est exposée explicitement, et le lecteur est informé de son statut.
2. **Chaque affirmation théorique porte un statut explicite.** Pour naviguer dans la littérature et dans nos propres déductions, nous utiliserons le registre des statuts suivant :
   - **PROUVÉ** : le résultat est démontré formellement dans le cadre de ce livre.
   - **CONNU** : le résultat est un théorème établi et accepté dans la littérature autorisée.
   - **EXPÉRIMENTAL** : le phénomène est observé de manière reproductible en simulation, mais ne dispose pas encore de preuve formelle complète.
   - **CONJECTURE** : une hypothèse forte, soutenue par des arguments théoriques partiels, mais non démontrée.
   - **RÉFUTÉ** : une affirmation anciennement considérée comme vraie, mais dont la fausseté a été démontrée (par exemple, la Turing-complétude des transformers à précision finie).
   - **OUVERT** : une question fondamentale dont la résolution échappe encore à l'état de l'art.
3. **Aucune annonce de découverte.** Ce livre est un ouvrage de synthèse, de clarification et de traduction entre des modèles existants. Il ne prétend pas résoudre les grandes questions ouvertes de la théorie de la complexité, mais il les expose avec clarté.
4. **Références strictement contrôlées.** Seules les références fondamentales et autorisées sont citées, toujours avec leur auteur et leur année, sans artifice bibliographique superflu.

En appliquant ce registre, le lecteur saura toujours exactement sur quel sol il marche. Lorsqu'il lira que la convergence des réseaux de Hopfield (1982) vers des minima locaux d'une fonction d'énergie est **CONNUE**, il saura qu'il s'agit d'un théorème de physique statistique appliqué. Lorsqu'il lira que la capacité des transformers à généraliser hors de leur domaine d'entraînement est **EXPÉRIMENTALE**, il saura qu'il entre dans le territoire encore non balisé de la théorie de l'apprentissage.

### Public visé et méthode pédagogique

À qui s'adresse ce livre ? J'ai conçu cet ouvrage pour le **lecteur cultivé non spécialiste**. Vous n'avez pas besoin d'être chercheur en théorie de la calculabilité pour comprendre les enjeux des traductions à ressources. Il vous suffit de posséder une culture mathématique de premier cycle universitaire : vous savez ce qu'est une fonction, vous êtes familier avec le concept de matrice, vous comprenez la notion d'algorithme et vous avez une intuition de ce qu'est la complexité algorithmique.

Pour rendre les concepts abstraits de la théorie des automates et de la complexité des circuits accessibles sans rien sacrifier de leur rigueur, chaque concept clé, chaque traduction et chaque théorème seront déployés selon une méthode pédagogique en cinq temps :

1. **L'Intuition** : nous commencerons toujours par une métaphore physique, logique ou linguistique. Avant de définir formellement un automate fini, nous le concevrons comme un tourniquet de métro ou un distributeur de boissons.
2. **La Définition** : une fois l'intuition ancrée, nous poserons le cadre mathématique strict. Les objets seront définis sous forme de tuples, les espaces seront spécifiés, les fonctions de transition seront écrites en LaTeX, par exemple $\delta : Q \times \Sigma \to Q$.
3. **L'Énoncé** : le théorème ou la propriété de traduction sera formulé de manière concise et non ambiguë.
4. **L'Exemple** : nous déroulerons l'énoncé sur un cas concret, pas à pas, pour montrer comment la machinerie mathématique opère en pratique.
5. **L'Exercice** : à la fin de chaque section majeure, un exercice permettra au lecteur de tester sa compréhension active, souvent en calculant un coût spécifique d'une traduction donnée.

Cette structure vise à désacraliser la théorie du calcul. Les machines de Turing et les réseaux de neurones ne sont pas des entités mystiques ; ce sont des objets mathématiques que l'on peut démonter, comparer et recomposer.

### Le sens des traductions : un voyage en quatre parties

Le plan de cet ouvrage est structuré comme un voyage progressif, partant des fondations pour aller vers les architectures les plus modernes, avant de confronter la théorie à la réalité matérielle.

**La Partie I — Modèles sources et modèles cibles : poser le cadre des traductions**
Avant de traduire, il faut maîtriser les langues en présence.
Le **Chapitre 1** établit la machine de Turing (Turing 1936) comme l'étalon absolu du calcul, en définissant la Turing-complétude et les limites de la calculabilité.
Le **Chapitre 2** explore les automates finis et les expressions régulières (Kleene 1956), qui constituent le niveau le plus basique de la mémoire computationnelle.
Le **Chapitre 3** introduit les circuits booléens et la notion de profondeur (Arora et Barak 2009), un modèle essentiel pour comprendre les limites du parallélisme.
Enfin, le **Chapitre 4** pose les fondations des réseaux de neurones formels, des premiers modèles logiques de McCulloch et Pitts (1943) aux architectures profondes modernes.

**La Partie II — Traductions descendantes : du symbolique au neuronal**
Cette partie examine comment compiler des structures logiques explicites en poids synaptiques.
Le **Chapitre 5** détaille la traduction historique des automates finis vers les réseaux de McCulloch-Pitts, en évaluant le coût en taille et en temps.
Le **Chapitre 6** s'attaque au sommet de la traduction descendante : la simulation d'une machine de Turing par un réseau récurrent rationnel, en analysant la construction de Siegelmann et Sontag (1995) et son coût exorbitant en précision arithmétique.
Le **Chapitre 7** aborde les réseaux de Hopfield (1982) sous l'angle de l'optimisation combinatoire, montrant comment un problème symbolique (comme le voyageur de commerce) se traduit en un paysage d'énergie continue, et ce qui se perd en termes de garantie de solution optimale.

**La Partie III — Traductions modernes : transformers et rôle de la précision**
C'est le cœur contemporain de l'ouvrage.
Le **Chapitre 8** dissèque l'architecture transformer (Vaswani et al. 2017) non comme un modèle statistique, mais comme un modèle de calcul formel, en isolant le mécanisme d'attention.
Le **Chapitre 9** explore les conditions sous lesquelles les transformers atteignent la Turing-complétude, en s'appuyant sur les travaux de Pérez, Marinković et Barceló (2019), et révèle le coût caché de ces constructions théoriques.
Le **Chapitre 10** opère un retour au principe de réalité : il détaille les limites drastiques des transformers à précision logarithmique (Merrill et Sabharwal 2023), démontrant l'effondrement de leur puissance vers des classes de circuits de faible profondeur.
Le **Chapitre 11** synthétise ces analyses dans un vaste tableau comparatif des traductions TM $\to$ modèles neuronaux, croisant le septuplet de coûts et le bilan de conservation.

**La Partie IV — Limites, questions ouvertes et transfert vers RTC**
La dernière partie tire les conséquences de nos analyses et ouvre les perspectives de recherche.
Le **Chapitre 12** généralise la réflexion sur la précision finie et l'effondrement inévitable de la Turing-complétude dans tout système physique réel.
Le **Chapitre 13** met en lumière les coûts cachés des traductions, notamment l'explosion du temps d'inférence et les goulets d'étranglement mémoire.
Le **Chapitre 14** inverse la direction du voyage : il explore les traductions ascendantes, du neuronal vers le symbolique, et la difficulté d'extraire des automates lisibles à partir de réseaux entraînés.
Le **Chapitre 15** élargit le cadre vers des notions plus vastes : la robustesse face au bruit, les limites de l'apprentissage par descente de gradient pour découvrir des algorithmes symboliques, et la modélisation du calcul naturel.
Enfin, le **Chapitre 16**, intitulé « Transfert vers le programme RTC », conclut l'ouvrage en exposant comment les leçons tirées de ces traductions entre modèles enrichissent l'étude globale des ressources computationnelles, et comment ce cadre peut guider la conception des architectures de demain.

### Conclusion de l'introduction

Traduire, c'est choisir. Choisir de sacrifier l'exactitude symbolique pour gagner en robustesse statistique ; choisir d'abandonner la séquentialité stricte pour embrasser le parallélisme massif ; choisir de limiter la précision arithmétique pour rendre le calcul matériellement possible.

En refermant ce livre, vous ne verrez plus les réseaux de neurones comme des boîtes noires magiques, ni les machines de Turing comme des reliques d'un passé révolu. Vous les verrez pour ce qu'ils sont véritablement : des points distincts dans un vaste espace de modèles de calcul, reliés par des transformations dont les coûts et les bénéfices peuvent être pesés, mesurés et compris.

Le voyage de la machine de Turing au transformer n'est pas une simple progression technologique. C'est l'histoire profonde de la manière dont l'information se plie aux contraintes de la matière et du temps. Commençons ce voyage.

# Partie I — Modèles sources et modèles cibles : poser le cadre des traductions

## Chapitre 1 – La machine de Turing comme étalon de calcul

### L'Intuition : Le bureaucrate myope et le ruban infini

Pour comprendre ce que signifie « traduire » un calcul, il faut d'abord comprendre ce qu'est un calcul dans sa forme la plus pure, la plus dépouillée de toute contingence matérielle. Lorsque Alan Turing publie son article fondateur en 1936 (Turing 1936), son objectif n'est pas de concevoir l'ancêtre de nos ordinateurs modernes. Son but est de répondre à l'*Entscheidungsproblem* (le problème de la décision) posé par David Hilbert, en formalisant la notion même de « méthode » ou de « procédure effective ».

Pour y parvenir, Turing s'inspire d'une image profondément humaine : celle du « calculateur humain », un clerc de bureau assis à un pupitre, armé d'un crayon, d'une gomme et d'un cahier de règles, exécutant aveuglément des opérations arithmétiques ou logiques. Turing opère alors une réduction géniale. Il retire à ce clerc toute son intelligence, toute sa mémoire à long terme, toute sa capacité à embrasser du regard une page entière. Il ne lui laisse qu'une vision strictement locale (myope), un ruban de papier infiniment long divisé en cases, et la capacité de modifier son propre état d'esprit interne en fonction du symbole qu'il a sous les yeux.

C'est cette métaphore du bureaucrate myope qui fonde notre étalon de calcul. L'intuition profonde est la suivante : la complexité d'un algorithme ne réside pas dans la richesse de son support physique, mais dans la profondeur de la séquence d'actions élémentaires. En réduisant le calcul à son atome indiscutable — lire un symbole, changer d'état, écrire un symbole, se déplacer d'une case — Turing a isolé l'essence même de l'information algorithmique. C'est à partir de cet atome que nous construirons toutes nos traductions vers les architectures neuronales.

### La Définition : L'anatomie formelle de l'étalon

Passons maintenant de la métaphore à la rigueur mathématique. Une machine de Turing déterministe à un seul ruban est définie par un tuple à sept composantes :

$$M = (Q, \Sigma, \Gamma, \delta, q_0, q_{accept}, q_{reject})$$

Décomposons cette anatomie :
- $Q$ est un ensemble fini d'**états**. C'est la « mémoire interne » ou l'état d'esprit du bureaucrate.
- $\Sigma$ est l'**alphabet d'entrée**, l'ensemble des symboles qui peuvent composer le problème initial (par exemple, $\{0, 1\}$). Le symbole blanc $\sqcup$ n'appartient jamais à $\Sigma$.
- $\Gamma$ est l'**alphabet du ruban**, avec $\Sigma \subset \Gamma$ et $\sqcup \in \Gamma$. C'est l'ensemble de tous les symboles que la machine est autorisée à lire et à écrire.
- $q_0 \in Q$ est l'**état initial**, le point de départ de tout calcul.
- $q_{accept} \in Q$ et $q_{reject} \in Q$ sont les états terminaux d'**acceptation** et de **rejet**.
- $\delta$ est la **fonction de transition**, le cœur algorithmique de la machine. Elle est définie par :
  $$\delta : Q \times \Gamma \to Q \times \Gamma \times \{G, D\}$$

Cette fonction $\delta$ dicte la loi unique de l'univers de la machine : « Si tu es dans l'état $q$ et que tu lis le symbole $a$, alors tu passes dans l'état $q'$, tu écris le symbole $b$ à la place de $a$, et tu déplaces ta tête de lecture d'une case vers la Gauche ($G$) ou vers la Droite ($D$). »

Pour analyser le calcul, nous devons définir la notion de **configuration**. Une configuration est une photographie instantanée de la machine à un instant $t$. Elle s'écrit généralement sous la forme $u \ q \ v$, où $u, v \in \Gamma^*$. Cela signifie que le ruban contient la séquence $uv$, que la tête de lecture pointe sur le premier symbole de $v$, et que l'état interne actuel est $q$. Le calcul n'est rien d'autre qu'une séquence de configurations $C_0 \vdash C_1 \vdash C_2 \dots \vdash C_k$, où $\vdash$ désigne la relation de transition en un pas de temps.

### L'Énoncé : La thèse de Church-Turing et l'universalité

Sur la base de cette définition formelle, nous pouvons énoncer le pilier central de l'informatique théorique.

**Énoncé de la Thèse de Church-Turing :** Toute fonction intuitivement calculable par une procédure effective peut être calculée par une machine de Turing.

Il est crucial de préciser le statut de cet énoncé.
**[STATUT : CONNU]** pour ce qui concerne l'équivalence mathématique entre le modèle de Turing, le lambda-calcul d'Alonzo Church et les fonctions récursives de Gödel. Tous ces formalismes, bien que radicalement différents dans leur syntaxe, délimitent exactement la même classe de fonctions calculables.
**[STATUT : OUVERT]** sur le plan philosophique et physique, car la thèse n'est pas un théorème mathématique démontrable (on ne peut pas prouver mathématiquement qu'une définition formelle épuise le concept intuitif de « calcul »), et la question de savoir si l'univers physique lui-même peut calculer des fonctions non-turingiennes reste un débat de physique théorique.

De cette thèse découle la notion de **Turing-complétude**. Un système formel, un langage de programmation ou, comme nous le verrons, un réseau de neurones, est dit *Turing-complet* s'il est capable de simuler une Machine de Turing Universelle (MTU). La MTU est l'invention conceptuelle la plus vertigineuse de Turing (1936) : une machine $U$ capable de lire sur son ruban la description formelle $\langle M \rangle$ d'une autre machine $M$, ainsi qu'une entrée $x$, et de simuler pas à pas le comportement de $M$ sur $x$. C'est l'acte de naissance du logiciel : le code et les données partagent le même support physique.

### L'Exemple : L'addition en notation unaire

Pour ancrer cette abstraction, dérouillons l'exécution d'une machine de Turing sur une tâche simple : l'addition de deux entiers en notation unaire.
Soit l'entrée $111 \sqcup 11$, représentant l'addition $3 + 2$. Le but est d'obtenir $11111$ sur le ruban.

Construisons une machine $M_{add}$ avec les états $Q = \{q_0, q_1, q_2, q_{accept}\}$.
- $\delta(q_0, 1) = (q_0, 1, D)$ : Tant qu'on lit un 1, on avance vers la droite pour chercher le séparateur.
- $\delta(q_0, \sqcup) = (q_1, 1, D)$ : Quand on trouve le blanc, on le remplace par un 1 (on fusionne les deux blocs) et on continue.
- $\delta(q_1, 1) = (q_1, 1, D)$ : On traverse le deuxième nombre.
- $\delta(q_1, \sqcup) = (q_2, \sqcup, G)$ : Arrivé à la fin du deuxième nombre, on recule d'une case pour effacer le dernier 1 (car en remplaçant le blanc par un 1, nous avons ajouté une unité de trop).
- $\delta(q_2, 1) = (q_{accept}, 1, D)$ : On efface le 1 superflu et on accepte.

**Trace de la configuration :**
1. $q_0 \ 111 \sqcup 11$ (Départ)
2. $1 \ q_0 \ 11 \sqcup 11$ (Avance)
3. $11 \ q_0 \ 1 \sqcup 11$ (Avance)
4. $111 \ q_0 \ \sqcup 11$ (Avance)
5. $1111 \ q_1 \ 11$ (Fusion et avance)
6. $11111 \ q_1 \ \sqcup$ (Traversée)
7. $1111 \ q_2 \ 1\sqcup$ (Recul)
8. $11111 \ q_{accept} \ \sqcup$ (Effacement et acceptation)

Cet exemple, bien que trivial, illustre la lourdeur séquentielle du modèle. Pour additionner deux nombres de taille $n$ et $m$, la tête de lecture doit physiquement traverser l'intégralité des symboles. Le temps de calcul est intrinsèquement lié à la géométrie du ruban.

### Le Septuplet de coûts appliqué à l'étalon

Puisque ce livre est consacré aux *traductions à ressources*, nous devons évaluer notre modèle source (la machine de Turing) à l'aune du septuplet de coûts qui structurera toutes nos comparaisons futures. Comment la machine de Turing se positionne-t-elle sur ces sept dimensions ?

1. **La taille** : Elle se mesure par la complexité de description de la machine, c'est-à-dire la taille de la table de transition $|\delta| \le |Q| \times |\Gamma|$. C'est une ressource finie et statique.
2. **Le temps** : Noté $T(n)$, c'est le nombre de transitions $\vdash$ nécessaires pour atteindre un état terminal pour une entrée de taille $n$. C'est la ressource la plus étudiée en théorie de la complexité (Arora et Barak 2009).
3. **La mémoire (Espace)** : Notée $S(n)$, c'est le nombre de cases distinctes du ruban visitées par la tête de lecture au cours du calcul.
4. **La profondeur** : Cette notion, native des circuits booléens, est étrangère à la machine de Turing native. Cependant, dans une optique de traduction, on peut considérer que chaque pas de temps $t$ de la machine correspond à une couche (ou *layer*) d'un circuit séquentiel. La profondeur est donc équivalente au temps $T(n)$.
5. **La largeur** : La machine de Turing opère avec une largeur strictement locale de $1$ symbole à la fois. C'est l'antithèse du parallélisme massif.
6. **La précision** : C'est la caractéristique la plus fondamentale de l'étalon. La précision est **absolue, symbolique et infinie**. Le symbole $1$ est identique à lui-même, qu'il soit lu au premier ou au milliardième pas de temps. Il n'y a aucune dégradation, aucune erreur d'arrondi, aucune dérive stochastique.
7. **Le partage** : La fonction de transition $\delta$ est invariablement réutilisée à chaque pas de temps. En termes modernes, on dirait que la machine de Turing possède un *partage de poids* (weight sharing) parfait et infini à travers le temps.

### Exercice : Complexité spatiale et temporelle des palindromes

**Énoncé de l'exercice :**
Considérez le langage des palindromes $L = \{w \in \{a, b\}^* \mid w = w^R\}$, où $w^R$ est le mot $w$ lu de droite à gauche. Concevez mentalement une machine de Turing $M_{pal}$ qui décide ce langage en comparant le premier et le dernier symbole, en les effaçant (ou en les marquant), puis en répétant l'opération vers le centre.
*Question :* Quel est le coût en espace $S(n)$ et le coût en temps $T(n)$ de cette machine pour un mot de longueur $n$ ?

**Idée de la preuve et résolution :**
**[STATUT : CONNU]**
- **Espace $S(n)$ :** La machine n'a besoin que de lire l'entrée initiale et de marquer les symboles visités. Elle ne s'aventure jamais au-delà des limites initiales du mot. L'espace requis est donc strictement linéaire : $S(n) = O(n)$.
- **Temps $T(n)$ :** Pour vérifier le premier symbole, la tête de lecture doit se déplacer jusqu'à l'extrémité droite du mot, ce qui prend $n$ pas. Elle marque le symbole et revient au début, prenant encore $n$ pas. Pour le deuxième symbole, le trajet est de $n-2$ pas, et ainsi de suite. Le temps total est la somme d'une suite arithmétique : $\sum_{i=1}^{n/2} 2(n - 2i) \approx n^2 / 2$. La complexité temporelle est donc quadratique : $T(n) = O(n^2)$.

Cet exercice met en lumière une limite structurelle de l'étalon de Turing : l'absence de mémoire à accès direct (RAM). L'information est stockée séquentiellement, ce qui impose un coût temporel quadratique pour une tâche qui, sur un ordinateur moderne (machine de Turing à accès aléatoire ou modèle RAM), se résout en temps linéaire $O(n)$. Cette friction spatiale sera un défi majeur lorsque nous traduirons des algorithmes symboliques vers des réseaux de neurones récurrents.

### Bilan de traduction : Ce qui se conserve, ce qui se perd

Nous arrivons au terme de ce chapitre fondateur en nous posant la question qui guidera le reste de l'ouvrage : lorsque nous tenterons de traduire cette machine de Turing vers un modèle neuronal (que ce soit un réseau de McCulloch-Pitts, un réseau récurrent rationnel ou un transformer), quel sera le bilan de l'opération ?

**Ce qui se conserve (L'Universalité Algorithmique) :**
Si le modèle cible dispose de ressources suffisantes (notamment une précision arithmétique arbitraire et une mémoire non bornée), il est théoriquement possible de conserver la Turing-complétude. Le réseau neuronal pourra alors mimer la fonction de transition $\delta$ et la manipulation du ruban. L'intention algorithmique, la logique sous-jacente du calcul, survit à la traduction.

**Ce qui se perd (La Localité, la Linéarité et l'Exactitude Symbolique) :**
La traduction vers le neuronal impose des pertes structurelles profondes.
1. **La perte de la localité explicite :** Dans une machine de Turing, l'état $q$ et le symbole lu $a$ sont des entités discrètes et séparables. Dans un réseau de neurones, l'état et le symbole seront encodés dans un vecteur de haute dimension, distribué et superposé. L'interprétabilité humaine de l'état interne s'effondre.
2. **La perte de l'exactitude symbolique (Le coût de la précision) :** C'est le point de bascule de notre livre. Pour qu'un réseau récurrent simule le déplacement de la tête de lecture et la croissance du ruban, il doit encoder des positions et des valeurs dans ses poids et ses activations. Comme nous le démontrerons au Chapitre 6 avec les travaux de Siegelmann et Sontag (1995), cette simulation exige une précision arithmétique qui croît indéfiniment. Dès que l'on restreint cette précision aux limites du monde physique (précision finie ou logarithmique), la traduction s'effondre : le réseau perd sa Turing-complétude et dégénère en un simple automate fini ou en un circuit de faible profondeur.
3. **La perte du déterminisme strict :** Bien que les machines de Turing déterministes soient notre étalon, les implémentations neuronales introduisent souvent du bruit, des approximations non-linéaires et des dynamiques chaotiques qui rendent la trajectoire de calcul sensible aux conditions initiales d'une manière que le modèle symbolique ignore.

La machine de Turing n'est pas seulement un point de départ historique ; elle est le miroir dans lequel les architectures neuronales modernes doivent se regarder pour révéler leurs propres limites. En comprenant exactement ce que l'étalon symbolique possède en abondance (temps séquentiel, précision infinie, exactitude discrète) et ce qu'il lui manque (parallélisme, accès direct, robustesse au bruit), nous sommes désormais armés pour explorer les modèles cibles.

Le ruban infini est déroulé. La tête de lecture est en position. Il est temps d'observer comment les automates finis et les circuits booléens vont venir complexifier notre compréhension des ressources computationnelles, avant d'aborder le grand saut vers le calcul neuronal.