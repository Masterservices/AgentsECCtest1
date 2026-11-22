## Conclusion : Le paysage des traductions à ressources

### Synthèse des apports principaux : Le grand dictionnaire des traductions

Dans ce livre, nous avons entrepris un voyage au cœur de la structure du calcul. Notre point de départ était une intuition simple, mais profondément féconde : les réseaux de neurones artificiels et les circuits booléens, bien qu'issus de traditions historiques et de motivations radicalement différentes, parlent en réalité le même langage fondamental. Ce langage, c'est celui de la computation discrète, et notre objectif a été d'en établir le dictionnaire complet. Mais un dictionnaire ne se contente pas de donner des équivalences sémantiques ; il doit préciser le coût de chaque traduction. C'est tout l'enjeu des traductions à ressources.

Récapitulons les grandes traductions qui ont jalonné notre parcours, en précisant pour chacune son sens, son coût, ce qu'elle conserve, ce qu'elle perd, et son statut dans notre registre.

**Traduction 1 : Des portes logiques aux neurones à seuil.**
- *Sens* : Circuit booléen $\rightarrow$ Réseau de neurones à seuil.
- *Coût* : Taille linéaire, profondeur conservée, largeur conservée. Précision des poids polynomiale.
- *Conservé* : La fonction calculée, la structure topologique profonde.
- *Perdu* : La modularité sémantique des portes (un neurone n'a pas de "nom" logique intrinsèque).
- *Statut* : PROUVÉ. Les travaux fondateurs de McCulloch et Pitts 1943 ont posé cette base, et les bornes sur la taille des poids ont été rigoureusement établies par Håstad 1994.

**Traduction 2 : L'encodage SAT et la transformation de Tseitin.**
- *Sens* : Circuit booléen $\rightarrow$ Formule SAT (Fichier CNF).
- *Coût* : Taille linéaire par rapport au circuit, introduction de variables auxiliaires.
- *Conservé* : La satisfiabilité (équivalence équisatisfiable).
- *Perdu* : L'équivalence logique stricte (à cause des variables de Tseitin).
- *Statut* : CONNU. La transformation de Tseitin 1968 est un pilier de l'ingénierie de la satisfiabilité, magistralement détaillée dans l'ouvrage de Biere, Heule, van Maaren et Walsh 2009.

**Traduction 3 : De la profondeur des circuits à la profondeur des réseaux.**
- *Sens* : Réseau peu profond $\rightarrow$ Réseau profond (ou l'inverse pour simuler).
- *Coût* : Simulation d'un réseau profond par un réseau peu profond exige une taille exponentielle.
- *Conservé* : La capacité d'approximation universelle.
- *Perdu* : L'efficacité structurelle (explosion de la largeur ou de la taille).
- *Statut* : PROUVÉ. Les théorèmes de séparation de profondeur, illustrés par Telgarsky 2016, démontrent que la profondeur est une ressource irremplaçable pour certaines familles de fonctions.

**Traduction 4 : L'extraction de circuits à partir de réseaux entraînés.**
- *Sens* : Réseau de neurones (boîte noire) $\rightarrow$ Circuit booléen explicite.
- *Coût* : Temps exponentiel dans le pire des cas, taille potentiellement exponentielle.
- *Conservé* : Le comportement exact sur le domaine discret.
- *Perdu* : La capacité de généralisation continue, la robustesse aux bruits.
- *Statut* : CONNU et partiellement EXPÉRIMENTAL. L'extraction exacte est coûteuse, mais les méthodes approchées ouvrent des voies d'interprétabilité.

Chacune de ces traductions nous rappelle une règle d'or de l'informatique théorique : il n'y a pas de repas gratuit. Gagner en expressivité ou en compacité dans un modèle se paie inévitablement par une consommation accrue d'une autre ressource dans le modèle cible.

### Le registre des statuts : Ce que nous savons et ce qui nous échappe

Tout au long de ces seize chapitres, nous avons rigoureusement séparé l'intuition de la preuve. Le registre des statuts n'est pas une simple nomenclature ; c'est une boussole épistémologique.

Ce qui est **PROUVÉ** forme le socle de notre édifice. Nous savons, grâce à Hajnal, Maass, Pudlák, Szegedy et Turán 1993, que les circuits à seuil de profondeur bornée possèdent une puissance de calcul remarquable, capable de simuler certaines classes de complexité. Nous savons également, par les résultats de Cook 1971, que la satisfiabilité (SAT) est le pivot central autour duquel gravite toute la complexité structurelle. La borne sur la taille des poids, établie par Håstad 1994, nous garantit qu'un neurone à seuil n'a pas besoin d'une précision infinie pour calculer ce qu'un circuit booléen calcule.

Ce qui est **CONNU** englobe les techniques et les heuristiques qui, sans faire l'objet de théorèmes de séparation profonds, constituent le savoir-faire de la communauté. La transformation de Tseitin 1968 en est l'exemple parfait : elle est universellement utilisée, son coût est parfaitement maîtrisé, et son implémentation est au cœur des solveurs SAT modernes (Biere, Heule, van Maaren et Walsh 2009). De même, la complexité des fonctions booléennes, telle qu'explorée par Jukna 2012, nous fournit des bornes inférieures solides pour évaluer la difficulté intrinsèque de certains calculs. Les limites du perceptron, mises en évidence par Minsky et Papert 1969, restent un avertissement CONNU sur les limites de la largeur sans profondeur.

Ce qui relève de la **CONJECTURE** ou de ce qui reste **OUVERT** est tout aussi fascinant. La frontière exacte entre ce qu'un réseau de neurones à seuil de profondeur deux peut calculer efficacement par rapport à un réseau de profondeur trois reste, pour de nombreuses classes de fonctions naturelles, une question ouverte. De plus, le passage des réseaux à seuil (notre modèle théorique) aux réseaux à activations continues utilisés en pratique soulève des questions de traduction qui n'ont pas encore trouvé de réponse exhaustive.

Enfin, nous avons croisé des résultats **EXPÉRIMENTAUX**, notamment lorsque nous avons abordé l'élagage de réseaux entraînés ou l'extraction de circuits. Ici, la théorie précède souvent la pratique, ou inversement, et le statut de ces affirmations évolue au gré des avancées empiriques.

### Transfert vers le programme RTC

Ce livre n'est pas seulement un traité de correspondances mathématiques ; il est une contribution au programme plus vaste des Traductions à Ressources, que nous nommons ici le programme RTC (Ressources, Traductions, Complexité). Qu'apporte ce tome à l'étude globale des traductions à ressources ?

Premièrement, il consolide le **vocabulaire des ressources**. En circulant entre les circuits booléens, les formules SAT et les réseaux de neurones, nous avons dû unifier les métriques. La "taille" d'un circuit (nombre de portes) devient la "largeur" d'un réseau (nombre de neurones par couche) ou le "nombre de clauses" d'une formule SAT. La "profondeur" d'un circuit devient le "nombre de couches cachées" d'un réseau ou la "longueur de dérivation" dans un solveur SAT. Le programme RTC exige cette discipline métrologique : on ne peut comparer des modèles que si l'on mesure leurs ressources avec la même toise.

Deuxièmement, ce tome met en lumière le rôle crucial de la **précision** comme ressource à part entière. Trop souvent, la complexité algorithmique se concentre sur le temps et l'espace. Or, les travaux de Håstad 1994 sur les portes à seuil, et plus récemment les analyses de Merrill et Sabharwal 2023 sur les transformeurs à précision logarithmique, montrent que la précision des poids (ou des activations) est une ressource limitante. Le programme RTC intègre désormais la précision numérique dans son inventaire des coûts de traduction. Passer d'un modèle continu à un modèle discret, ou d'un réseau haute précision à un réseau quantifié, a un coût structurel qui doit être borné.

Troisièmement, nous avons démontré l'utilité du **partage** (ou *sharing*) comme ressource transversale. Dans un circuit booléen, le partage de sous-expressions (un graphe acyclique dirigé plutôt qu'un arbre) réduit drastiquement la taille. Dans un réseau de neurones, le partage des poids joue un rôle analogue. Dans les preuves de résolution pour SAT, le partage de lemmes est la clé de l'efficacité. Le programme RTC identifie le partage comme le mécanisme universel de compression structurelle, et toute traduction entre modèles doit spécifier comment le partage est préservé ou détruit.

En définitive, ce tome ancre le programme RTC dans la matérialité du calcul. Il montre que les modèles ne sont pas de pures abstractions, mais des architectures contraintes par des ressources physiques et logiques.

### Perspectives et questions ouvertes

Si nous avons clos notre étude sur les réseaux à seuil et les circuits booléens, le paysage de l'intelligence artificielle et de la complexité continue d'évoluer. Quelles perspectives s'ouvrent à l'issue de cette lecture ?

La première perspective concerne l'architecture des grands modèles de langage et le parallélisme. Bien que leur mécanisme d'attention semble éloigné de la simple porte à seuil, les travaux de Merrill et Sabharwal 2023 rappellent à l'ordre la théorie de la complexité : sous des contraintes de précision (par exemple, précision logarithmique), le parallélisme massif des transformeurs trouve ses limites structurelles. Traduire un transformeur en circuit booléen de profondeur bornée, en tenant compte de la précision finie des représentations, est le prochain grand chantier du programme RTC. Le statut de la puissance exacte de ces architectures massivement parallèles sous précision bornée reste largement OUVERT.

La deuxième perspective est celle de l'interprétabilité par la traduction. Nous avons vu que l'extraction d'un circuit à partir d'un réseau entraîné est coûteuse. Cependant, dans des domaines critiques, la capacité d'extraire un sous-circuit booléen vérifiable à partir d'une portion d'un réseau de neurones pourrait devenir une exigence. Le défi est de concevoir des traductions qui ne soient pas exactes sur tout le domaine, mais qui soient *localement fidèles* et *globalement vérifiables*. C'est une question où le statut passe de CONNU à EXPÉRIMENTAL, et où la théorie de la complexité (Jukna 2012) devra fournir de nouvelles bornes inférieures pour l'approximation locale.

La troisième perspective touche à la nature même de l'apprentissage. Un circuit booléen est conçu ; un réseau de neurones est entraîné. La traduction que nous avons étudiée est principalement structurelle (une fois le réseau figé). Mais que se passe-t-il si l'on traduit le *processus d'apprentissage* lui-même ? Peut-on encoder la dynamique d'optimisation comme un circuit booléen massif, et en déduire des bornes sur la complexité de l'apprentissage ? Ici, nous touchons aux limites de notre cadre actuel : la traduction de la dynamique d'optimisation reste une CONJECTURE majeure, à la frontière entre l'informatique théorique et la physique statistique.

### Exercice de synthèse : Penser en traducteur

Avant de nous quitter, je vous propose un dernier exercice, non pas pour tester vos connaissances, mais pour aiguiser votre regard.

*Exercice.* Imaginez que vous deviez concevoir un système de décision automatisé. Vous disposez d'un réseau de neurones profond, entraîné sur des millions d'exemples, qui offre une excellente précision statistique mais aucune explicabilité. Vous disposez également d'un moteur de règles booléennes, rapide, vérifiable par SAT, mais rigide.
En utilisant le cadre des traductions à ressources, formulez le problème.
1. Quelle traduction choisissez-vous ? (Réseau $\rightarrow$ Circuit, ou Circuit $\rightarrow$ Réseau ?)
2. Quelles ressources êtes-vous prêt à sacrifier ? (Taille du circuit extrait, ou précision statistique du réseau ?)
3. Quel est le statut de votre approche actuelle ? (Est-ce PROUVÉ que le circuit extrait généralisera, ou est-ce seulement EXPÉRIMENTAL ?)

Cet exercice n'a pas de réponse unique. Il vise simplement à vous faire adopter le réflexe du traducteur : face à deux paradigmes de calcul, ne pas chercher lequel est "meilleur" dans l'absolu, mais lequel est le plus adapté à la contrainte de ressource qui vous étreint.

### Mot final au lecteur

Nous arrivons au terme de ce voyage. Lorsque j'ai commencé à structurer les idées qui ont donné naissance à ce livre, j'étais frappé par le fossé apparent entre la communauté de la complexité booléenne et celle de l'apprentissage profond. D'un côté, des chercheurs traquant la moindre porte logique, obsédés par les bornes inférieures et la profondeur des circuits. De l'autre, des ingénieurs empilant des millions de neurones, guidés par l'intuition, le gradient et la puissance de calcul brute.

Pourtant, en grattant la surface, la roche est la même. Le neurone de McCulloch et Pitts 1943 est la porte à seuil de Minsky et Papert 1969. La dérivation de Tseitin 1968 est l'ancêtre de la vérification formelle des réseaux de neurones modernes. Les théorèmes de Hajnal, Maass, Pudlák, Szegedy et Turán 1993 sur les circuits de profondeur bornée résonnent étrangement avec les avantages de la profondeur démontrés par Telgarsky 2016.

Ce livre est une invitation à l'unité. Il vous invite à ne plus voir les modèles de calcul comme des îles isolées, mais comme des continents reliés par des ponts souterrains. Chaque fois que vous lirez un article sur une nouvelle architecture de réseau de neurones, demandez-vous : quel est le circuit booléen qui se cache derrière ? Quel en est le coût en largeur, en profondeur, en précision ? Chaque fois que vous étudierez un algorithme de satisfiabilité, demandez-vous : quel réseau de neurones pourrait approximer cette heuristique de branchement ?

La beauté de l'informatique théorique réside dans cette capacité à révéler l'invisible. Les ressources — taille, profondeur, largeur, précision — sont les lois de la physique de l'information. Elles s'imposent à nous, que nous le voulions ou non. Les ignorer conduit à des systèmes opaques et inefficaces ; les comprendre et les maîtriser ouvre la voie à une ingénierie du calcul raisonnée, sobre et profonde.

J'espère que ce livre vous aura non seulement transmis des connaissances, mais surtout une méthode : celle du registre des statuts et de la comptabilité rigoureuse des ressources. Le programme RTC ne fait que commencer. Les questions ouvertes que nous avons laissées en suspens sont des invitations à la recherche, des terrains de jeu pour la prochaine génération de théoriciens et de praticiens.

Merci de m'avoir accompagné dans cette exploration. Que vos futurs circuits soient compacts, que vos réseaux soient profonds, et que vos traductions conservent toujours l'essentiel.