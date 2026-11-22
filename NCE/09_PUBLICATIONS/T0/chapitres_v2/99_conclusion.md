## Conclusion — Ce qui se conserve, ce qui se perd, ce qui reste à mesurer

### Un point de départ, pas un point d'arrivée

Ce livre est né d'une insatisfaction simple. La théorie de la calculabilité nous offre un résultat magnifique : lambda-calcul, machines de Turing, circuits booléens, formules satisfiables, réseaux neuronaux à seuil — tous ces modèles calculent exactement la même classe de fonctions. La thèse de Church-Turing, dans ses multiples reformulations, a clos la question du *pouvoir* expressif. Et pourtant, chaque fois qu'un praticien traduit un algorithme d'un formalisme à l'autre, quelque chose se passe qui n'apparaît dans aucun théorème d'équivalence : une explosion de taille, une perte de structure, un gain inattendu de parallélisme, une profondeur qui s'effondre ou qui enfle. Ces phénomènes sont réels, mesurables, conséquents. Mais ils n'avaient pas de langage commun.

J'ai écrit *Les Traductions du Calcul* pour proposer ce langage. Non pas pour annoncer une théorie nouvelle, non pas pour revendiquer une découverte, mais pour poser une question que tout le monde pratique sans la nommer : *quand on traduit un calcul d'un modèle à un autre, quelles ressources survivent à la traduction, lesquelles meurent, lesquelles naissent ?*

Ce tome 0 est un programme de recherche. Il en porte le nom, les ambitions modestes, les premiers résultats et les premiers échecs. Il n'est pas une somme. Il est un point de départ.

### Ce que le cadre apporte : les traductions à ressources

L'outil central du livre tient en une définition. Une traduction $T$ d'un modèle $M$ vers un modèle $M'$ est dite $(f,g)$-bornée si $|T(x)| \leq f(|x|)$ pour la taille, et si chaque ressource suivie $\rho$ vérifie $\rho'(T(x)) \leq g(\rho(x))$. Une ressource est *préservée à facteur $c$* si $\rho'(T(x)) \leq c \cdot \rho(x) + O(1)$ ; elle est *détruite* si elle peut rester bornée d'un côté et exploser de l'autre.

Cette définition n'est pas profonde. C'est précisément sa vertu. Elle force à nommer ce qu'on mesure, à choisir la fonction $f$, à choisir la fonction $g$, à décider quelle ressource on suit. Elle interdit les affirmations vagues du type « la traduction est efficace » sans préciser *efficace en quoi, pour quelle entrée, à quelle constante près*.

À cette définition s'ajoute le registre des statuts : PROUVÉ, CONNU, EXPÉRIMENTAL, CONJECTURE, RÉFUTÉ, OUVERT. Chaque assertion du livre porte l'un de ces six labels. Cette contrainte rédactionnelle n'est pas un ornement. Elle est la réponse méthodologique à un problème que j'ai rencontré trop souvent dans la littérature à l'intersection de l'informatique théorique et de l'apprentissage automatique : des intuitions présentées comme des preuves, des résultats expérimentaux sur trois instances élevés au rang de théorèmes, des conjectures formulées comme des évidences. Le registre des statuts est un garde-fou. Il m'a obligé, chapitre après chapitre, à distinguer ce que je *sais* de ce que je *soupçonne*.

### Ce que la Partie I a établi

Les quatre premiers chapitres ont posé le décor. Le chapitre 1 a présenté quatre manières de calculer — lambda-calcul, machines de Turing, circuits, réseaux neuronaux — non pas pour les enseigner, mais pour montrer que chacune porte une géométrie propre, une manière de disposer l'information dans l'espace et le temps. Le chapitre 2 a rappelé, preuves à l'appui, que l'équivalence en calculabilité est un fait acquis depuis les années 1930. Il n'y a rien à y ajouter. Toute prétention de « dépasser » la thèse de Church-Turing par un nouveau modèle est, au mieux, une confusion entre calculabilité et complexité.

Le chapitre 3 a accompli une clarification nécessaire : SAT n'est pas un modèle de calcul. C'est un problème, une famille d'instances, un point d'arrivée pour des réductions. Le traiter comme un modèle conduit à des contresens que j'ai voulu dissiper. Le chapitre 4, enfin, a cartographié les limites que personne ne franchit : les bornes inférieures qui résistent, les séparations de classes qui restent ouvertes, les murs contre lesquels toute traduction à ressources finit par buter. Ce chapitre est un rappel d'humilité. Il dit : voici ce qu'on ne sait pas, et voici pourquoi on ne le saura peut-être pas demain.

### Ce que la Partie II a construit

La Partie II est le cœur méthodologique. Le chapitre 5 a donné la définition complète des traductions à ressources, avec ses variantes : traductions uniformes et non uniformes, traductions à ressource unique et à ressources multiples, traductions inversibles et traductions à sens unique. Le chapitre 6 a dressé un inventaire des ressources pertinentes : taille, temps, mémoire, profondeur, largeur structurelle, précision des poids, degré de partage. Cet inventaire n'est pas clos. Il est provisoire et assumé comme tel.

