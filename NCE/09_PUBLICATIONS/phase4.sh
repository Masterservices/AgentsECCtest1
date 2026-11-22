#!/bin/bash
# RTC — génération des tomes de fondation T1 à T4 : plan (Dialagram, sous contraintes), rédaction, nettoyage, PDF.
# Claude écrit seulement les consignes ci-dessous, puis relit chaque tome avant publication.
O=/home/user/agentsecctest1/bibliotheque/outils
D=/home/user/agentsecctest1/NCE/09_PUBLICATIONS
REGLES="RÈGLES ABSOLUES : (1) ne citer QUE les références de la liste ci-dessous, avec l'auteur et l'année indiqués ; n'en inventer aucune ; aucun DOI, aucun numéro de page, aucune citation entre guillemets attribuée à un chercheur ; (2) ne jamais présenter une intuition comme une preuve ; donner des preuves complètes pour les résultats démontrés dans le livre, et pour les grands théorèmes connus donner l'idée de la preuve en le disant ; (3) chaque affirmation porte un statut : PROUVÉ, CONNU, EXPÉRIMENTAL, CONJECTURE, RÉFUTÉ ou OUVERT ; (4) aucune annonce de découverte ; (5) formules en LaTeX entre \$...\$ ou \$\$...\$\$ ; (6) lecteur cultivé non spécialiste : intuition, définition, énoncé, exemple, exercice ; (7) dernier chapitre : « Transfert vers le programme RTC » (ce que ce tome apporte à l'étude des traductions à ressources : quelles ressources, quelles traductions, quelles questions ouvertes)."

