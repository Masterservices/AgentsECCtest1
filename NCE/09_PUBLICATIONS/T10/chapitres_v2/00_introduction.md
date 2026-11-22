## Introduction

### Un problème ancien, une formulation nouvelle

Lorsque Alonzo Church publie en 1936 sa définition des fonctions calculables par le lambda-calcul et qu'Alan Turing, la même année, propose ses machines à ruban, deux langages radicalement différents viennent de naître pour décrire une même réalité : ce qu'il est possible de calculer. Church 1936 et Turing 1936 ne le savaient peut-être pas encore avec toute la netteté que nous leur prêtons aujourd'hui, mais ils venaient de poser la première pierre d'une question qui traverse ce livre de bout en bout : *que se passe-t-il exactement quand on traduit un calcul d'un modèle à un autre ?*

Traduire, ce n'est pas copier. Passer d'un terme du lambda-calcul à une machine de Turing, d'un circuit booléen à une formule SAT, d'un réseau de neurones à un automate fini, c'est accepter qu'une partie de la structure survive et qu'une autre se dissolve. Le temps d'exécution peut gonfler d'un facteur polynomial ; la profondeur d'un circuit peut exploser ; la précision des poids peut s'effondrer. Pourtant, au cœur de toutes ces métamorphoses, quelque chose résiste. Un noyau. Un invariant.

Ce livre est l'exploration systématique de ce noyau. Il s'intitule *Les Invariants du Calcul*, et son sous-titre annonce la couleur : *Ce que conservent et perdent les traductions entre lambda-calcul, machines de Turing, circuits, SAT et réseaux de neurones*. J'y défends une thèse que je formule ainsi : toute traduction fidèle entre modèles de calcul préserve un ensemble identifiable d'invariants — calculabilité, temps et taille à un polynôme près, largeur arborescente, profondeur, précision, partage — tandis que d'autres ressources se dégradent de manière contrôlée ou incontrôlable. Identifier ces invariants, démontrer leurs bornes, cartographier les barrières qui interdisent de les séparer : tel est le programme que j'appelle RTC, pour *Traductions à Ressources et Calcul*, et dont ce livre constitue la première synthèse publique.

### La thèse : invariants préservés, ressources dégradées

Prenons un exemple concret pour fixer les idées. Considérons une fonction booléenne $f : \{0,1\}^n \to \{0,1\}$ calculée par un circuit de taille $s$. Si je traduis ce circuit en une formule SAT via l'encodage de Tseitin (Tseitin 1968), j'obtiens une formule $\varphi$ dont la satisfaisabilité est équivalente à $f = 1$. La taille de $\varphi$ est proportionnelle à $s$, mais la *structure* du circuit — sa largeur arborescente, sa profondeur, son degré de parallélisme — ne se transpose pas sans coût. Le statut de cette observation est CONNU : elle est établie depuis les travaux fondateurs de Cook 1971 et Tseitin 1968.

Ce que je propose dans ce livre, c'est de dépasser le constat qualitatif pour obtenir des *bornes quantitatives*. Par exemple, le résultat L-01, démontré dans le cadre du programme RTC et dont le statut est PROUVÉ, affirme que si un circuit possède une largeur arborescente au plus $w$ et un degré maximal $k$, alors la formule de Tseitin associée admet une largeur arborescente au plus :

$$\mathrm{tw}(T(C)) \leq (k+1)(w+1) - 1$$

**Énoncé en mots.** Pour tout circuit booléen $C$ de largeur arborescente $w$ et de degré maximal $k$, la formule de Tseitin $T(C)$ construite sur le graphe de dépendance des portes a une largeur arborescente bornée supérieurement par $(k+1)(w+1)-1$.

**Conditions de validité.** Le circuit $C$ est un DAG de portes à entrées bornées ; $k$ désigne le nombre maximal d'entrées d'une porte ; $w$ est la largeur arborescente du graphe sous-jacent (sommets = portes, arêtes = fils de dépendance).

**Statut.** PROUVÉ (résultat L-01 du programme RTC).

