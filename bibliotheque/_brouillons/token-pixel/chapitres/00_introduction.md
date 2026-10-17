## Introduction

### Une convergence longtemps attendue

Il y a une décennie à peine, générer une image photoréaliste à partir d'une description textuelle relevait de la science-fiction. Les systèmes de vision par ordinateur reconnaissaient des objets ; les modèles de langage produisaient des phrases. Deux mondes parallèles, séparés par un fossé représentationnel que peu imaginaient franchissable. Puis les architectures transformer ont bouleversé l'ordre établi. En traitant le texte comme une séquence de tokens discrets, les grands modèles de langage — GPT, LLaMA, Mistral et leurs successeurs — ont démontré qu'une seule fonction objectif, la prédiction du token suivant, pouvait engendrer des capacités d'une richesse stupéfiante : raisonnement, traduction, synthèse, code. La question qui s'est alors imposée, presque mécaniquement, fut la suivante : si l'on peut réduire la langue à une suite de tokens, peut-on réduire une image à la même abstraction ? Et si oui, le même moteur autorégressif peut-il générer un pixel aussi naturellement qu'il génère un mot ?

Ce livre est né de cette question. Il n'est ni un survol journalistique des dernières avancées en génération d'images, ni un tutoriel pas-à-pas pour fine-tuner un modèle sur un GPU de bureau. Il est une exploration systématique, rigoureuse et pratique du chemin qui mène d'un LLM entraîné sur du texte à un système capable de produire des images cohérentes, contrôlables et esthétiquement acceptables. Ce chemin passe par la tokenisation visuelle, la modélisation autorégressive de grilles de patches, l'alignement intermodal, l'ingénierie de l'entraînement et l'optimisation de l'inférence. Il est semé de choix architecturaux, de compromis computationnels et de pièges expérimentaux que j'ai voulu documenter avec la plus grande honnêteté possible.

### Le sujet : du token au pixel, et retour

Le titre de cet ouvrage n'est pas une métaphore. Il désigne un trajet représentationnel précis. D'un côté, le *token* : unité discrète, indexée dans un vocabulaire fini, manipulée par des opérations d'embedding, d'attention et de projection linéaire. De l'autre, le *pixel* : valeur continue (ou quantifiée sur 8 bits), inscrite dans une grille bidimensionnelle, porteuse d'information chromatique, spatiale et fréquentielle. Entre les deux se trouve un ensemble de transformations — encodeurs, quantifieurs, décodeurs — dont la conception détermine presque entièrement la qualité, la fidélité et le coût de la génération.

Comprendre ce trajet, c'est comprendre pourquoi un VQGAN avec un codebook de 1 024 entrées et une dimension de 256 produit des reconstructions sensiblement différentes d'un VQ-VAE à 8 192 codes ; c'est saisir pourquoi l'ordre de balayage d'une grille 32 × 32 influence la convergence de l'entraînement ; c'est mesurer pourquoi un modèle à 7 milliards de paramètres, pensé pour le texte, doit être adapté avec précaution pour ne pas catastrophiquement oublier ses capacités linguistiques tout en acquérant une compétence visuelle. Ce livre traite chacun de ces points, non comme des curiosités isolées, mais comme les maillons d'une chaîne dont la solidité conditionne le résultat final.

J'ai souhaité que le lecteur puisse, à la dernière page, répondre à des questions concrètes : combien de tokens faut-il pour représenter une image 256 × 256 avec une perte perceptuelle acceptable ? Quel budget GPU est raisonnable pour entraîner un adaptateur visuel sur un LLM open-source ? Comment diagnostiquer un effondrement de codebook ou une dérive de la norme des gradients lors d'un entraînement multimodal ? Ce sont ces questions, prosaïques mais décisives, qui structurent la matière de l'ouvrage.

### La démarche : formaliser, expérimenter, transmettre

Trois principes guident la rédaction.

Le premier est la **formalisation**. Chaque concept — entropie d'une distribution de patches, facteur de compression d'un auto-encodeur, divergence de KL dans un VAE, score FID entre deux distributions d'images — est défini mathématiquement avant d'être illustré. Je ne cherche pas l'élégance formelle pour elle-même ; je cherche la précision qui évite les malentendus. Quand j'écris que la tokenisation visuelle « discrétise » l'espace latent, je précise quelle quantification est utilisée, selon quelle métrique de distorsion, et avec quelles garanties (ou absences de garanties) théoriques.

Le deuxième principe est l'**ancrage expérimental**. Les protocoles présentés — notamment celui du chapitre 22, qui détaille l'adaptation d'un LLM 7B en générateur 256 × 256 — s'appuient sur des configurations réalistes : types de GPU, tailles de batch, durées d'entraînement, courbes de perte typiques. Je ne promets aucun résultat miracle. La génération d'images autorégressive reste un domaine où la variance entre runs est élevée, où un hyperparamètre mal réglé peut diviser la qualité par deux, où les comparaisons entre méthodes dépendent fortement du budget computationnel alloué. Je m'efforce de présenter les ordres de grandeur honnêtement, en signalant les incertitudes.

Le troisième principe est la **pédagogie progressive**. Le livre est conçu pour être lu linéairement, chaque chapitre s'appuyant sur les notions introduites précédemment. Cependant, des encadrés de rappel permettent à un lecteur déjà familier avec les transformers ou les auto-encodeurs de sauter les sections introductives sans perdre le fil. Des figures schématiques, des tableaux comparatifs et des extraits de pseudocode jalonnent le texte pour ancrer l'abstraction dans le concret.

### Le public visé

Ce livre s'adresse en priorité à trois profils.