livre() {  # $1 dossier, $2 titre, $3 sujet, $4 références
  mkdir -p $D/$1 && cd $D/$1
  cat > brief_plan.txt <<EOF
Tu es l'auteur, pour le compte d'Oussama Ghorbel, d'un livre de la collection scientifique « Les Traductions du Calcul » (programme de recherche RTC : étudier quelles ressources — taille, temps, mémoire, profondeur, largeur, précision, partage — chaque traduction entre modèles de calcul conserve ou perd). Titre : « $2 ». Sujet : $3

$REGLES

Références autorisées (et seulement elles) : $4

Conçois le plan d'un livre d'environ 220 pages : 4 parties, 16 chapitres (le 16e est le transfert vers RTC), 4 à 6 sections par chapitre, exercices. Réponds UNIQUEMENT avec un JSON valide, sans balises markdown :
{"titre":"$2","sous_titre":"...","these":"...","cadre":{"nom":"Les traductions à ressources et le registre des statuts","description":"(recopie ici intégralement les règles absolues ci-dessus et la liste des références autorisées)"},"bibliographie":[{"auteur":"...","titre":"...","annee":"...","idee":"...","apport":"..."}],"parties":[{"titre":"...","chapitres":[{"numero":1,"titre":"...","objectif":"...","sections":["..."],"exercices":["..."]}]}]}
EOF
  for i in 1 2 3; do
    [ -s plan.json ] && break
    python3 $O/ask.py brief_plan.txt plan_raw.txt
    python3 -c "
import json;t=open('plan_raw.txt').read().strip()
if t.startswith('\`\`\`'): t=t.split('\n',1)[1].rsplit('\`\`\`',1)[0]
p=json.loads(t);assert sum(len(x['chapitres']) for x in p['parties'])>=14
json.dump(p,open('plan.json','w'),ensure_ascii=False,indent=1)" 2>/dev/null || rm -f plan.json
  done
  [ -s plan.json ] || { echo "$1 ERREUR plan"; return; }
  python3 -u $O/redaction.py plan.json chapitres --parallele 4 > redaction.log 2>&1
  python3 -u $O/nettoyage.py chapitres chapitres_v2 > nettoyage.log 2>&1
  python3 $O/mise_en_page.py plan.json chapitres_v2 livre.pdf --corps 11.3 > pdf.log 2>&1
  echo "$1 FIN $(ls chapitres_v2/*.md 2>/dev/null | wc -l) fichiers ; $(tail -1 pdf.log)"
}
REGLES="$REGLES (8) livre RICHE EN FORMULES : chaque chapitre contient au moins 15 formules en LaTeX (display \$\$...\$\$), avec énoncé, conditions, statut et exemple numérique calculé pas à pas ; tables de vérité ternaires complètes là où elles servent. (9) HONNÊTETÉ : le ternaire ne change aucune classe de complexité ; le livre doit le dire clairement et montrer où il gagne et où il perd."
livre Ternaire "Bits et Trits : le Calcul Ternaire Équilibré" "le calcul en base 3 équilibrée, avec trits valant 1, 0 et T (= -1), comparé au calcul binaire, dans le cadre des traductions à ressources : représentation des entiers en ternaire équilibré (négation par échange de 1 et T, arrondi par troncature), logiques à trois valeurs (Łukasiewicz, Kleene), portes ternaires (négation, min, max, somme modulo 3, demi-additionneur et additionneur complet ternaires avec retenue dans {T,0,1}), économie de radix (coût base fois nombre de chiffres, optimum en e, gain de 5,4 % de la base 3 sur la base 2, PROUVÉ), traductions ternaire vers binaire (deux bits par trit, codage double rail) et binaire vers ternaire, neurones à seuil à poids {-1,0,1} et réseaux à poids ternaires (BitNet b1.58), trits et SAT. Résultats de l'investigation INV-02 du programme, à reprendre avec leurs statuts EXACTS : lemme L-T2 PROUVÉ (les traductions ternaire-binaire coûtent un facteur constant en taille, profondeur et largeur, donc aucune classe ne change) ; EXPÉRIMENTAL (circuits classiques non minimaux, n au plus 16) : en portes ternaires natives le ternaire est plus petit (facteur 0,61 pour l'addition, 0,35 pour la multiplication), mais ramené en portes binaires il perd (facteur 2,7 pour l'addition, 1,65 pour la multiplication à n=8), égalité pour la comparaison (124 contre 128 portes), gain net seulement pour l'opposé (0 porte contre 49) et pour x modulo 3 (0 contre 123) ; PROUVÉ : circuits binaires minimaux des portes ternaires trouvés par SAT, la négation gratuite est une propriété du codage double rail et non du ternaire, et ces circuits ne sont corrects que sur des codes valides (sans contrainte, le miter est satisfaisable) ; EXPÉRIMENTAL : sur le miter de commutativité du multiplieur, le coût du solveur suit l'information et non la base (143 000 à 167 000 conflits pour 5 trits contre 8 bits, 4 encodages, 3 graines) ; lemme L-T1 PROUVÉ : des poids {-1,0,1} suffisent pour compiler tout circuit en neurones à seuil, 3 neurones par OU exclusif, environ 25 % de neurones de plus que le lemme L-03, largeur inchangée ; PROUVÉ par recherche exhaustive : un seul neurone caché à poids ternaires ne suffit pas pour le OU exclusif. Verdict à donner : le ternaire est un changement de codage, utile pour certaines opérations et pour la quantification des réseaux, pas un changement de puissance de calcul." "Łukasiewicz 1920 (O logice trójwartościowej — Sur la logique à trois valeurs) ; Shannon 1948 (A mathematical theory of communication) ; McCulloch et Pitts 1943 (A logical calculus of the ideas immanent in nervous activity) ; Kleene 1952 (Introduction to Metamathematics) ; Tseitin 1968 (On the complexity of derivation in propositional calculus) ; Knuth 1969 (The Art of Computer Programming, Volume 2: Seminumerical Algorithms) ; Hayes 2001 (Third base) ; Bogdanov et al. 2007 (PRESENT: an ultra-lightweight block cipher) ; Courbariaux, Bengio et David 2015 (BinaryConnect: training deep neural networks with binary weights during propagations) ; Li, Zhang et Liu 2016 (Ternary weight networks) ; Zhu, Han, Mao et Dally 2017 (Trained ternary quantization) ; Ma et al. 2024 (The era of 1-bit LLMs: all large language models are in 1.58 bits)"