Le chapitre 7 a tenté une carte des traductions connues. Pour chaque paire de modèles, pour chaque ressource, que sait-on ? La réponse honnête est : peu de choses, de manière dispersée, sans formalisme unifié. Des résultats CONNUS existent — la réduction de Cook-Levin, la transformation de Tseitin, la simulation des circuits par des réseaux à seuil — mais ils sont éparpillés dans des sous-communautés qui se parlent peu. La carte du chapitre 7 est lacunaire. C'est voulu. Montrer les trous, c'est déjà justifier le programme.

Le chapitre 8, enfin, a formulé une méthode contre les découvertes fictives. Ce chapitre est peut-être le plus personnel du livre. Il ne contient pas de mathématiques. Il contient des règles : ne pas confondre une simulation polynomial avec une préservation de structure ; ne pas généraliser un résultat sur une famille d'instances ; ne pas attribuer à une traduction une propriété qu'elle n'a que pour un codage particulier. Ces règles sont simples. Les respecter est difficile.

### Ce que la Partie III a démontré — et ce qu'elle a manqué

La Partie III est celle des premiers résultats. Elle se concentre sur une seule ressource : la *largeur*. Ce choix n'est pas anodin. La largeur — le nombre maximal de fils actifs simultanément dans un circuit, le nombre maximal de neurones actifs dans une couche, le nombre maximal de variables non assignées dans une résolution — est une ressource intermédiaire. Elle n'est ni aussi grossière que la taille, ni aussi fine que le temps exact. Elle capture quelque chose de la « géométrie transversale » d'un calcul.

Le chapitre 9 a défini la largeur pour chacun des modèles du livre. Le chapitre 10 a examiné ce que la réduction de Cook-Levin conserve. Le résultat, CONNU dans ses grandes lignes mais rarement énoncé en termes de largeur, est que la traduction d'une machine de Turing en une formule SAT par Cook-Levin préserve la largeur à facteur polynomial, mais la profondeur peut exploser. La traduction est $(f,g)$-bornée pour des $f$ et $g$ polynomiaux, mais elle n'est pas $(f,g)$-bornée pour $g$ constant sur la profondeur. C'est un résultat modeste. Il précise ce qu'on savait intuitivement. Il le met en forme.

Le chapitre 11 a établi que la transformation de Tseitin préserve la largeur. C'est le résultat le plus net du livre. Statut : PROUVÉ. La traduction d'un circuit booléen en une formule CNF par introduction de variables auxiliaires ne fait pas exploser la largeur structurelle. Elle la multiplie par une constante bornée. Ce résultat est petit. Il concerne une transformation spécifique, une ressource spécifique. Mais il est exact, et il résiste à la vérification.

Le chapitre 12 a examiné la traduction des circuits vers les réseaux neuronaux à seuil. Là, le résultat est plus fragile. Statut : CONNU pour la simulation fonctionnelle, EXPÉRIMENTAL pour la préservation de la largeur. Les expériences menées sur des circuits de petite taille montrent une préservation à facteur proche de 1, mais l'échantillon est trop restreint pour généraliser. Je l'ai écrit tel quel.

Le chapitre 13 a posé la question : la largeur prédit-elle la difficulté ? La réponse honnête est : parfois, pas toujours. Il existe des familles de formules où la largeur corrèle avec la complexité de résolution, et d'autres où elle ne corrèle pas. Statut : EXPÉRIMENTAL, non universel.

Le chapitre 14 est un chapitre d'échec. L'outil de mesure — la largeur telle que définie au chapitre 9 — ment dans certains cas. Il existe des calculs de largeur bornée qui sont intrinsèquement difficiles, et des calculs de largeur élevée qui sont triviaux. La largeur n'est pas un invariant suffisant. J'ai voulu écrire ce chapitre pour montrer qu'un programme de recherche contient aussi des impasses, et que les documenter est aussi important que documenter les succès.

Le chapitre 15 a abordé l'apprentissage. Quand un réseau neuronal apprend une fonction, il oublie la structure du circuit qui l'aurait réalisée. La largeur du circuit source n'est pas encodée dans les poids du réseau appris. L'apprentissage est une traduction qui détruit la ressource de largeur. Ce résultat, partiellement CONNU, partiellement EXPÉRIMENTAL, ouvre une question : existe-t-il des régularisations qui *préservent* la largeur lors de l'apprentissage ? La question est OUVERTE.

### Ce que la Partie IV annonce

Le chapitre 16 esquisse la bibliothèque à venir. Il ne promet rien. Il liste les directions : étudier la profondeur comme on a étudié la largeur ; examiner la précision des poids comme ressource ; formaliser les traductions entre lambda-calcul et circuits avec partage ; construire un catalogue de traductions $(f,g)$-bornées avec preuves vérifiables. Chaque entrée de cette bibliothèque est un travail de plusieurs mois, peut-être de plusieurs années. Le tome 0 n'en réalise aucune. Il les nomme.

### Les limites de ce livre

