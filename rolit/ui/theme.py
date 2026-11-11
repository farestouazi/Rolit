"""Thèmes de l'interface et palette des boules."""
from __future__ import annotations

from dataclasses import dataclass

from ..parametres import parametres

@dataclass(frozen=True)
class Theme:
    fond: str
    trait: str
    inverse: str

CLAIR = Theme(fond="#F1E3A4", trait="black", inverse="white")
SOMBRE = Theme(fond="#010014", trait="white", inverse="black")
THEMES = (CLAIR, SOMBRE)

def theme_actuel() -> Theme:
    return THEMES[parametres.theme_interface]

PALETTE = {
    "non":    ("#3C3B40", "#5F5C73", "#7D7C8E", "#B7B4C7"),
    "red":    ("#B90F12", "#E61D24", "#EE4A4B", "#F36C69"),
    "orange": ("#CC5D15", "#E97818", "#F59B5C", "#F8BB8E"),
    "yellow": ("#F2A81D", "#FAE202", "#F8E666", "#FDF899"),
    "blue":   ("#055A99", "#0083C4", "#3C9CCE", "#6BB0D9"),
    "indigo": ("#551CA6", "#762CBF", "#934ED9", "#B16BF0"),
    "pink":   ("#CE2290", "#F249C5", "#F86DD0", "#FA98E0"),
    "green":  ("#226A21", "#308D2F", "#369E35", "#58C158"),
}

def couleur_principale(nom: str) -> str:
    """Code hexadécimal de la couleur principale d'un joueur."""
    return PALETTE[nom][1]
