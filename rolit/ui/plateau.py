"""Affichage du plateau de jeu : décor, boules, indicateurs et scores."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import fltk

from ..affichage import px
from ..constantes import TAILLE_PLATEAU
from ..parametres import parametres
from ..partie import Partie
from ..regles import Case, Plateau
from ..traductions import t
from .formes import RAYON_BOULE, dessiner_forme
from .theme import Theme, couleur_principale
from .widgets import Zone, dessiner_fond, dessiner_rectangle, ecrire, effacer

# --- Géométrie (fractions de la largeur de la fenêtre) ---------------------
ORIGINE_GRILLE = (0.080, 0.180)
PAS_CASE = 0.105

CENTRES_COTES = ((0.500, 0.155), (0.945, 0.600), (0.500, 1.045), (0.055, 0.600))
CENTRES_MINI_COTES = (
    ((0.400, 0.155), (0.600, 0.155)),
    ((0.945, 0.500), (0.945, 0.700)),
    ((0.400, 1.045), (0.600, 1.045)),
    ((0.055, 0.500), (0.055, 0.700)),
)

_CONTOUR_PLATEAU = [
    (0.050, 0.180), (0.060, 0.450), (0.080, 0.600), (0.060, 0.750), (0.050, 1.020),
    (0.053, 1.026), (0.0615, 1.0395), (0.074, 1.047), (0.350, 1.040), (0.500, 1.020),
    (0.650, 1.040), (0.920, 1.050), (0.926, 1.047), (0.9395, 1.0395), (0.947, 1.026),
    (0.950, 1.020), (0.940, 0.750), (0.920, 0.600), (0.940, 0.450), (0.950, 0.180),
    (0.947, 0.173), (0.9395, 0.1635), (0.926, 0.153), (0.920, 0.150), (0.650, 0.160),
    (0.500, 0.180), (0.350, 0.160), (0.080, 0.150), (0.074, 0.153), (0.0615, 0.1615),
    (0.053, 0.174), (0.050, 0.180),
]

ZONE_PAUSE = Zone(0.010, 0.010, 0.060, 0.060)
ZONE_ANNULER = Zone(0.080, 0.010, 0.400, 0.060)
ZONE_CONTINUER = Zone(0.600, 0.010, 0.920, 0.060)

def centre_case(ligne: int, colonne: int) -> Tuple[float, float]:
    """Centre (en pixels) de la case (ligne, colonne)."""
    return px(0.1325 + PAS_CASE * colonne), px(0.2325 + PAS_CASE * ligne)

def case_sous_curseur(x: float, y: float) -> Optional[Case]:
    """Case de la grille contenant le point (x, y) en pixels, ou ``None``."""
    colonne = (x - px(ORIGINE_GRILLE[0])) / px(PAS_CASE)
    ligne = (y - px(ORIGINE_GRILLE[1])) / px(PAS_CASE)
    if 0 <= colonne < TAILLE_PLATEAU and 0 <= ligne < TAILLE_PLATEAU:
        return int(ligne), int(colonne)
    return None

# --- Styles du plateau -----------------------------------------------------
@dataclass(frozen=True)
class StylePlateau:
    plateau: str
    cercle: str
    trou: str
    contour: str
    nuances_trou: Tuple[str, str, str]

STYLES = (
    StylePlateau("#828282", "#787878", "#707070", "black", ("#000000", "#151515", "#262626")),
    StylePlateau("#BFBFBF", "#BEBEBE", "#BBBBBB", "black", ("#757575", "#858585", "#AAAAAA")),
    StylePlateau("#F1C40F", "#F4D03F", "black", "white", ("#101010", "#252525", "#363636")),
    StylePlateau("black", "black", "black", "white", ("#101010", "#252525", "#363636")),
)

# --- Décor -----------------------------------------------------------------
def _dessiner_interieur_trou(x: float, y: float, rayon: float, style: StylePlateau) -> None:
    n1, n2, n3 = style.nuances_trou
    fltk.cercle(x, y, rayon, "black", n1)
    fltk.cercle(x - rayon * 5 / 32, y - rayon / 32, rayon * 17 / 32, n2, n2)
    fltk.cercle(x - rayon * 7 / 32, y + rayon * 2 / 32, rayon / 6, n3, n3)

def _dessiner_trous(style: StylePlateau) -> None:
    for ligne in range(TAILLE_PLATEAU):
        for colonne in range(TAILLE_PLATEAU):
            x, y = centre_case(ligne, colonne)
            fltk.cercle(x, y, px(0.048), style.contour, style.trou)
            _dessiner_interieur_trou(x, y, px(0.040), style)

def _dessiner_etoiles() -> None:
    """Ciel étoilé du mode nuit : points blancs aléatoires."""
    for _ in range(random.randint(200, 400)):
        fltk.cercle(
            random.uniform(px(0.080), px(0.920)),
            random.uniform(px(0.180), px(1.020)),
            px(0.001), "white", "white",
        )

def _dessiner_cotes(partie: Partie, style: StylePlateau) -> None:
    """Réserves de chaque joueur sur les quatre côtés du plateau."""
    for (cx, cy), minis in zip(CENTRES_COTES, CENTRES_MINI_COTES):
        fltk.cercle(px(cx), px(cy), px(0.016), style.contour, "gray", px(0.001))
        for mx, my in minis:
            fltk.cercle(px(mx), px(my), px(0.008), style.contour, "gray", px(0.001))

    for (cx, cy), couleur in zip(CENTRES_COTES, partie.couleurs_joueurs[: partie.nombre_participants]):
        fltk.cercle(px(cx), px(cy), px(0.018), style.contour, couleur_principale(couleur), px(0.001))

def _dessiner_bouton_pause(theme: Theme) -> None:
    fltk.cercle(px(0.035), px(0.035), px(0.025), theme.trait, theme.inverse, px(0.001))
    for x1, x2 in ((0.025, 0.0325), (0.0375, 0.045)):
        fltk.rectangle(px(x1), px(0.025), px(x2), px(0.045), theme.trait, theme.trait, px(0.001))

def dessiner_decor(partie: Partie, theme: Theme) -> None:
    """Dessine le fond, le plateau vide, les réserves et le bouton pause."""
    style = STYLES[parametres.mode_plateau]
    dessiner_fond(theme)
    fltk.cercle(px(0.5), px(0.6), px(0.47), style.contour, style.cercle, px(0.001))
    fltk.polygone([(px(x), px(y)) for x, y in _CONTOUR_PLATEAU], style.contour, style.plateau)
    _dessiner_cotes(partie, style)
    _dessiner_bouton_pause(theme)
    if parametres.mode_plateau == 3:
        _dessiner_etoiles()
    _dessiner_trous(style)

# --- Boules posées ---------------------------------------------------------
class VuePieces:
    """Suit les objets graphiques de chaque case pour les redessiner à la demande."""

    def __init__(self) -> None:
        self._objets: Dict[Case, List] = {}

    def afficher(self, plateau: Plateau, cases: Optional[Sequence[Case]] = None) -> None:
        """Synchronise l'affichage avec ``plateau`` (toutes les cases par défaut)."""
        if cases is None:
            cases = [(l, c) for l in range(TAILLE_PLATEAU) for c in range(TAILLE_PLATEAU)]
        for ligne, colonne in cases:
            effacer(self._objets.pop((ligne, colonne), None))
            couleur = plateau[ligne][colonne]
            if couleur is not None:
                x, y = centre_case(ligne, colonne)
                self._objets[(ligne, colonne)] = dessiner_forme(
                    parametres.mode_boules, x, y, px(RAYON_BOULE), couleur
                )

