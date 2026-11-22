## Chapitre 16 — Transfert vers le programme RTC

Nous arrivons au terme de ce voyage. Depuis les premiers rubans infinis imaginés par Turing 1936 jusqu'aux architectures massivement parallèles de Vaswani et al. 2017, nous avons exploré la frontière mouvante entre le calcul symbolique et le calcul neuronal. L'ambition de ce livre, lorsque je l'ai conçu, n'était pas de dresser un simple catalogue de modèles, mais de proposer une grammaire rigoureuse pour penser leurs conversions mutuelles. Cette grammaire, c'est celle des traductions à ressources.

### Synthèse des traductions : le bilan du voyage

Tout au long de ces pages, j'ai soutenu une thèse centrale : toute traduction entre un modèle de calcul symbolique et un modèle neuronal n'est pas une simple équivalence logique, mais une opération payante. Chaque traduction se caractérise par un sextuplet de coûts — taille, temps, mémoire, profondeur, largeur et précision — ainsi que par une dimension de partage, et par un bilan de conservation ou de perte de propriétés fondamentales comme la Turing-complétude, le déterminisme, le parallélisme ou la robustesse.

Reprenons les traductions majeures qui ont structuré notre parcours, en explicitant pour chacune son sens, son coût et son statut.

**Des automates finis aux réseaux de McCulloch-Pitts**
La traduction des automates finis vers les réseaux de McCulloch-Pitts, fondée sur les travaux de Kleene 1956, est une traduction descendante.
*Intuition* : Un automate lit un mot séquentiellement et change d'état. Un réseau de neurones peut maintenir cet état dans ses activations récurrentes.
*Coût* : La taille et la largeur du réseau sont linéaires par rapport au nombre d'états de l'automate. Le temps est strictement séquentiel. Le partage des poids à travers le temps permet une mémoire constante.
*Conservation/Perte* : Le déterminisme et la parallélisation temporelle sont conservés. La robustesse au bruit est perdue, car une activation erronée fait basculer le réseau dans un état incorrect.
*Statut* : CONNU.

**De la machine de Turing aux réseaux récurrents rationnels**
La simulation d'une machine de Turing par un réseau récurrent rationnel, établie par Siegelmann et Sontag 1995, exige une précision arbitraire.
*Définition* : Un réseau récurrent rationnel utilise des poids et des activations qui sont des nombres rationnels, mais dont la taille des numérateurs et dénominateurs peut croître indéfiniment.
*Énoncé* : Pour toute machine de Turing, il existe un réseau récurrent rationnel de taille fixe qui simule ses calculs étape par étape.
*Coût* : Le coût en mémoire (nombre de neurones) est constant. Le coût en temps est linéaire par rapport au temps de la machine de Turing. Le coût en précision $p$ est infini et croît avec le temps de calcul.
*Conservation/Perte* : La Turing-complétude est conservée. La réalisabilité physique et la robustesse aux perturbations sont perdues.
*Statut* : PROUVÉ.

**Des problèmes d'optimisation aux réseaux de Hopfield**
La traduction de problèmes combinatoires vers les réseaux de Hopfield 1982 est une traduction descendante d'une nature différente.
*Intuition* : On encode la fonction objectif d'un problème dans la matrice de poids du réseau, de sorte que les minima locaux de l'énergie correspondent aux solutions valides.
*Coût* : La taille du réseau est quadratique par rapport au nombre de variables. Le temps de convergence n'est pas borné polynomialement en général.
*Conservation/Perte* : Le parallélisme massif est conservé et exploité pour la recherche locale. La Turing-complétude est perdue, car le réseau converge vers des attracteurs et ne peut pas simuler de boucles infinies.
*Statut* : CONNU.

**De la machine de Turing aux transformers à précision arbitraire**
La traduction des machines de Turing vers les transformers, explorée par Pérez, Marinković et Barceló 2019, montre que le mécanisme d'attention peut simuler le ruban et la tête de lecture.
*Exemple* : Pour simuler un déplacement de la tête de lecture vers la droite, le transformer utilise l'attention pour copier l'activation de la position $i$ vers la position $i+1$ à la couche suivante.
*Coût* : La profondeur $d$ est proportionnelle au nombre d'étapes de calcul. La largeur $w$ et la mémoire $M$ croissent avec la taille de l'entrée. Le partage spatial des poids remplace le partage temporel des réseaux récurrents.
*Conservation/Perte* : La Turing-complétude est conservée grâce à la précision arbitraire. Le parallélisme spatial est gagné, mais au prix d'une explosion de la mémoire quadratique.
*Statut* : PROUVÉ.

**L'effondrement des transformers à précision logarithmique**
Enfin, la restriction des transformers à une précision logarithmique, analysée par Merrill et Sabharwal 2023, révèle un effondrement de la Turing-complétude.
*Coût* : La précision est bornée par $p = O(\log n)$, où $n$ est la taille de l'entrée.
*Conservation/Perte* : Ce qui est perdu est fondamental : la capacité à simuler des calculs séquentiels profonds. Les transformers se réduisent à des circuits de faible profondeur, appartenant à la classe $\mathsf{TC}^0$.
*Statut* : PROUVÉ.

