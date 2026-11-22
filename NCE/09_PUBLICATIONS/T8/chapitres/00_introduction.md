## Introduction

### Le grand malentendu : deux modèles, deux ontologies

Il existe en informatique théorique un grand malentendu, une fracture silencieuse qui sépare deux manières fondamentales de concevoir le calcul. D'un côté, nous avons le lambda-calcul, introduit par Church 1936 pour formaliser la calculabilité effective. C'est un monde de symboles discrets, de règles de réduction exactes, de fonctions traitées comme des valeurs de première classe et de substitutions structurelles. C'est le règne de l'ordre supérieur, où un programme peut non seulement manipuler des données, mais aussi engendrer et consommer d'autres programmes. La sémantique de ce monde, magistralement établie par Barendregt 1984, repose sur la confluence et la normalisation : le calcul y est une réécriture déterministe et transparente.

De l'autre côté, nous avons le réseau de neurones, dont les fondations logiques et biologiques remontent à McCulloch et Pitts 1943. C'est un monde continu, statistique, gouverné par l'approximation, les gradients et les espaces vectoriels de haute dimension. L'apprentissage profond moderne, tel que synthétisé par Goodfellow, Bengio et Courville 2016, a démontré la capacité phénoménale de ces architectures à extraire des représentations à partir de données massives, mais au prix d'une opacité structurelle et d'une imprécision inhérente aux représentations flottantes.

Depuis des décennies, le rêve de l'intelligence artificielle neuro-symbolique est de jeter un pont direct entre ces deux rives. L'idée, séduisante mais périlleuse, serait qu'un réseau de neurones puisse *nativement* et *efficacement* évaluer un terme du lambda-calcul, apprenant par lui-même la mécanique de la réduction et de la liaison des variables. Face à cette ambition, la thèse centrale de ce livre est sans appel : à ce jour, aucune traduction directe efficace du lambda-calcul vers les réseaux de neurones n'est connue. Ce tome affirme ce statut **OUVERT**. Nous ne revendiquons aucune découverte miraculeuse, ni ne prétendons démontrer une impossibilité absolue ; nous constatons et formalisons l'absence d'une telle route directe dans le cadre des ressources bornées.

### La route indirecte et la facture en ressources

Puisque la route directe est, en l'état de nos connaissances, une impasse ou du moins un mystère **OUVERT**, quelle est la seule voie rigoureuse dont nous disposons ? C'est la route indirecte, ou route composée. Pour qu'un réseau de neurones simule un calcul d'ordre supérieur, il ne faut pas lui donner le terme brut à digérer. Il faut d'abord traduire le terme en une machine abstraite intermédiaire — spécifiquement, une machine à environnements —, puis traduire les états et les transitions de cette machine vers un réseau récurrent.

Cette route composée fonctionne. Elle est mathématiquement valide. Mais la question qui anime ce livre n'est pas seulement de savoir *si* cela fonctionne, mais de savoir *ce que cela coûte*. C'est ici qu'intervient le concept de « facture en ressources ». Dans le programme des Traductions à ressources et du calcul (RTC), nous ne nous contentons pas de la complétude calculatoire. Savoir qu'un modèle peut simuler un autre est un résultat **CONNU** depuis les travaux fondateurs sur la puissance de calcul des réseaux (Siegelmann et Sontag 1995 ; Pérez, Marinković et Barceló 2019). Mais la complétude est une notion asymptotique, gratuite, qui ignore la réalité physique et matérielle du calcul.

Notre démarche consiste à chiffrer la traduction ressource par ressource : la taille du réseau, le temps d'inférence, la mémoire, la profondeur, la largeur, la précision numérique, et le partage des sous-termes. Pour chaque traduction, nous donnons son sens, son coût, ce qui est conservé et ce qui est irrémédiablement perdu.

Il est important de préciser d'emblée que la « facture » et la « comptabilité » dont il sera question ici ne concernent que les ressources computationnelles abstraites et physiques (temps, espace, précision) et n'ont aucun lien avec la finance, l'investissement ou la monnaie ; ce livre est un traité d'informatique théorique, et son contenu est purement informatif et scientifique.

### Le résultat majeur : la précision comme mémoire déguisée

