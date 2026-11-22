## Introduction

### Deux langages pour une même machine

L'histoire de l'informatique et celle des neurosciences computationnelles partagent une racine commune, une intuition fondatrice qui remonte au milieu du vingtième siècle. En 1943, Warren McCulloch et Walter Pitts publiaient un article au titre évocateur, *A logical calculus of the ideas immanent in nervous activity* (McCulloch et Pitts 1943). Dans ce travail séminal, ils démontraient qu'un réseau de neurones formels, opérant par seuils d'activation, pouvait simuler n'importe quelle fonction de la logique propositionnelle. Autrement dit, le cerveau, ou du moins sa modélisation mathématique la plus épurée, pouvait être vu comme un circuit logique. Cette découverte a posé la première pierre d'un édifice théorique que nous allons explorer en profondeur dans cet ouvrage : l'équivalence computationnelle entre les circuits booléens et les réseaux de neurones à seuil.

Mais affirmer que deux modèles de calcul peuvent simuler les mêmes fonctions n'est que le début de l'histoire. En informatique théorique, la question n'est pas seulement de savoir *si* un calcul est possible, mais *à quel prix*. C'est ici que réside le cœur de ce livre. Les réseaux de neurones et les circuits booléens sont deux modèles qui, bien que d'origines distinctes, partagent une structure profonde. Ce livre étudie les traductions formelles entre ces deux modèles sous l'angle des ressources, en démontrant ce qui est conservé ou perdu lors du passage de l'un à l'autre.

Pour bien saisir l'enjeu, définissons brièvement nos deux protagonistes. Un circuit booléen est un graphe acyclique dirigé où les nœuds sont des portes logiques (ET, OU, NON) et les arêtes sont des fils transportant des valeurs binaires ($0$ ou $1$). Un réseau de neurones à seuil, en revanche, est composé de neurones formels qui calculent une somme pondérée de leurs entrées et appliquent une fonction d'activation à seuil : si la somme dépasse une certaine valeur, le neurone s'active (sortie $1$), sinon il reste inactif (sortie $0$).

Prenons un exemple simple : la fonction ET logique (AND) à deux entrées, $x_1$ et $x_2$. Dans un circuit booléen, cette fonction est triviale : il suffit d'une seule porte ET. Dans un réseau de neurones à seuil, nous pouvons l'implémenter avec un seul neurone. Il suffit d'attribuer un poids de $1$ à chaque entrée ($w_1 = 1$, $w_2 = 1$) et de fixer le seuil d'activation à $2$ (ou un biais de $-1.5$ avec une fonction échelon à $0.5$). Le neurone ne s'activera que si $x_1 = 1$ et $x_2 = 1$, produisant ainsi la table de vérité exacte de la porte ET. Le statut de cette équivalence fonctionnelle de base est CONNU.

Cependant, dès que l'on complexifie la fonction à calculer, les divergences structurelles apparaissent. Comment traduire un circuit profond en un réseau peu profond ? Que se passe-t-il si l'on restreint la précision des poids dans le réseau de neurones ? Comment la largeur d'un circuit (le nombre de portes sur une même couche) se traduit-elle en termes de complexité pour un solveur SAT (Satisfiabilité Booléenne) ? Ce sont ces questions de *traductions à ressources* qui structureront notre voyage.

### L'illusion de l'équivalence gratuite

Avant de plonger dans la mécanique des traductions, il nous faut détruire une illusion tenace : celle de l'équivalence gratuite. Les théorèmes d'approximation universelle et les résultats de complétude de Turing nous garantissent que nos modèles peuvent, en théorie, calculer n'importe quelle fonction raisonnable. Mais cette garantie théorique est un mirage lorsqu'il s'agit de concevoir des systèmes réels ou de prouver des propriétés formelles.

