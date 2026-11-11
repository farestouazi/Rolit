"""Paramètres utilisateur persistants (langue, police, thème, apparence)."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path

from .constantes import FICHIER_CONFIG, LANGUES, POLICES

# Nombre de valeurs acceptées pour chaque paramètre.
_LIMITES = {
    "index_langue": len(LANGUES),
    "index_police": len(POLICES),
    "mode_plateau": 4,
    "mode_boules": 4,
    "theme_interface": 2,
}

@dataclass
class Parametres:
    index_langue: int = 1
    index_police: int = 3
    mode_plateau: int = 0
    mode_boules: int = 0
    theme_interface: int = 0  # 0 = clair, 1 = sombre

    @classmethod
    def charger(cls, chemin: Path = FICHIER_CONFIG) -> "Parametres":
        """Lit le fichier de configuration ; retombe sur les valeurs par défaut."""
        try:
            with open(chemin, encoding="utf-8") as fichier:
                donnees = json.load(fichier)
        except (OSError, ValueError):
            return cls()
        if not isinstance(donnees, dict):
            return cls()

        valeurs = {}
        for champ in fields(cls):
            valeur = donnees.get(champ.name)
            if isinstance(valeur, int) and 0 <= valeur < _LIMITES[champ.name]:
                valeurs[champ.name] = valeur
        return cls(**valeurs)

    def sauvegarder(self, chemin: Path = FICHIER_CONFIG) -> None:
        try:
            with open(chemin, "w", encoding="utf-8") as fichier:
                json.dump(asdict(self), fichier, indent=2)
        except OSError:
            pass  # dossier en lecture seule : on garde les réglages en mémoire

parametres = Parametres.charger()
