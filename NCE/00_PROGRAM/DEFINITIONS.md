# INV-00 — Traductions à ressources : définitions (v0.1)

Nom provisoire du programme : **RTC — Resource Translations of Computation** (« Traductions à ressources du calcul »). L'ancien nom, NCE, est abandonné pour éviter la confusion avec le « Principe d'équivalence computationnelle » de Wolfram (2002).

## D1. Modèle de calcul

Un *modèle* M est la donnée de quatre éléments :
- un ensemble d'objets (termes, machines, circuits, réseaux) ;
- une sémantique ⟦·⟧ qui associe à chaque objet une fonction partielle ou une relation ;
- une taille |·| ;
- une famille de **mesures de ressources** ρ = (ρ₁, …, ρ_k).

Exemples de mesures : temps, espace, taille, profondeur, largeur arborescente du graphe sous-jacent, bits de précision des poids, degré de partage.

SAT n'est pas un modèle : c'est un *problème* posé sur le modèle « circuits » ou « CNF » (voir FAILURES.md, F-001).

## D2. Traduction à ressources

Une traduction T : M → M' est une application calculable qui préserve la sémantique à un codage près : ⟦T(x)⟧ ≅ ⟦x⟧, ou bien l'équisatisfaisabilité pour les traductions vers SAT.

Elle est dite **(f, g)-bornée** si deux conditions sont réunies :
- |T(x)| ≤ f(|x|) ;
- pour chaque ressource suivie, ρ'_i(T(x)) ≤ g_i(ρ(x)).

Le surcoût g d'une ressource est l'objet principal d'étude du programme.

## D3. Préservation d'un invariant

Une ressource ρ est **préservée à facteur c** par T si ρ'(T(x)) ≤ c·ρ(x) + O(1), pour tout x d'une classe explicite.

Elle est **détruite** s'il existe une famille (x_n) telle que ρ(x_n) reste bornée alors que ρ'(T(x_n)) tend vers l'infini.

## D4. Équivalences indexées

On note M ≡_C M' s'il existe des traductions dans les deux sens dont les surcoûts appartiennent à la classe C. Les classes utiles sont :
- **lin** : surcoût linéaire ;
- **poly** : surcoût polynomial ;
- **param(ρ)** : la ressource ρ est préservée à facteur constant.

L'équivalence de calculabilité est le cas où l'on ne borne rien.

Ces relations ne coïncident pas. Le programme cherche **lesquelles** relient quelles paires de modèles.

## D5. Réexpression des résultats connus (critère de validation de M1)

| Résultat | Énoncé dans le cadre |
|---|---|
| Tseitin | Circuits → CNF : lin en taille ; préservation de la largeur à facteur (k+1) pour un degré d'entrée k (lemme L-01) |
| Cook-Levin | MT (temps t, espace s) → CNF : taille polynomiale ; largeur de chemin ≤ 4s+1 pour notre encodage (lemme L-02), indépendante de t |
| Pippenger-Fischer | MT → circuits : taille O(t log t) |
| Siegelmann-Sontag | MT ↔ réseaux récurrents à poids rationnels : temps lin ; la *précision* est une ressource non bornée par la simulation (et avec des poids réels, la puissance dépasse celle de la MT) |
| Compilation à seuil | Circuits → réseaux à seuil : lin en taille ; poids entiers |w| ≤ 2 ; largeur préservée à facteur (k+2) (lemme L-03) |

Ces cinq résultats s'énoncent dans le cadre sans perte apparente. Le critère de validation de M1 est donc rempli au niveau v0.1. Le reviewer hostile doit encore attaquer la définition D2, en particulier la notion de « codage » de la sémantique, trop permissive en l'état.