L'exemple classique de ce mirage est la fonction de parité. Calculer la parité d'une entrée binaire (savoir si le nombre de $1$ est pair ou impair) est trivial pour un circuit booléen utilisant des portes XOR. Mais pour un réseau de neurones à seuil sans couche cachée (un perceptron monocouche), cette tâche est pathologique. Minsky et Papert 1969 ont démontré qu'un tel réseau ne peut pas calculer la parité de manière efficace. Le statut de cette limitation est CONNU. Pour contourner ce mur, il faut soit ajouter de la profondeur (des couches cachées), soit augmenter la largeur de manière exponentielle, soit utiliser des poids de précision exponentielle. Ce résultat historique a gelé une partie de la recherche en IA pendant des années, précisément parce que les chercheurs de l'époque n'avaient pas encore formalisé le cadre des traductions à ressources : ils ont confondu l'incapacité d'un modèle *restreint en ressources* avec l'incapacité du *paradigme neuronal* dans son ensemble.

Traduire, ce n'est pas simplement trouver une correspondance mathématique. C'est négocier avec les lois de la complexité. Si la traduction d'un circuit vers un réseau de neurones exige une explosion exponentielle de la taille des poids, alors cette traduction est, en pratique, une impasse. C'est pourquoi nous devons abandonner la simple calculabilité pour embrasser la complexité structurelle.

### La démarche : le prisme des traductions à ressources

Le cadre conceptuel propre à ce livre repose sur une notion centrale : les traductions à ressources. Lorsque nous traduisons un algorithme ou une structure d'un modèle à un autre, nous ne nous contentons pas d'une boîte noire qui préserve la fonction d'entrée-sortie. Nous examinons la traduction comme une opération qui consomme et transforme des ressources.

Les ressources que nous allons traquer tout au long de ces pages sont multiples :
- **La taille** : le nombre total de portes dans un circuit ou de neurones dans un réseau.
- **La profondeur** : le nombre de couches successives, qui détermine le temps de calcul parallèle.
- **La largeur** : le nombre maximal de nœuds sur une même couche, reflétant l'espace mémoire ou le parallélisme instantané.
- **La précision des poids** : le nombre de bits nécessaires pour représenter les coefficients synaptiques dans un réseau de neurones.
- **Le partage** : la capacité à réutiliser le résultat d'un calcul intermédiaire, une propriété naturelle des circuits (graphe acyclique) mais parfois coûteuse à émuler dans d'autres formalismes.

Pour chaque traduction étudiée dans ce livre, nous évaluerons son coût selon ces métriques. Mais évaluer un coût ne suffit pas ; il faut également qualifier la certitude de nos affirmations. C'est pourquoi j'introduis ici le **registre des statuts**, une nomenclature stricte qui sera appliquée à chaque résultat, théorème ou affirmation technique de cet ouvrage.

Tout résultat sera étiqueté selon l'un des statuts suivants :
- **PROUVÉ** : Le résultat est démontré de manière complète et rigoureuse dans les pages de ce livre.
- **CONNU** : Le résultat est un théorème classique de la littérature ; nous en donnerons l'idée de la preuve et les références fondatrices.
- **EXPÉRIMENTAL** : L'affirmation repose sur des observations empiriques ou des simulations, sans garantie théorique formelle.
- **CONJECTURE** : Une hypothèse forte, soutenue par des indices théoriques, mais qui résiste encore à la démonstration.
- **RÉFUTÉ** : Une intuition ou une hypothèse qui a été formellement invalidée par une preuve ou un contre-exemple.
- **OUVERT** : Une question fondamentale pour laquelle aucune réponse, même partielle, n'a encore été établie.

Ce registre des statuts est une boussole pour le lecteur. Il permet de distinguer immédiatement le socle mathématique inébranlable des frontières encore exploratoires de la discipline. Il n'y aura ici aucune annonce de découverte miraculeuse, ni de promesses irréalistes. Nous resterons sur le terrain solide de la complexité structurelle et de la théorie du calcul.

### À qui s'adresse ce livre ?

Ce livre a été conçu pour un lecteur cultivé non spécialiste. Vous n'avez pas besoin d'être un chercheur en complexité computationnelle ou un ingénieur en apprentissage automatique pour en saisir les enjeux. Il vous suffit d'avoir une appétence pour la logique, une familiarité avec les mathématiques de niveau universitaire (algèbre linéaire de base, notions de graphes et de fonctions) et une curiosité pour les fondements du calcul.

