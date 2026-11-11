"""Boucle principale : navigation entre les écrans."""
import fltk

from .affichage import HAUTEUR, TAILLE
from .ecrans import jeu, menu_principal, options, preparation

ECRANS = {
    "menu": menu_principal.afficher,
    "options": options.afficher,
    "prepartie": preparation.afficher,
    "reprendre": jeu.jouer_partie,
    "jouer": jeu.jouer_partie,
}

def main() -> None:
    fltk.cree_fenetre(TAILLE, int(HAUTEUR))
    ecran = "menu"
    while ecran in ECRANS:
        ecran = ECRANS[ecran]()
    fltk.ferme_fenetre()