**L'ingénieur en apprentissage automatique** qui maîtrise les fondamentaux du deep learning — rétropropagation, optimisation par descente de gradient, architectures convolutionnelles et attentionnelles — et qui souhaite comprendre comment étendre un pipeline LLM existant vers la génération d'images. Pour ce lecteur, les chapitres pratiques (16, 17, 22, 23) constituent le cœur de l'ouvrage, mais ils ne prennent leur pleine saveur qu'après la lecture des parties théoriques qui les précèdent.

**Le chercheur ou le doctorant** en vision par ordinateur, en traitement du langage naturel ou en apprentissage génératif, qui cherche une synthèse structurée des approches par tokens discrets, de leurs fondements informationnels et de leurs limites. Les chapitres 3, 7, 10, 11, 18 et 21 offrent un état de l'art critique, avec des références aux travaux fondateurs et aux résultats récents, sans prétendre à l'exhaustivité encyclopédique.

**Le curieux techniquement instruit** — développeur senior, architecte logiciel, passionné d'IA — qui veut comprendre *pourquoi* et *comment* un modèle de langage peut devenir un générateur d'images, au-delà des annonces marketing et des démonstrations spectaculaires. Pour ce lecteur, j'ai veillé à ce que chaque équation soit accompagnée d'une interprétation intuitive, et chaque choix architectural d'une justification en termes de compromis.

Un prérequis raisonnable : une familiarité avec l'algèbre linéaire de base, les probabilités élémentaires et le fonctionnement général d'un réseau de neurones. Aucun cadre logiciel spécifique n'est imposé ; les extraits de code, lorsqu'ils apparaissent, sont en Python avec PyTorch, mais les concepts sont indépendants de toute bibliothèque.

### Comment lire ce livre

L'ouvrage est organisé en six parties, totalisant vingt-quatre chapitres. Chaque partie peut se lire comme un bloc cohérent, mais je recommande vivement une première lecture séquentielle, car les définitions introduites en Partie I sont réutilisées sans redondance dans les parties suivantes. Les chapitres 1 à 4 posent le vocabulaire commun ; les chapitres 5 à 9 construisent la brique de tokenisation ; les chapitres 10 à 13 explorent la génération proprement dite ; les chapitres 14 à 17 traitent de l'entraînement et de l'adaptation ; les chapitres 18 à 21 offrent les outils de diagnostic ; les chapitres 22 à 24 fournissent le protocole intégral et ouvrent sur l'avenir.

Le lecteur pressé pourra se rendre directement au chapitre 22 pour le protocole complet, puis revenir en arrière pour approfondir les points qui l'intéressent. Le lecteur chercheur privilégiera les chapitres 11, 12, 19 et 24, où les questions ouvertes et les comparaisons méthodologiques sont développées avec le plus de détail.

### Annonce du plan

**Partie I — Fondations : le Token, le Pixel et la Représentation.** Quatre chapitres pour établir le terrain. Le chapitre 1 dissèque l'anatomie d'un LLM : embeddings positionnels, couches d'attention, tête de prédiction, fonction de perte cross-entropie. Le chapitre 2 aborde l'image comme signal : résolution, canaux RVB, entropie de Shannon appliquée aux distributions de pixels, redondance spatiale et spectrale. Le chapitre 3 formalise la relation token-pixel : combien de bits d'information porte un pixel, combien un token, et quel est le coût représentationnel du passage de l'un à l'autre. Le chapitre 4 dresse un panorama des grandes familles génératives — autoregression, diffusion, GAN, modèles de flux — en situant l'approche par tokens dans ce paysage.

**Partie II — Tokenisation Visuelle : du Continu au Discret.** Cinq chapitres dédiés à la transformation de l'image en séquence de tokens. Le chapitre 5 introduit les auto-encodeurs et les VAE comme étape de compression. Le chapitre 6 approfondit VQGAN et ses successeurs, en analysant les mécanismes de quantification vectorielle et de régularisation adversariale. Le chapitre 7 se concentre sur le codebook : taille, dimension, stratégies d'initialisation, phénomènes d'effondrement et remèdes. Le chapitre 8 traite de la patchification et des inducteurs visuels, du CNN au Vision Transformer. Le chapitre 9 compare tokenisation discrète et tokenisation continue, en discutant les implications pour l'intégration dans un LLM.

**Partie III — Modélisation Autorégressive : Ordre, Balayage et Génération.** Quatre chapitres sur la mécanique de génération. Le chapitre 10 pose la factorisation autoregressive de la distribution conjointe des pixels (ou des tokens visuels). Le chapitre 11 compare les ordres de balayage — raster, serpentin, courbe de Hilbert, spirale — et leurs effets sur la qualité et la vitesse. Le chapitre 12 présente les approches parallèles et semi-autorégressives : MaskGIT, MAR, et les méthodes par masquage itératif. Le chapitre 13 explore la génération multi-échelle et la résolution progressive.

**Partie IV — Alignement Texte-Image, Entraînement et Architecture.** Quatre chapitres sur l'intégration multimodale. Le chapitre 14 montre comment unifier les vocabulaires textuel et visuel dans un espace de tokens commun. Le chapitre 15 détaille les mécanismes de cross-attention et de conditionnement textuel. Le chapitre 16 aborde les protocoles d'entraînement : constitution des données, curriculum learning, stabilité numérique. Le chapitre 17 propose une étude de cas : adapter concrètement un LLM existant (GPT, LLaMA, Mistral) à la génération d'images, avec les modifications architecturales nécessaires.

