"""Modèle de données d'une partie (sérialisable en JSON)."""
from __future__ import annotations

import copy
import random
from dataclasses import asdict, dataclass, fields
from typing import Any, Dict, List, Sequence

from . import regles
from .constantes import COULEUR_NEUTRE, COULEURS_SELECTIONNABLES, NOM_CPU
from .regles import Plateau

@dataclass
class Partie:
    """État complet d'une partie.

    ``nombre_joueurs`` vaut 1 pour une partie contre le CPU ; il y a alors
    deux participants (voir :attr:`nombre_participants`).
    ``index_couleur`` est l'indice (à partir de 1) du joueur dont c'est le tour.
    """

    nombre_joueurs: int
    limite_points: int
    noms_joueurs: List[str]
    couleurs_joueurs: List[str]
    couleurs_boules: Plateau
    couleurs_boules_init: Plateau
    score_total: List[int]
    score_manche: List[int]
    index_couleur: int = 1
    statut_manche: bool = True   # True : la manche vient de commencer
    nombre_manches: int = 1
    statut_partie: bool = False  # True : la partie est terminée

    # --- Création ----------------------------------------------------------
    @classmethod
    def nouvelle(
        cls,
        nombre_joueurs: int,
        limite_points: int,
        noms: Sequence[str],
        couleurs: Sequence[str],
    ) -> "Partie":
        """Crée une partie à partir des noms et couleurs des joueurs humains."""
        contre_cpu = nombre_joueurs == 1
        participants = 2 if contre_cpu else nombre_joueurs

        couleurs_joueurs = list(couleurs) + [COULEUR_NEUTRE] * (4 - len(couleurs))
        noms_joueurs = list(noms)
        if contre_cpu:
            libres = [c for c in COULEURS_SELECTIONNABLES if c not in couleurs_joueurs]
            couleurs_joueurs[1] = random.choice(libres)
            noms_joueurs.append(NOM_CPU)

        plateau = regles.plateau_initial(participants, couleurs_joueurs)
        partie = cls(
            nombre_joueurs=nombre_joueurs,
            limite_points=limite_points,
            noms_joueurs=noms_joueurs,
            couleurs_joueurs=couleurs_joueurs,
            couleurs_boules=plateau,
            couleurs_boules_init=copy.deepcopy(plateau),
            score_total=[0] * participants,
            score_manche=[0] * participants,
        )
        partie.recalculer_scores()
        return partie

    # --- Informations dérivées --------------------------------------------
    @property
    def contre_cpu(self) -> bool:
        return self.nombre_joueurs == 1

    @property
    def nombre_participants(self) -> int:
        return 2 if self.contre_cpu else self.nombre_joueurs

    @property
    def couleur_courante(self) -> str:
        return self.couleurs_joueurs[self.index_couleur - 1]

    @property
    def gagnant_manche(self) -> str:
        return self.noms_joueurs[self.score_manche.index(max(self.score_manche))]

    @property
    def gagnant_partie(self) -> str:
        return self.noms_joueurs[self.score_total.index(max(self.score_total))]

    @property
    def limite_atteinte(self) -> bool:
        return any(score >= self.limite_points for score in self.score_total)

    # --- Évolution de la partie -------------------------------------------
    def passer_au_joueur_suivant(self) -> None:
        self.index_couleur = self.index_couleur % self.nombre_participants + 1

    def recalculer_scores(self) -> None:
        self.score_manche = regles.calculer_scores(
            self.couleurs_boules, self.couleurs_joueurs, self.nombre_participants
        )

    def terminer_manche(self) -> None:
        """Cumule les scores de la manche puis prépare la manche suivante."""
        for i, points in enumerate(self.score_manche):
            self.score_total[i] += points
        self.nombre_manches += 1
        self.couleurs_boules = copy.deepcopy(self.couleurs_boules_init)
        self.statut_manche = True
        self.recalculer_scores()

    # --- Sérialisation -----------------------------------------------------
    def vers_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def depuis_dict(cls, donnees: Dict[str, Any]) -> "Partie":
        noms = {champ.name for champ in fields(cls)}
        return cls(**{cle: valeur for cle, valeur in donnees.items() if cle in noms})
