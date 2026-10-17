# L'usine à livres sur ton PC allumé en permanence

Ce qu'il faut sur le PC : **Docker, rien d'autre.** Pas besoin d'installer Claude, ni Claude Cowork, ni Python.
Le PC lance la boucle de l'usine ; Qwen (via Dialagram) fait le travail ; Claude n'est qu'un réveil optionnel,
déclenché depuis le cloud, sans rien installer.

## Installation (10 minutes)

1. Installer Docker : https://www.docker.com/products/docker-desktop (Windows/Mac) ou `docker` + `docker compose` (Linux).
   Dans Docker Desktop : réglage « Start Docker Desktop when you sign in » activé, pour qu'il démarre avec le PC.
2. Empêcher la mise en veille du PC (Windows : Paramètres -> Système -> Alimentation -> « Jamais » ; Mac : Réglages ->
   Énergie ; Linux : désactiver la suspension).
3. Récupérer ce dossier `deploy/pc/` (cloner le dépôt, ou télécharger les 3 fichiers `docker-compose.yml`,
   `.env.exemple`, `LISEZMOI.md`).
4. Copier `.env.exemple` en `.env` et remplir `DIALAGRAM_API_KEY` et `GITHUB_TOKEN` (explications dans le fichier).
5. Lancer :
   ```
   docker compose up -d --build
   ```
6. Suivre le travail : `docker compose logs -f`. Arrêter : `docker compose down` (le travail est conservé).

## Comment ça marche

- Le conteneur clone le dépôt, restaure les brouillons, demande à Qwen l'ordre et le modèle de chaque livre
  (8 requêtes simultanées au plus), produit les livres, pousse chaque livre fini dans le dépôt, et sauvegarde les
  brouillons toutes les 5 minutes.
- Il redémarre tout seul (`restart: unless-stopped`) : redémarrage du PC, coupure, panne : il reprend sans perte.
- Quand tout est fini, il continue de surveiller et reprend dès qu'un nouveau sujet est ajouté.

## Réveiller Claude à la fin (optionnel)

Voir `bibliotheque/outils/DEPLOIEMENT-SERVEUR.md`, section 4 : on crée une routine sur claude.ai/code/routines avec un
déclencheur API, puis on copie son URL et son jeton dans `.env` (`ROUTINE_FIRE_URL`, `ROUTINE_FIRE_TOKEN`).
Rien à installer : c'est un appel HTTP vers le cloud de Claude.

## À savoir

- Le PC doit rester allumé, connecté à Internet et non en veille. Si tu l'éteins, l'usine s'arrête, puis reprend au
  redémarrage (Docker Desktop doit se relancer avec la session).
- Une copie du dépôt et le dossier de travail vivent dans des volumes Docker : `docker compose down -v` les efface.
- Le jeton GitHub est enregistré dans la configuration git du conteneur, sur ton PC uniquement.