Pour respecter ce contrat de lecture, chaque chapitre suivra une progression pédagogique rigoureuse en cinq temps :
1. **Intuition** : Nous commencerons toujours par une explication conceptuelle, une analogie ou une motivation concrète pour ancrer le sujet.
2. **Définition** : Nous poserons les objets mathématiques avec clarté et sans ambiguïté.
3. **Énoncé** : Les théorèmes et propriétés seront formulés explicitement.
4. **Exemple** : Chaque concept abstrait sera incarné par un cas pratique, souvent de petite taille, pour permettre une vérification manuelle.
5. **Exercice** : Des pistes de réflexion seront proposées pour tester votre compréhension.

Une règle d'or guide la rédaction des preuves : je ne présenterai jamais une intuition comme une preuve. Pour les résultats qui constituent le cœur inédit de notre cadre d'analyse (les traductions spécifiques et leurs bilans de ressources), vous trouverez des preuves complètes, détaillées pas à pas, avec le statut PROUVÉ. Pour les grands théorèmes connus qui jalonnent le paysage (comme les bornes de profondeur ou les limites des perceptrons), je fournirai l'idée de la preuve, en expliquant le mécanisme sous-jacent, tout en renvoyant à la littérature pour les détails techniques les plus ardus, avec le statut CONNU.

### L'anatomie d'une traduction

Puisque ce tome est fondamentalement un ouvrage de TRADUCTION entre deux modèles, il est essentiel de comprendre comment chaque opération de traduction sera disséquée. Pour chaque passage d'un formalisme à un autre (par exemple, d'un circuit à seuil vers une formule SAT, ou d'un réseau de neurones profond vers un circuit de largeur bornée), nous remplirons une fiche de traduction structurée ainsi :

- **Le sens** : Du modèle source vers le modèle cible.
- **Le coût** : L'impact sur la taille, le temps, la mémoire, la profondeur, la largeur, la précision et le partage.
- **Ce qui est conservé** : Les propriétés invariantes (par exemple, la fonction calculée, la robustesse au bruit).
- **Ce qui est perdu** : Les propriétés qui s'effondrent lors de la traduction (par exemple, la capacité d'apprentissage par gradient, la compacité structurelle).
- **Le statut** : La qualification épistémique de cette traduction (PROUVÉ, CONNU, etc.).

Prenons un avant-goût avec la traduction d'un circuit booléen vers une formule de satisfiabilité (SAT). L'encodage de Tseitin (Tseitin 1968) est un exemple parfait de traduction à ressources maîtrisées. Plutôt que de développer un circuit en une équation booléenne géante (ce qui provoquerait une explosion exponentielle de la taille), Tseitin a introduit des variables auxiliaires pour chaque porte du circuit. Le sens de la traduction va du Circuit vers SAT. Le coût en taille est linéaire par rapport au nombre de portes (conservation de la taille). Ce qui est conservé, c'est la satisfiabilité de la formule globale. Ce qui est perdu, c'est l'équivalence logique stricte (on obtient une équivalence en termes de satisfiabilité, ou *equisatisfiabilité*, et non une équivalence fonctionnelle directe sans les variables auxiliaires). Le statut de cette traduction est CONNU.

### Plan de l'ouvrage

L'architecture de ce livre reflète la progression naturelle de notre enquête, divisée en quatre grandes parties et seize chapitres.

**Partie I – Fondements des modèles et premières traductions**
Nous poserons les bases mathématiques et historiques.
Le **Chapitre 1** explorera *Le neurone formel et la porte à seuil*, en partant de l'héritage de McCulloch et Pitts 1943 pour aboutir à la définition moderne des réseaux à seuil et à la géométrie des hyperplans séparateurs.
Le **Chapitre 2** détaillera les *Circuits booléens et complexité structurelle*, en introduisant les classes de complexité non uniforme, les notions de fan-in et fan-out, et les bornes inférieures, en nous appuyant sur les synthèses de Jukna 2012.
Le **Chapitre 3** abordera la *Satisfiabilité et encodage*, où nous verrons comment le problème SAT (Cook 1971) et les encodeurs modernes (Biere, Heule, van Maaren et Walsh 2009) permettent de capturer la logique des circuits sous forme normale conjonctive.
Enfin, le **Chapitre 4** formalisera les *Ressources de calcul et registre des statuts*, en consolidant le cadre méthodologique et épistémique qui servira de fil rouge à tout le reste du livre.

