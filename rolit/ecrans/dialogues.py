"""Fenêtres de dialogue superposées au jeu : pause, fin de manche, fin de partie."""
from __future__ import annotations

from typing import List

import fltk

from ..affichage import px
from ..partie import Partie
from ..sauvegarde import sauvegarder_partie
from ..traductions import t
from ..ui.theme import Theme, couleur_principale, theme_actuel
from ..ui.widgets import (Zone, attendre_action, dessiner_bouton, dessiner_rectangle,
                          ecrire, effacer)

ZONE_PAUSE_REPRENDRE = Zone(0.300, 0.400, 0.700, 0.500)
ZONE_PAUSE_SAUVER = Zone(0.300, 0.550, 0.700, 0.650)

ZONE_MANCHE_SUIVANTE = Zone(0.5125, 0.725, 0.825, 0.825)
ZONE_MANCHE_QUITTER = Zone(0.175, 0.725, 0.4875, 0.825)
ZONE_PARTIE_QUITTER = Zone(0.325, 0.700, 0.675, 0.800)

_X_RESULTATS = {2: (0.350, 0.650), 3: (0.325, 0.500, 0.675), 4: (0.300, 0.425, 0.550, 0.675)}

def menu_pause() -> str:
    """Retourne ``"jouer"`` (reprendre), ``"menu"`` (sauvegarder et quitter) ou ``"quitter"``."""
    theme = theme_actuel()
    objets: List = [
        dessiner_rectangle(Zone(0.250, 0.300, 0.750, 0.700), theme.trait, theme.fond),
        ecrire(0.5, 0.35, t("menu_pause_pause"), 0.024, theme),
    ]
    objets += dessiner_bouton(ZONE_PAUSE_REPRENDRE, t("menu_pause_reprendre"), theme, 0.016)
    objets += dessiner_bouton(ZONE_PAUSE_SAUVER, t("menu_pause_sauvquit"), theme, 0.016)

    decision = attendre_action(((ZONE_PAUSE_REPRENDRE, "jouer"), (ZONE_PAUSE_SAUVER, "menu")))
    effacer(objets)
    return decision

def _panneau_resultats(partie: Partie, scores: List[int], cle_titre: str,
                       cle_gagnant: str, gagnant: str, theme: Theme) -> List:
    """Cadre commun : titre, gagnant et tableau des scores."""
    objets: List = [
        dessiner_rectangle(Zone(0.150, 0.200, 0.850, 0.850), theme.trait, theme.fond),
        ecrire(0.5, 0.25, t(cle_titre), 0.030, theme),
        ecrire(0.5, 0.35, f"{t(cle_gagnant)} : {gagnant}", 0.024, theme),
        ecrire(0.5, 0.45, t("menu_fin_manche_scores"), 0.020, theme),
    ]
    positions = _X_RESULTATS[len(scores)]
    for x, nom, score, couleur in zip(positions, partie.noms_joueurs, scores, partie.couleurs_joueurs):
        objets.append(ecrire(x, 0.500, nom, 0.018, theme))
        objets.append(ecrire(x, 0.545, str(score), 0.018, theme))
        objets.append(fltk.cercle(
            px(x), px(0.600), px(0.015), theme.trait, couleur_principale(couleur),
            max(1, int(px(0.002))),
        ))
    return objets

def fin_de_manche(partie: Partie) -> str:
    """Retourne ``"jouer"`` (manche suivante), ``"menu"`` ou ``"quitter"``."""
    theme = theme_actuel()
    objets = _panneau_resultats(
        partie, partie.score_manche, "menu_fin_manche_fini",
        "menu_fin_manche_gagnant", partie.gagnant_manche, theme,
    )
    objets += dessiner_bouton(ZONE_MANCHE_SUIVANTE, t("menu_fin_manche_suivant"), theme, 0.016)
    objets += dessiner_bouton(ZONE_MANCHE_QUITTER, t("menu_fin_manche_quitter"), theme, 0.016)

    decision = attendre_action(((ZONE_MANCHE_SUIVANTE, "jouer"), (ZONE_MANCHE_QUITTER, "menu")))
    effacer(objets)
    return decision

def fin_de_partie(partie: Partie) -> str:
    """Retourne ``"menu"`` ou ``"quitter"``. Marque la partie comme terminée."""
    theme = theme_actuel()
    objets = _panneau_resultats(
        partie, partie.score_total, "menu_fin_partie_fini",
        "menu_fin_partie_gagnant", partie.gagnant_partie, theme,
    )
    objets += dessiner_bouton(ZONE_PARTIE_QUITTER, t("menu_fin_manche_quitter"), theme, 0.018)

    decision = attendre_action(((ZONE_PARTIE_QUITTER, "menu"),))
    effacer(objets)
    if decision == "menu":
        partie.statut_partie = True
        sauvegarder_partie(partie)
    return decision
