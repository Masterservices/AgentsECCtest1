"""Régénère sortie/journal.md à partir des bilan.json de chaque tome terminé.
Usage : GAMMA_WORK=<dossier de travail> python3 journal.py"""
import json, os

WORK = os.environ['GAMMA_WORK']
ICI = os.path.dirname(os.path.abspath(__file__))
TOMES = [f'{l}-t{n}' for n in range(1, 11) for l in ('fr', 'ru')]
# Compteurs de t1 effacés par la revalidation locale du 25/11 : valeurs relevées avant.
USAGE_T1 = {'fr-t1': {'appels': 228, 'prompt_tokens': 2890537, 'completion_tokens': 3808603},
            'ru-t1': {'appels': 202, 'prompt_tokens': 2151960, 'completion_tokens': 2625912}}

def n(x): return f'{x:,}'.replace(',', ' ')

B = {}
for t in TOMES:
    p = f'{WORK}/{t}/bilan.json'
    if os.path.exists(p):
        B[t] = json.load(open(p))
        B[t]['usage'] = B[t].get('usage') or USAGE_T1.get(t, {})

L = ['# Édition gamma — journal', '',
     'Correction des fiches « 10 000 mots » par Dialagram (modèle qwen-3.8-max-thinking), '
     'vérification automatique de chaque fiche (script `lexique/gamma/gamma.py`).', '',
     '## Tomes terminés', '',
     '| Tome | Fiches | Conformes | Impossibles | Appels Dialagram | Tokens envoyés | Tokens reçus |',
     '|---|---|---|---|---|---|---|']
tot = [0, 0, 0, 0, 0, 0]
for t, b in B.items():
    u = b['usage']; v = [b['total'], b['corrigees'], len(b['impossibles']),
                         u.get('appels', 0), u.get('prompt_tokens', 0), u.get('completion_tokens', 0)]
    tot = [a + c for a, c in zip(tot, v)]
    L.append(f'| {t} | ' + ' | '.join(n(x) for x in v) + ' |')
L.append('| **Total** | ' + ' | '.join(f'**{n(x)}**' for x in tot) + ' |')
L += ['', 'Coût ru-t1 : seule la reprise a été mesurée. La première passe (interrompue par la limite de 2 h '
      'puis par un redémarrage du conteneur) n’a pas laissé de compteur ; son coût réel est donc supérieur.', '',
      '## Règles de tolérance appliquées', '',
      '- Exemples russes : 3 à 10 mots acceptés (le prompt de référence contient « Я хочу́ пить. »). Exemples français : 4 à 10 mots.',
      '- Accent tonique russe : au plus 1 mot polysyllabique sans accent toléré par fiche ; « ё » compte comme accentué.',
      '- Une fiche « impossible » garde sa meilleure version obtenue si elle existe, sinon la fiche source inchangée.', '',
      '## Incidents', '',
      '- ru-t1 : sauvegarde de progression tronquée par un redémarrage du conteneur ; 178 fiches récupérées, le reste refait. '
      'Le script écrit désormais sa sauvegarde de façon atomique.',
      '- ru-t1 : le contrôle des accents coupait les mots contenant « ё » ou « й » (ex. « идёт » lu « иде »), ce qui rejetait '
      'à tort des fiches correctes. Corrigé, puis revalidation locale sans nouvel appel : 721 → 961 fiches conformes.', '',
      '## Fiches impossibles (rang — mot — raison)', '']
for t, b in B.items():
    L += [f'### {t}', '']
    L += [f"- {r} — {m} — {'; '.join(f)}" for r, m, f in b['impossibles']] or ['- aucune']
    L.append('')
open(f'{ICI}/sortie/journal.md', 'w').write('\n'.join(L))
print('journal :', ', '.join(B))