Au terme de cette comptabilité impitoyable, un résultat émerge, qui constitue le cœur analytique de cet ouvrage. Lorsque l'on traduit une machine à environnements (qui nécessite une pile potentiellement non bornée pour sauvegarder les contextes d'évaluation) vers un réseau récurrent de dimension fixe, le poste dominant de la facture n'est ni la taille du réseau ni le temps de calcul. Le poste dominant, c'est la *précision numérique*.

Dans un espace vectoriel de dimension fixe, la seule manière d'encoder une quantité arbitraire d'information discrète (comme une pile d'environnements) est d'utiliser les décimales des nombres réels qui composent les activations des neurones. La précision fonctionne donc comme une mémoire déguisée. Ce résultat est **PROUVÉ** pour les bornes élémentaires établies dans ce livre : pour simuler $n$ étapes de calcul nécessitant une pile de profondeur $n$, la précision requise sur les poids et les activations croît de manière exponentielle ou polynomiale stricte selon l'encodage, rendant la simulation physiquement irréalisable sur du matériel flottant standard (IEEE 754) au-delà de quelques dizaines d'étapes.

À l'inverse, les ressources les plus mal conservées lors de cette traduction sont le partage (la capacité à référencer un même sous-terme en mémoire sans le dupliquer) et la liaison des variables. Le réseau de neurones, par sa nature de somme pondérée continue, dilue la structure de graphe acyclique dirigé qui sous-tend le partage dans le lambda-calcul.

### L'analogie de l'attention et la fin du folklore

Il est impossible d'aborder la traduction entre le calcul symbolique et le calcul neuronal sans affronter le folklore contemporain entourant les mécanismes d'attention. Depuis les travaux séminaux de Vaswani et al. 2017, une intuition s'est répandue dans la communauté : l'attention serait une forme de « substitution douce », une manière pour le réseau de neurones d'aller chercher des valeurs dans un contexte, mimant ainsi la substitution $M[x := N]$ du lambda-calcul.

Ce livre prend le contre-pied de cette enthousiasme non formalisé. L'attention comme substitution reste une stricte ANALOGIE. Nous la formalisons en une **CONJECTURE** testable, délimitant exactement les cas où un mécanisme d'attention par produit scalaire peut approximer une lookup table discrète. Mais nous accompagnons cette conjecture de séparations **PROUVÉES** et de contre-exemples explicites montrant que les formulations trop fortes sont **RÉFUTÉES**. L'attention ne préserve pas la compositionnalité exacte des termes ; elle opère une interpolation continue qui détruit la sémantique de l'ordre supérieur dès que la profondeur de liaison dépasse un certain seuil. Jamais l'attention n'est présentée comme un résultat de traduction exacte.

### Le registre des statuts : une épistémologie de la traduction

Pour naviguer dans ce champ miné par les intuitions non vérifiées et les annonces prématurées, ce livre impose un cadre conceptuel strict : le registre des statuts. Chaque affirmation, chaque lemme, chaque observation empirique porte un statut en tête, garantissant au lecteur une honnêteté intellectuelle totale.

1. **PROUVÉ** : Les résultats démontrés intégralement dans le texte. Il s'agit d'assemblages élémentaires (syntaxe, encodages, comptages, correction de la machine intermédiaire, séparations sur exemples finis). Nous ne cachons aucune étape.
2. **CONNU** : Les grands théorèmes importés (confluence, indécidabilité, normalisation du fragment typé, puissance de calcul des réseaux). Pour ceux-ci, nous donnons l'idée de la preuve, en le disant explicitement, sans prétendre réinventer la roue.
3. **EXPÉRIMENTAL** : Les mesures sur poids appris, les observations de convergence ou de divergence lors de la simulation de petites machines sur des architectures réelles.
4. **CONJECTURE** : Les analogies formalisables mais non encore démontrées dans le cas général, comme le lien entre attention et substitution.
5. **RÉFUTÉ** : Les affirmations trop fortes, souvent issues du folklore, que nous invalidons par un contre-exemple explicite et constructif.
6. **OUVERT** : Les questions fondamentales, comme l'existence d'une traduction directe et efficace, que nous laissons en l'état, sans forcer de conclusion.

Ce registre est notre boussole. Il interdit de présenter une intuition comme une preuve, et bannit toute annonce de découverte là où il n'y a qu'une clarification de bornes.

### À qui s'adresse ce livre ?

Ce livre est écrit pour le lecteur cultivé non spécialiste : l'informaticien curieux des fondations de l'IA, le mathématicien s'interrogeant sur la nature du calcul continu, le chercheur en apprentissage automatique cherchant à comprendre les limites structurelles de ses modèles, et l'étudiant désireux de voir comment la sémantique formelle rencontre l'algèbre linéaire.

Pour servir ce public, chaque chapitre suit une pédagogie immuable :
*   **Intuition** : Une métaphore ou une observation phénoménologique pour ancrer le concept.
*   **Définition** : La formalisation mathématique rigoureuse, mais accessible.
*   **Énoncé** : Le théorème ou la propriété, toujours coiffé de son statut.
*   **Exemple** : Une instanciation concrète, souvent sur des termes lambda minimaux ou des petits réseaux.
*   **Exercice** : En fin de chapitre, pour que le lecteur s'approprie la comptabilité des ressources.

Les types, compris à la suite de Howard 1980 et de Pierce 2002 comme des contrats de ressources et des formules, y jouent un rôle central : ils délimitent le fragment où tout est fini, où la normalisation est garantie, et où la facture en ressources devient bornée et prédictible.

### Annonce du plan

L'ouvrage est structuré en quatre parties et seize chapitres, conçus comme une progression logique de la représentation vers la simulation, puis vers l'analyse critique et le transfert.

**Partie I — Deux modèles, deux économies, un protocole de traduction**
Cette partie plante le décor et définit le vocabulaire commun.
Le *Chapitre 1* explore le lambda-calcul non pas comme une simple syntaxe, mais comme un modèle à ressources, où la substitution a un coût et où le partage est une optimisation vitale.
Le *Chapitre 2* fait de même pour le réseau de neurones, en analysant l'économie de la continuité, de la largeur et de la précision.
Le *Chapitre 3* introduit le protocole RTC et le registre des statuts, définissant ce qu'est une traduction rigoureuse.
Le *Chapitre 4* dresse un panorama des résultats disponibles dans la littérature, en explicitant leurs hypothèses souvent cachées.

**Partie II — Représenter : termes, liaisons, partage et types dans un espace vectoriel**
Ici, nous attaquons le premier versant de la route indirecte : comment encoder le discret dans le continu.
Le *Chapitre 5* détaille l'encodage de la syntaxe, des arbres et des indices de liaison (notation de De Bruijn) en vecteurs.
Le *Chapitre 6* s'attaque au problème épineux du partage : comment passer d'un graphe à un vecteur, et ce qui s'y perd irrémédiablement.
Le *Chapitre 7* aborde l'ordre supérieur : la représentation des fermetures (closures), des environnements, et des fonctions traitées comme valeurs.
Le *Chapitre 8* introduit les types comme contrats de ressources, isolant un fragment où la finitude des structures permet une comptabilité exacte.

**Partie III — Simuler : la machine intermédiaire, la traduction composée et le chemin inverse**
C'est le cœur technique de l'ouvrage.
Le *Chapitre 9* construit une machine à environnements pour le lambda-calcul, évitant l'explosion combinatoire de la substitution pure.
Le *Chapitre 10* opère la traduction de cette machine vers un réseau récurrent, en posant les hypothèses explicites de cette simulation.
Le *Chapitre 11* présente la facture de cette traduction composée, démontrant le rôle de la précision comme mémoire et chiffrant la perte du partage.
Le *Chapitre 12* explore le chemin inverse, souvent négligé : comment extraire des termes symboliques à partir des états continus d'un réseau, et les limites de cette extraction.

**Partie IV — Analogies, obstacles, mesures et transfert au programme RTC**
La dernière partie prend de la hauteur, confronte les mythes contemporains et prépare l'avenir.
Le *Chapitre 13* dissèque l'anatomie de l'analogie entre attention et substitution, séparant le mythe de la conjecture testable.
Le *Chapitre 14* cartographie les obstacles à une traduction directe, clarifiant ce qui est **OUVERT** et ce qui est **RÉFUTÉ**.
Le *Chapitre 15* propose un protocole expérimental pour mesurer une traduction sans la survendre, offrant une méthodologie pour les chercheurs en IA.
Enfin, le *Chapitre 16* opère le transfert vers le programme RTC, synthétisant ce que ce tome apporte à l'étude des traductions à ressources : quelles ressources compter, quelles traductions privilégier, et quelles questions ouvertes léguer à la communauté.

### Conclusion de l'introduction

La route qui mène du lambda-calcul aux réseaux de neurones n'est pas une autoroute directe. C'est un chemin de traverse, escarpé, qui oblige à passer par la mécanique des machines abstraites et à payer, à chaque étape, une facture en ressources que l'on ne peut plus se permettre d'ignorer. En acceptant que la traduction directe efficace reste un problème **OUVERT**, nous nous libérons de l'obligation de produire des miracles pour nous concentrer sur l'ingénierie rigoureuse de ce qui est possible aujourd'hui.

Ce livre est une invitation à regarder sous le capot du calcul neuronal, non pas avec le cynisme de celui qui rejette l'approximation, mais avec la rigueur du comptable qui sait que chaque décimale de précision est une parcelle de mémoire, et que chaque liaison de variable est un pont fragile entre deux mondes. Commençons, sans plus tarder, par examiner la première de ces deux économies : celle du lambda-calcul.

## Chapitre 1 – Le lambda-calcul comme modèle à ressources

### 1.1 Intuition : Le calcul comme réécriture et consommation

Lorsque l'on découvre le lambda-calcul pour la première fois, on est souvent frappé par sa pureté. C'est un monde de symboles, de règles élégantes et de théorèmes intemporels. Dans les manuels, la réduction d'un terme est présentée comme une simple égalité mathématique, une évidence logique qui se déploie sur le papier sans effort. Mais cette vision, héritée de la logique formelle, masque une réalité fondamentale que nous devons affronter d'emblée dans le cadre du programme RTC (Traductions à ressources et calcul) : le calcul n'est pas seulement une vérité abstraite, c'est un processus physique qui consomme de l'espace et du temps.

Pour comprendre cette shift de perspective, imaginons un atelier de reliure. Vous disposez d'un manuel d'instructions (le programme) et de pages vierges (la mémoire). Lorsque l'instruction dit « copiez le chapitre A à l'intérieur de chaque section du chapitre B », vous ne vous contentez pas de noter une référence abstraite ; vous devez physiquement photocopier les pages, les assembler, et occuper de l'espace sur votre établi. Si le chapitre A fait cent pages et que le chapitre B contient dix emplacements, vous venez de générer mille pages de papier.

Le lambda-calcul, introduit par Church 1936 pour fonder la calculabilité, est exactement cet atelier. La règle centrale de ce modèle, la $\beta$-réduction, est l'acte de substitution. Elle nous dit que l'application d'une fonction à un argument consiste à remplacer toutes les occurrences de la variable formelle par cet argument. Mais *remplacer* n'est pas un concept gratuit. C'est une opération de duplication, de routage et de réécriture qui a une facture. Dans ce chapitre, je vous propose de cesser de regarder le lambda-calcul comme le philosophe qui contemple la vérité, pour l'observer comme l'ingénieur qui doit payer la facture de l'encre et du papier. Nous allons y définir ce qu'est une ressource syntaxique, et pourquoi la structure même de ce modèle cache des pièges exponentiels que toute traduction vers un autre modèle de calcul devra assumer.

### 1.2 Définition : Syntaxe, substitution et complexité structurelle

Avant de pouvoir compter, il faut définir ce que l'on compte. La syntaxe du lambda-calcul pur, telle que consolidée par Barendregt 1984, est d'une minimalisme redoutable. Elle ne repose que sur trois constructions. Soit $V$ un ensemble infini dénombrable de variables. L'ensemble des $\lambda$-termes, noté $\Lambda$, est défini inductivement par la grammaire suivante :

$$ M, N ::= x \mid (\lambda x. M) \mid (M N) $$

où $x \in V$.
1. **Variable** ($x$) : la ressource atomique, le nom d'un fil.
2. **Abstraction** ($\lambda x. M$) : la création d'une fonction, qui lie la variable $x$ dans le corps $M$. C'est la promesse d'un calcul futur.
3. **Application** ($M N$) : l'acte de calcul lui-même, où le terme $M$ est appliqué au terme $N$.

À cette syntaxe s'ajoute la notion de variables libres et liées. Une variable est *liée* si elle se trouve sous le scope d'un $\lambda$ qui la nomme ; elle est *libre* sinon. La mécanique du calcul repose sur la substitution, notée $M[x := N]$, qui remplace toutes les occurrences libres de $x$ dans $M$ par le terme $N$. Pour éviter le problème bien connu de la capture de variable (où une variable libre de $N$ se retrouverait accidentellement liée par un $\lambda$ dans $M$), on s'appuie sur l'$\alpha$-conversion, qui permet de renommer les variables liées de manière transparente. La règle de calcul fondamentale, la $\beta$-réduction, s'écrit alors :

$$ (\lambda x. M) N \rightarrow_\beta M[x := N] $$

Pour transformer ce modèle logique en modèle à ressources, nous devons lui adjoindre une métrique de coût. La mesure la plus immédiate est la **taille syntaxique** d'un terme, notée $|M|$, qui correspond au nombre de nœuds dans son arbre de syntaxe abstraite (AST). Elle se définit récursivement ainsi :

*   $|x| = 1$
*   $|\lambda x. M| = 1 + |M|$
*   $|M N| = 1 + |M| + |N|$

Cette définition de la taille est cruciale. Elle postule que le lambda-calcul, dans sa définition originelle, est une structure arborescente. Chaque fois qu'un sous-terme est utilisé à deux endroits différents, il est physiquement dupliqué dans l'arbre. C'est cette hypothèse structurelle, souvent invisible, qui va dicter la facture de nos traductions.

### 1.3 Énoncé : La non-gratuité de la substitution et l'explosion exponentielle

Dans la littérature classique, on s'émerveille souvent de la confluence du lambda-calcul (le théorème de Church-Rosser), qui garantit que si un terme peut se réduire de plusieurs manières, toutes les voies mènent au même résultat final. C'est un résultat **CONNU**, dont l'idée de preuve repose sur la propriété du diamant et les réductions parallèles. Mais la confluence ne dit rien sur le *coût* du chemin parcouru.

Ce que nous devons établir ici, c'est que la $\beta$-réduction, lorsqu'elle est opérée sur une représentation arborescente stricte, n'est pas une opération à coût borné. Elle peut engendrer une explosion de la taille du terme.

**Énoncé 1.1 (Statut : PROUVÉ)**
*Il existe une famille de termes $E_n$ telle que la taille du terme initial non réduit $|E_n|$ croît de manière linéaire par rapport à $n$ ($O(n)$), tandis que la taille de sa forme normale (le terme entièrement réduit) $|E_n^*|$ croît de manière exponentielle ($O(2^n)$).*

**Preuve complète :**
Construisons cette famille de termes. Soit $z$ une variable fixe. Définissons le terme duplicateur $D = \lambda x. x x$. Sa taille est $|D| = 1 + |x x| = 1 + (1 + 1 + 1) = 4$.
Définissons maintenant la suite de termes $(E_n)_{n \geq 0}$ par récurrence :
*   $E_0 = z$
*   $E_{n+1} = D E_n = (\lambda x. x x) E_n$

Calculons d'abord la taille du terme *avant* toute réduction, c'est-à-dire la taille de l'expression $E_n$ telle qu'elle est écrite :
*   $|E_0| = |z| = 1$
*   $|E_{n+1}| = |D E_n| = 1 + |D| + |E_n| = 5 + |E_n|$
Par une récurrence triviale, on obtient $|E_n| = 5n + 1$. La taille de l'entrée est donc strictement linéaire, $O(n)$.

Observons maintenant ce qui se passe lorsque nous exécutons le calcul, c'est-à-dire lorsque nous appliquons la $\beta$-réduction jusqu'à obtenir la forme normale $E_n^*$.
*   Pour $n=0$ : $E_0^* = z$, de taille $|E_0^*| = 1$.
*   Pour $n=1$ : $E_1 = (\lambda x. x x) z \rightarrow_\beta z z$. Donc $E_1^* = z z$, de taille $|E_1^*| = 1 + 1 + 1 = 3$.
*   Pour $n=2$ : $E_2 = (\lambda x. x x) (z z) \rightarrow_\beta (z z) (z z)$. Donc $E_2^* = (z z) (z z)$, de taille $|E_2^*| = 1 + 3 + 3 = 7$.

Posons $S_n = |E_n^*|$. La règle de réduction $E_{n+1} \rightarrow_\beta E_n^* E_n^*$ nous donne la relation de récurrence sur la taille de la forme normale :
$S_{n+1} = 1 + S_n + S_n = 2S_n + 1$.
Avec $S_0 = 1$, la solution de cette récurrence est $S_n = 2^{n+1} - 1$.

**Conclusion de la preuve :** Le terme initial nécessite un espace mémoire proportionnel à $5n + 1$ pour être stocké. Son évaluation complète nécessite un espace mémoire proportionnel à $2^{n+1} - 1$. Pour $n = 30$, l'entrée tient en 151 nœuds, mais le résultat exige plus de 2 milliards de nœuds. La substitution arborescente a un coût exponentiel. $\blacksquare$

### 1.4 Exemple : Le partage, ou la survie face à l'explosion

L'exemple précédent pourrait laisser croire que le lambda-calcul est un modèle de calcul intrinsèquement inefficace. C'est faux. L'inefficacité ne réside pas dans le modèle, mais dans la représentation arborescente stricte que nous avons choisie pour mesurer sa taille.

Reprenons notre terme $E_3$, dont la forme normale arborescente est :
$$ (((z z) (z z)) ((z z) (z z))) (((z z) (z z)) ((z z) (z z))) $$
Cet arbre contient 15 nœuds d'application et 16 feuilles $z$. Pourtant, l'information contenue dans ce terme est minime : c'est juste l'instruction de dupliquer $z$ trois fois de suite.

Pour survivre à l'explosion exponentielle, les implémentations réelles des langages fonctionnels n'utilisent pas des arbres, mais des **graphes orientés acycliques (DAG)**, voire des graphes avec cycles pour la récursion. C'est ce qu'on appelle le **partage** (sharing). Au lieu de copier le sous-terme lors de la substitution $M[x := N]$, on se contente de créer un pointeur vers l'unique exemplaire de $N$ en mémoire.

Dans une représentation DAG, la forme normale de $E_n$ ne nécessite que $n+1$ nœuds uniques :
*   Nœud 0 : la feuille $z$
*   Nœud 1 : l'application du Nœud 0 au Nœud 0
*   Nœud 2 : l'application du Nœud 1 au Nœud 1
*   ...
*   Nœud $n$ : l'application du Nœud $n-1$ au Nœud $n-1$.

Le partage transforme une complexité spatiale exponentielle en une complexité spatiale linéaire. C'est une optimisation vitale. Mais pour le programme RTC, cette optimisation est un cauchemar de traduction. Pourquoi ? Parce que le partage repose sur la notion d'identité mémoire et de pointeur. Deux sous-termes qui sont structurellement identiques mais créés indépendamment ne doivent pas être confondus avec deux sous-termes qui partagent la même adresse mémoire.

Lorsque nous traduirons ces structures vers des réseaux de neurones (Goodfellow, Bengio et Courville 2016), nous verrons que l'espace vectoriel continu ne possède pas de notion native de « pointeur » ou d'« adresse mémoire ». Un réseau de neurones manipule des densités et des interpolations, pas des graphes de pointeurs discrets. La perte du partage lors de la traduction sera l'une des factures les plus lourdes que nous aurons à payer.

### 1.5 La liaison des variables : le fil invisible de l'ordre supérieur

La seconde ressource fondamentale du lambda-calcul, après la taille des termes, est la gestion de la liaison des variables (variable binding). C'est ce qui confère au modèle sa puissance d'ordre supérieur : la capacité de traiter les fonctions comme des valeurs, de les passer en argument et de les retourner comme résultats.

Lorsque vous évaluez l'expression $(\lambda f. f z) (\lambda x. x)$, la variable $f$ est temporairement liée à la fonction identité. Mais que se passe-t-il si cette fonction identité est capturée, stockée dans une structure de données, et ressortie cent étapes plus loin, dans un contexte où la variable $x$ a déjà une tout autre signification ?

Pour garantir la correction du calcul, le lambda-calcul exige que la liaison soit préservée par-dessus tout. C'est le rôle de l'$\alpha$-conversion et, dans les implémentations modernes, de l'utilisation des indices de De Bruijn, qui remplacent les noms de variables par des entiers indiquant la distance au $\lambda$ lieur. Par exemple, $\lambda x. \lambda y. x y$ s'écrit $\lambda \lambda 1 0$ avec les indices de De Bruijn.

Cette translation des noms vers des indices résout le problème de la capture, mais elle ne supprime pas le coût de la liaison. Chaque fois qu'une fermeture (closure) est créée, il faut capturer son environnement. Chaque fois qu'elle est appliquée, il faut restaurer cet environnement. Howard 1980, dans sa correspondance de Curry-Howard, a montré que les programmes sont des preuves et que l'évaluation est l'élimination des coupures. Mais éliminer une coupure en présence de liaisons dynamiques exige de router l'information à travers le graphe de calcul de manière non locale.

Dans une machine de Turing, le ruban est plat, la tête de lecture est locale. Dans le lambda-calcul, l'application d'une fonction peut instantanément « téléporter » un terme profondément imbriqué à un autre endroit de l'expression, en exigeant que toutes ses liaisons internes restent cohérentes avec son point de création, et non son point d'utilisation. Cette non-localité structurelle est la signature de l'ordre supérieur. C'est également la raison principale pour laquelle l'existence d'une traduction directe et efficace vers les réseaux de neurones récurrents standard reste, à ce jour, un problème **OUVERT**. Les poids d'un réseau de neurones (McCulloch et Pitts 1943) sont statiques une fois l'apprentissage terminé ; ils peinent à router dynamiquement des liaisons de variables dont la topologie change à chaque étape d'inférence.

### 1.6 Exercices de fin de chapitre

Pour ancrer ces concepts et vous familiariser avec la comptabilité des ressources, je vous invite à résoudre les exercices suivants. Ils ne nécessitent pas d'outils mathématiques avancés, mais une attention rigoureuse à la structure des termes.

**Exercice 1 : Comptabilité de la duplication**
Soit le terme $M = \lambda x. \lambda y. x y y$.
1. Calculez la taille $|M|$ selon la métrique arborescente définie en section 1.2.
2. Soit $N$ un terme de taille $S$. Calculez la taille du terme $M N$ avant réduction, puis la taille de sa forme normale après une étape de $\beta$-réduction.
3. Exprimez le facteur de croissance de la taille en fonction de $S$. Que constatez-vous lorsque $S$ devient grand ?

**Exercice 2 : Topologie du partage**
Considérez le terme des entiers de Church, où l'entier $n$ est encodé par $c_n = \lambda f. \lambda x. f (f (... (f x)...))$ avec $n$ applications de $f$.
1. Dessinez l'arbre de syntaxe abstraite de $c_3$. Combien de nœuds contient-il ?
2. Représentez $c_3$ sous forme de graphe orienté acyclique (DAG) en factorisant les sous-termes identiques. Combien de nœuds uniques le DAG contient-il ?
3. Généralisez pour $c_n$ : donnez la complexité spatiale de l'arbre et celle du DAG en fonction de $n$.

**Exercice 3 : Réflexion sur le statut de la sémantique**
La confluence du lambda-calcul garantit que l'ordre d'évaluation ne change pas le résultat final (s'il existe). Cependant, l'Énoncé 1.1 montre que la taille du terme intermédiaire peut varier drastiquement selon la stratégie de réduction (par exemple, réduction de l'argument le plus à gauche vs réduction de l'application la plus à l'extérieur).
En vous appuyant sur le registre des statuts du livre, formulez en une phrase pourquoi l'affirmation « le lambda-calcul est un modèle de calcul indépendant de la machine » doit être nuancée lorsqu'on s'intéresse aux ressources bornées. Quel statut (**CONNU**, **PROUVÉ**, **CONJECTURE**, etc.) donneriez-vous à l'affirmation « toute stratégie de réduction préserve la complexité spatiale polynomiale » ? Justifiez votre réponse par un contre-exemple ou une référence à la section 1.3.