#!/usr/bin/env python3
"""Étend frequence.json (lemmes français par fréquence, sous-titres OpenSubtitles 2018 via FrequencyWords) sans toucher aux rangs déjà publiés.

Usage : frequence.py [TOTAL=11000] [GELES=1000]   (GELES = rangs déjà publiés, conservés tels quels)
Les entrées existantes gardent leur rang ; les nouveaux lemmes (simplemma) sont ajoutés à la suite, après nettoyage :
noms propres et mots inconnus du dictionnaire écartés (sauf interjections usuelles), formes verbales à trait d'union
(« dis-moi ») ramenées au verbe, fusions manuelles (FUSION), exclusions manuelles (EXCLURE).
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import simplemma

ICI = Path(__file__).resolve().parent
EXCLURE = set("""jack john sam york new charlie michael you david tom joe mike frank george peter paul max the ii ie ll l c h t fbi dr mr
mme mlle pos ia okay est-ce marie pierre paris jean louis nick henry martin simon victor alex ben lucas daniel thomas jacques
of and to it is in what my your it's don't i'm that this we are be go yes mark tommy charles eric carter william mac dan r km choir
voiler henry james alex danny bob jimmy jane bill sarah nick will tony mary harry jim richard ray robert vis black team user robin girl charlotte lady boy carolin boston oscar penny diane spencer val baby stone mickey green
mn tap lover sous-titrer moyenner
bonnir harper tara archer rob colin marc benjamin palmer plain michel lex ris river valentin virginie piper blair denise rosir brandon khan andré alfred philippe pan ana haver superman loser kid bang marshal ci cassie françois group home
if marina marian griser brick claude jeanne gray hart break jan merlin yard brook bridge prion milan nicolas martiner gaber robinson zoé luc jasper archi-e sal more news rush master tanner lester terrer fût négro rainer sataner bull napoléon gratte
jade gardon haler gun sierra creek mol dalton tenon cary golden chester picard water gretchen oxford hercule moïse der about tarzan dakota cendrillon daphné lulu tata mémé stater gitan tuber vitrer volanter repriser cliver bette maryland pascal guillaume cora éric serge gille mao pékin jap signor kappa skip set land book open rand derrick capitole eue réer jaffer rafer tac tan cracker vielle mirer écosser shooter tempêter axel nova paddy havane panama baptiste morganer winchester ain caraïbe jojo péri paso galle sabine mu guinée far full avançon entendant ouvrant trust ex-petit jouée fauchée romano gouine nique""".split())
GARDER = set("ouais hé hein ah oh euh bah bon chut aïe ouf waouh salut coucou ok".split())
FUSION = {"copiner": "copine", "saurer": "savoir", "priser": "prise", "soeur": "sœur", "ecoute": "écouter", "ecoutez": "écouter",
          "écoute": "écouter", "sors": "sortir", "joue": "jouer", "mets": "mettre", "bouge": "bouger", "oublie": "oublier",
          "plait": "plaire", "prie": "prier", "vu": "voir", "fini": "finir", "venu": "venir", "rendu": "rendre", "cru": "croire",
          "disparu": "disparaître", "aura": "avoir", "seconder": "seconde", "monte": "monter", "donne": "donner",
          "lève": "lever", "paie": "payer", "paye": "payer", "frappe": "frapper", "dépêche": "dépêcher", "blanche": "blanc",
          "claire": "clair", "casse": "casser", "jeté": "jeter", "passée": "passé", "lance": "lancer", "trouvé": "trouver",
          "coupé": "couper", "embrasse": "embrasser", "enfermé": "enfermer", "brisé": "briser", "forcé": "forcer",
          "rempli": "remplir", "rigole": "rigoler", "réglé": "régler", "moque": "moquer", "spéciale": "spécial",
          "différents": "différent", "ose": "oser", "emmerde": "emmerder", "fausser": "faux", "brûlé": "brûler",
          "laissée": "laisser", "attrape": "attraper", "laisse": "laisser", "normale": "normal", "habillé": "habiller",
          "tenu": "tenir", "oeuf": "œuf", "cesse": "cesser", "connu": "connaître", "engagé": "engager", "élevé": "élever",
          "énervé": "énerver", "déçu": "décevoir", "lis": "lire",
          "embrassé": "embrasser", "rêvé": "rêver", "rompu": "rompre", "fiancée": "fiancé", "trompe": "tromper",
          "ouvrer": "ouvrir", "frappé": "frapper", "couché": "coucher", "vécu": "vivre", "raté": "rater", "caché": "cacher",
          "tarer": "taré", "remiser": "remise", "loué": "louer", "aimé": "aimer", "perdu": "perdre", "rencontré": "rencontrer",
          "enlevé": "enlever", "trompé": "tromper", "payé": "payer", "annulé": "annuler", "sauté": "sauter", "bloqué": "bloquer",
          "poussé": "pousser", "éteint": "éteindre", "planté": "planter", "allumé": "allumer", "séparé": "séparer", "écrasé": "écraser",
          "serré": "serrer", "levé": "lever", "couru": "courir", "effacé": "effacer", "revu": "revoir", "discuté": "discuter",
          "piqué": "piquer", "lâché": "lâcher", "guéri": "guérir", "informé": "informer", "puni": "punir", "résolu": "résoudre",
          "chaude": "chaud", "criminelle": "criminel", "mignonne": "mignon", "sainte": "saint", "centrale": "central",
          "familiale": "familial", "empreint": "empreinte", "débrouille": "débrouiller", "crève": "crever", "traîne": "traîner",
          "pige": "piger", "accroche": "accrocher", "oeuvrer": "œuvre", "voeu": "vœu", "clef": "clé", "regardant": "regarder",
          "rate": "rater", "pique": "piquer",
          "réfléchi": "réfléchir", "coté": "côté", "lave": "laver", "rit": "rire",
          "dépose": "déposer", "avoué": "avouer", "emporté": "emporter", "évanoui": "évanouir", "singer": "singe", "mérité": "mériter", "range": "ranger", "prouvé": "prouver", "garanti": "garantir", "retenu": "retenir", "fouillé": "fouiller", "accroché": "accrocher", "assassiné": "assassiner", "oublié": "oublier", "limité": "limiter", "balancé": "balancer", "attaché": "attacher", "infecté": "infecter", "cuit": "cuire", "autorisé": "autoriser", "osé": "oser", "touchée": "toucher", "précieuse": "précieux", "remplier": "remplir", "fine": "fin", "voisiner": "voisin", "prêté": "prêter", "persuadé": "persuader", "allongé": "allonger", "enterré": "enterrer", "avancé": "avancer", "vomi": "vomir", "inspiré": "inspirer", "vaguer": "vague", "dû": "devoir", "saisi": "saisir", "emprunté": "emprunter", "gâche": "gâcher", "choqué": "choquer", "affecté": "affecter", "choisi": "choisir", "rentraire": "rentrer", "roulé": "rouler", "tombé": "tomber", "pété": "péter", "pointé": "pointer", "disputé": "disputer", "largué": "larguer", "déguisé": "déguiser", "ramasse": "ramasser", "dégagé": "dégager", "chassé": "chasser", "amenée": "amener", "retourne": "retourner", "sente": "sentir", "rentré": "rentrer", "volé": "voler", "glissé": "glisser", "activé": "activer", "rentrant": "rentrer", "fourni": "fournir", "mêlé": "mêler", "rejeté": "rejeter", "laissé": "laisser", "pars": "partir", "roser": "rose", "humilié": "humilier", "loupé": "louper", "défendu": "défendre", "réussi": "réussir", "programmé": "programmer", "relié": "relier", "emballé": "emballer", "relâché": "relâcher", "veiner": "veine", "lavé": "laver", "glisse": "glisser", "fumé": "fumer", "gardé": "garder", "supposé": "supposer", "agressé": "agresser", "allonge": "allonger", "barré": "barrer", "collé": "coller", "menacé": "menacer", "né": "naître", "répété": "répéter", "media": "média",
          "age": "âge", "fui": "fuir", "défends": "défendre", "avalé": "avaler", "éclaté": "éclater", "gelé": "geler", "brisée": "briser", "effondré": "effondrer", "localisé": "localiser", "joyeuse": "joyeux", "gonflé": "gonfler", "ignoré": "ignorer", "craché": "cracher", "coulé": "couler", "abandonné": "abandonner", "initiale": "initial", "renonce": "renoncer", "tirée": "tirer", "approché": "approcher", "dessiné": "dessiner", "entraîné": "entraîner", "amusé": "amuser", "détesté": "détester", "exagéré": "exagérer", "paralysé": "paralyser", "bouclé": "boucler", "écoulé": "écouler", "pressée": "pressé", "scellé": "sceller", "offensé": "offenser", "changé": "changer", "tuant": "tuer", "cogné": "cogner", "approuvé": "approuver", "possédé": "posséder", "trempé": "tremper", "baissé": "baisser", "nourri": "nourrir", "envahi": "envahir", "effraie": "effrayer", "étranglé": "étrangler", "posté": "poster", "impatiente": "impatient", "retardé": "retarder", "égaré": "égarer", "gâté": "gâter", "prononcé": "prononcer", "gravé": "graver", "entendu": "entendre", "convenu": "convenir", "banni": "bannir", "négative": "négatif", "libéré": "libérer", "mélangé": "mélanger", "insulté": "insulter", "classé": "classer", "heurté": "heurter", "tremble": "trembler", "doublé": "doubler", "placé": "placer", "cogne": "cogner", "recouvert": "recouvrir", "opéré": "opérer", "motivé": "motiver", "lu": "lire", "expulsé": "expulser", "rangé": "ranger", "goûté": "goûter", "débarqué": "débarquer", "planqué": "planquer", "abusé": "abuser", "conçu": "concevoir", "rapproché": "rapprocher", "prononce": "prononcer", "détaché": "détacher", "écarté": "écarter", "recommandé": "recommander", "réjoui": "réjouir", "terrifié": "terrifier", "lente": "lent", "embarrassé": "embarrasser", "confronté": "confronter", "identifié": "identifier", "détourné": "détourner", "fondu": "fondre", "brune": "brun", "entrant": "entrer", "amène": "amener", "appuyé": "appuyer", "brouillé": "brouiller", "creusé": "creuser", "dure": "dur", "plaqué": "plaquer", "promis": "promettre", "reçu": "recevoir", "signé": "signer", "remue": "remuer",
          "buté": "buter", "analysé": "analyser", "plate": "plat", "suicidé": "suicider", "bousillé": "bousiller", "visé": "viser", "retiré": "retirer", "repoussé": "repousser", "favorite": "favori", "étouffé": "étouffer", "marchant": "marcher", "sourde": "sourd", "épousée": "épouser", "enfoncé": "enfoncer", "refusé": "refuser", "touché": "toucher", "tiré": "tirer", "décidé": "décider", "gagné": "gagner", "déclenche": "déclencher", "dévasté": "dévaster", "évacué": "évacuer", "mineure": "mineur", "éclairé": "éclairer", "détaillé": "détailler", "pêché": "péché", "arraché": "arracher", "désiré": "désirer", "rayé": "rayer", "assuré": "assurer", "manqué": "manquer", "découpé": "découper", "habité": "habiter", "ennuyé": "ennuyer", "fréquenté": "fréquenter", "cerné": "cerner", "dressé": "dresser", "adapté": "adapter", "dépassé": "dépasser", "injecté": "injecter", "exclu": "exclure", "dégonflé": "dégonfler", "verrouillé": "verrouiller", "commençant": "commencer", "congelé": "congeler", "comblé": "combler", "compris": "comprendre", "licencié": "licencier", "codé": "coder", "cuisiné": "cuisiner", "pénétré": "pénétrer", "équipé": "équiper", "posée": "poser", "flippé": "flipper", "maximale": "maximal", "brève": "bref", "digitale": "digital", "sandwiche": "sandwich", "confisqué": "confisquer", "dupé": "duper", "défait": "défaire", "recueilli": "recueillir", "hurlant": "hurler", "douloureuse": "douloureux", "grandissant": "grandir", "offrant": "offrir", "appliqué": "appliquer", "rappelé": "rappeler", "ruiné": "ruiner", "détraqué": "détraquer", "logé": "loger", "déployé": "déployer", "converti": "convertir", "déclaré": "déclarer", "cousu": "coudre", "respecté": "respecter", "dispersé": "disperser", "abîmé": "abîmer", "révélé": "révéler", "tombant": "tomber", "appelant": "appeler", "appris": "apprendre", "absorbé": "absorber", "inondé": "inonder", "grossi": "grossir", "désarmé": "désarmer", "pleurant": "pleurer", "écoutant": "écouter", "troublé": "troubler", "agressive": "agressif", "flottant": "flotter", "voué": "vouer", "blanchi": "blanchir", "affronté": "affronter", "cloué": "clouer", "torturé": "torturer", "plié": "plier", "mutilé": "mutiler", "intercepté": "intercepter", "peint": "peindre", "crevée": "crever", "corrigé": "corriger", "soutenu": "soutenir", "navale": "naval", "serrée": "serrer", "ligoté": "ligoter", "coupée": "couper", "penché": "pencher", "monté": "monter", "coiffé": "coiffer", "bombardé": "bombarder", "convaincu": "convaincre", "amélioré": "améliorer", "comparé": "comparer", "futée": "futé", "affaibli": "affaiblir", "romaine": "romain", "commerciale": "commercial", "distribué": "distribuer", "déformé": "déformer", "dissimulé": "dissimuler", "bronzé": "bronzer", "admis": "admettre", "aligné": "aligner", "conditionné": "conditionner", "candidate": "candidat", "chié": "chier", "ile": "île", "connection": "connexion", "gouverne": "gouverner", "plie": "plier", "essuie": "essuyer", "frotte": "frotter", "manipule": "manipuler", "gonfle": "gonfler", "renverse": "renverser", "éclaire": "éclairer", "rase": "raser", "plane": "planer", "largue": "larguer", "vive": "vif", "tirant": "tirer", "ferré": "ferrer", "enflammé": "enflammer", "dégoûté": "dégoûter", "redresse": "redresser", "présidentielle": "présidentiel", "retourné": "retourner", "refroidi": "refroidir", "anticipé": "anticiper", "figé": "figer", "enflé": "enfler", "désorienté": "désorienter", "nié": "nier", "neutralisé": "neutraliser", "sacrifié": "sacrifier", "abordé": "aborder", "exploité": "exploiter", "embrouillé": "embrouiller", "prolongé": "prolonger", "haï": "haïr", "acquitté": "acquitter", "harcelé": "harceler", "refoulé": "refouler", "exigé": "exiger", "groupé": "grouper", "déserté": "déserter", "alerté": "alerter", "aspiré": "aspirer", "éliminé": "éliminer", "empêché": "empêcher", "entouré": "entourer", "accéléré": "accélérer", "emprisonné": "emprisonner", "approfondi": "approfondir", "maîtrisé": "maîtriser", "transmis": "transmettre", "projeté": "projeter", "reporté": "reporter", "jugé": "juger", "vidé": "vider", "importé": "importer", "enveloppé": "envelopper", "déshabillé": "déshabiller", "sucé": "sucer", "incarné": "incarner", "honorée": "honorer", "ôté": "ôter", "omis": "omettre", "vérifié": "vérifier", "ravagé": "ravager", "déterré": "déterrer", "tourmenté": "tourmenter", "investi": "investir", "bandé": "bander", "divisé": "diviser", "trempée": "tremper", "dilaté": "dilater", "reposé": "reposer", "improvisé": "improviser", "confiné": "confiner", "ensorcelé": "ensorceler", "prémédité": "préméditer", "dérobé": "dérober", "botté": "botter", "fracturé": "fracturer", "aiguisé": "aiguiser", "embêté": "embêter", "sème": "semer", "comporte": "comporter", "procure": "procurer", "consulte": "consulter", "délivre": "délivrer", "routière": "routier", "roulante": "roulant", "porteuse": "porteur", "étroite": "étroit", "exclusive": "exclusif", "partielle": "partiel", "muette": "muet", "joueuse": "joueur", "agace": "agacer", "louée": "louer"}
FIGES = {"peut-être", "aujourd'hui", "là-bas", "là-dedans", "rendez-vous", "celui-là", "celui-ci", "moi-même", "lui-même"}
PRONOMS = ("-t-il", "-moi", "-toi", "-y", "-vous", "-elle", "-il", "-nous", "-je", "-tu", "-on", "-le", "-la", "-les", "-lui", "-en")


def lemme(w):
    if "-" in w and w not in FIGES and w.endswith(PRONOMS):
        w = w.split("-")[0]
    if not w.strip("'-"):
        return ""
    l =simplemma.lemmatize(w, lang="fr").lower()
    return FUSION.get(l, FUSION.get(w, l))


def main():
    total = int(sys.argv[1]) if len(sys.argv) > 1 else 11000
    cnt, formes = Counter(), defaultdict(Counter)
    for ligne in (ICI / "fr_50k.txt").open(encoding="utf-8"):
        w, n = ligne.split()
        if not re.fullmatch(r"[a-zàâäçéèêëîïôöùûüÿœæ'-]+", w) or (len(w) < 2 and w not in ("a", "y", "à")):
            continue
        l = lemme(w)
        if not l or l in EXCLURE or (l not in GARDER and not simplemma.is_known(l, lang="fr")):
            continue
        cnt[l] += int(n)
        formes[l][w] += int(n)
    geles = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    liste = json.loads((ICI / "frequence.json").read_text(encoding="utf-8"))[:geles]
    deja = {x["lemme"] for x in liste}
    for l, n in cnt.most_common():
        if len(liste) >= total:
            break
        if l not in deja:
            liste.append({"rang": len(liste) + 1, "lemme": l, "occurrences": n, "formes": [f for f, _ in formes[l].most_common(4)]})
    (ICI / "frequence.json").write_text(json.dumps(liste, ensure_ascii=False, indent=0), encoding="utf-8")
    print(len(liste), "lemmes")


if __name__ == "__main__":
    main()