**Partie V — Évaluation, Comparaison et Limites.** Quatre chapitres pour mesurer et comprendre. Le chapitre 18 passe en revue les métriques quantitatives : FID, Inception Score, CLIP-score, LPIPS, et leurs limites. Le chapitre 19 propose une comparaison approfondie entre autoregression par tokens et diffusion, en termes de qualité, de coût, de contrôlabilité et de scalabilité. Le chapitre 20 discute honnêtement les limites actuelles : artefacts de quantification, incohérences spatiales, coût computationnel, enjeux de sécurité et de biais. Le chapitre 21 introduit les méthodologies d'ablation pour isoler les facteurs qui comptent réellement.

**Partie VI — Protocoles Pratiques, Déploiement et Pistes de Recherche.** Trois chapitres pour passer à l'action et regarder devant. Le chapitre 22 fournit un protocole complet, étape par étape, pour adapter un LLM 7 milliards de paramètres en générateur d'images 256 × 256 : choix du tokenizer, modification de l'architecture, entraînement, évaluation itérative. Le chapitre 23 traite de l'optimisation et du déploiement : inférence efficace, quantification, techniques de serving, réduction de latence. Le chapitre 24 ouvre sur les frontières de la recherche : ce qui vient après le paradigme token-pixel, les modèles unifiés, la génération vidéo, les interfaces neuronales et les questions ouvertes.

### Conventions typographiques et notes

Les termes techniques anglais couramment utilisés dans la littérature (token, patch, codebook, embedding, cross-attention, fine-tuning, etc.) sont conservés en anglais et signalés en *italique* à leur première occurrence, avec une définition ou un équivalent français entre parenthèses. Les équations sont numérotées par chapitre. Les références bibliographiques sont données entre crochets [Auteur, année] et regroupées en fin d'ouvrage. Les extraits de pseudocode sont présentés dans des blocs monospaces.

J'ai fait le choix de ne pas multiplier les notes de bas de page, préférant intégrer les remarques contextuelles directement dans le corps du texte. Lorsqu'une affirmation repose sur un résultat empirique spécifique, je cite la source. Lorsqu'il s'agit d'une observation issue de ma propre pratique expérimentale, je le signale explicitement.

### Un mot sur l'état du domaine

La génération d'images est un champ en évolution rapide. Les méthodes décrites ici reflètent l'état des connaissances au moment de la rédaction. Certaines architectures mentionnées seront peut-être supplantées avant même la publication de cet ouvrage ; d'autres, plus fondamentales — la quantification vectorielle, la factorisation autoregressive, l'attention multi-têtes — constituent des briques dont la pertinence dépasse les modes. J'ai tâché de distinguer clairement ce qui relève du principe durable et ce qui relève de l'implémentation contingente, afin que le lecteur puisse extrapoler au-delà de ce texte.

Je ne promets pas qu'à la fin de ce livre vous saurez générer des images indiscernables de photographies avec un simple ordinateur portable. Ce serait malhonnête. Je promets, en revanche, que vous comprendrez précisément ce qui rend cette tâche difficile, quels leviers existent pour l'approcher, et comment concevoir un protocole expérimental rigoureux pour progresser, étape par étape, vers des résultats solides.

### Remerciements et avertissement

Ce livre a bénéficié des échanges avec de nombreux collègues, chercheurs et praticiens dont les retours critiques ont affiné ma pensée. Je les remercie collectivement, sans les nommer individuellement, car leurs contributions sont trop entremêlées pour être attribuées ligne à ligne. Je remercie également les communautés open-source dont les implémentations publiques ont rendu possible l'expérimentation à moindre coût.

Un avertissement, enfin : les considérations de coût computationnel abordées dans cet ouvrage sont indicatives. Les prix du matériel, les tarifs cloud et les performances des puces évoluent rapidement. Les ordres de grandeur donnés visent à fournir une intuition, non à constituer un devis. De même, les questions éthiques liées à la génération d'images — consentement des données d'entraînement, biais représentationnels, usages malveillants — sont évoquées mais ne sauraient être traitées exhaustivement dans un ouvrage technique. J'encourage le lecteur à consulter les travaux dédiés à ces enjeux sociétaux.

### En route

Le token est une abstraction. Le pixel est une réalité physique. Entre les deux, il y a un choix d'ingénierie, un compromis informationnel, une architecture. Ce livre est l'histoire de ce passage. Commençons par le commencement : comprendre ce qu'est un token, ce qu'est un pixel, et pourquoi leur rencontre est à la fois si naturelle et si délicate.

Bonne lecture.

## Chapitre 1 — Anatomie d'un LLM : de l'embedding au next-token prediction

Un grand modèle de langage n'a jamais vu un mot. Au niveau de ses opérations internes, il n'a jamais vu non plus une phrase, une langue ou un sens. Il voit des entiers.

L'entrée est une suite d'identifiants. La sortie est une distribution de probabilité sur un ensemble fini d'identifiants. Entre les deux, des multiplications de matrices, une normalisation, une fonction non linéaire, et encore des multiplications de matrices. Tout le reste — la grammaire, la logique, la capacité à résumer un contrat ou à corriger une fonction Python — émerge de l'optimisation de cette fonction numérique sur un volume considérable de séquences.

C'est précisément cette austérité opérationnelle qui rend le projet de ce livre possible. Si le moteur ne sait traiter que des entiers ordonnés, rien dans son architecture n'interdit que ces entiers désignent autre chose que des fragments de texte. Un indice dans un *codebook* visuel est un entier comme un autre. On peut l'envoyer dans la même table d'embedding, le faire circuler dans les mêmes couches d'attention, et le prédire avec la même tête de sortie.