Je dois être honnête sur ce que ce livre n'est pas. Il n'est pas un traité de complexité computationnelle. Il n'est pas un manuel de logique. Il n'est pas un article de recherche avec un théorème principal et sa preuve. C'est un cadre, une méthode, un premier pas. Les résultats PROUVÉS qu'il contient sont peu nombreux et de portée limitée. Les résultats EXPÉRIMENTAUX reposent sur des instances trop petites pour être universels. Les CONJECTURES sont des conjectures : elles peuvent être fausses, et je n'ai aucune garantie qu'elles ne le sont pas.

Ce livre est aussi un choix. J'ai choisi la largeur comme première ressource. J'aurais pu choisir la profondeur, la précision, le partage. D'autres choix auraient produit d'autres livres, d'autres résultats, d'autres échecs. La largeur n'est pas la ressource la plus importante. Elle est celle par laquelle j'ai commencé, parce qu'elle m'a semblé la plus accessible à une analyse élémentaire. Ce choix est contingent. Il n'est pas justifié par une hiérarchie objective des ressources.

### Perspectives : ce qui reste à faire

Le programme de recherche ouvert par ce tome 0 est vaste. Quelques directions se dégagent.

Premièrement, la profondeur. La traduction de circuits de profondeur $d$ en formules SAT par Tseitin produit des formules dont la structure arborescente impose une profondeur de résolution liée à $d$, mais le lien exact reste à préciser. Est-ce que Tseitin préserve la profondeur à facteur constant, comme il préserve la largeur ? Les premiers calculs suggèrent que non, mais la preuve manque. Statut : OUVERT.

Deuxièmement, le partage. Un circuit avec partage — un même sous-circuit utilisé à plusieurs endroits — se traduit en un réseau neuronal où les poids sont dupliqués. Le partage est une ressource qui se détruit naturellement dans la traduction circuit-vers-réseau. Peut-on définir une traduction qui le préserve ? La question est OUVERTE et, à ma connaissance, n'a pas été formulée en ces termes.

Troisièmement, la précision finie. Les réseaux neuronaux réels utilisent des poids en virgule flottante à 16 ou 32 bits. Cette contrainte de précision est une ressource au sens du cadre de ce livre. Comment se comporte-t-elle sous traduction ? Un circuit booléen exact traduit en réseau à poids 16 bits perd de l'information. Cette perte est-elle bornée ? Peut-on la quantifier en termes de $(f,g)$ ? La question est OUVERTE.

Quatrièmement, l'extension du registre des statuts à la vérification formelle. Les preuves de ce livre sont écrites en prose mathématique. Elles sont, je l'espère, correctes. Mais elles ne sont pas vérifiées par un assistant de preuve. Un objectif à moyen terme du programme est de formaliser au moins les lemmes principaux dans un système de preuve interactif. Ce n'est pas une promesse. C'est une intention.

### Un mot au lecteur

Si vous avez lu ce livre jusqu'ici, vous avez accepté une contrainte inhabituelle : celle de distinguer, à chaque page, ce qui est prouvé de ce qui est conjecturé, ce qui est mesuré de ce qui est imaginé. Cette contrainte est fatigante. Elle ralentit la lecture. Elle empêche le plaisir simple de se laisser emporter par une idée. Je le sais. Je l'ai ressentie en écrivant.

Mais je crois qu'elle est nécessaire. Nous vivons une époque où les modèles de calcul — réseaux neuronaux, circuits quantiques, systèmes de preuve automatique — se multiplient, où les traductions entre eux se font à une vitesse industrielle, où les affirmations de supériorité d'un modèle sur un autre se succèdent sans toujours préciser *en quelle ressource, sur quelle famille d'instances, à quelle constante près*. Le cadre des traductions à ressources n'est pas une réponse à cette confusion. C'est un outil pour la rendre visible.

Ce livre ne vous donnera pas de théorème spectaculaire. Il ne vous dira pas que $P = NP$ ou que $P \neq NP$. Il ne vous donnera pas d'algorithme nouveau. Il vous donnera, peut-être, une habitude : celle de demander, devant toute traduction entre modèles de calcul, *qu'est-ce qui se conserve ? qu'est-ce qui se perd ? à quel facteur ? avec quelle preuve ?* Si cette habitude vous accompagne dans vos propres travaux, alors ce tome 0 aura rempli sa fonction.

Je n'ai pas de certitude sur la fécondité du programme que j'ouvre ici. Peut-être la largeur se révélera-t-elle une ressource trop grossière pour produire des résultats significatifs. Peut-être les traductions à ressources se heurteront-elles à des obstacles techniques que je n'anticipe pas. Peut-être d'autres chercheurs, ailleurs, ont-ils déjà construit un cadre équivalent sans que je le sache. Tout cela est possible. Ce livre est un pari modeste : celui qu'une question bien posée, même si elle ne produit que de petits résultats, vaut mieux qu'une grande réponse mal fondée.

La suite, si suite il y a, s'écrira dans les tomes suivants. Ils porteront sur la profondeur, sur la précision, sur le partage. Ils contiendront, je l'espère, des preuves et des expériences. Ils contiendront aussi, inévitablement, des erreurs et des impasses. Le registre des statuts sera là pour les signaler.

En attendant, je vous remercie d'avoir lu celui-ci.

*Oussama Ghorbel*