La précision arithmétique s'est ainsi imposée comme la ressource pivot de notre étude. À précision arbitraire, le neuronal rejoint le symbolique dans sa puissance théorique maximale. À précision finie ou logarithmique, le neuronal révèle ses limites structurelles.

### Le registre des statuts et la rigueur du programme RTC

L'un des apports méthodologiques de ce livre est l'instauration d'un registre des statuts pour chaque affirmation. Dans un domaine où l'enthousiasme empirique précède souvent la compréhension théorique, il est crucial de distinguer ce qui est démontré de ce qui est simplement observé. Je me suis astreint à cette discipline pour éviter que l'intuition ne se fasse passer pour une preuve.

Nous avons ainsi balisé le terrain :
- **PROUVÉ** : Les théorèmes de simulation dont nous avons détaillé les constructions. Pour ces résultats, j'ai fourni des preuves complètes ou les idées de preuve explicites.
- **CONNU** : Les résultats classiques de la théorie de la complexité, tels que la caractérisation des automates finis (Kleene 1956) ou la hiérarchie des classes (Arora et Barak 2009).
- **EXPÉRIMENTAL** : Les observations sur la capacité des transformers à généraliser, ou l'émergence de capacités algorithmiques. Ces phénomènes sont fascinants, mais ils ne constituent pas des preuves de capacité computationnelle universelle.
- **CONJECTURE** : Les hypothèses sur la séparation stricte entre les classes de complexité, par exemple $\mathsf{P} \neq \mathsf{NP}$, qui impactent directement les bornes inférieures de nos traductions.
- **RÉFUTÉ** : L'idée selon laquelle l'attention seule, sans mécanisme de récurrence ou de profondeur suffisante, pourrait maintenir la Turing-complétude en précision finie.
- **OUVERT** : La caractérisation exacte de la classe de complexité des transformers à précision mixte, ou l'impact de l'apprentissage par descente de gradient sur la préservation des propriétés topologiques des espaces de calcul.

Ce registre n'est pas une simple précaution rhétorique. Il est le socle du programme RTC. Il nous interdit les annonces de découvertes prématurées et nous oblige à quantifier le prix de chaque passage d'un paradigme à l'autre.

### Apports au programme RTC : le sextuplet de coûts et le partage

Ce tome a formalisé le coût d'une traduction sous la forme d'un sextuplet $(T, t, M, d, w, p)$, complété par la notion de partage. Le partage désigne la manière dont les ressources sont réutilisées : partage temporel des poids dans les réseaux récurrents, partage spatial dans les convolutions, ou partage des matrices de projection dans l'attention de Vaswani et al. 2017.

Prenons un exemple concret pour illustrer l'utilité de ce cadre. Supposons que nous souhaitions traduire un algorithme de tri symbolique, qui s'exécute en temps $O(n \log n)$ sur une machine de Turing, vers un transformer.
Si nous utilisons un transformer à précision arbitraire, la profondeur $d$ du réseau sera proportionnelle au nombre d'étapes, ou réduite si nous exploitons le parallélisme de l'attention, mais au prix d'une largeur $w$ et d'une mémoire $M$ quadratiques en $n$. La précision $p$ devra croître avec $n$ pour distinguer les positions sur le ruban.
Si nous passons à un transformer à précision logarithmique, le théorème de Merrill et Sabharwal 2023 nous avertit que nous ne pouvons plus maintenir cette simulation. Le calcul s'effondre en un circuit de profondeur constante ou logarithmique. La traduction est donc impossible sans modifier radicalement la nature du calcul.

Ce que ce tome apporte au programme RTC, c'est la démonstration que la précision $p$ n'est pas un simple paramètre d'implémentation, mais une ressource computationnelle à part entière. Négliger la précision, c'est se condamner à des illusions de Turing-complétude.

### Exercice de synthèse

Pour ancrer ces concepts, je vous propose un exercice de réflexion.
*Énoncé* : Considérez un réseau de Hopfield 1982 utilisé pour résoudre un problème de satisfaction de contraintes. On souhaite traduire ce processus de relaxation énergétique en une machine de Turing symbolique.
*Question* : Quel est le coût en mémoire $M$ et en temps $t$ de cette traduction ascendante (du neuronal vers le symbolique) ? Quelles propriétés du réseau de Hopfield sont perdues lors de cette traduction ?
*Piste de solution* : La machine de Turing doit stocker l'état de tous les neurones (mémoire $M = O(N)$). Le temps $t$ dépend du nombre d'itérations pour atteindre l'attracteur. La propriété perdue est la robustesse au bruit et le parallélisme massif de la mise à jour asynchrone, remplacés par une simulation séquentielle et déterministe. Statut de l'équivalence de puissance pour ce cas précis : CONNU.