Mais cette possibilité architecturale ne doit pas être confondue avec une facilité statistique. Le moteur est neutre ; les données ne le sont pas. Une image n'a pas la même redondance, la même locality, ni la même tolérance à l'erreur qu'une phrase. Le propos de ce chapitre est de disséquer le moteur avec suffisamment de précision pour que, lorsque nous y introduirons des tokens visuels, nous sachions exactement quelles hypothèses nous conservons et lesquelles nous brisons.

### 1.1 L'interface discrète : ce que le modèle consomme vraiment

Un LLM ne manipule pas du texte. Il manipule une suite $x_{1:T} = (x_1, x_2, \ldots, x_T)$ où chaque $x_t$ appartient à un vocabulaire fini $\mathcal{V} = \{0, 1, \ldots, |\mathcal{V}|-1\}$. Le passage du caractère à cet entier est assuré par un tokenizer, le plus souvent de type *byte-pair encoding* — BPE, une algorithme de fusion statistique décrit par Sennrich et ses collaborateurs [Sennrich et al., 2016].

Le BPE part d'un alphabet de bytes et fusionne récursivement les paires les plus fréquentes dans le corpus d'entraînement. Il en résulte un vocabulaire hybride : certains indices correspondent à des mots entiers, d'autres à des sous-mots, d'autres à des fragments orthographiques ou à des séquences d'octets. Un terme technique rare peut occuper cinq positions dans la séquence ; un article fréquent en occupe une. De cette simple asymétrie découlent des conséquences pratiques que nous retrouverons au chapitre 16 : la longueur d'une séquence n'est pas une mesure du nombre de mots, et la densité informationnelle varie considérablement d'un token à l'autre.

Deux remarques méritent d'être fixées dès maintenant.

Premièrement, **un token n'est pas une unité sémantique**. C'est une unité de compression séquentielle. Pensser le token comme « un mot » est une heuristic commode pour le lecteur, mais une erreur pour l'ingénieur : le modèle ne dispose d'aucun privilège architectural sur les boundaries lexicales.

Deuxièmement, **l'entier lui-même ne porte pas de sens**. L'indice 4 821 n'est ni « plus proche » de 4 822 que de 912. La numérotation est un convention d'adressage. Toute la géométrie sémantique est portée par la table d'embedding :

$$
h^{(0)}_t = E[x_t], \qquad E \in \mathbb{R}^{|\mathcal{V}| \times d}.
\tag{1.1}
$$

Cette table est l'unique point de contact entre le monde discret et le monde continu. Elle assigne à chaque indice un vecteur de $d$ réels, appris par rétropropagation. Deux tokens qui apparaissent dans des contextes semblables voient leurs vecteurs converger vers des régions voisines de $\mathbb{R}^d$ — non parce que quelqu'un l'a prescrit, mais parce que c'est une solution économique pour le modèle.

Certaines architectures multiplient ensuite ce vecteur par $\sqrt{d}$ pour équilibrer les échelles avec les couches suivantes ; d'autres non. C'est un détail d'implémentation, mais un détail qui peut faire échouer un transfert de poids si on l'omet.

Pour notre projet, un troisième élément est décisif : les **tokens spéciaux**. Les LLM modernes disposent d'indices réservés marquant le début et la fin d'un document, le rôle d'un interlocuteur, ou la fin d'une génération. Ces jetons sont la couture sur laquelle nous coudrons la modalité visuelle. Un marqueur `<img_start>`, suivi de deux cents indices de codebook, puis d'un marqueur `<img_end>`, n'est pour le transformeur qu'une séquence parfaitement ordinaire. Le chapitre 14 exploitera cette coutrure en détail.

### 1.2 La position : donner un ordre à un ensemble

L'attention telle qu'introduite par Vaswani et ses collaborateurs [Vaswani et al., 2017] est, sans dispositif supplémentaire, insensible à l'ordre des éléments. Permuter la séquence permute le résultat de la même manière : aucun mécanisme ne dit à la couche « ce token vient avant celui-là ».

Or l'ordre est précisément ce qui fait d'une suite de tokens un énoncé. « Le chat poursuit le chien » et « le chien poursuit le chat » contiennent les mêmes éléments dans des ordres différents. Le modèle doit donc recevoir l'information positionnelle explicitement.

Trois familles de solutions coexistent. Les *embeddings positionnels appris* attribuent à chaque rang un vecteur entraîné, ajouté à l'embedding du token. Les *encodages sinusoïdaux* utilisent des fonctions périodiques fixes de différentes fréquences. La troisième, aujourd'hui dominante dans les modèles ouverts, est la *RoPE* — *Rotary Position Embedding* [Su et al., 2021] — qui n'ajoute rien au vecteur mais rotationne les requêtes et les clés dans des sous-espaces de deux dimensions.

Pour un indice de fréquence $r$, la RoPE définit une angle $\theta_r = b^{-2r/d_h}$, où $d_h$ est la dimension d'une tête et $b$ une base généralement grande. Le vecteur de requête à la position $m$ est rotationné de $m\theta_r$, celui de clé à la position $n$ de $n\theta_r$. La propriété essentielle est que leur produit scalaire ne dépend alors que du décalage $m-n$ :

$$
\tilde{q}_m^{\top} \tilde{k}_n \;=\; \operatorname{Re} \sum_r q_{m,r}\,\overline{k_{n,r}}\; e^{\mathrm{i}(m-n)\theta_r}.
\tag{1.2}
$$

Le modèle apprend ainsi des relations relatives — « deux positions plus loin », « bien plus tôt dans le contexte » — plutôt que des coordonnées absolues. C'est un inducteur puissant, et c'est aussi un piège pour la génération d'images.

