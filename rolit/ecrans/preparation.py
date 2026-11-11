"""Préparation d'une partie : nombre de joueurs, limite de points, noms et couleurs."""
from __future__ import annotations

from typing import List, Optional, Tuple

import fltk

from ..affichage import px
from ..constantes import (COULEURS_SELECTIONNABLES, LONGUEUR_NOM_MAX, LONGUEUR_NOM_MIN,
                          TOUCHES_POSSIBLES)
from ..partie import Partie
from ..sauvegarde import sauvegarder_partie
from ..traductions import t
from ..ui.theme import couleur_principale, theme_actuel
from ..ui.widgets import (GroupeRadio, OptionRadio, Zone, dessiner_bouton, dessiner_fond,
                          dessiner_rectangle, ecrire, effacer)

ZONE_VALIDER_OPTIONS = Zone(0.300, 0.550, 0.700, 0.650)
ZONE_MENU_OPTIONS = Zone(0.300, 0.700, 0.700, 0.800)

ZONE_VALIDER_JOUEUR = Zone(0.300, 0.700, 0.700, 0.800)
ZONE_MENU_JOUEUR = Zone(0.300, 0.850, 0.700, 0.950)
ZONE_MAJUSCULE = Zone(0.100, 0.300, 0.200, 0.400)
ZONE_NOM = Zone(0.250, 0.300, 0.750, 0.400)

# (valeur, abscisse de la case, libellé, abscisse du libellé)
_JOUEURS = ((1, 0.345, "CPU", 0.395), (2, 0.465, "2", 0.500),
            (3, 0.585, "3", 0.620), (4, 0.705, "4", 0.740))
_POINTS = ((100, 0.345, "100", 0.400), (250, 0.465, "250", 0.520), (450, 0.585, "450", 0.640),
           (700, 0.705, "700", 0.760), (1000, 0.825, "1000", 0.880))

GROUPE_JOUEURS = GroupeRadio([
    OptionRadio(valeur, Zone(x, 0.390, x + 0.02, 0.410), libelle, tx)
    for valeur, x, libelle, tx in _JOUEURS
])
GROUPE_POINTS = GroupeRadio([
    OptionRadio(valeur, Zone(x, 0.450, x + 0.02, 0.470), libelle, tx)
    for valeur, x, libelle, tx in _POINTS
])

_X_COULEURS = {c: 0.2 + 0.1 * i for i, c in enumerate(COULEURS_SELECTIONNABLES)}

def afficher() -> str:
    """Retourne ``"jouer"`` (partie créée), ``"menu"`` ou ``"quitter"``."""
    statut, nombre_joueurs, limite_points = _choisir_options()
    if statut != "jouer":
        return statut
    return _saisir_joueurs(nombre_joueurs, limite_points)

# --- Étape 1 : nombre de joueurs et limite de points ------------------------
def _choisir_options() -> Tuple[str, int, int]:
    theme = theme_actuel()
    nombre_joueurs, limite_points = 4, 100

    fltk.efface_tout()
    dessiner_fond(theme)
    dessiner_bouton(ZONE_VALIDER_OPTIONS, t("menu_principal_jouer"), theme)
    dessiner_bouton(ZONE_MENU_OPTIONS, t("menu_options_menu"), theme)
    ecrire(0.18, 0.40, t("menu_prepartie_njoueurs"), 0.018, theme)
    ecrire(0.18, 0.46, t("menu_prepartie_lpoints"), 0.018, theme)
    GROUPE_JOUEURS.dessiner(theme)
    GROUPE_POINTS.dessiner(theme)

    indicateurs: List = []
    while True:
        indicateurs = [GROUPE_JOUEURS.indicateur(nombre_joueurs, theme),
                       GROUPE_POINTS.indicateur(limite_points, theme)]
        type_evenement = fltk.type_ev(fltk.attend_ev())
        effacer(indicateurs)

        if type_evenement == "Quitte":
            return "quitter", 0, 0
        if type_evenement != "ClicGauche":
            continue

        valeur = GROUPE_JOUEURS.valeur_cliquee()
        if valeur is not None:
            nombre_joueurs = valeur
        valeur = GROUPE_POINTS.valeur_cliquee()
        if valeur is not None:
            limite_points = valeur

        if ZONE_VALIDER_OPTIONS.sous_la_souris():
            return "jouer", nombre_joueurs, limite_points
        if ZONE_MENU_OPTIONS.sous_la_souris():
            return "menu", 0, 0

