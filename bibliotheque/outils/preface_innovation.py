#!/usr/bin/env python3
"""Ajoute en tête d'un livre de la collection « Innovation Engine » un avant-propos :
but et ingénierie de la collection, puis l'innovation propre au livre (concepts tirés,
stratégies du moteur d'idées, ce qui le distingue des autres livres du marché).

Usage : preface_innovation.py <slug> <fichier_intro.md>
Lit la généalogie dans sujets.json (champ "genealogie" de l'entrée du slug). Sans
généalogie ou si la collection n'est pas "innovation", ne fait rien. Idempotent (marqueur).
"""
import json
import os
import sys

R = "/home/user/AgentsECCtest"
MARQUEUR = "<!-- avant-propos-innovation -->"

SERIE = (
    "## Avant-propos — La collection « Innovation Engine »\n\n"
    f"{MARQUEUR}\n\n"
    "Ce livre n'a pas commencé par un sujet. Il a commencé par une **idée fabriquée**.\n\n"
    "**Le but de la collection.** La plupart des livres pratiques reformulent un marché déjà "
    "saturé : on y retrouve les mêmes conseils, habillés autrement. La collection *Innovation "
    "Engine* vise l'inverse : proposer, à chaque titre, un **angle neuf par construction** — un "
    "cadre de pensée que la logique habituelle du domaine n'aurait pas trouvé seule. L'objectif "
    "n'est pas d'ajouter un livre de plus, mais de donner au lecteur une **manière différente de "
    "voir** un problème qu'il croyait connaître.\n\n"
    "**L'ingénierie derrière chaque livre.** Chaque ouvrage naît d'un *moteur d'idées* "
    "combinatoire. Le moteur tire au hasard des concepts dans cinq réservoirs — objets, "
    "méthodes, **principes naturels et scientifiques**, domaines de la vie, contraintes fortes — "
    "puis leur applique une des douze **stratégies d'innovation** : combinaison intersectorielle, "
    "transposition d'un principe naturel, inversion d'une hypothèse admise, poussée d'un paramètre "
    "à l'extrême, changement d'architecture, association aléatoire contrôlée, transfert par "
    "analogie, résolution sous contrainte… Chaque idée produite est notée (nouveauté, clarté, "
    "potentiel) ; la plus prometteuse devient une **étude de projet**, puis ce livre. Le lecteur "
    "n'a donc pas entre les mains un résumé de l'existant, mais le **développement rigoureux d'une "
    "idée originale** : les connaissances établies y sont synthétisées, mais *transposées* à un "
    "terrain où on ne les attendait pas.\n\n"
    "**Honnêteté intellectuelle.** Ces livres sont conçus et dirigés par Oussama Ghorbel et "
    "rédigés avec l'assistance d'outils d'intelligence artificielle, sans accès à Internet : ils "
    "s'appuient sur des connaissances générales établies et signalent leurs incertitudes. Un livre "
    "de cette collection propose un **cadre explicatif**, pas une vérité garantie ni un conseil "
    "médical, juridique ou financier personnalisé. L'analogie scientifique est un outil de "
    "compréhension : nous en indiquons aussi les limites.\n\n"
)


def innovation(g):
    parts = ["### L'innovation de ce livre\n\n"]
    if g.get("concepts"):
        parts.append("**Les concepts d'origine (tirés par le moteur) :** " + ", ".join(g["concepts"]) + ".\n\n")
    if g.get("strategies"):
        parts.append("**Les stratégies d'innovation appliquées :** " + " ; ".join(g["strategies"]) + ".\n\n")
    if g.get("marche"):
        parts.append("**Ce qui existe déjà :** " + g["marche"] + "\n\n")
    parts.append("**Ce que ce livre apporte de neuf :** " + g["innovation"] + "\n\n")
    parts.append("Voilà pourquoi ce livre ne ressemble pas aux autres : son angle est le produit "
                 "d'une méthode, pas d'une mode. Lisez-le comme une **recherche appliquée** — une "
                 "hypothèse de travail que vous allez tester dans votre propre vie.\n\n---\n\n")
    return "".join(parts)


def main():
    slug, intro = sys.argv[1], sys.argv[2]
    sujets = {b["slug"]: b for b in json.load(open(f"{R}/bibliotheque/outils/sujets.json", encoding="utf-8"))}
    s = sujets.get(slug, {})
    g = s.get("genealogie")
    if s.get("collection") != "innovation" or not g or not g.get("innovation"):
        return 0
    if not os.path.exists(intro):
        print(f"[{slug}] intro introuvable: {intro}", file=sys.stderr)
        return 1
    corps = open(intro, encoding="utf-8").read()
    if MARQUEUR in corps:
        return 0  # déjà inséré
    open(intro, "w", encoding="utf-8").write(SERIE + innovation(g) + corps)
    print(f"[{slug}] avant-propos innovation inséré")
    return 0


if __name__ == "__main__":
    sys.exit(main())