Une image n'est pas une ligne. C'est une grille. Lorsque nous aplatirons une carte latente $16 \times 16$ en une séquence de 256 éléments, la RoPE unidimensionnelle verra deux patches adjacents verticalement comme séparés de seize positions, alors que deux patches adjacents horizontalement ne seront séparés que d'une. Cette distorsion n'est pas fatale : le modèle peut l'apprendre. Mais elle gaspille de la capacité et ralentit la convergence.

Nous verrons au chapitre 11 comment factoriser l'encodage positionnel en deux axes, et au chapitre 8 comment la patchification elle-même constitue un choix d'induction spatiale. Pour l'instant, retenez seulement ceci : **l'ordre de balayage n'est pas un détail d'implémentation, c'est une hypothèse structurelle sur le monde**.

### 1.3 Le bloc transformeur : lire et écrire dans un résidu

Un LLM décodeur standard empile des blocs identiques dans leur forme et distincts dans leurs paramètres. Chaque bloc consomme un tenseur $h \in \mathbb{R}^{T \times d}$ et en produit un autre de même forme. La structure moderne est dite *pré-norm* : on normalise avant chaque sous-module, et on ajoute le résultat à l'entrée.

$$
h' = h + \mathrm{Attn}\big(\mathrm{Norm}(h)\big), \qquad
h'' = h' + \mathrm{FFN}\big(\mathrm{Norm}(h')\big).
\tag{1.3}
$$

La normalisation est le plus souvent une RMSNorm, qui divise le vecteur par la racine de sa moyenne quadratique puis le rescale par un vecteur appris $g$ :

$$
\mathrm{RMSNorm}(z) = \frac{z}{\sqrt{\frac{1}{d}\sum_{j=1}^{d} z_j^2 + \varepsilon}} \odot g.
\tag{1.4}
$$

Contrairement à une LayerNorm classique, elle ne recentre pas les activations. C'est un choix d'efficacité, pas une hypothèse sur la nature du langage.

**L'attention.** On projette les représentations normalisées en trois familles de vecteurs — requêtes $Q$, clés $K$, valeurs $V$ — puis on calcule :

$$
\mathrm{Attn}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_h}} + M\right)V.
\tag{1.5}
$$

Le masque causal $M$ vaut zéro lorsque la position consultée est antérieure ou égale à la position courante, et $-\infty$ sinon. Il garantit qu'aucune information du futur ne fuit dans la prédiction du présent. Cette contrainte est ce qui permet d'entraîner sur toute la séquence en un seul passage, tout en définissant une véritable distribution autorégressive.

La division par $\sqrt{d_h}$ stabilise les logits avant le softmax : sans elle, la variance des produits scalaires croît avec la dimension et pousse l'attention vers des distributions dégénérées. Multiple heads signifie simplement que l'on répète l'opération dans plusieurs sous-espaces, puis que l'on concatène les résultats avant une projection de sortie.

Une variante importante pour la suite : le *grouped-query attention*, où plusieurs têtes de requête partagent une même clé et une même valeur. Le coût mémoire du cache d'inférence en est réduit proportionnellement. Nous y reviendrons au chapitre 23 ; sachez dès maintenant qu'un modèle à 7 milliards de paramètres peut voir son cache divisé par quatre par ce seul choix.

**Le réseau feed-forward.** Après l'attention, chaque position est traitée individuellement par un petit réseau à deux couches. Les architectures récentes utilisent une gating de type SwiGLU :

$$
\mathrm{FFN}(z) = W_d\big(\mathrm{SiLU}(W_g z) \odot (W_u z)\big).
\tag{1.6}
$$

Trois matrices au lieu de deux, mais une nonlinearité plus expressive. Shazeer a discuté cette famille de gates dans un article court et influent [Shazeer, 2020].

**Le résidu.** L'équation (1.3) mérite une lecture particulière. Le tenseur $h$ n'est pas écrasé à chaque couche : il est enrichi. Chaque bloc lit une partie de $h$ via ses projections, calcule une correction, et l'ajoute. Cette métaphore du *résidu* comme bande passante commune — une sorte de tableau noir sur lequel les couches écrivent et se relisent — n'est pas une description mécaniste définitive, mais c'est un modèle mental remarquablement utile.

Pour notre projet, il suggère où intervenir : ajouter une modalité ne nécessite pas de remplacer le tableau noir, seulement d'apprendre à y écrire un nouveau type d'information sans effacer l'ancien. C'est exactement la tension que nous étudierons au chapitre 17.

**Où sont les paramètres ?** À titre d'exemple, la configuration ouverte usuellement désignée comme LLaMA-2 7B [Touvron et al., 2023] présente les ordres de grandeur suivants :

| Composant | Calcul | Ordre de grandeur |
|---|---|---|
| Table d'embedding | $32\,000 \times 4\,096$ | 131 M |
| Attention par couche | $4d^2$ | 67 M |
| Feed-forward par couche | $3 \times d \times d_{ff}$, $d_{ff}=11\,008$ | 135 M |
| 32 blocs complets | $32 \times 202$ M | 6,47 B |
| Tête de sortie non partagée | $4\,096 \times 32\,000$ | 131 M |

Le total approche 6,7 milliards. Deux constatations en découlent. D'abord, la majeure partie des paramètres n'est pas dans l'interface discrète mais dans le traitement contextuel : c'est là que réside la capacité de modélisation. Ensuite, la table d'embedding et la tête de sortie représentent un volume non négligeable — environ 4 % chacune. Lorsque nous agrandirons le vocabulaire avec des tokens visuels, ce coût n'est pas annexe.

### 1.4 La tête de sortie : d'un vecteur à une distribution

Au sommet du réseau, une dernière normalisation précède une projection linéaire vers le vocabulaire :

$$
z_t = W_U\,\mathrm{Norm}(h_t), \qquad W_U \in \mathbb{R}^{|\mathcal{V}| \times d},
\tag{1.7}
$$