**Partie II – Des circuits aux réseaux de neurones**
Ici, nous traduirons les structures logiques vers des architectures neuronales.
Le **Chapitre 5** présentera la *Compilation porte par porte en neurones à seuil*, une traduction directe et naïve dont nous évaluerons les limites et les surcoûts.
Le **Chapitre 6** s'attaquera aux *Circuits à seuil de profondeur bornée*, en explorant les résultats fondateurs de Hajnal, Maass, Pudlák, Szegedy et Turán 1993 sur la puissance et les limites des réseaux peu profonds, notamment avec les portes majoritaires.
Le **Chapitre 7** est crucial : *La taille des poids dans les traductions*. Nous y démontrerons, en suivant les travaux de Håstad 1994, que la précision des poids n'est pas un détail d'implémentation, mais une ressource computationnelle à part entière, dont la restriction peut entraîner une explosion de la taille du réseau.
Le **Chapitre 8** élargira la perspective en considérant les *Réseaux comme solveurs approchés de contraintes*, analysant comment l'architecture neuronale peut relaxer la rigueur booléenne au profit de l'optimisation continue.

**Partie III – Des réseaux de neurones aux circuits et à SAT**
Nous inverserons la direction de la traduction. Comment comprendre un réseau de neurones entraîné en le compilant vers des modèles symboliques ?
Le **Chapitre 9** traitera de l'*Extraction d'un circuit à partir d'un réseau entraîné*, un enjeu majeur pour l'explicabilité de l'intelligence artificielle, en explorant les arbres de décision et les formules booléennes comme cibles d'extraction.
Le **Chapitre 10** reviendra sur la *Largeur structurelle : Tseitin et dérivations*, en montrant comment la largeur d'un réseau impacte la complexité des preuves par résolution propositionnelle.
Le **Chapitre 11** analysera l'*Élagage de réseaux entraînés et limites*, en cherchant à réduire la taille des réseaux tout en préservant leur fonction, et en identifiant les murs théoriques de cette approche heuristique.
Le **Chapitre 12** se penchera sur les avantages de la profondeur, en s'appuyant sur les théorèmes de séparation de Telgarsky 2016, qui prouvent que certaines fonctions (comme les dents de scie itérées) nécessitent des réseaux exponentiellement plus larges si l'on réduit leur profondeur. Le statut de ces séparations est PROUVÉ.

**Partie IV – Limites, précision et transfert RTC**
La dernière partie élèvera le débat vers les architectures modernes et les perspectives de recherche.
Le **Chapitre 13** examinera la *Précision logarithmique et parallélisme*, en intégrant les découvertes récentes de Merrill et Sabharwal 2023 sur les limites des transformers lorsqu'ils sont contraints par une précision finie, ce qui nous permettra de faire le pont entre les réseaux à seuil classiques et l'attention mécanique.
Le **Chapitre 14** proposera une *Synthèse des coûts de traduction*, sous forme de tables et de bilans, récapitulant ce qui se conserve et ce qui se perd à travers tous les modèles étudiés.
Le **Chapitre 15** listera les *Questions ouvertes et conjectures*, cartographiant les zones d'ombre où le registre des statuts affiche fièrement la mention OUVERT.
Enfin, le **Chapitre 16** conclura par le *Transfert vers le programme RTC*. Ce chapitre final exposera ce que ce tome apporte à l'étude des traductions à ressources : quelles ressources avons-nous isolées, quelles traductions avons-nous validées, et comment ce cadre peut être généralisé à d'autres modèles de calcul.

### Ce qui se conserve, ce qui se perd : une philosophie de la traduction

Au-delà des mathématiques, ce livre porte une vision de l'informatique théorique. Traduire, ce n'est pas trahir, mais c'est inévitablement transformer. Lorsque nous passons d'un réseau de neurones, avec ses poids continus et sa capacité d'approximation universelle, à un circuit booléen, avec sa logique discrète et sa rigidité structurelle, nous perdons la souplesse de l'optimisation par gradient. En revanche, nous gagnons la vérifiabilité formelle, la capacité d'utiliser des solveurs SAT pour prouver des propriétés de robustesse ou d'équivalence.

