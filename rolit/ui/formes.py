"""Dessin des boules (rond, carré, triangle, étoile) avec leurs reflets."""
from __future__ import annotations

from typing import List, Optional, Sequence

import fltk

from ..affichage import TAILLE
from .theme import PALETTE

RAYON_BOULE = 0.036      # rayon d'une boule du plateau (fraction de la fenêtre)
CARRE_DEMI_COTE = 0.031
TRIANGLE_COTE = 0.072
ETOILE_TAILLE = 0.080

# Sommets des étoiles, en fractions de ETOILE_TAILLE autour du centre.
_ETOILE_CONTOUR = ((0, .25), (.25, .5), (.15, .12), (.5, -.04), (.08, -.04), (0, -.4),
                   (-.08, -.04), (-.5, -.04), (-.15, .12), (-.25, .5))
_ETOILE_CORPS = ((0, .2), (.2, .41), (.11, .1), (.4, -.02), (.06, -.02), (0, -.31),
                 (-.06, -.02), (-.4, -.02), (-.11, .1), (-.2, .41))
_ETOILE_REFLET = ((0, .2), (.11, .1), (.06, -.02), (-.06, -.02), (-.11, .1))

def _disque(x: float, y: float, rayon: float, couleur: str):
    return fltk.cercle(x, y, rayon, couleur, couleur)

def _boule_ronde(x, y, rayon, echelle, nuances):
    n1, n2, n3, n4 = nuances
    return [
        _disque(x, y, rayon, n1),
        _disque(x, y - rayon / 20, rayon / 1.1, n2),
        _disque(x - rayon / 6, y - rayon / 5, rayon / 1.8, n3),
        _disque(x - rayon / 12, y - rayon / 2.8, rayon / 4, n4),
        _disque(x - rayon / 2.5, y - rayon / 20, rayon / 7, n4),
    ]

def _boule_carree(x, y, rayon, echelle, nuances):
    n1, n2, n3, n4 = nuances
    c = TAILLE * CARRE_DEMI_COTE * echelle
    return [
        fltk.rectangle(x - c, y - c, x + c, y + c, "black", n1),
        fltk.rectangle(x - c * 7 / 8, y - c * 7 / 8, x + c * 7 / 8, y + c * 7 / 8, n2, n2),
        _disque(x + c / 56, y - c / 46, c * 3 / 5, n3),
        _disque(x + c / 10, y - c / 7, c * 3 / 12, n4),
        _disque(x - c / 6, y + c / 5, c * 3 / 26, n4),
    ]

def _boule_triangulaire(x, y, rayon, echelle, nuances):
    n1, n2, n3, n4 = nuances
    c = TAILLE * TRIANGLE_COTE * echelle

    def triangle(haut, base_x, base_y):
        return [(x, y - c * haut), (x + c * base_x, y + c * base_y), (x - c * base_x, y + c * base_y)]

    return [
        fltk.polygone(triangle(1 / 1.68, .48, .34), "black", n1),
        fltk.polygone(triangle(1 / 1.96, .42, .30), n2, n2),
        fltk.polygone(triangle(1 / 3, .24, .16), n3, n3),
        _disque(x + c / 78, y - c / 10, c * .07, n4),
        _disque(x - c / 16, y + c / 30, c * .04, n4),
    ]

def _boule_etoile(x, y, rayon, echelle, nuances):
    n1, n2, n3, n4 = nuances
    c = TAILLE * ETOILE_TAILLE * echelle

    def polygone(sommets: Sequence):
        return [(x + c * dx, y + c * dy) for dx, dy in sommets]

    return [
        fltk.polygone(polygone(_ETOILE_CONTOUR), n1, n1),
        fltk.polygone(polygone(_ETOILE_CORPS), n2, n2),
        fltk.polygone(polygone(_ETOILE_REFLET), n3, n3),
        _disque(x - c * .04, y + c * .11, c * .015, n4),
        _disque(x + c * .01, y + c * .04, c * .04, n4),
        _disque(x, y + c * .12, c * .014, n4),
    ]

_FORMES = (_boule_ronde, _boule_carree, _boule_triangulaire, _boule_etoile)

def dessiner_forme(index: int, x: float, y: float, rayon: float,
                   couleur: Optional[str]) -> List:
    if couleur is None:
        return []
    echelle = rayon / (TAILLE * RAYON_BOULE)
    return _FORMES[index](x, y, rayon, echelle, PALETTE[couleur])
