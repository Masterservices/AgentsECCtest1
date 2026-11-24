#!/usr/bin/env python3
"""Édition gamma des tomes « 10 000 mots » : correction par Dialagram, contrôle automatique, assemblage.
Usage : gamma.py <tome> [<tome> ...]   (ex. fr-t1 ru-t1)
Sources : $GAMMA_SRC/<tome>.jsonl ; travail : $GAMMA_WORK/<tome>/ ; sortie : $GAMMA_OUT/<tome>.jsonl
"""
import json, os, re, sys, time, threading, urllib.request, unicodedata
from concurrent.futures import ThreadPoolExecutor

SRC = os.environ['GAMMA_SRC']; WORK = os.environ['GAMMA_WORK']; OUT = os.environ['GAMMA_OUT']
PROMPT_MD = os.environ['GAMMA_PROMPT']
MODEL = os.environ.get('DIALAGRAM_MODEL', 'qwen-3.8-max-thinking')
PAR = int(os.environ.get('GAMMA_PAR', '8')); TAILLE = int(os.environ.get('GAMMA_TAILLE', '25'))
TOURS = int(os.environ.get('GAMMA_TOURS', '4'))
LANG = {'fr': 'français', 'ru': 'russe'}
lock = threading.Lock(); USAGE = {}

# ---------- vérificateur ----------
def norm(s):
    s = unicodedata.normalize('NFD', s.lower().replace('’', "'"))
    s = s.replace('́', '').replace('̀', '')
    s = unicodedata.normalize('NFC', s).replace('ё', 'е')
    return s
def toks(s): return re.findall(r"[^\W\d_]+", norm(s))
def contient(texte, formes):
    T = toks(texte)
    for f in formes:
        F = toks(f)
        if not F: continue
        n = len(F)
        for i in range(len(T) - n + 1):
            seg = T[i:i + n]
            if seg[:-1] == F[:-1] and (seg[-1] == F[-1] or (seg[-1].startswith(F[-1]) and seg[-1][len(F[-1]):] in ('ся', 'сь'))):
                return True
    return False
VOY = set('аеёиоуыэюяАЕЁИОУЫЭЮЯ')
def sans_accent(texte):
    m = []
    for w in re.findall(r"[А-Яа-яЁё́-]+", unicodedata.normalize('NFD', texte)):
        w2 = unicodedata.normalize('NFC', w)
        if sum(c in VOY for c in w2) > 1 and '́' not in w and 'ё' not in w2 and 'Ё' not in w2:
            m.append(w2)
    return m
def exemple_ok(ex, langue):
    n, mini = len(toks(ex)), (3 if langue == 'ru' else 4)
    if not mini <= n <= 10: return f'exemple hors {mini}–10 mots : « {ex} »'
    lettre = next((c for c in ex if c.isalpha()), '')
    if not lettre.isupper(): return f'exemple sans majuscule au début : « {ex} »'
    if ex.rstrip(' »"”\'')[-1:] not in '.!?…': return f'exemple sans . ! ? à la fin : « {ex} »'
    return None
def besoin_tournures(nature):
    n = (nature or '').lower()
    return bool(re.search(r'verbe|\bnom\b|adjectif|pronom|глагол|существ|прилагат|местоим', n))