À l'inverse, traduire un problème SAT complexe en un réseau de neurones à seuil peut sembler contre-nature pour un ingénieur, mais c'est une opération qui révèle la capacité des réseaux à agir comme des heuristiques d'optimisation massivement parallèles. Le coût en précision des poids (souvent exponentiel si l'on veut une exactitude stricte, comme le montre Håstad 1994) nous rappelle que le continu n'est pas toujours un avantage gratuit ; il a un coût matériel et théorique.

L'étude de la largeur et de la profondeur, qu'il s'agisse de circuits (Jukna 2012) ou de réseaux de neurones (Telgarsky 2016), nous enseigne que le temps (la profondeur) et l'espace (la largeur) sont les deux faces d'une même pièce. Les théorèmes de compromis nous montrent qu'on ne peut pas toujours comprimer le temps sans exploser l'espace, et vice-versa. Le parallélisme, souvent vanté dans les architectures neuronales modernes, trouve ses limites fondamentales lorsque la précision de la mémoire est bornée, un fait mis en lumière par Merrill et Sabharwal 2023 pour les modèles de type transformer, et qui résonne profondément avec les limites des circuits à seuil de profondeur bornée (Hajnal et al. 1993).

### Une boussole pour le lecteur

En tant qu'auteur, mon rôle n'est pas de vous vendre une méthode miracle pour entraîner de meilleurs réseaux de neurones, ni de vous promettre que la compilation de vos modèles d'IA en circuits logiques résoudra tous vos problèmes de déploiement. Mon rôle est de vous fournir une carte rigoureuse, un cadre d'analyse qui vous permette de comprendre les limites fondamentales de vos outils.

Si vous êtes un chercheur en IA, ce livre vous aidera à comprendre pourquoi certaines architectures résistent à la compression, et pourquoi la profondeur n'est pas un simple hyperparamètre mais une nécessité topologique pour certaines classes de fonctions. Si vous êtes un ingénieur en vérification formelle, vous comprendrez comment les encodeurs SAT (Biere et al. 2009) peuvent être optimisés en exploitant la structure des réseaux de neurones qu'ils cherchent à vérifier. Si vous êtes un étudiant en informatique, vous découvrirez que les frontières entre la logique, la complexité et l'apprentissage automatique sont artificielles, et que les mathématiques qui les sous-tendent forment un tout cohérent.

Les formules que vous rencontrerez, rédigées en LaTeX, seront toujours accompagnées de leur explication textuelle. Par exemple, si nous écrivons la fonction d'activation d'un neurone à seuil sous la forme $f(x) = \text{sgn}(\sum_{i=1}^n w_i x_i - \theta)$, nous prendrons le temps de définir $w_i$ comme les poids synaptiques, $x_i$ comme les entrées, et $\theta$ comme le seuil, avant d'explorer comment la variation de $\theta$ modifie la géométrie de l'hyperplan séparateur.

### Vers le programme RTC

Ce livre est le premier tome d'une exploration plus vaste qui s'inscrit dans ce que j'appelle le programme RTC (Resource-bounded Translations and Compilations). Le programme RTC vise à systématiquement classifier les modèles de calcul non pas par les fonctions qu'ils peuvent calculer en théorie (car, par la thèse de Church-Turing, beaucoup de modèles sont équivalents en termes de calculabilité), mais par la manière dont ils consomment les ressources physiques et mathématiques lors de la traduction de l'un vers l'autre.

Le transfert vers le programme RTC, qui sera détaillé dans le dernier chapitre, consistera à extraire les leçons de notre voyage entre circuits et réseaux de neurones pour les appliquer à d'autres dualités de l'informatique : les automates et les expressions rationnelles, les programmes logiques et les bases de données, les modèles quantiques et les circuits réversibles. Chaque fois, nous chercherons le coût, la largeur, la profondeur, et ce qui se perd dans l'abîme de la traduction.

En refermant ce livre, vous ne verrez plus un réseau de neurones comme une simple boîte noire statistique, ni un circuit booléen comme un assemblage obsolète de portes logiques. Vous les verrez comme deux dialectes d'une même langue computationnelle, avec leurs idiomes, leurs lourdeurs et leurs élégances propres. Et surtout, vous saurez exactement combien coûte le passage de l'un à l'autre.

Bonne lecture, et bon voyage au cœur de la machine.