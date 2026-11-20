#!/usr/bin/env python3
"""Trouve sur YouTube de vraies prononciations d'une même phrase (via les sous-titres) et, en option, en fait un montage.

À lancer sur votre ordinateur (YouTube refuse les serveurs de data-center) :
    pip install yt-dlp
    python supercut.py phrases.txt --langue ru [--videos 15] [--chaines chaines.txt] [--montage]

phrases.txt : une phrase par ligne (ex. « куда ты идёшь »).
chaines.txt (facultatif) : une chaîne YouTube par ligne (URL ou @nom) où chercher en plus de la recherche générale.
Sortie : occurrences.json — {"langue", "phrases": [{"phrase", "occurrences": [{"video", "titre", "chaine", "debut", "fin", "texte"}]}]}
(temps en secondes), à ouvrir dans l'artifact « Prononciations réelles ». Avec --montage (ffmpeg requis) : montages/<phrase>.mp4.
Usage personnel et d'étude : respectez les droits des vidéos si vous publiez les montages.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path


def normaliser(t: str) -> str:
    """Minuscules, sans accents toniques ni ponctuation, ё = е : la recherche ignore ces différences."""
    t = unicodedata.normalize("NFKD", t.lower()).replace("ё", "е")
    t = "".join(c for c in t if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^\w\s]", " ", t).split())


def secondes(h: str) -> float:
    return sum(float(x) * 60 ** i for i, x in enumerate(reversed(h.replace(",", ".").split(":"))))


def lire_vtt(chemin: Path):
    """Segments (début, fin, texte) d'un VTT, sans les balises mot à mot ni les doublons des sous-titres automatiques."""
    segs, dernier = [], ""
    for b in chemin.read_text(encoding="utf-8", errors="replace").split("\n\n"):
        m = re.search(r"(\d[\d:.,]+)\s+-->\s+(\d[\d:.,]+)", b)
        if not m:
            continue
        texte = re.sub(r"<[^>]+>", "", " ".join(l for l in b.split("\n")[1:] if "-->" not in l)).strip()
        if texte and texte != dernier:
            segs.append((secondes(m.group(1)), secondes(m.group(2)), texte))
            dernier = texte
    return segs


def lister(url_ou_recherche: str, n: int):
    s = subprocess.run(["yt-dlp", "--flat-playlist", "--playlist-end", str(n), "--print", "%(id)s\t%(title)s\t%(channel)s",
                        url_ou_recherche], capture_output=True, text=True)
    return [l.split("\t") for l in s.stdout.splitlines() if l.count("\t") == 2]


def sous_titres(video: str, langue: str, dossier: Path):
    """Télécharge uniquement les sous-titres (écrits par un humain de préférence, sinon automatiques)."""
    subprocess.run(["yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", f"{langue}.*,{langue}",
                    "--sub-format", "vtt", "-o", str(dossier / "%(id)s.%(ext)s"), f"https://www.youtube.com/watch?v={video}"],
                   capture_output=True, text=True)
    fichiers = sorted(dossier.glob(f"{video}*.vtt"), key=lambda f: ("orig" in f.name or "auto" in f.name, f.name))
    return fichiers[0] if fichiers else None


def occurrences(segs, phrase):
    """Occurrences de la phrase, y compris à cheval sur deux segments consécutifs (marge de 0,6 s)."""
    cible, out = normaliser(phrase), []
    for i, (d, f, t) in enumerate(segs):
        suite = segs[i + 1] if i + 1 < len(segs) else (f, f, "")
        dedans = cible in normaliser(t)
        a_cheval = cible in normaliser(t + " " + suite[2]) and cible not in normaliser(suite[2])
        if cible and (dedans or a_cheval) and (not out or d > out[-1]["fin"]):
            fin = f if cible in normaliser(t) else suite[1]
            out.append({"debut": round(max(d - 0.6, 0), 1), "fin": round(fin + 0.6, 1), "texte": t})
    return out