# --- Informations de tour --------------------------------------------------
def dessiner_indicateur_tour(partie: Partie) -> List:
    """Entoure en blanc la réserve du joueur dont c'est le tour."""
    joueur = partie.index_couleur - 1
    couleur = couleur_principale(partie.couleurs_joueurs[joueur])
    cx, cy = CENTRES_COTES[joueur]
    objets = [fltk.cercle(px(cx), px(cy), px(0.018), "white", None, px(0.003))]
    for mx, my in CENTRES_MINI_COTES[joueur]:
        objets.append(fltk.cercle(px(mx), px(my), px(0.009), "white", couleur, px(0.002)))
    return objets

_X_SCORES = {2: (0.300, 0.700), 3: (0.250, 0.500, 0.750), 4: (0.155, 0.385, 0.615, 0.845)}

def afficher_scores_manche(partie: Partie, theme: Theme) -> List:
    """Affiche « nom : score » de chaque participant en haut de l'écran."""
    return [
        ecrire(x, 0.090, f"{nom} : {score}", 0.018, theme)
        for x, nom, score in zip(
            _X_SCORES[partie.nombre_participants], partie.noms_joueurs, partie.score_manche
        )
    ]

def afficher_invite_validation(theme: Theme) -> List:
    """Rappelle les commandes : clic droit pour annuler, clic gauche pour valider."""
    objets = []
    for zone, cle in ((ZONE_ANNULER, "menu_jeu_retour"), (ZONE_CONTINUER, "menu_jeu_continue")):
        objets.append(dessiner_rectangle(zone, theme.trait, theme.fond, px(0.003)))
        objets.append(ecrire(*zone.centre, t(cle), 0.016, theme))
    return objets
