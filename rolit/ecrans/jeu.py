"""Écran de jeu : déroulement d'une partie et de ses manches."""
from __future__ import annotations

import random
from typing import Optional

import fltk

from .. import regles
from ..affichage import px
from ..constantes import PREMIER_JOUEUR_ALEATOIRE
from ..parametres import parametres
from ..partie import Partie
from ..sauvegarde import charger_partie, sauvegarder_partie
from ..traductions import t
from ..ui.formes import dessiner_forme
from ..ui.plateau import (ZONE_PAUSE, VuePieces, afficher_invite_validation,
                          afficher_scores_manche, case_sous_curseur, dessiner_decor,
                          dessiner_indicateur_tour)
from ..ui.theme import Theme, theme_actuel
from ..ui.widgets import dessiner_fond, dessiner_rectangle, Zone, ecrire, effacer
from . import dialogues

_ZONE_ANNONCE = Zone(0.350, 0.350, 0.650, 0.650)

def jouer_partie() -> str:
    """Enchaîne les manches jusqu'à la fin de la partie ou une sortie.
    Retourne ``"menu"`` ou ``"quitter"``.
    """
    partie = charger_partie()
    if partie is None:
        return "menu"

    fltk.efface_tout()
    dessiner_fond(theme_actuel())

    while True:
        if partie.limite_atteinte:
            return dialogues.fin_de_partie(partie)

        decision = jouer_manche(partie)
        sauvegarder_partie(partie)
        if decision != "jouer":
            return decision

def jouer_manche(partie: Partie) -> str:
    """Joue (ou reprend) une manche.
    Retourne ``"jouer"`` pour enchaîner sur une nouvelle manche (ou reprendre
    après la pause), ``"menu"`` ou ``"quitter"``.
    """
    theme = theme_actuel()

    fltk.efface_tout()
    dessiner_decor(partie, theme)
    vue = VuePieces()
    vue.afficher(partie.couleurs_boules)

    if partie.statut_manche and not _annoncer_premier_joueur(partie, theme):
        return "quitter"

    texte_manche = ecrire(
        0.5, 0.040, f"{t('menu_jeu_nmanches')} : {partie.nombre_manches}", 0.021, theme
    )
    scores = afficher_scores_manche(partie, theme)
    indicateur = dessiner_indicateur_tour(partie)

    while not regles.plateau_plein(partie.couleurs_boules):
        evenement = fltk.attend_ev()
        type_evenement = fltk.type_ev(evenement)
        if type_evenement == "Quitte":
            return "quitter"
        if type_evenement != "ClicGauche":
            continue

        if ZONE_PAUSE.sous_la_souris():
            return dialogues.menu_pause()

        case = case_sous_curseur(fltk.abscisse_souris(), fltk.ordonnee_souris())
        if case is None or not regles.coup_valide(partie.couleurs_boules, *case):
            continue

        effacer(indicateur)
        if _jouer_coup(partie, case, vue, theme) == "quitter":
            return "quitter"

        partie.recalculer_scores()
        sauvegarder_partie(partie)
        effacer(scores)
        scores = afficher_scores_manche(partie, theme)
        indicateur = dessiner_indicateur_tour(partie)

    partie.recalculer_scores()
    sauvegarder_partie(partie)

    decision = dialogues.fin_de_manche(partie)
    if decision == "jouer":
        partie.terminer_manche()
        sauvegarder_partie(partie)
    return decision

def _annoncer_premier_joueur(partie: Partie, theme: Theme) -> bool:
    """Affiche qui commence ; retourne False si la fenêtre est fermée."""
    if PREMIER_JOUEUR_ALEATOIRE and not partie.contre_cpu:
        premier = random.randrange(partie.nombre_participants)
    else:
        premier = 0
    partie.index_couleur = premier + 1

    objets = [
        dessiner_rectangle(_ZONE_ANNONCE, theme.trait, theme.fond, px(0.003)),
        dessiner_forme(parametres.mode_boules, px(0.5), px(0.5), px(0.080),
                       partie.couleurs_joueurs[premier]),
        ecrire(0.5, 0.605,
               f"{partie.noms_joueurs[premier]} {t('jeu_selection_commence')}", 0.018, theme),
    ]
    evenement = fltk.attend_ev()
    if fltk.type_ev(evenement) == "Quitte":
        return False

    partie.statut_manche = False
    effacer(objets)
    return True

def _attendre_decision() -> str:
    """Clic gauche : ``"valider"`` ; clic droit : ``"annuler"``."""
    while True:
        type_evenement = fltk.type_ev(fltk.attend_ev())
        if type_evenement == "Quitte":
            return "quitter"
        if type_evenement == "ClicGauche":
            return "valider"
        if type_evenement == "ClicDroit":
            return "annuler"

def _jouer_coup(partie: Partie, case, vue: VuePieces, theme: Theme) -> str:
    """Pose une boule, demande confirmation, puis fait jouer le CPU si besoin.
    Retourne ``"quitter"`` si la fenêtre est fermée pendant la confirmation
    (le coup en attente est alors annulé), sinon ``"ok"``.
    """
    plateau_avant = [rangee[:] for rangee in partie.couleurs_boules]
    cases = regles.jouer_coup(partie.couleurs_boules, *case, partie.couleur_courante)
    vue.afficher(partie.couleurs_boules, cases)

    invite = afficher_invite_validation(theme)
    decision = _attendre_decision()
    effacer(invite)

    if decision != "valider":
        partie.couleurs_boules = plateau_avant
        vue.afficher(partie.couleurs_boules, cases)
        return "quitter" if decision == "quitter" else "ok"

    partie.passer_au_joueur_suivant()
    if partie.contre_cpu:
        _jouer_cpu(partie, vue)
    return "ok"

def _jouer_cpu(partie: Partie, vue: VuePieces) -> None:
    """Le CPU joue un coup valide au hasard."""
    case: Optional[tuple] = regles.coup_aleatoire(partie.couleurs_boules)
    if case is None:
        return
    cases = regles.jouer_coup(partie.couleurs_boules, *case, partie.couleur_courante)
    vue.afficher(partie.couleurs_boules, cases)
    partie.passer_au_joueur_suivant()
