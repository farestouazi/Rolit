"""Écran des paramètres : plateau, forme des boules, langue, police et thème."""
from __future__ import annotations

from typing import List

import fltk

from ..affichage import px
from ..constantes import LANGUES, POLICES
from ..parametres import parametres
from ..traductions import t
from ..ui.formes import RAYON_BOULE, dessiner_forme
from ..ui.theme import Theme, theme_actuel
from ..ui.widgets import (GroupeRadio, OptionRadio, Zone, dessiner_bouton, dessiner_fond,
                          dessiner_rectangle, ecrire, effacer)

# --- Aperçus des plateaux --------------------------------------------------
# (origine x, origine y, fond du disque, fond de la plaque, style des trous)
_APERCUS_PLATEAU = (
    (0.13, 0.08, "#828282", "#828282", 0),
    (0.29, 0.08, "#DDDDDD", "#DDDDDD", 1),
    (0.13, 0.31, "#F7DC6F", "#F4D03F", 1),
    (0.29, 0.31, "black", "black", 2),
)
# (contour extérieur, fond extérieur, contour intérieur, fond intérieur)
_STYLES_TROUS = {
    0: ("black", "#828282", "black", "black"),
    1: ("black", "#BFBFBF", "black", "#606060"),
    2: ("#AAAAAA", "black", "#AAAAAA", "#050505"),
}
_CONTOUR_APERCU = (
    (0, 0), (.001, .035), (.003, .05), (.001, .065), (0, .1), (.035, .099), (.05, .097),
    (.065, .099), (.1, .1), (.099, .065), (.097, .05), (.099, .035), (.1, 0),
    (.065, .001), (.05, .003), (.035, .001), (0, 0),
)

# (forme, x, y, couleur)
_APERCUS_FORME = (
    (0, 0.50, 0.13, "orange"),
    (1, 0.66, 0.13, "blue"),
    (2, 0.50, 0.36, "red"),
    (3, 0.66, 0.35, "indigo"),
)

def _carre(x: float, y: float) -> Zone:
    return Zone(x, y, x + 0.02, y + 0.02)

GROUPE_PLATEAU = GroupeRadio([
    OptionRadio(0, _carre(0.17, 0.21)), OptionRadio(1, _carre(0.33, 0.21)),
    OptionRadio(2, _carre(0.17, 0.44)), OptionRadio(3, _carre(0.33, 0.44)),
])
GROUPE_FORME = GroupeRadio([
    OptionRadio(0, _carre(0.49, 0.21)), OptionRadio(1, _carre(0.65, 0.21)),
    OptionRadio(2, _carre(0.49, 0.44)), OptionRadio(3, _carre(0.65, 0.44)),
])
GROUPE_LANGUE = GroupeRadio([
    OptionRadio(i, Zone(0.60, 0.60 + 0.06 * i, 0.62, 0.62 + 0.06 * i), nom, 0.68)
    for i, nom in enumerate(LANGUES)
])
_X_POLICES = (0.870, 0.870, 0.880, 0.870, 0.885)
GROUPE_POLICE = GroupeRadio([
    OptionRadio(i, Zone(0.79, 0.60 + 0.06 * i, 0.81, 0.62 + 0.06 * i), nom, x, police=nom)
    for i, (nom, x) in enumerate(zip(POLICES, _X_POLICES))
])

ZONE_THEME = Zone(0.800, 0.290, 0.900, 0.390)
ZONE_MENU = Zone(0.300, 0.930, 0.700, 1.030)

def _dessiner_apercu_plateau(theme: Theme, ox: float, oy: float,
                             fond_disque: str, fond_plaque: str, style_trous: int) -> None:
    fltk.cercle(px(ox + 0.05), px(oy + 0.05), px(0.055), theme.trait, fond_disque)
    fltk.polygone([(px(ox + dx), px(oy + dy)) for dx, dy in _CONTOUR_APERCU],
                  theme.trait, fond_plaque)

    contour_ext, fond_ext, contour_int, fond_int = _STYLES_TROUS[style_trous]
    for ligne in range(8):
        for colonne in range(8):
            x = px(ox + 0.008 + 0.012 * colonne)
            y = px(oy + 0.008 + 0.012 * ligne)
            fltk.cercle(x, y, px(0.004), contour_ext, fond_ext)
            fltk.cercle(x, y, px(0.0025), contour_int, fond_int)