# --- Étape 2 : nom et couleur de chaque joueur ------------------------------
def _saisir_joueurs(nombre_joueurs: int, limite_points: int) -> str:
    noms: List[str] = []
    couleurs: List[str] = []
    majuscule = False

    for rang in range(nombre_joueurs):
        statut, nom, couleur, majuscule = _saisir_joueur(
            rang, nombre_joueurs, couleurs, majuscule
        )
        if statut != "suivant":
            return statut
        noms.append(nom)
        couleurs.append(couleur)

    sauvegarder_partie(Partie.nouvelle(nombre_joueurs, limite_points, noms, couleurs))
    return "jouer"

def _saisir_joueur(rang: int, total: int, couleurs_prises: List[str],
                   majuscule: bool) -> Tuple[str, str, Optional[str], bool]:
    """Saisie d'un joueur. Retourne (statut, nom, couleur, majuscule).

    Le statut vaut ``"suivant"`` quand le joueur est validé, sinon ``"menu"``
    ou ``"quitter"``.
    """
    theme = theme_actuel()
    fltk.efface_tout()
    dessiner_fond(theme)

    libelle = t("menu_principal_jouer") if rang == total - 1 else t("menu_prepartie_suivant")
    dessiner_bouton(ZONE_VALIDER_JOUEUR, libelle, theme)
    dessiner_bouton(ZONE_MENU_JOUEUR, t("menu_options_menu"), theme)
    dessiner_rectangle(ZONE_MAJUSCULE, theme.trait, theme.inverse)
    dessiner_rectangle(ZONE_NOM, theme.trait, theme.inverse)
    ecrire(0.5, 0.13, f"{t('menu_prepartie_joueur')} {rang + 1}", 0.030, theme)
    ecrire(0.5, 0.25, f"{t('menu_prepartie_nom')} :", 0.024, theme)

    for couleur, x in _X_COULEURS.items():
        fltk.cercle(px(x), px(0.53), px(0.025), theme.trait,
                    couleur_principale(couleur), px(0.001))
    groupe_couleurs = GroupeRadio([
        OptionRadio(couleur, Zone(x - 0.01, 0.59, x + 0.01, 0.61))
        for couleur, x in _X_COULEURS.items() if couleur not in couleurs_prises
    ])
    groupe_couleurs.dessiner(theme)

    nom = ""
    couleur: Optional[str] = None

    while True:
        dynamiques = [
            ecrire(0.5, 0.35, nom, 0.024, theme),
            ecrire(0.15, 0.35, "min" if majuscule else "MAJ", 0.018, theme),
            groupe_couleurs.indicateur(couleur, theme),
        ]
        evenement = fltk.attend_ev()
        type_evenement = fltk.type_ev(evenement)
        effacer(dynamiques)

        if type_evenement == "Quitte":
            return "quitter", nom, couleur, majuscule

        if type_evenement == "Touche":
            touche = fltk.touche(evenement)
            if touche == "BackSpace":
                nom = nom[:-1]
            elif len(touche) == 1 and touche in TOUCHES_POSSIBLES and len(nom) < LONGUEUR_NOM_MAX:
                nom += touche.upper() if majuscule else touche

        elif type_evenement == "ClicGauche":
            if ZONE_MAJUSCULE.sous_la_souris():
                majuscule = not majuscule

            choix = groupe_couleurs.valeur_cliquee()
            if choix is not None:
                couleur = choix

            if ZONE_VALIDER_JOUEUR.sous_la_souris():
                if couleur is not None and len(nom) >= LONGUEUR_NOM_MIN:
                    return "suivant", nom, couleur, majuscule
            elif ZONE_MENU_JOUEUR.sous_la_souris():
                return "menu", nom, couleur, majuscule
