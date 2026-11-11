# Rolit

[Français](README.fr.md) | **English**

Python implementation of the board game **Rolit** (an Othello-like game for 1 to 4 players),
with a graphical interface built on `fltk` and automatic game saving.

> Originally an AP1 project — Université Gustave Eiffel, 2024-2025
> Author: TOUAZI FARES

## Rules

- The board is an 8×8 grid; the game starts with four balls in the centre.
- On your turn, place a ball on an **empty square adjacent** (8 directions) to an existing ball.
- Every ball lined up (row, column or diagonal) between the ball you placed and another ball
  **of your own colour** is converted to your colour.
- A round ends when the board is full: each player scores one point per ball of their colour.
- The game ends when a player reaches the chosen point limit.

Modes: 2, 3 or 4 local players, or 1 player against the CPU (random moves).

## Installation

Python 3.9 or later.

```bash
pip install -r requirements.txt
```

The graphical module **`fltk.py`** is not included in this repository (it belongs to its
own authors and is not ours to redistribute). Download it from the
[original source](https://fltk-b9f35a.frama.io/) and put it at the project root, next to `main.py`.

## Run

```bash
python main.py
```

| Action | Control |
|---|---|
| Place a ball | left-click a playable square, then left-click to confirm |
| Undo the move | right-click (before confirming) |
| Pause / save and quit | button in the top-left corner |

The game is saved after every move (`save_game.json`) and can be resumed from the main menu.
Settings (language, font, theme, appearance) are stored in `config.json`.
Both files are ignored by Git. The interface is in English by default; the language can be
changed in the settings (French, English, Spanish, Italian, German).

## Project structure

```
main.py                    entry point
fltk.py                    graphics library (provided separately, not in the repo)
rolit/
├── app.py                 navigation between screens
├── regles.py              game rules (pure logic, testable)
├── partie.py              game data model
├── sauvegarde.py          JSON save / load
├── parametres.py          persistent user settings
├── traductions.py         UI texts in 5 languages
├── constantes.py          global constants
├── affichage.py           window size, fraction -> pixel conversion
├── ui/
│   ├── theme.py           light/dark themes and ball palette
│   ├── widgets.py         clickable zones, buttons, radio buttons
│   ├── formes.py          ball drawing (round, square, triangle, star)
│   └── plateau.py         board decor, balls, scores, turn indicators
└── ecrans/
    ├── menu_principal.py
    ├── options.py
    ├── preparation.py     player count, point limit, names, colours
    ├── jeu.py             round / game flow
    └── dialogues.py       pause, end of round, end of game
tests/                     unit tests (rules, game, saving)
```

`rolit/regles.py`, `partie.py` and `sauvegarde.py` do not depend on `fltk`, so they can be tested
without a display. (Module and identifier names are in French, as in the original project.)

## Tests

```bash
python -m unittest discover -s tests -t . -v
```

## License

Released under the [MIT License](LICENSE). This does not cover `fltk.py`, which belongs to its own authors.

## Acknowledgements

Graphics are powered by `fltk.py` ([source](https://fltk-b9f35a.frama.io/)), © its original authors.