def verifier(f, src):
    """Renvoie la liste des fautes de la fiche f (src = fiche source, pour l'identité)."""
    if not isinstance(f, dict): return ['pas un objet JSON']
    F = []
    for k in ('rang', 'mot', 'langue', 'langue_eleve'):
        if f.get(k) != src.get(k): F.append(f'champ {k} différent de la source')
    L, E = src['langue'], src['langue_eleve']
    formes = [f.get('mot', ''), src.get('mot_accent', '')] + [x for x in (f.get('formes') or []) if isinstance(x, str)]
    for e in f.get('expressions') or []:
        if isinstance(e, dict) and e.get('forme'): formes.append(e['forme'])
    tr = f.get('tournures')
    if besoin_tournures(f.get('nature')) and not (isinstance(tr, list) and 4 <= len(tr) <= 6):
        F.append('tournures absentes ou hors 4–6')
    for t in tr or []:
        if not (isinstance(t, dict) and t.get(L) and t.get(E)): F.append('tournure mal formée'); continue
        if not contient(t[L], formes): F.append(f'tournure sans le mot : « {t[L]} »')
        if '/' in t[E]: F.append(f'traduction avec « / » : « {t[E]} »')
    sens = f.get('sens')
    if not (isinstance(sens, list) and sens): F.append('sens absents')
    for s in sens or []:
        if not isinstance(s, dict): F.append('sens mal formé'); continue
        if re.search(r'[/;,]', str(s.get('traduction', ''))): F.append(f"plusieurs traductions (« / », « , » ou « ; ») au lieu d'une principale : « {s.get('traduction')} »")
        for a in s.get('aussi') or []:
            if '/' in str(a): F.append(f'« aussi » avec « / » : « {a} »')
        ex = s.get('exemples') or []
        if len(ex) < 2: F.append('moins de 2 exemples pour un sens')
        for p in ex:
            if not (isinstance(p, list) and len(p) == 2 and all(isinstance(x, str) and x.strip() for x in p)):
                F.append('exemple mal formé'); continue
            if not contient(p[0], formes): F.append(f'exemple sans le mot : « {p[0]} »')
            m = exemple_ok(p[0], L)
            if m: F.append(m)
    exs = f.get('expressions')
    if not isinstance(exs, list): F.append('expressions absentes')
    for e in exs or []:
        if not (isinstance(e, dict) and e.get('expr') and e.get('trad') and e.get('forme')):
            F.append('expression au mauvais format (objet {expr, trad, forme} attendu)'); continue
        if '…' in e['expr'] or '...' in e['expr']: F.append(f"expression à trous : « {e['expr']} »")
        if not contient(e['expr'], [e['forme']]) or not contient(e['expr'], formes):
            F.append(f"expression sans le mot : « {e['expr']} »")
        if '/' in e['trad']: F.append(f"traduction avec « / » : « {e['trad']} »")
    if not isinstance(f.get('homographes'), list): F.append('champ homographes absent')
    if f.get('registre') not in ('neutre', 'familier', 'soutenu'): F.append('registre absent ou invalide')
    c = f.get('carte')
    if not (isinstance(c, dict) and c.get('recto') == f.get('mot') and c.get('verso')): F.append('carte invalide (recto = mot, verso = traduction)')
    elif re.search(r'[/;,]', c['verso']): F.append(f"verso de carte avec plusieurs traductions : « {c['verso']} »")
    if not f.get('formes'): F.append('formes absentes')
    if L == 'ru':
        manq = []
        for x in [f.get('mot', '')] + list(f.get('formes') or []) + [t.get('ru', '') for t in tr or [] if isinstance(t, dict)] \
                + [p[0] for s in sens or [] if isinstance(s, dict) for p in s.get('exemples') or [] if isinstance(p, list) and p] \
                + [e.get('expr', '') for e in exs or [] if isinstance(e, dict)]:
            manq += sans_accent(str(x))
        if len(manq) > 1: F.append('accent tonique manquant : ' + ', '.join(sorted(set(manq))[:8]))
    return F

# ---------- Dialagram ----------
def appel(msg, tome):
    body = json.dumps({'model': MODEL, 'stream': True, 'messages': [{'role': 'user', 'content': msg}]}).encode()
    for essai in range(4):
        try:
            req = urllib.request.Request('https://dialagram.me/router/v1/chat/completions', data=body,
                                         headers={'Content-Type': 'application/json'})
            out = []; usage = {}
            for l in urllib.request.urlopen(req, timeout=1800):
                l = l.decode().strip()
                if l.startswith('data: {'):
                    d = json.loads(l[6:]); usage = d.get('usage') or usage
                    for ch in d.get('choices', []): out.append(ch.get('delta', {}).get('content') or '')
            with lock:
                u = USAGE.setdefault(tome, {'appels': 0, 'prompt_tokens': 0, 'completion_tokens': 0})
                u['appels'] += 1
                for k in ('prompt_tokens', 'completion_tokens'): u[k] += int(usage.get(k) or 0)
            return ''.join(out)
        except urllib.error.HTTPError as e:
            if e.code in (401, 402, 403): raise SystemExit(f'BLOQUÉ : Dialagram refuse l\'accès (HTTP {e.code}) — clé ou crédit manquant')
            time.sleep(20 * (essai + 1))
        except Exception:
            time.sleep(20 * (essai + 1))
    return ''

def gabarit():
    md = open(PROMPT_MD).read()
    i = md.index('## Le prompt'); a = md.index('```', i) + 3; b = md.index('```', a)
    return md[a:b].strip('\n')

