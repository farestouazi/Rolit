# Rolit

**Français** | [English](README.md)

Implémentation en Python du jeu de plateau **Rolit** (variante de l'Othello pour 1 à 4 joueurs),
avec une interface graphique basée sur `fltk` et une sauvegarde automatique de la partie.

> À l'origine un projet AP1 — Université Gustave Eiffel, 2024-2025
> Auteur : TOUAZI FARES

## Règles

- Le plateau est une grille 8×8 ; la partie commence avec quatre boules au centre.
- À son tour, un joueur pose une boule sur une case **vide adjacente** (8 directions) à une boule existante.
- Toutes les boules alignées (ligne, colonne, diagonale) entre la boule posée et une autre boule
  **de la même couleur** passent à la couleur du joueur.
- La manche s'arrête quand le plateau est plein : chaque joueur marque autant de points que de boules de sa couleur.
- La partie se termine quand un joueur atteint la limite de points choisie.

Modes : 2, 3 ou 4 joueurs en local, ou 1 joueur contre le CPU (coups aléatoires).

## Installation

Python 3.9 ou supérieur.

```bash
pip install -r requirements.txt
```

Le module graphique **`fltk.py`** n'est pas inclus dans ce dépôt (il appartient à ses
propres auteurs et nous ne pouvons pas le redistribuer). Téléchargez-le depuis la
[source d'origine](https://fltk-b9f35a.frama.io/) et placez-le à la racine du projet, à côté de `main.py`.

## Lancer le jeu

```bash
python main.py
```

| Action | Commande |
|---|---|
| Poser une boule | clic gauche sur une case jouable, puis clic gauche pour valider |
| Annuler le coup | clic droit (avant validation) |
| Pause / sauvegarder et quitter | bouton en haut à gauche |

La partie est sauvegardée à chaque coup (`save_game.json`) et peut être reprise depuis le menu principal.
Les paramètres (langue, police, thème, apparence) sont conservés dans `config.json`.
Ces deux fichiers sont ignorés par Git. L'interface est en anglais par défaut ; la langue se change
dans les paramètres (français, anglais, espagnol, italien, allemand).

## Structure du projet

```
main.py                    point d'entrée
fltk.py                    bibliothèque graphique (fournie séparément, hors dépôt)
rolit/
├── app.py                 navigation entre les écrans
├── regles.py              règles du jeu (logique pure, testable)
├── partie.py              modèle de données d'une partie
├── sauvegarde.py          lecture / écriture de la partie en JSON
├── parametres.py          paramètres utilisateur persistants
├── traductions.py         textes en 5 langues
├── constantes.py          constantes globales
├── affichage.py           taille de la fenêtre, conversion fraction -> pixels
├── ui/
│   ├── theme.py           thèmes clair/sombre et palette des boules
│   ├── widgets.py         zones cliquables, boutons, boutons radio
│   ├── formes.py          dessin des boules (rond, carré, triangle, étoile)
│   └── plateau.py         décor du plateau, boules, scores, indicateurs
└── ecrans/
    ├── menu_principal.py
    ├── options.py
    ├── preparation.py     nombre de joueurs, points, noms, couleurs
    ├── jeu.py             déroulement d'une manche / d'une partie
    └── dialogues.py       pause, fin de manche, fin de partie
tests/                     tests unitaires (règles, partie, sauvegarde)
```

`rolit/regles.py`, `partie.py` et `sauvegarde.py` ne dépendent pas de `fltk` : ils peuvent être testés
sans écran.

## Tests

```bash
python -m unittest discover -s tests -t . -v
```

## Licence

Distribué sous [licence MIT](LICENSE). Elle ne couvre pas `fltk.py`, qui appartient à ses propres auteurs.

## Remerciements

L'interface graphique repose sur `fltk.py` ([source](https://fltk-b9f35a.frama.io/)), © ses auteurs d'origine.