def montage(phrase, occs, dossier: Path):
    """Découpe chaque passage (vidéo en 480p) et les enchaîne en un seul MP4."""
    dossier.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        morceaux = []
        for k, o in enumerate(occs):
            src = Path(tmp) / f"{o['video']}.mp4"
            if not src.exists():
                subprocess.run(["yt-dlp", "-f", "mp4[height<=480]/best[height<=480]", "-o", str(src),
                                f"https://www.youtube.com/watch?v={o['video']}"], capture_output=True)
            if not src.exists():
                continue
            m = Path(tmp) / f"m{k:03d}.mp4"
            subprocess.run(["ffmpeg", "-y", "-ss", str(o["debut"]), "-to", str(o["fin"]), "-i", str(src),
                            "-vf", "scale=854:480:force_original_aspect_ratio=decrease,pad=854:480:(ow-iw)/2:(oh-ih)/2,setsar=1",
                            "-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-c:a", "aac", "-ar", "44100", "-ac", "2", str(m)],
                           capture_output=True)
            if m.exists():
                morceaux.append(m)
        if not morceaux:
            return None
        liste = Path(tmp) / "liste.txt"
        liste.write_text("".join(f"file '{m}'\n" for m in morceaux), encoding="utf-8")
        sortie = dossier / f"{re.sub(r'[^\w]+', '-', normaliser(phrase)).strip('-')[:60] or 'phrase'}.mp4"
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(liste), "-c", "copy", str(sortie)], capture_output=True)
        return sortie if sortie.exists() else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("phrases")
    ap.add_argument("--langue", default="ru", help="code de langue des sous-titres (ru, fr…)")
    ap.add_argument("--videos", type=int, default=15, help="vidéos examinées par phrase dans la recherche YouTube")
    ap.add_argument("--chaines", help="fichier de chaînes YouTube à examiner en plus")
    ap.add_argument("--max", type=int, default=8, help="occurrences gardées par phrase")
    ap.add_argument("--montage", action="store_true", help="télécharger les passages et monter une vidéo par phrase")
    ap.add_argument("--sortie", default="occurrences.json")
    a = ap.parse_args()
    phrases = [l.strip() for l in Path(a.phrases).read_text(encoding="utf-8").splitlines() if l.strip()]
    chaines = [l.strip() for l in Path(a.chaines).read_text(encoding="utf-8").splitlines() if l.strip()] if a.chaines else []
    cache = Path("sous-titres")
    cache.mkdir(exist_ok=True)
    resultat = {"langue": a.langue, "phrases": []}
    for phrase in phrases:
        candidats = {v[0]: v for v in lister(f"ytsearch{a.videos}:{phrase}", a.videos)}
        for c in chaines:
            url = c if c.startswith("http") else f"https://www.youtube.com/{c.lstrip('/')}/videos"
            candidats.update({v[0]: v for v in lister(url, a.videos)})
        trouvees = []
        for vid, titre, chaine in candidats.values():
            vtt = sous_titres(vid, a.langue, cache)
            if vtt:
                trouvees += [{"video": vid, "titre": titre, "chaine": chaine, **o} for o in occurrences(lire_vtt(vtt), phrase)]
            if len({o["chaine"] for o in trouvees}) >= a.max:
                break
        # variété des voix : d'abord une occurrence par chaîne
        vues, choix = set(), []
        for o in trouvees:
            if o["chaine"] not in vues:
                vues.add(o["chaine"])
                choix.append(o)
        choix = (choix + [o for o in trouvees if o not in choix])[:a.max]
        entree = {"phrase": phrase, "occurrences": choix}
        if a.montage and choix:
            m = montage(phrase, choix, Path("montages"))
            entree["montage"] = str(m) if m else None
        resultat["phrases"].append(entree)
        print(f"{phrase} : {len(choix)} occurrence(s), {len({o['chaine'] for o in choix})} voix différentes", flush=True)
    Path(a.sortie).write_text(json.dumps(resultat, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {a.sortie} : à ouvrir dans l'artifact « Prononciations réelles »")


if __name__ == "__main__":
    sys.exit(main())