**Exemple numérique.** Prenons un circuit de largeur arborescente $w = 3$ et de degré maximal $k = 2$ (portes ET et OU binaires). Alors la borne donne $(2+1)(3+1)-1 = 3 \times 4 - 1 = 11$. La formule de Tseitin associée a donc une largeur arborescente au plus 11, là où le circuit initial n'en avait que 3. La traduction a multiplié la largeur par un facteur inférieur à 4 : c'est une dégradation contrôlée, polynomiale, et c'est précisément le type de phénomène que ce livre entend cartographier.

Ce résultat illustre la thèse générale : la calculabilité est préservée (la formule est satisfaisable si et seulement si le circuit accepte), la taille l'est à constante près, mais la largeur arborescente — ressource paramétrée — se dégrade selon une loi explicite.

### Le cadre conceptuel : traductions à ressources et registre des statuts

Deux outils structurent l'ensemble de l'ouvrage. Le premier est la notion de *traduction à ressources*. Une traduction $\tau$ d'un modèle $\mathcal{M}_1$ vers un modèle $\mathcal{M}_2$ n'est pas seulement une fonction qui envoie un objet de $\mathcal{M}_1$ sur un objet de $\mathcal{M}_2$ ; elle est accompagnée d'un *profil de ressources* qui indique, pour chaque ressource $r$ (temps, taille, largeur, profondeur, précision, partage), comment la valeur de $r$ dans $\mathcal{M}_2$ se compare à celle dans $\mathcal{M}_1$. Formellement, si $\rho_r(x)$ désigne la quantité de ressource $r$ utilisée par l'objet $x$, une traduction $\tau$ est dite *$r$-polynomiale* s'il existe un polynôme $p$ tel que :

$$\forall x \in \mathcal{M}_1, \quad \rho_r(\tau(x)) \leq p\!\left(\rho_r(x)\right)$$

**Énoncé en mots.** La ressource $r$ de l'image de $x$ par $\tau$ est bornée par un polynôme en la ressource $r$ de $x$.

**Conditions de validité.** La ressource $r$ doit être bien définie et à valeurs dans $\mathbb{N}$ ou $\mathbb{R}_{\geq 0}$ ; le polynôme $p$ est indépendant de $x$ mais peut dépendre de $\tau$.

**Statut.** CONNU (formalisation standard, cf. Arora et Barak 2009).

**Exemple numérique.** Si $\tau$ est la traduction circuit $\to$ SAT par Tseitin et $r$ la taille, alors $\rho_{\text{taille}}(\tau(C)) \leq 5 \cdot \rho_{\text{taille}}(C) + 3n$, où $n$ est le nombre d'entrées. Pour un circuit de taille 200 et 10 entrées : $5 \times 200 + 3 \times 10 = 1030$ clauses au plus.

Le second outil est le *registre des statuts*. Chaque affirmation mathématique de ce livre porte l'une des étiquettes suivantes : PROUVÉ (démonstration complète dans le texte ou référence interne), CONNU (résultat de la littérature, idée de preuve fournie), EXPÉRIMENTAL (obtenu par calcul numérique, reproductible), CONJECTURE (énoncé plausible non démontré), RÉFUTÉ (contre-exemple connu), OUVERT (question non résolue). Cette discipline m'a semblé indispensable : le lecteur doit pouvoir, à chaque ligne, savoir où en est le savoir.

### Une galerie de formules inaugurales

Pour donner un avant-goût de la densité mathématique du livre, voici quelques-unes des bornes que nous rencontrerons et qui jalonnent le programme RTC.

**Résultat L-02 (PROUVÉ).** Pour tout tableau de calcul d'une machine de Turing à $s$ étapes sur un ruban de largeur $n$, la largeur de chemin du graphe de dépendance du tableau est au plus :

$$\mathrm{pw}(\text{tableau}) \leq 4s + 1$$

**Énoncé en mots.** La structure tabulaire qui encode $s$ pas de calcul a une largeur de chemin linéaire en $s$, indépendamment de la taille du ruban.

**Conditions de validité.** La machine est à un seul ruban ; le tableau est construit selon la méthode standard de Cook 1971.

**Exemple numérique.** Pour $s = 50$ étapes, la largeur de chemin est au plus $4 \times 50 + 1 = 201$.

