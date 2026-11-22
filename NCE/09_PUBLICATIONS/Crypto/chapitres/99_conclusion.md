## Conclusion — La cryptographie comme science des traductions destructrices

Nous arrivons au terme d'un voyage qui, je l'espère, aura transformé votre regard sur la cryptographie. Ce livre n'était pas un catalogue de primitives, ni un manuel d'ingénierie, ni un traité de sécurité applicative. Il proposait une thèse : la cryptographie est la discipline des traductions computationnelles conçues pour anéantir l'information exploitable par un adversaire borné en ressources. Chaque chapitre a été l'étude d'une traduction particulière — du texte clair vers le texte chiffré, de la graine vers la suite pseudo-aléatoire, du message vers la signature — et de ce que cette traduction conserve, perd ou gagne en ressources. Il est temps de rassembler ces fils, de dresser le registre des statuts, de formuler ce que ce tome apporte au programme RTC, et de vous adresser, à vous qui avez cheminé avec moi, un mot final.

### Synthèse des apports : ce que nous avons traduit

La Partie I a posé le décor. Avec Shannon (1949), nous avons compris que l'information se mesure et que le secret parfait exige une clé aussi longue que le message. L'entropie, définie par

$$
H(X) = -\sum_{x \in \mathcal{X}} p(x) \log_2 p(x),
$$

quantifie l'incertitude moyenne d'une variable aléatoire $X$. Cette formule, de statut PROUVÉ, est valide pour toute distribution discrète finie. Prenons un exemple numérique : si $X$ est un dé équilibré à six faces, alors $p(x) = 1/6$ pour tout $x$, et $H(X) = -6 \cdot \frac{1}{6} \log_2 \frac{1}{6} = \log_2 6 \approx 2{,}585$ bits. Le masque jetable réalise la traduction $c = m \oplus k$ avec $|k| = |m|$, et Shannon (1949) a démontré que sous ces conditions, $H(M \mid C) = H(M)$ : le texte chiffré ne fuit rien. Statut PROUVÉ, exemple : pour $m = 1011$ et $k = 0110$, on obtient $c = 1101$, et sans $k$, toute valeur de $m$ reste équiprobable.

Mais le masque jetable est impraticable à grande échelle. La Partie I a alors introduit la traduction fondatrice de la cryptographie moderne : la fonction à sens unique. Yao (1982) en a formalisé la définition asymptotique. Pour une fonction $f : \{0,1\}^n \to \{0,1\}^n$, on exige que pour tout adversaire polynomial $A$,

$$
\Pr_{x \leftarrow \{0,1\}^n}[A(f(x)) \in f^{-1}(f(x))] \leq \text{negl}(n).
$$

