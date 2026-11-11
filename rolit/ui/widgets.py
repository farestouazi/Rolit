"""Briques de base de l'interface : zones cliquables, boutons, boutons radio."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List, Optional, Sequence, Tuple

import fltk

from ..affichage import HAUTEUR, TAILLE, px
from ..constantes import POLICES
from ..parametres import parametres
from .theme import Theme

def police_active() -> str:
    return POLICES[parametres.index_police]

def effacer(objets: Any) -> None:
    """Efface un objet fltk, ou récursivement une liste/tuple d'objets."""
    if objets is None:
        return
    if isinstance(objets, (list, tuple)):
        for objet in objets:
            effacer(objet)
    else:
        fltk.efface(objets)

def dessiner_fond(theme: Theme):
    return fltk.rectangle(0, 0, TAILLE, HAUTEUR, theme.fond, theme.fond)

def ecrire(x: float, y: float, contenu: str, taille: float, theme: Theme,
           police: Optional[str] = None):
    """Écrit un texte centré en (x, y) ; coordonnées et taille en fractions."""
    return fltk.texte(
        px(x), px(y), contenu,
        couleur=theme.trait,
        ancrage="center",
        police=police or police_active(),
        taille=int(px(taille)),
    )

@dataclass(frozen=True)
class Zone:
    """Rectangle exprimé en fractions de la largeur de la fenêtre."""

    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def centre(self) -> Tuple[float, float]:
        return (self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2

    def contient(self, x: float, y: float) -> bool:
        """``x`` et ``y`` sont des coordonnées en pixels."""
        return px(self.x1) <= x <= px(self.x2) and px(self.y1) <= y <= px(self.y2)

    def sous_la_souris(self) -> bool:
        return self.contient(fltk.abscisse_souris(), fltk.ordonnee_souris())

def dessiner_rectangle(zone: Zone, contour: str, remplissage: str, epaisseur: float = 1):
    return fltk.rectangle(
        px(zone.x1), px(zone.y1), px(zone.x2), px(zone.y2),
        contour, remplissage, epaisseur,
    )

def dessiner_bouton(zone: Zone, libelle: str, theme: Theme, taille: float = 0.024) -> List:
    """Dessine un bouton (cadre + libellé centré) et retourne ses objets."""
    return [
        dessiner_rectangle(zone, theme.trait, theme.inverse),
        ecrire(*zone.centre, libelle, taille, theme),
    ]

def attendre_action(actions: Iterable[Tuple[Zone, str]]) -> str:
    """Bloque jusqu'à un clic gauche dans l'une des zones ; retourne son action.

    Retourne ``"quitter"`` si la fenêtre est fermée.
    """
    actions = tuple(actions)
    while True:
        evenement = fltk.attend_ev()
        type_evenement = fltk.type_ev(evenement)
        if type_evenement == "Quitte":
            return "quitter"
        if type_evenement == "ClicGauche":
            for zone, action in actions:
                if zone.sous_la_souris():
                    return action

@dataclass(frozen=True)
class OptionRadio:
    valeur: Any
    zone: Zone                      # case cliquable
    libelle: str = ""
    texte_x: float = 0.0            # abscisse du libellé (fraction)
    police: Optional[str] = None    # police du libellé (police active par défaut)

class GroupeRadio:
    """Groupe de cases à cocher exclusives avec leur libellé."""

    def __init__(self, options: Sequence[OptionRadio], taille_texte: float = 0.016):
        self.options = tuple(options)
        self.taille_texte = taille_texte

    def dessiner(self, theme: Theme) -> None:
        for option in self.options:
            dessiner_rectangle(option.zone, theme.trait, theme.inverse, px(0.003))
            if option.libelle:
                ecrire(option.texte_x, option.zone.centre[1], option.libelle,
                       self.taille_texte, theme, option.police)

    def indicateur(self, valeur: Any, theme: Theme):
        """Dessine le repère de sélection sur ``valeur`` (``None`` si absente)."""
        for option in self.options:
            if option.valeur == valeur:
                x, y = option.zone.centre
                return fltk.cercle(px(x), px(y), px(0.007), theme.trait, theme.trait)
        return None

    def valeur_cliquee(self) -> Any:
        """Valeur de l'option sous la souris, ou ``None``."""
        for option in self.options:
            if option.zone.sous_la_souris():
                return option.valeur
        return None