**Résultat L-03 (PROUVÉ).** Dans la compilation d'un circuit en un réseau à seuil (threshold circuit), il existe une compilation préservant la fonction calculée telle que chaque poids du réseau est au plus :

$$|w_i| \leq 2$$

**Énoncé en mots.** On peut traduire tout circuit booléen en un circuit à seuils dont tous les poids sont dans $\{-2, -1, 0, 1, 2\}$.

**Conditions de validité.** Le circuit source est composé de portes AND, OR, NOT à fan-in borné.

**Exemple numérique.** Une porte AND à deux entrées $x_1, x_2$ se compile en un neurone à seuil de poids $w_1 = 1$, $w_2 = 1$ et de seuil $\theta = 2$. Vérifions : si $x_1 = x_2 = 1$, la somme vaut $1+1=2 \geq 2$, sortie 1. Si $x_1 = 0, x_2 = 1$, somme $= 1 < 2$, sortie 0. Correct.

**Théorème de Courcelle (CONNU).** Pour tout graphe $G$ de largeur arborescente au plus $w$ et toute propriété $P$ exprimable en logique monadique du second ordre (MSO) :

$$\text{Vérifier } P(G) \text{ se fait en temps } f(w, |P|) \cdot |G|$$

où $f$ est une fonction calculable (en général une tour d'exponentielles en $w$).

**Énoncé en mots.** Sur les graphes de largeur arborescente bornée, toute propriété MSO est décidable en temps linéaire en la taille du graphe, avec une constante qui dépend de la largeur et de la formule.

**Conditions de validité.** $G$ est un graphe fini ; $P$ est une sentence MSO ; une décomposition arborescente de largeur $w$ est fournie. Courcelle 1990.

**Exemple numérique.** Pour $w = 3$, $|P|$ fixée et $|G| = 10^6$ sommets, le temps est $f(3, |P|) \times 10^6$, linéaire en la taille du graphe. La constante $f(3, |P|)$ peut être astronomique, mais elle est indépendante de $|G|$.

**Thèse de Church-Turing étendue (CONNU).** Toute fonction calculable par un modèle de calcul « raisonnable » est calculable par une machine de Turing, et le surcoût en temps est au plus polynomial :

$$T_{\text{TM}}(n) \leq p\!\left(T_{\text{modèle}}(n)\right)$$

**Énoncé en mots.** Le temps d'une machine de Turing simulant un autre modèle raisonnable est polynomial en le temps de ce modèle. Turing 1936, Cook 1971, Arora et Barak 2009.

**Exemple numérique.** Un circuit de taille $s = 1000$ et profondeur $d = 10$ est simulé par une machine de Turing en $O(s^2) = O(10^6)$ étapes au plus.

**Invariance du temps polynomial (CONNU).** Si $\mathcal{M}_1$ et $\mathcal{M}_2$ sont deux modèles polynomialement équivalents, alors :

$$\mathcal{M}_1 \text{ résout } L \text{ en } n^{O(1)} \iff \mathcal{M}_2 \text{ résout } L \text{ en } n^{O(1)}$$

**Énoncé en mots.** La classe P est invariante par traduction polynomiale entre modèles raisonnables.

**Exemple numérique.** Le problème PATH (existence d'un chemin entre deux sommets) est dans P pour les machines de Turing, pour les circuits uniformes, et pour le lambda-calcul avec réduction leftmost-outermost (Accattoli et Dal Lago 2016, statut PROUVÉ pour l'invariance de la réduction).

**Réduction polynomiale à SAT (CONNU).** Pour tout langage $L \in \text{NP}$, il existe une réduction many-one $f$ calculable en temps polynomial telle que :

$$x \in L \iff f(x) \in \text{SAT}$$

**Énoncé en mots.** SAT est NP-complet : tout problème NP se traduit en SAT en temps polynomial. Cook 1971.

**Exemple numérique.** Pour 3-COLORING sur un graphe à $n = 5$ sommets et $m = 7$ arêtes, la réduction produit une formule à $3n = 15$ variables et $m + n = 12$ clauses au moins, en temps $O(n + m) = O(12)$.

**Barrière de relativisation (CONNU).** Il existe des oracles $A$ et $B$ tels que :

$$\text{P}^A = \text{NP}^A \quad \text{et} \quad \text{P}^B \neq \text{NP}^B$$

**Énoncé en mots.** Aucune preuve de $\text{P} \stackrel{?}{=} \text{NP}$ ne peut « relativiser », c'est-à-dire fonctionner uniformément en présence d'un oracle. Baker, Gill et Solovay 1975.

**Exemple numérique.** L'oracle $A$ est construit par diagonalisation sur les machines polynomiales ; l'oracle $B$ encode un problème EXPTIME-complet. La construction est effective mais non élémentaire.

**Barrière d'algébrisation (CONNU).** Pour toute extension algébrique $\tilde{A}$ d'un oracle $A$ :

$$\exists A : \text{P}^{\tilde{A}} = \text{NP}^{\tilde{A}} \quad \text{et} \quad \exists B : \text{P}^{\tilde{B}} \neq \text{NP}^{\tilde{B}}$$

**Énoncé en mots.** L'algébrisation ne suffit pas non plus à séparer ou identifier P et NP. Aaronson et Wigderson 2009.

**Limite de précision des Transformers (CONNU).** Un Transformer à précision logarithmique et profondeur constante ne peut pas calculer certaines fonctions nécessitant un parallélisme supérieur à :

$$\text{TC}^0 \not\subseteq \text{TC}^0_{\text{log-precision, } O(1)\text{-depth}}$$

**Énoncé en mots.** Les Transformers à précision log et profondeur constante ont une puissance de parallélisme strictement limitée. Merrill et Sabharwal 2023.

**Limitation des réseaux à poids réels (CONNU).** Un réseau de neurones à poids rationnels de précision finie $b$ bits et taille $s$ ne peut reconnaître que :

$$\text{au plus } 2^{O(s \cdot b)} \text{ langages réguliers distincts}$$

**Énoncé en mots.** La précision finie borne la diversité des comportements. Siegelmann et Sontag 1995 montrent qu'avec des poids réels exacts, la puissance est maximale, mais la précision finie restreint.

**Exemple numérique.** Avec $s = 10$ neurones et $b = 8$ bits, on a au plus $2^{O(80)}$ comportements distincts, là où des poids réels exacts permettraient une puissance non bornée.

**Résultat E-01b (EXPÉRIMENTAL).** Sur les benchmarks testés dans le programme RTC, les réseaux entraînés par descente de gradient atteignent une largeur effective de 11 à 14, tandis que les réseaux compilés à partir du circuit équivalent ont une largeur de 1 à 3 :

$$\frac{\text{largeur entraînée}}{\text{largeur compilée}} \approx \frac{11 \text{ à } 14}{1 \text{ à } 3} \in [3{,}7\ ;\ 14]$$

**Énoncé en mots.** L'entraînement produit des réseaux significativement plus larges que la compilation directe.

**Conditions de validité.** Benchmarks internes du programme RTC ; statut EXPÉRIMENTAL, non généralisé.

Ces quinze formules ne sont qu'un aperçu. Chaque chapitre en développe d'autres, avec preuves complètes pour les résultats du programme RTC et idées de preuve pour les théorèmes classiques.

### Méthode et démarche

La méthode de ce livre est triple. D'abord, *définir* : chaque ressource (temps, taille, largeur arborescente, largeur de chemin, profondeur, précision, partage) reçoit une définition formelle, motivée par l'intuition, illustrée par un exemple. Ensuite, *traduire* : pour chaque paire de modèles pertinents, j'exhibe la traduction, je calcule son profil de ressources, je démontre les bornes ou je cite celles de la littérature en donnant l'idée de la preuve. Enfin, *cartographier les barrières* : relativisation, preuves naturelles (Razborov et Rudich 1997), algébrisation (Aaronson et Wigderson 2009) — ces obstacles structurels qui expliquent pourquoi certaines questions restent ouvertes.

Je m'efforce de ne jamais présenter une intuition comme une preuve. Les démonstrations courtes sont écrites en entier ; les longues sont esquissées avec honnêteté. Le lecteur trouvera à chaque chapitre une progression : intuition, définition, énoncé, exemple, exercice.

### À qui s'adresse ce livre

Ce livre s'adresse à un lecteur cultivé, curieux de la logique mathématique et de l'informatique théorique, sans être nécessairement chercheur en complexité. Un étudiant de master en informatique ou en mathématiques y trouvera un fil conducteur clair. Un chercheur confirmé y trouvera la synthèse du programme RTC et des bornes nouvelles. Un ingénieur intéressé par la compilation de circuits ou l'architecture des réseaux de neurones y puisera des outils concrets.

Aucun prérequis beyond un cours d'introduction à la théorie de la calculabilité n'est strictement nécessaire : les définitions sont reprises, les notations introduites au fil de l'eau. En revanche, une certaine aisance avec le raisonnement formel et la lecture de formules est attendue.

### Plan de l'ouvrage

Le livre se déploie en quatre parties et seize chapitres.

**Partie I — Fondations : calculabilité, temps et taille comme invariants polynomiaux.** Le chapitre 1 présente les cinq modèles (lambda-calcul, machines de Turing, circuits, SAT, réseaux de neurones) et le paysage des traductions qui les relient. Le chapitre 2 établit la calculabilité comme invariant absolu : tout ce qui est calculable dans un modèle l'est dans tous les autres. Le chapitre 3 développe la thèse de Church-Turing étendue et l'invariance du temps polynomial. Le chapitre 4 montre comment SAT sert de pivot universel pour les traductions.

**Partie II — Invariants paramétrés : largeur, profondeur et parallélisme.** Le chapitre 5 introduit la largeur arborescente et la largeur de chemin, avec le théorème de Courcelle (1990) et les travaux de Robertson et Seymour (1986). Le chapitre 6 démontre le résultat L-01. Le chapitre 7 démontre le résultat L-02. Le chapitre 8 aborde la profondeur, le parallélisme et les classes NC et TC$^0$.

**Partie III — Ressources fragiles, précision, partage et barrières de preuve.** Le chapitre 9 analyse la précision et le partage comme ressources qui se dégradent lors des traductions. Le chapitre 10 démontre le résultat L-03 sur la compilation à seuil. Les chapitres 11 et 12 dressent le panorama des barrières de preuve : relativisation (Baker, Gill et Solovay 1975), preuves naturelles (Razborov et Rudich 1997), algébrisation (Aaronson et Wigderson 2009).

**Partie IV — Réseaux de neurones, expériences et transfert vers le programme RTC.** Le chapitre 13 situe les réseaux de neurones comme modèle de calcul, en s'appuyant sur Siegelmann et Sontag (1995) et Merrill et Sabharwal (2023). Le chapitre 14 présente le résultat expérimental E-01b. Le chapitre 15 synthétise le tableau complet des invariants et des fragilités. Le chapitre 16, enfin, opère le transfert vers le programme RTC : quelles ressources, quelles traductions, quelles questions ouvertes restent à explorer.

### Le programme RTC et ce livre

Ce livre est le premier volume d'une série consacrée au programme RTC. Il en pose les fondations théoriques et en démontre les premiers résultats. Les traductions à ressources y sont étudiées dans leur généralité ; le registre des statuts y est appliqué avec rigueur. Les résultats L-01, L-02, L-03 y sont démontrés ; le résultat E-01b y est rapporté avec ses conditions expérimentales.

Ce que ce tome apporte, concrètement : une classification des ressources selon leur comportement sous traduction (invariant polynomial, dégradation bornée, dégradation incontrôlée) ; trois bornes nouvelles sur la largeur et les poids ; une cartographie des barrières qui expliquent pourquoi certaines séparations de classes résistent ; et un pont vers l'expérimentation sur les réseaux de neurones.

### Une invitation à la lecture

J'ai écrit ce livre comme j'aurais aimé le lire : avec des formules, des preuves, des exemples numériques pas à pas, des exercices, et cette honnêteté qui consiste à dire « ceci est prouvé » ou « ceci est conjecturé » sans jamais brouiller la frontière. Le calcul est un objet mathématique d'une richesse inépuisable ; le traduire, c'est le faire voyager entre des mondes formels qui se ressemblent sans se confondre. Comprendre ce qui survit à ce voyage et ce qui s'y perd, c'est, je crois, l'une des questions les plus profondes de notre discipline.

Bonne lecture.

*Oussama Ghorbel*