def _dessiner_bouton_theme() -> None:
    """Le bouton montre le thème vers lequel on bascule."""
    zone = ZONE_THEME
    cx, cy = zone.centre
    if parametres.theme_interface == 1:  # sombre -> bouton « clair » (lune)
        dessiner_rectangle(zone, "black", "#FAF9D0")
        fltk.cercle(px(cx), px(cy), px(0.030), "black", "black")
        fltk.cercle(px(cx - 0.005), px(cy - 0.005), px(0.027), "#FAF9D0", "#FAF9D0")
    else:                                # clair -> bouton « sombre » (soleil)
        dessiner_rectangle(zone, "white", "#010014")
        fltk.cercle(px(cx), px(cy), px(0.015), "white", "white")
        for dx, dy in ((0, -.03), (0, .03), (-.025, 0), (.025, 0),
                       (.02, .02), (.02, -.02), (-.02, .02), (-.02, -.02)):
            fltk.cercle(px(cx + dx), px(cy + dy), px(0.003), "white", "white")

def _dessiner_ecran() -> None:
    theme = theme_actuel()
    fltk.efface_tout()
    dessiner_fond(theme)

    for ox, oy, fond_disque, fond_plaque, style in _APERCUS_PLATEAU:
        _dessiner_apercu_plateau(theme, ox, oy, fond_disque, fond_plaque, style)
    for forme, x, y, couleur in _APERCUS_FORME:
        dessiner_forme(forme, px(x), px(y), px(RAYON_BOULE), couleur)

    for groupe in (GROUPE_PLATEAU, GROUPE_FORME, GROUPE_LANGUE, GROUPE_POLICE):
        groupe.dessiner(theme)

    ecrire(0.66, 0.550, t("menu_options_langue"), 0.022, theme)
    ecrire(0.85, 0.550, t("menu_options_police"), 0.022, theme)
    ecrire(0.85, 0.435, t("menu_options_theme"), 0.016, theme)
    ecrire(0.30, 0.650, "ROLIT", 0.078, theme)
    ecrire(0.30, 0.730, "2025", 0.036, theme)

    _dessiner_bouton_theme()
    dessiner_bouton(ZONE_MENU, t("menu_options_menu"), theme)

def _dessiner_indicateurs() -> List:
    theme = theme_actuel()
    return [
        GROUPE_PLATEAU.indicateur(parametres.mode_plateau, theme),
        GROUPE_FORME.indicateur(parametres.mode_boules, theme),
        GROUPE_LANGUE.indicateur(parametres.index_langue, theme),
        GROUPE_POLICE.indicateur(parametres.index_police, theme),
    ]

def afficher() -> str:
    """Affiche les paramètres ; retourne ``"menu"`` ou ``"quitter"``."""
    _dessiner_ecran()
    indicateurs = _dessiner_indicateurs()

    while True:
        type_evenement = fltk.type_ev(fltk.attend_ev())
        if type_evenement == "Quitte":
            return "quitter"
        if type_evenement != "ClicGauche":
            continue
        if ZONE_MENU.sous_la_souris():
            return "menu"

        redessiner = False

        mode = GROUPE_PLATEAU.valeur_cliquee()
        # Le plateau « nuit » n'est disponible qu'avec le thème sombre.
        if mode is not None and (mode != 3 or parametres.theme_interface == 1):
            parametres.mode_plateau = mode

        forme = GROUPE_FORME.valeur_cliquee()
        if forme is not None:
            parametres.mode_boules = forme

        langue = GROUPE_LANGUE.valeur_cliquee()
        if langue is not None:
            parametres.index_langue = langue
            redessiner = True

        police = GROUPE_POLICE.valeur_cliquee()
        if police is not None:
            parametres.index_police = police
            redessiner = True

        if ZONE_THEME.sous_la_souris():
            parametres.theme_interface = 1 - parametres.theme_interface
            if parametres.theme_interface == 0 and parametres.mode_plateau == 3:
                parametres.mode_plateau = 0
            redessiner = True

        parametres.sauvegarder()

        if redessiner:
            _dessiner_ecran()
        else:
            effacer(indicateurs)
        indicateurs = _dessiner_indicateurs()