### Perspectives : robustesse, apprentissage et calcul naturel

Si les traductions formelles que nous avons étudiées éclairent la puissance expressive des modèles, elles laissent dans l'ombre la question de l'apprentissage. Une traduction PROUVÉE nous dit qu'un réseau de neurones *peut* calculer une fonction, mais elle ne nous dit pas si la descente de gradient *trouvera* les poids correspondants. C'est là que le programme RTC doit s'étendre.

**Robustesse et bruit**
Les réseaux de McCulloch-Pitts 1943 et les machines de Turing partagent une vulnérabilité commune : le déterminisme strict. Une altération d'un bit ou d'un poids peut faire dérailler le calcul. Les réseaux de Hopfield ont introduit la notion d'attracteurs, offrant une robustesse face au bruit. Cependant, cette robustesse se paie par une perte de Turing-complétude. Une perspective majeure du programme RTC est de formaliser les traductions à ressources dans des environnements bruités. Comment traduire un algorithme symbolique en un réseau neuronal qui tolère une variance $\sigma^2$ sur ses activations, tout en garantissant une borne sur le taux d'erreur ? Statut de cette formalisation : OUVERT.

**Apprentissage et complexité de l'optimisation**
La théorie de la complexité (Arora et Barak 2009) nous enseigne que trouver la solution d'un problème $\mathsf{NP}$-complet est difficile. L'apprentissage d'un réseau de neurones qui simule ce problème l'est tout autant. Les traductions descendantes construisent des poids de manière algorithmique. Mais l'apprentissage par données exige que ces poids soient atteignables par optimisation continue. Le fossé entre l'existence d'une traduction et son apprenabilité est l'une des frontières les plus fertiles. Statut : CONJECTURE (il existerait des barrières topologiques empêchant l'apprentissage de certaines traductions symboliques exactes par descente de gradient).

**Interprétabilité : la traduction inversée**
L'une des grandes quêtes actuelles est l'interprétabilité des modèles de neurones. Dans le cadre du programme RTC, l'interprétabilité n'est rien d'autre qu'une traduction ascendante, du neuronal vers le symbolique. Extraire un arbre de décision ou un automate fini à partir des poids d'un transformer revient à chercher une traduction qui minimise la perte de fidélité tout en restant lisible pour un humain. Le coût de cette traduction est souvent une explosion de la taille $T$ du modèle symbolique résultant. Statut : OUVERT (quantification exacte du coût en taille de l'extraction d'automates à partir de transformers à précision finie).

**Calcul naturel et biologique**
Enfin, le calcul neuronal formel s'inspire du biologique, mais s'en éloigne par sa rigidité arithmétique. Le cerveau n'utilise pas de précision arbitraire. Il opère avec des signaux stochastiques, des délais de propagation et une métabolisation de l'énergie. Le transfert du programme RTC vers le calcul naturel exigera de redéfinir notre sextuplet de coûts pour y inclure l'énergie et la stochasticité.

### Mot final au lecteur

Vous avez entre les mains le fruit d'une longue méditation sur la nature du calcul. Lorsque Alan Turing a formalisé la notion de procédure effective en 1936, il cherchait à circonscrire les limites de la logique mathématique. Il ne pouvait pas prévoir que, moins d'un siècle plus tard, ses rubans infinis seraient confrontés aux matrices d'attention et aux gradients stochastiques.

En parcourant ce livre, vous avez vu que la frontière entre le symbolique et le neuronal n'est pas une muraille, mais un marché d'échanges. On y négocie de la mémoire contre de la profondeur, du temps contre de la précision, du déterminisme contre de la robustesse. Vous avez compris que l'extraordinaire puissance des transformers modernes ne viole pas les lois fondamentales de la complexité ; elle les exploite en déplaçant le fardeau du calcul séquentiel vers le parallélisme spatial et la précision arithmétique.

Le programme RTC que nous avons esquissé ici n'est pas un aboutissement, c'est un appel. Il appelle les informaticiens, les mathématiciens et les chercheurs en intelligence artificielle à cesser de s'ignorer. Il exige que nous regardions chaque nouvelle architecture non pas comme une magie empirique, mais comme un objet mathématique dont on peut, et dont on doit, mesurer les coûts et les limites.

La précision arithmétique est la clé de voûte de cet édifice. Tant que nous confondrons la simulation théorique à précision infinie avec la réalité matérielle à précision finie, nous bâtirons nos intuitions sur du sable. Les limites des transformers à précision logarithmique ne sont pas des défauts de fabrication ; ce sont les signatures profondes de la structure mathématique de l'attention.

Je vous laisse sur cette pensée : la machine de Turing n'a pas été remplacée par le réseau de neurones. Elle s'y est traduite. Et dans cette traduction, comme dans toute traduction digne de ce nom, quelque chose s'est conservé, quelque chose s'est perdu, et quelque chose s'est payé. C'est à vous, désormais, de décider ce que vous êtes prêts à payer pour les calculs de demain.