def prompt(tome, fiches):
    L, E = fiches[0][0]['langue'], fiches[0][0]['langue_eleve']
    p = gabarit().replace('{LANGUE ÉTUDIÉE}', LANG[L]).replace("{LANGUE DE L'ÉLÈVE}", LANG[E])
    p = p.replace('{"<langue étudiée>": "...", "<langue de l\'élève>": "..."}', '{"%s": "...", "%s": "..."}' % (L, E))
    p += f'\n\nPRÉCISIONS : les clés des tournures sont exactement "{L}" (langue étudiée) et "{E}" (langue de l\'élève). Les explications ("sens", "pieges") restent en {LANG[E]}. Le champ "rang" de chaque ligne reste identique.'
    bloc = '\n\n'.join(json.dumps(f, ensure_ascii=False) + '\nFAUTES : ' + ('; '.join(F) if F else 'aucune') for f, F in fiches)
    return p.replace('{COLLER ICI LE PAQUET}', bloc)

def lire_reponse(txt):
    res = {}
    for l in txt.splitlines():
        l = l.strip().strip('`')
        if not l.startswith('{'): continue
        try: d = json.loads(l)
        except Exception: continue
        if isinstance(d, dict) and isinstance(d.get('rang'), int): res[d['rang']] = d
    return res

GARDER = ('niveau', 'tome', 'page', 'api', 'nature', 'mot_accent')
def traiter_tome(tome):
    src = [json.loads(l) for l in open(f'{SRC}/{tome}.jsonl') if l.strip()]
    S = {f['rang']: f for f in src}
    W = f'{WORK}/{tome}'; os.makedirs(W, exist_ok=True)
    etat_p = f'{W}/etat.json'
    etat = json.load(open(etat_p)) if os.path.exists(etat_p) else {'bon': {}, 'meilleur': {}}
    bon = {int(k): v for k, v in etat['bon'].items()}; meilleur = {int(k): v for k, v in etat['meilleur'].items()}
    def sauver():
        with lock: json.dump({'bon': bon, 'meilleur': meilleur}, open(etat_p, 'w'), ensure_ascii=False)
    for tour in range(TOURS):
        reste = [r for r in S if r not in bon]
        if not reste: break
        taille = TAILLE if tour == 0 else max(5, TAILLE // 2 ** tour)
        paquets = []
        for i in range(0, len(reste), taille):
            lot = []
            for r in reste[i:i + taille]:
                base = meilleur.get(r, {}).get('fiche') or S[r]
                lot.append((base, verifier(base, S[r])))
            paquets.append(lot)
        print(f'{tome} tour {tour + 1} : {len(reste)} fiches, {len(paquets)} paquets', flush=True)
        def un(lot):
            rep = lire_reponse(appel(prompt(tome, lot), tome))
            for base, _ in lot:
                r = base['rang']; d = rep.get(r)
                if d is None: continue
                for k in GARDER:
                    if k in S[r]: d[k] = S[r][k]
                F = verifier(d, S[r])
                with lock:
                    if not F: bon[r] = d
                    elif r not in meilleur or len(F) < meilleur[r]['n']: meilleur[r] = {'fiche': d, 'n': len(F), 'fautes': F}
            sauver()
        with ThreadPoolExecutor(PAR) as ex: list(ex.map(un, paquets))
    lignes, impossibles = [], []
    for r in sorted(S):
        if r in bon: lignes.append(bon[r])
        elif r in meilleur: lignes.append(meilleur[r]['fiche']); impossibles.append((r, S[r]['mot'], meilleur[r]['fautes']))
        else: lignes.append(S[r]); impossibles.append((r, S[r]['mot'], ['aucune réponse exploitable : fiche source conservée']))
    os.makedirs(OUT, exist_ok=True)
    with open(f'{OUT}/{tome}.jsonl', 'w') as fo:
        for d in lignes: fo.write(json.dumps(d, ensure_ascii=False) + '\n')
    json.dump({'tome': tome, 'total': len(S), 'corrigees': len(bon), 'impossibles': impossibles, 'usage': USAGE.get(tome, {})},
              open(f'{W}/bilan.json', 'w'), ensure_ascii=False, indent=1)
    print(f'{tome} FIN : {len(bon)}/{len(S)} fiches conformes, {len(impossibles)} impossibles', flush=True)

if __name__ == '__main__':
    with ThreadPoolExecutor(len(sys.argv) - 1) as ex: list(ex.map(traiter_tome, sys.argv[1:]))
