"""Menu principal."""
import fltk

from .. import __annee__, __version__
from ..constantes import POLICE_TITRE
from ..sauvegarde import charger_partie
from ..traductions import t
from ..ui.theme import theme_actuel
from ..ui.widgets import Zone, attendre_action, dessiner_bouton, dessiner_fond, ecrire

ZONE_REPRENDRE = Zone(0.350, 0.350, 0.650, 0.450)
ZONE_JOUER = Zone(0.350, 0.500, 0.650, 0.600)
ZONE_OPTIONS = Zone(0.350, 0.650, 0.650, 0.750)
ZONE_QUITTER = Zone(0.350, 0.800, 0.650, 0.900)

def afficher() -> str:
    """Affiche le menu principal et retourne l'écran choisi."""
    theme = theme_actuel()
    partie = charger_partie()
    reprise_possible = partie is not None and not partie.statut_partie

    fltk.efface_tout()
    dessiner_fond(theme)
    ecrire(0.5, 0.175, "ROLIT", 0.110, theme, police=POLICE_TITRE)
    ecrire(0.5, 0.275, f"V{__version__} - {__annee__}", 0.040, theme, police=POLICE_TITRE)

    boutons = [
        (ZONE_JOUER, "menu_principal_jouer", "prepartie"),
        (ZONE_OPTIONS, "menu_principal_options", "options"),
        (ZONE_QUITTER, "menu_principal_quitter", "quitter"),
    ]
    if reprise_possible:
        boutons.insert(0, (ZONE_REPRENDRE, "menu_principal_reprendre", "reprendre"))

    for zone, cle, _ in boutons:
        dessiner_bouton(zone, t(cle), theme)

    return attendre_action((zone, action) for zone, _, action in boutons)