$$
p_\theta(x_{t+1} \mid x_{1:t}) = \mathrm{softmax}(z_t).
\tag{1.8}
$$

Les $z_t$ sont les *logits* : des scores réels, non normalisés, dont le softmax fait une distribution. Notez l'alignement : la sortie à la position $t$ prédit le token à la position $t+1$. Ce décalage d'une unité, apparemment anodin, est une source classique de bugs dans les implémentations multimodales. Nous le reverrons dans le protocole du chapitre 22.

Dans de nombreuses architectures, $W_U$ est lié à la table d'embedding $E$ : les mêmes vecteurs servent à encoder l'entrée et à scorer la sortie. Cette *weight tying* réduit le nombre de paramètres et impose une géométrie cohérente entre ce que le modèle reconnaît et ce qu'il produit. Pour un vocabulaire visuel, la question du partage devient un choix de design à part entière, discuté au chapitre 14.

**De la distribution au token.** La prédiction la plus probable n'est pas nécessairement le choix souhaitable. Le *greedy decoding* sélectionne $\arg\max$ ; l'échantillonnage tire selon la distribution, éventuellement temperée :

$$
p_i \propto \exp(z_i / \tau).
$$

Une température $\tau < 1$ accentue le pic ; $\tau > 1$ aplati la distribution. Les filtres *top-k* et *top-p* restreignent l'échantillonnage aux candidats les plus plausibles.

Pour le texte, ces leviers contrôlent la créativité. Pour l'image, ils contrôlent autre chose : la texture, la diversité des modes, la stabilité de la composition. Une température trop basse tend à produire des surfaces lisses et répétitives ; une température trop élevée désorganise la scène. Il n'existe pas de valeur universelle, ce qui explique pourquoi les protocoles sérieux prévoient une grille de températures plutôt qu'un réglage unique hérité du langage.

**Le coût de la génération.** Une fois la séquence de contexte traitée, on peut conserver pour chaque couche les clés et les valeurs déjà calculées : c'est le *KV cache*. Générer un token supplémentaire ne requiert alors qu'une passe sur un seul vecteur, et non sur toute la séquence.

La mémoire du cache suit une loi simple :

$$
\text{Mémoire} = 2 \cdot L \cdot T \cdot n_{kv} \cdot d_h \cdot b,
\tag{1.9}
$$

où $L$ est le nombre de couches, $T$ la longueur, $n_{kv}$ le nombre de têtes de clé/valeur, et $b$ le nombre d'octets par élément. Avec 32 couches, 32 têtes, une dimension de tête de 128 et du demi-précision, on obtient environ 0,5 Mio par position. Une séquence de 4 096 positions consomme donc près de 2 Go de cache — pour un seul utilisateur.

Cette équation sera l'une des plus utiles de l'ouvrage. Elle explique pourquoi la résolution d'une image, via le nombre de tokens qu'elle impose, se traduit directement en coût mémoire et en latence.

### 1.5 L'objectif : la cross-entropie comme contrat

L'entraînement d'un LLM repose sur une fonction objectif d'une sobriété trompeuse :

$$
\mathcal{L}(\theta) = -\frac{1}{T}\sum_{t=1}^{T} \log p_\theta\!\left(x_t \mid x_{<t}\right).
\tag{1.10}
$$

On minimise la négatif log-vraisemblance moyen des tokens observés. Le *teacher forcing* consiste à fournir au modèle la séquence réelle comme contexte, plutôt que sa propre génération précédente. Grâce au masque causal, toutes les positions peuvent être supervisées simultanément : un unique passage avant et un passage arrière entraînent le modèle à prédire chaque token à partir de son préfixe.

C'est un point crucial pour la suite. **L'entraînement autorégressif est parallèle dans le temps ; l'inférence autorégressive ne l'est pas.** Cette asymétrie explique pourquoi un modèle peut être entraîné efficacement sur des séquences longues alors que sa génération reste séquentielle et coûteuse. Le chapitre 12 explorera les architectures qui cherchent à briser cette contrainte.

La cross-entropie possède une interprétation informationnelle exacte. Si $p^\star$ désigne la véritable distribution des séquences, alors :

$$
\mathcal{L}(\theta) = H(p^\star) + \mathbb{E}_{x \sim p^\star}\!\left[D_{KL}\big(p^\star(\cdot \mid x_{<t}) \,\|\, p_\theta(\cdot \mid x_{<t})\big)\right].
\tag{1.11}
$$

Le premier terme est une constante incompressible : l'entropie intrinsèque du données. Le second mesure l'excès de redondance du modèle. Minimiser la perte, c'est réduire cet écart — jamais faire disparaître le premier terme.

La *perplexité*, $\exp(\mathcal{L})$, est une reformulation commode : elle se lit comme un nombre effectif de choix auxquels le modèle est confronté à chaque position. En divisant la perte par $\ln 2$, on obtient directement un nombre de bits par token. Ce conversion sera notre outil principal au chapitre 3.

**Que se passe-t-il quand le vocabulaire devient multimodal ?** L'équation (1.10) ne change pas formellement. Mais sa pondération implicite, si. Dans un corpus mélangeant texte et images, chaque image contribue plusieurs centaines de positions visuelles contre quelques dizaines de positions textuelles. Une loss moyenne non pondérée devient donc un objectif majoritairement visuel, même si le corpus est majoritairement textuel en volume sémantique.

Trois stratégies coexistent : masquer certaines positions de la perte en les marquant comme ignorées ; pondérer les deux familles de tokens ; ou séparer les phases d'entraînement. Aucune n'est neutre. Le chapitre 16 les compare en termes de stabilité et de rétention des capacités linguistiques.

