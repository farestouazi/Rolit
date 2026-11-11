"""Règles du jeu Rolit.
Le plateau est une grille 8x8 (liste de listes) contenant le nom de la couleur
de chaque boule, ou ``None`` pour une case vide.
"""
from __future__ import annotations

import random
from collections import Counter
from typing import List, Optional, Sequence, Tuple

from .constantes import TAILLE_PLATEAU

Plateau = List[List[Optional[str]]]
Case = Tuple[int, int]

DIRECTIONS: Tuple[Case, ...] = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
)

def creer_plateau_vide() -> Plateau:
    return [[None] * TAILLE_PLATEAU for _ in range(TAILLE_PLATEAU)]

def plateau_initial(nombre_participants: int, couleurs_joueurs: Sequence[str]) -> Plateau:
    """Plateau de départ : quatre boules au centre.

    À 3 ou 4 joueurs, chacun a une boule (la 4ᵉ est neutre à 3 joueurs).
    À 1 ou 2 joueurs, les deux boules des diagonales sont neutres.
    """
    c = couleurs_joueurs
    if nombre_participants >= 3:
        centre = (c[0], c[1], c[2], c[3])
    else:
        centre = (c[0], c[2], c[1], c[3])

    plateau = creer_plateau_vide()
    plateau[3][3], plateau[3][4], plateau[4][4], plateau[4][3] = centre
    return plateau

def dans_le_plateau(ligne: int, colonne: int) -> bool:
    return 0 <= ligne < TAILLE_PLATEAU and 0 <= colonne < TAILLE_PLATEAU

def a_une_voisine(plateau: Plateau, ligne: int, colonne: int) -> bool:
    """Vrai si au moins une des 8 cases voisines contient une boule."""
    for d_ligne, d_colonne in DIRECTIONS:
        l, c = ligne + d_ligne, colonne + d_colonne
        if dans_le_plateau(l, c) and plateau[l][c] is not None:
            return True
    return False

def coup_valide(plateau: Plateau, ligne: int, colonne: int) -> bool:
    """Une boule se pose sur une case vide, au contact d'une boule existante."""
    return (
        dans_le_plateau(ligne, colonne)
        and plateau[ligne][colonne] is None
        and a_une_voisine(plateau, ligne, colonne)
    )

def coups_valides(plateau: Plateau) -> List[Case]:
    return [
        (l, c)
        for l in range(TAILLE_PLATEAU)
        for c in range(TAILLE_PLATEAU)
        if coup_valide(plateau, l, c)
    ]

def boules_retournees(plateau: Plateau, ligne: int, colonne: int, couleur: str) -> List[Case]:
    """Cases qui changent de couleur si ``couleur`` est posée en (ligne, colonne)."""
    capturees: List[Case] = []
    for d_ligne, d_colonne in DIRECTIONS:
        ligne_courante, colonne_courante = ligne + d_ligne, colonne + d_colonne
        candidates: List[Case] = []
        while dans_le_plateau(ligne_courante, colonne_courante):
            contenu = plateau[ligne_courante][colonne_courante]
            if contenu is None:
                break
            if contenu == couleur:
                capturees.extend(candidates)
                break
            candidates.append((ligne_courante, colonne_courante))
            ligne_courante += d_ligne
            colonne_courante += d_colonne
    return capturees

def jouer_coup(plateau: Plateau, ligne: int, colonne: int, couleur: str) -> List[Case]:
    """Pose une boule et applique les captures.
    Retourne la liste des cases modifiées (la case jouée en premier).
    :raises ValueError: si le coup est invalide.
    """
    if not coup_valide(plateau, ligne, colonne):
        raise ValueError(f"Coup invalide en ({ligne}, {colonne})")

    capturees = boules_retournees(plateau, ligne, colonne, couleur)
    plateau[ligne][colonne] = couleur
    for l, c in capturees:
        plateau[l][c] = couleur
    return [(ligne, colonne)] + capturees

def coup_aleatoire(plateau: Plateau) -> Optional[Case]:
    """Choisit un coup valide au hasard."""
    possibles = coups_valides(plateau)
    return random.choice(possibles) if possibles else None

def plateau_plein(plateau: Plateau) -> bool:
    return all(case is not None for rangee in plateau for case in rangee)

def calculer_scores(
    plateau: Plateau, couleurs_joueurs: Sequence[str], nombre_participants: int
) -> List[int]:
    """Nombre de boules de chaque participant (les boules neutres ne comptent pas)."""
    compte = Counter(case for rangee in plateau for case in rangee)
    return [compte[couleurs_joueurs[i]] for i in range(nombre_participants)]
