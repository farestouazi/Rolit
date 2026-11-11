"""Sauvegarde et restauration de la partie en cours."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from .constantes import FICHIER_SAUVEGARDE
from .partie import Partie

def sauvegarder_partie(partie: Partie, chemin: Path = FICHIER_SAUVEGARDE) -> None:
    """Écrit la partie sur disque (écriture atomique pour éviter un fichier corrompu)."""
    temporaire = Path(f"{chemin}.tmp")
    with open(temporaire, "w", encoding="utf-8") as fichier:
        json.dump(partie.vers_dict(), fichier)
    os.replace(temporaire, chemin)

def charger_partie(chemin: Path = FICHIER_SAUVEGARDE) -> Optional[Partie]:
    """Retourne la partie sauvegardée, ou ``None`` si absente ou illisible."""
    try:
        with open(chemin, encoding="utf-8") as fichier:
            return Partie.depuis_dict(json.load(fichier))
    except (OSError, ValueError, TypeError, AttributeError):
        return None