### 1.6 Quand les tokens ne sont plus des mots

Nous pouvons maintenant identifier précisément les hypothèses que le passage à l'image vient briser. Elles sont au nombre de quatre, et chacune irriguera plusieurs chapitres.

**Première rupture : la géométrie du vocabulaire.** Dans un vocabulaire BPE, les indices n'ont aucune structure intrinsèque ; toute la géométrie est apprise dans $E$. Dans un codebook visuel issu d'une quantification vectorielle, les indices correspondent à des vecteurs centraux qui possèdent déjà une métrique : deux codes voisins dans l'espace latent sont, par construction, des représentations semblables d'un même contenu visuel.

Cette structure est à la fois une opportunité et une contrainte. Une opportunité, car le modèle peut exploiter une similarité préexistante plutôt que l'apprendre ex nihilo. Une contrainte, car la répartition des fréquences est souvent très inégale : quelques codes dominent, d'autres presque jamais utilisés. Nous verrons au chapitre 7 comment ce déséquilibre conduit à l'effondrement du codebook.

Une subtilité mérite d'être signalée : réindexer bijectivement un codebook ne change pas la classe de distributions représentables. Cela change néanmoins la géométrie d'initialisation de la table d'embedding et de la tête de sortie, donc la dynamique d'optimisation. Deux implémentations mathématiquement équivalentes peuvent converger vers des qualités très différentes.

**Deuxième rupture : la nature de la dépendance.** Le texte présente une localité forte et une structure hiérarchique : la fin d'une phrase dépend de son début, mais souvent par l'intermédiaire de quelques entités saillantes. Une image présente une localité bidimensionnelle et des contraintes globales : l'ombre portée en bas à droite doit correspondre à une source de lumière définie en haut à gauche.

L'aplatissement raster transforme cette géométrie en une chaîne où les relations longues deviennent littéralement longues. L'attention peut les apprendre, mais elle n'y est pas induite. D'où l'importance des chapitres 11 et 13.

**Troisième rupture : le coût de l'erreur.** Une erreur de token dans du texte est souvent locale et réparable : un mot mal choisi n'empêche pas la phrase suivante d'être correcte. Dans une image générée token par token, une erreur précoce est une décision structurelle qui conditionne tout la suite. Le modèle qui place un bord d'objet au mauvais endroit ne pourra pas le déplacer ensuite ; il devra accommoder le reste de la scène autour de cette erreur.

C'est le *exposure bias* — le décalage entre un entraînement sur préfixes réels et une inférence sur préfixes auto-produits — qui prend ici une dimension nouvelle. En génération d'images, il ne se manifeste pas seulement par une dégradation progressive de la qualité, mais par des incohérences globales : deux perspectives, trois sources de lumière, un objet dédoublé.

**Quatrième rupture : ce que mesure la perte.** La cross-entropie pénalise uniformément chaque erreur d'indice. L'œil, lui, ne pénalise pas uniformément chaque erreur de patch. Confondre deux codes représentant des textures de feuillage proches est perceptuellement bénin ; confondre un code de ciel avec un code de contour sombre est catastrophique.

Deux modèles peuvent donc afficher une perte identique et produire des images de qualité très différente. C'est sans doute la leçon la plus importante de ce chapitre : **la perte d'entraînement n'est pas une mesure de qualité visuelle**. Elle est un signal d'optimisation, pas un verdict. Le chapitre 18 sera consacré aux métriques qui tentent de combler cet écart.

Le tableau suivant résume ces ruptures.

| Dimension | Texte | Image tokenisée |
|---|---|---|
| Unité de base | Fragment orthographique | Patch latent quantifié |
| Structure du vocabulaire | Arbitraire, géométrie apprise | Métrique préexistante dans l'espace latent |
| Topologie des dépendances | Linéaire, hiérarchique | Bidimensionnelle, avec contraintes globales |
| Tolérance à l'erreur | Locale, souvent rattrapable | Structurelle, accumulative |
| Objectif de qualité | Fidélité sémantique locale | Cohérence perceptuelle globale |
| Métrique naturelle | Perplexité, exactitude | FID, CLIP-score, évaluation humaine |

### 1.7 Premier calcul : une image 256 × 256 coûte combien ?

Avant d'écrire une ligne d'entraînement, faisons un compte. Ce type de calcul, fait tôt, évite des semaines d'égarement.

Prenons une image de $256 \times 256$ pixels en RVB 8 bits. Sa représentation brute occupe :

$$
256 \times 256 \times 3 \times 8 = 1\,572\,864 \text{ bits}.
$$

Appliquons maintenant un auto-encodeur quantifié avec un facteur de compression spatial de 16. La carte latente mesure $16 \times 16$, soit 256 positions. Avec un codebook de 1 024 entrées, chaque position tient sur $\log_2 1024 = 10$ bits. La séquence visuelle complète occupe donc 2 560 bits.

Le facteur de compression est d'environ 614.

Il faut immédiatement nuancer ce chiffre : il ne signifie pas que l'image contient 1,57 million de bits d'information. Il signifie que sa représentation brute utilise 1,57 million de bits, dont une immense partie est redondante. Toute la question de la tokenisation visuelle est de savoir quelle partie de cette redondance peut être supprimée sans perdre ce qui compte perceptuellement. Le chapitre 2 posera les outils pour y répondre.

Traduisons maintenant en coût de calcul. Ajoutons un prompt textuel de 64 tokens et deux marqueurs spéciaux : la séquence complète compte 322 positions. Avec la configuration évoquée plus haut, le KV cache représente environ 161 Mio. Les poids du modèle en demi-précision occupent près de 13 Go. La génération de l'image exige 256 passes avant séquentielles.