Cette inégalité, de statut CONJECTURE (l'existence des fonctions à sens unique reste un problème OUVERT, lié à P vs NP), conditionne toute la discipline. Le théorème HILL (Håstad, Impagliazzo, Levin et Luby 1999) a ensuite montré que de toute fonction à sens unique on peut extraire un générateur pseudo-aléatoire : la traduction « graine courte $\to$ suite longue » est universellement disponible dès lors que le sens unique existe. Statut PROUVÉ conditionnellement.

La Partie II a déplacé le regard vers le probabilisme. Goldwasser et Micali (1984) ont introduit la sécurité sémantique, formalisée par l'indistinguabilité : pour tout adversaire polynomial $A$,

$$
\left| \Pr[A(c_0) = 1] - \Pr[A(c_1) = 1] \right| \leq \text{negl}(n),
$$

où $c_b$ est le chiffrement de $m_b$. Cette borne, de statut PROUVÉ pour certaines constructions sous hypothèses standards, impose que le chiffrement soit probabiliste : la traduction déterministe $m \mapsto c$ est structurellement insuffisante. Nous avons étudié la résiduosité quadratique, puis RSA. La traduction RSA repose sur

$$
c = m^e \bmod N, \quad m = c^d \bmod N, \quad ed \equiv 1 \pmod{\varphi(N)},
$$

formule de statut CONNU, valide lorsque $N = pq$ avec $p, q$ premiers distincts et $\gcd(e, \varphi(N)) = 1$. Exemple numérique : avec $p = 5, q = 11$, on a $N = 55$, $\varphi(N) = 40$. Choisissons $e = 3$, alors $d = 27$ car $3 \cdot 27 = 81 \equiv 1 \pmod{40}$. Pour $m = 7$, $c = 7^3 \bmod 55 = 343 \bmod 55 = 13$. Le déchiffrement donne $13^{27} \bmod 55 = 7$, comme attendu. Diffie et Hellman (1976) ont ouvert la voie à l'échange de clés par la commutativité de l'exponentiation :

$$
(g^a)^b = (g^b)^a = g^{ab} \bmod p.
$$

Statut PROUVÉ algébriquement, CONNU pour la sécurité sous l'hypothèse DDH. Exemple : $p = 23, g = 5, a = 6, b = 15$. Alors $A = 5^6 \bmod 23 = 8$, $B = 5^{15} \bmod 23 = 19$, et le secret partagé est $19^6 \bmod 23 = 8^{15} \bmod 23 = 2$.

Les cinq mondes d'Impagliazzo (1995) ont fourni une cartographie précieuse : Algorithmica, Heuristica, Pessiland, Cryptomania, Heuristica. Chaque monde correspond à un régime de traductions possibles ou impossibles, selon que OWF existe, que la complexité moyenne est difficile, que le pseudo-aléatoire est constructible. Ce cadre, de statut CONNU, reste une boussole conceptuelle.

La Partie III a traduit la cryptographie elle-même en formules logiques et algébriques. Tseitin (1968) a montré que tout circuit $C$ de taille $s$ se traduit en une formule CNF $\Phi_C$ de taille $O(s)$, préservant la satisfiabilité :

$$
|\Phi_C| \leq c \cdot |C|, \quad \Phi_C \text{ est satisfiable} \iff C \text{ accepte une entrée}.
$$

Statut PROUVÉ, avec des variables auxiliaires introduites pour chaque porte. Exemple : pour une porte AND $z = x \wedge y$, on ajoute les clauses $(\neg x \vee \neg y \vee z)$, $(x \vee \neg z)$, $(y \vee \neg z)$, soit 3 clauses par porte. Massacci et Marraro (2000) ont ensuite formulé la cryptanalyse comme instance SAT, et Soos, Nohl et Castelluccia (2009) ont étendu les solveurs SAT à ces instances. Côté algébrique, Courtois et Pieprzyk (2002) ont introduit la méthode XL pour les systèmes surdéterminés :

$$
\text{si } m \gg n, \text{ alors } D_{\text{reg}} \approx \text{petit}, \text{ et la résolution est polynomiale en pratique}.
$$

Statut EXPÉRIMENTAL pour les bornes pratiques, CONNU pour le principe. La largeur structurelle, enfin, a relié la difficulté des formules cryptographiques à la complexité de preuve (Tseitin 1968, Razborov et Rudich 1997).

La Partie IV a confronté la discipline à ses propres limites. Razborov et Rudich (1997) ont démontré que les preuves naturelles, si elles existent, détruiraient les générateurs pseudo-aléatoires :

$$
\text{Preuve naturelle contre } \mathcal{C} \implies \text{pas de PRG dans } \mathcal{C}.
$$

Statut PROUVÉ, conditionné à l'existence de PRG. Ce théorème est la pierre angulaire de notre propos : la cryptographie bloque certaines voies de la complexité, car les traductions destructrices qu'elle construit sont précisément ce que les preuves de séparation cherchent à attaquer. Goldreich (2001) a formalisé la méthodologie des réductions :

$$
\Pr[\text{A casse le schéma}] \leq \Pr[\text{B résout le problème dur}] + \text{negl}(n).
$$

Statut PROUVÉ pour les réductions explicites, fondement de toute la sécurité prouvée. Katz et Lindell (2007) en ont fait la colonne vertébrale pédagogique de la cryptographie moderne.

### Le registre des statuts : bilan des certitudes et des ombres

Le cadre conceptuel de ce livre — les traductions à ressources et leur registre des statuts — nous impose l'honnêteté. Ce qui est PROUVÉ : la sécurité inconditionnelle du masque jetable (Shannon 1949), la traduction de Tseitin (Tseitin 1968), le théorème HILL conditionnel (Håstad, Impagliazzo, Levin et Luby 1999), l'impossibilité des preuves naturelles sous PRG (Razborov et Rudich 1997), la méthodologie des réductions (Goldreich 2001). Ce qui est CONNU : RSA, Diffie-Hellman, la sécurité sémantique, les cinq mondes d'Impagliazzo, la cryptanalyse SAT et XL dans leurs principes. Ce qui est EXPÉRIMENTAL : les bornes pratiques de XL, les performances des solveurs SAT cryptographiques, les largeurs structurelles mesurées sur des instances concrètes. Ce qui est CONJECTURE : l'existence des fonctions à sens unique, la difficulté de la résiduosité quadratique, la sécurité de RSA contre tout adversaire polynomial. Ce qui est RÉFUTÉ : certains schémas déterministes, certaines preuves de sécurité trop optimistes. Ce qui est OUVERT : P vs NP, l'existence inconditionnelle de PRG, la résistance post-quantique des primitives à base de réseaux ou de codes, la largeur structurelle minimale des formules cryptographiques.

Ce registre n'est pas un aveu de faiblesse. Il est la condition de la scientificité. Annoncer une découverte serait trahir le cadre ; prétendre qu'une intuition est une preuve serait trahir le lecteur.

### Les ressources traduites : un inventaire

Revenons au prisme RTC. Chaque traduction cryptographique redistribue les ressources selon un profil précis. Le masque jetable conserve l'information (statut PROUVÉ : $H(M|C) = H(M)$) mais consomme une ressource clé colossale. Les fonctions à sens unique conservent la calculabilité directe et détruisent l'inversabilité, au prix d'une ressource « hypothèse de difficulté » non prouvée. Les PRG traduisent une graine courte en une suite longue, gagnant en largeur ce qu'elles perdent en prouvabilité inconditionnelle. Le chiffrement probabiliste ajoute la ressource « aléa » pour gagner la sécurité sémantique. Les fonctions à trappe introduisent la ressource « secret structurel » (la factorisation de $N$) qui rend la traduction inversible sous condition. La traduction de Tseitin conserve la taille (linéaire) mais augmente la largeur du problème. La traduction XL échange la surdétermination contre la complexité algébrique. Les preuves naturelles montrent que certaines ressources — la constructibilité, l'utilité, la grandeur — ne peuvent coexister avec la pseudo-aléatoire.

### Perspectives ouvertes

Plusieurs directions prolongent ce livre sans le contredire. La cryptographie post-quantique redéfinit les traductions à l'ère des algorithmes de Shor et Grover : les primitives à base de réseaux, de codes, de multivariées ou d'isogénies proposent de nouvelles fonctions à trappe dont la sécurité repose sur des problèmes OUVERT différents. Les preuves à divulgation nulle, les calculs multipartites sécurisés, le chiffrement entièrement homomorphe étendent le domaine des traductions : on ne traduit plus seulement le message, mais le calcul lui-même, préservant la sémantique fonctionnelle tout en détruisant la sémantique informationnelle. La complexité fine (fine-grained complexity) promet des réductions plus précises que les réductions polynomiales, affinant le registre des statuts.

Je n'annonce aucune découverte dans ces directions. Je signale des chantiers où le cadre des traductions à ressources pourra s'appliquer avec profit.

### Transfert vers le programme RTC

Ce tome apporte au programme RTC une classe nouvelle de traductions : les traductions destructrices, conçues pour anéantir l'information exploitable. Alors que les tomes précédents étudiaient des traductions qui préservent (compilation, encodage, simulation), la cryptographie étudie des traductions qui effacent. Cette asymétrie est féconde. Elle révèle que les ressources ne sont pas toujours conservées : certaines sont volontairement détruites, d'autres transférées à un détenteur de secret, d'autres encore rendues inaccessibles à tout adversaire borné.

Les questions ouvertes que ce lègue au programme RTC sont les suivantes. Existe-t-il une théorie unifiée des traductions à ressources qui englobe à la fois les traductions préservatrices et les traductions destructrices ? Peut-on mesurer la quantité d'information détruite par une traduction cryptographique, au-delà de l'entropie de Shannon, par une entropie computationnelle ? Peut-on classifier les traductions selon la ressource qu'elles attaquent prioritairement : temps (OWF), mémoire (fonctions à mémoire-dure), profondeur (preuves à divulgation nulle), largeur (cryptanalyse SAT), partage (MPC) ? La barrière des preuves naturelles (Razborov et Rudich 1997) est-elle un obstacle interne au programme RTC, signalant que certaines traductions ne peuvent être analysées par certaines méthodes ?

Ces questions sont OUVERTES. Elles justifient la poursuite du programme.

### Mot final au lecteur

Vous avez, en refermant ce livre, accompli une traduction vous-même. Vous êtes entré avec une intuition de la cryptographie — l'art des codes, la science du secret, la technique des clés. Vous ressortez, je l'espère, avec une vision structurée : la cryptographie est la théorie computationnelle des traductions qui détruisent l'information exploitable. Vous avez rencontré Shannon et son secret parfait, Yao et ses fonctions à sens unique, Håstad, Impagliazzo, Levin et Luby et leur théorème fondateur, Goldwasser et Micali et leur sécurité sémantique, Diffie et Hellman, Rivest, Shamir et Adleman et leurs fonctions à trappe, Tseitin et sa traduction linéaire, Razborov et Rudich et leur barrière, Impagliazzo et ses cinq mondes.

Vous avez aussi appris une discipline intellectuelle : ne pas confondre intuition et preuve, ne pas annoncer de découverte à la légère, attribuer à chaque affirmation son statut, respecter les références et les auteurs. Cette discipline est, à mes yeux, aussi importante que les théorèmes eux-mêmes. Elle est ce qui distingue la science de la rhétorique.

La cryptographie, telle que je l'ai présentée, est une discipline modeste. Elle sait ce qu'elle ne sait pas. Elle sait que P vs NP est OUVERT, que l'existence des fonctions à sens unique est CONJECTURE, que la sécurité de RSA repose sur une hypothèse non prouvée. Cette modestie n'est pas une faiblesse : elle est la condition de la confiance. Lorsque vous utilisez un protocole sécurisé, vous ne faites pas confiance à une promesse ; vous faites confiance à une réduction, à un registre de statuts, à une communauté qui a collectivement accepté de ne pas affirmer plus qu'elle ne peut démontrer.

Gardez cette modestie. Lorsque vous concevrez vos propres traductions — cryptographiques ou non — demandez-vous toujours : quelles ressources sont conservées, lesquelles sont perdues, lesquelles sont gagnées ? Quel est le statut de chacune de mes affirmations ? Ai-je le droit de prétendre ce que je prétends ?

La cryptographie est une science jeune. Shannon (1949) lui a donné ses fondations il y a moins d'un siècle. Diffie et Hellman (1976) l'ont ouverte au monde il y a cinquante ans. Goldwasser et Micali (1984) l'ont rendue rigoureuse il y a quarante ans. Nous sommes encore au début. Les traductions destructrices que nous construisons aujourd'hui protégeront, demain, des conversations, des votes, des identités, des secrets d'État, des fortunes, des vies. Cette responsabilité exige la rigueur que ce livre a tenté de vous transmettre.

Je vous remercie d'avoir lu ces pages. Puisse ce livre vous avoir donné, sinon des réponses, du moins de meilleures questions. Et puisse le programme RTC, dont ce tome est une étape, trouver en vous des continuateurs exigeants, patients et lucides.

La cryptographie est la science des traductions qui détruisent l'information exploitable. Elle est aussi, et peut-être surtout, la science de ceux qui acceptent de ne pas tout savoir — et qui, précisément pour cette raison, peuvent protéger ce qui compte.