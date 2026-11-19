#!/bin/bash
# Fabrique le livre de référence « L'Art de Décider » à partir de plan.json (relançable à chaque étape).
# rédaction (Dialagram) -> rectification -> figures -> PDF -> Word -> controle.json
set -u
cd "$(dirname "$0")"; O=../outils
export DIALAGRAM_MODEL=${DIALAGRAM_MODEL:-qwen-3.8-max-thinking}
attendus=$(python3 -c "import json;p=json.load(open('plan.json'));print(sum(len(x['chapitres']) for x in p['parties'])+2)")
for i in 1 2 3 4; do
  python3 -u $O/redaction.py plan.json chapitres --mots 4500 --parallele ${PAR:-6} >> redaction.log 2>&1
  [ $(ls chapitres/*.md 2>/dev/null | wc -l) -ge $attendus ] && break; sleep 60
done
[ $(ls chapitres/*.md 2>/dev/null | wc -l) -ge $attendus ] || { echo "ERREUR rédaction $(ls chapitres/*.md | wc -l)/$attendus"; exit 1; }
for i in 1 2 3; do
  python3 -u $O/nettoyage.py chapitres chapitres_v2 >> nettoyage.log 2>&1
  [ $(ls chapitres_v2/*.md 2>/dev/null | wc -l) -ge $attendus ] && break; sleep 60
done
[ $(ls chapitres_v2/*.md 2>/dev/null | wc -l) -ge $attendus ] || { echo "ERREUR rectification"; exit 1; }
python3 figures.py plan.json chapitres_v2
NOM=$(python3 -c "
import json,re,unicodedata;t=json.load(open('plan.json'))['titre']
t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode();print(re.sub(r'[^A-Za-z0-9]+','-',t).strip('-'))")-Oussama-Ghorbel
python3 $O/mise_en_page.py plan.json chapitres_v2 "$NOM.pdf" --corps 11.3 --collection "Livre de référence · Première édition" > pdf.log 2>&1
python3 $O/md2docx.py plan.json chapitres_v2 "$NOM.docx"
python3 - "$NOM" <<'PY'
import json,glob,re,sys
from pypdf import PdfReader
n=sys.argv[1]; p=json.load(open('plan.json')); fs=glob.glob('chapitres_v2/*.md')
fuite=re.compile(r"dites-moi|souhaitez-vous que je|voulez-vous que je|si vous souhaitez que j",re.I)
c={"slug":"art-de-decider","titre":p["titre"],"sous_titre":p["sous_titre"],"cadre":p.get("cadre",{}).get("nom"),
   "pages":len(PdfReader(n+".pdf").pages),"mots":sum(len(open(f).read().split()) for f in fs),"fichiers":len(fs),
   "figures":len(glob.glob('figures/*.png')),"fuites":sum(1 for f in fs if fuite.search(open(f).read())),
   "pdf":n+".pdf","docx":n+".docx","edition":"livre de référence, première édition"}
json.dump(c,open('controle.json','w'),ensure_ascii=False,indent=1); print(c)
PY
