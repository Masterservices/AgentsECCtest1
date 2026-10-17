# Faire tourner l'usine sans session Claude (serveur + déclencheur Claude)

Principe : Dialagram est une API de modèles, elle ne garde pas de tâche en cours. Le travail tourne donc sur un
petit serveur toujours allumé (le calcul lourd est chez Dialagram, une machine à 1 Go suffit). L'orchestrateur Qwen
choisit les modèles, produit les livres, les pousse dans le dépôt, et réveille Claude (vérificateur) à la fin.

```
serveur (orchestrateur.py, Qwen) ──requêtes──> Dialagram
        │ push des livres et brouillons
        v
dépôt / projet web (PDF, etat.json)
        │ à chaque lot de livres terminés : POST HTTP
        v
routine Claude (déclencheur API) ──> session Claude : vérifie, améliore
```

## 1. Le serveur (Linux, n'importe quel hébergeur : VPS ~5 €/mois, Fly.io, Railway, Render, ou un PC allumé)

```bash
sudo apt-get install -y python3 python3-pip git
git clone <URL du dépôt> ~/usine && cd ~/usine && git checkout claude/millionaire-book-500-pages-kb2v7u
pip install reportlab pypdf matplotlib
# usine.sh attend le dépôt à ce chemin
sudo mkdir -p /home/user && sudo ln -sfn ~/usine /home/user/AgentsECCtest
git config user.name "Usine Dialagram" && git config user.email "usine@users.noreply.github.com"
```
Le serveur doit pouvoir pousser dans le dépôt : jeton GitHub à portée limitée (droit « Contents : écriture » sur ce seul
dépôt) enregistré avec `git config credential.helper store` puis un premier `git push`.

## 2. Les clés (fichier /etc/usine.env, jamais dans le dépôt)

```
DIALAGRAM_API_KEY=nxr-...            # obligatoire
ROUTINE_FIRE_URL=https://api.anthropic.com/v1/claude_code/routines/trig_.../fire   # optionnel : réveil de Claude
ROUTINE_FIRE_TOKEN=sk-ant-oat01-...  # optionnel : jeton de la routine
NOTIFIER_LOT=5                       # une notification Claude par lot de 5 livres terminés
```

## 3. Le service (redémarre tout seul après une panne ou un redémarrage du serveur)

/etc/systemd/system/usine.service :
```
[Unit]
Description=Usine à livres (Qwen orchestrateur)
After=network-online.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/usine
EnvironmentFile=/etc/usine.env
ExecStart=/usr/bin/python3 bibliotheque/outils/orchestrateur.py --cible restants --minutes 100000
Restart=on-failure
RestartSec=60

[Install]
WantedBy=multi-user.target
```
`sudo systemctl enable --now usine` — suivi : `journalctl -u usine -f`.
Les brouillons sont poussés toutes les 5 minutes : même si le serveur est remplacé, le travail reprend depuis le dépôt.

## 4. Le déclencheur Claude (routine)

1. Sur claude.ai/code/routines : créer une routine « Vérificateur de livres », y attacher le dépôt, avec ce prompt :
   « Tu es le vérificateur final de l'usine à livres. Le texte reçu liste les livres terminés (slugs). Pour chacun,
   lis bibliotheque/<slug>/controle.json et plan.json, lis trois chapitres de chapitres_v2 (début, milieu, fin) et
   contrôle : cohérence avec le plan, français, messages au commanditaire, chiffres non vérifiables, promesses de
   résultat, conseils médicaux/juridiques/financiers, formules LaTeX. Écris bibliotheque/<slug>/verification.md
   (note /20, constats précis, corrections recommandées) et pousse sur la branche. »
2. Dans la routine : « Add another trigger » -> API -> « Generate token ». Copier l'URL et le jeton (affichés une seule
   fois) dans /etc/usine.env.
3. Limites (API expérimentale) : 30 appels par heure et par routine, 100 par heure par compte ; chaque appel crée une
   session qui consomme l'abonnement Claude. D'où la notification par lot (NOTIFIER_LOT), pas par livre.

Sans ces deux variables, l'usine travaille quand même : Claude n'est alors simplement pas réveillé.

## Test sans rien exécuter
`python3 bibliotheque/outils/orchestrateur.py --dry` : Qwen propose le plan (ordre, modèle, parallélisme) et le script
l'affiche, sans lancer de livre.
