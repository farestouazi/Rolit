"""Dimensions de la fenêtre."""
from __future__ import annotations

from typing import Optional, Tuple

TAILLES_DISPONIBLES = (400, 500, 600, 700, 800, 900, 1000, 1100, 1200)
TAILLE_PAR_DEFAUT = 600
RATIO_HAUTEUR = 1.1
MARGE_VERTICALE = 80

def _dimensions_ecran() -> Optional[Tuple[int, int]]:
    """Retourne (largeur, hauteur) de l'écran, ou None s'il est inconnu."""
    try:
        import pyautogui

        taille = pyautogui.size()
        return int(taille[0]), int(taille[1])
    except Exception:  # bibliothèque absente, pas d'écran, etc.
        return None

def trouver_taille_ideale(dimensions: Optional[Tuple[int, int]] = None) -> int:
    """Choisit la plus grande largeur de fenêtre qui tient sur l'écran."""
    if dimensions is None:
        return TAILLE_PAR_DEFAUT
    largeur, hauteur = dimensions
    possibles = [
        t
        for t in TAILLES_DISPONIBLES
        if t <= largeur and t * RATIO_HAUTEUR + MARGE_VERTICALE <= hauteur
    ]
    return max(possibles) if possibles else min(TAILLES_DISPONIBLES)

TAILLE = trouver_taille_ideale(_dimensions_ecran())
HAUTEUR = TAILLE * RATIO_HAUTEUR

def px(fraction: float) -> float:
    """Convertit une fraction de la largeur de la fenêtre en pixels."""
    return TAILLE * fraction