Si le facteur de compression passe de 16 à 8, la carte latente devient $32 \times 32$ : 1 024 tokens, soit quatre fois plus de passes, quatre fois plus de cache, et un coût d'attention qui croît plus vite encore à cause du terme quadratique. **La résolution ne coûte pas linéairement : elle coûte au moins quadratiquement dans le pire cas.**

Voici à quoi ressemble l'ossature d'un pas d'entraînement, une fois le vocabulaire visuel intégré :

```python
# x : indices de tokens, forme (B, T), texte et image mêlés
h = embed(x) * math.sqrt(d)            # (B, T, d)
h = backbone(h, mask=causal_mask)      # (B, T, d)
logits = head(normalize(h))            # (B, T, |V|)

# La sortie en t doit prédire l'entrée en t+1.
loss = cross_entropy(
    logits[:, :-1, :].reshape(-1, vocab_size),
    x[:, 1:].reshape(-1),
    ignore_index=-100,                 # positions non supervisées
)
```

Et l'ossature de la génération :

```python
cache = None
tokens = [bos_id, *prompt_ids, img_start_id]

for _ in range(n_visual_tokens):
    logits, cache = step(tokens[-1:], cache)
    logits = logits[:, -1, visual_slice]   # restreindre au codebook
    next_id = sample(temperature_and_top_p(logits))
    tokens.append(next_id)

image = visual_tokenizer.decode(tokens[len(prompt_ids) + 1:])
```

Deux lignes méritent une attention particulière. La première est `ignore_index` : c'est par ce mécanisme que l'on choisit quelles positions contribuent à la perte. La seconde est `visual_slice` : rien n'oblige la tête de sortie à rester libre sur l'ensemble du vocabulaire pendant la génération d'une image. En masquant les logits textuels entre les marqueurs visuels, on garantit que le modèle ne peut pas produire un token qui n'a pas de décodage image. Cette contrainte simple élimine une classe entière de bugs.

### 1.8 Diagnostic : quand la perte ment

Un LLM adapté à la génération d'images peut échouer de nombreuses manières, et certaines sont contre-intuitives. Voici les cinq signatures que j'ai toujours cherché à distinguer en premier, parce qu'elles orientent le diagnostic vers des causes très différentes.

| Signature observée | Cause probable à vérifier en premier |
|---|---|
| Perte élevée et plate dès l'initialisation | Décalage d'une position entre logits et cibles ; indices visuels mal alignés avec la table d'embedding |
| Perte très basse, images bruitées ou incohérentes | Bug de décodage : ordre de balayage inversé, normalisation du décodeur incorrecte, mauvaise reshape de la carte latente |
| Images structurées mais textures répétitives | Goulot d'étranglement du codebook : trop peu de codes, ou effondrement d'une partie des entrées |
| Motifs périodiques ou seams visibles | Inadéquation entre l'encodage positionnel 1D et la topologie 2D de la grille |
| Détérioration du texte après adaptation visuelle | Oubli catastrophique : taux d'apprentissage trop élevé sur les poids partagés, absence de régularisation ou de replay textuel |

La deuxième ligne est la plus frustrante, car elle ressemble à un succès du point de vue de l'optimisation. Un modèle peut parfaitement apprendre à prédire une séquence de codes que le décodeur restitue ensuite dans le désordre. La perte ne le saura jamais. Seul un contrôle visuel régulier, sur un ensemble fixe de prompts, révèle ce type de rupture.

C'est pourquoi je recommande une discipline simple dès le premier jour d'expérimentation : fixer une douzaine de prompts, les conserver inchangés pendant toute la durée du projet, et visualiser leurs générations à intervalles réguliers. Pas les prompts d'évaluation finale. Une petite collection personnelle, représentative des cas que vous souhaitez maîtriser. La courbe de perte vous dit si l'optimisation progresse ; cette planche visuelle vous dit si le modèle comprend ce que vous lui demandez.

Le chapitre 21 généralisera cette démarche en méthodologie d'ablation : modifier un seul facteur à la fois, conserver les mêmes graines, et documenter ce qui ne change pas autant que ce qui change.

### 1.9 Ce qu'il faut emporter

Ce chapitre a volontairement traité le LLM comme ce qu'il est opérationnellement : une machine à prédire des entiers conditionnés par un préfixe. Quelques idées doivent maintenant être solidement ancrées.

L'interface discrète est une table d'adressage, pas une ontologie. Toute la sémantique — linguistique ou visuelle — est portée par des vecteurs appris. L'attention est un mécanisme de mélange conditionnel, rendu causal par un masque, et positionnel par un encodage externe ou par rotation. Le résidu est un espace de computation partagé dans lequel on peut apprendre à écrire une nouvelle modalité. La tête de sortie transforme un vecteur en distribution, et le choix d'échantillonnage fait partie intégrante de la définition du modèle.

L'objectif de cross-entropie est un contrat mathématiquement propre mais perceptuellement aveugle. Il faut le compléter par des évaluations qui parlent le langage de l'image.

Enfin, le coût de génération est une fonction directe du nombre de tokens. Ce chiffre — 256, 1 024, 4 096 — est probablement la variable la plus déterminante de tout le projet. Il conditionne la mémoire, la latence, la longueur de contexte nécessaire, et la faisabilité même de l'entraînement.

Nous savons maintenant ce qu'est un token du point de vue du moteur. Il nous reste à comprendre ce qu'est un pixel du point de vue du signal : sa redondance, son entropie, sa structure fréquentielle, et la quantité d'information qu'il faut réellement conserver pour qu'une image paraisse juste. C'est l'objet du chapitre suivant.