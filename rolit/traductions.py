"""Textes de l'interface dans les langues disponibles."""
from .parametres import parametres

# L'ordre des traductions suit constantes.LANGUES :
# français, anglais, espagnol, italien, allemand.
TEXTES = {
    "menu_principal_reprendre": ["REPRENDRE", "RESUME", "REANUDAR", "RIPRENDERE", "FORTSETZEN"],
    "menu_principal_jouer": ["JOUER", "PLAY", "JUGAR", "GIOCARE", "SPIELEN"],
    "menu_principal_options": ["PARAMETRES", "SETTINGS", "PARAMETROS", "PARAMETRI", "PARAMETER"],
    "menu_principal_quitter": ["QUITTER", "EXIT", "SALIDA", "USCITA", "AUSFAHRT"],
    "menu_options_menu": ["MENU", "MENU", "MENU", "MENU", "MENU"],
    "menu_options_police": ["Police", "Font", "Fuente", "Carattere", "Schriftart"],
    "menu_options_langue": ["Langue", "Language", "Idioma", "Lingua", "Sprache"],
    "menu_options_theme": ["Thème", "Theme", "Tema", "Tema", "Thema"],
    "menu_prepartie_njoueurs": ["Nombre de joueurs", "Number of players", "Numero de jugadores", "Numero di giocatori", "Anzahl der Spieler"],
    "menu_prepartie_lpoints": ["Limite de points", "Point limit", "Límite de puntos", "Limite di punti", "Punktegrenze"],
    "menu_prepartie_suivant": ["SUIVANT", "NEXT", "SIGUIENTE", "SUCCESSIVO", "NACHSTE"],
    "menu_prepartie_joueur": ["Joueur", "Player", "Jugador", "Giocatore", "Spieler"],
    "menu_prepartie_nom": ["Nom", "Name", "Nombre", "Nome", "Name"],
    "jeu_selection_commence": ["commence", "starts", "comienza", "inizia", "beginnt"],
    "menu_jeu_nmanches": ["Manche", "Round", "Ronda", "Mano", "Runde"],
    "menu_jeu_retour": ["Clic droit pour annuler", "Right click to cancel", "Clic derecho para cancelar", "Clic destro per annullare", "Rechtsklick zum Abbrechen"],
    "menu_jeu_continue": ["Clic gauche pour continuer", "Left click to continue", "Clic izquierdo para continuar", "Clic sinistro per continuare", "Linksklick um fortzufahren"],
    "menu_fin_manche_fini": ["Fin de manche", "End of round", "Fin de ronda", "Fine della manche", "Rundenende"],
    "menu_fin_manche_scores": ["Scores", "Scores", "Puntuaciones", "Punteggi", "Punktzahlen"],
    "menu_fin_manche_gagnant": ["Gagnant", "Winner", "Ganador", "Vincitore", "Gewinner"],
    "menu_fin_manche_suivant": ["Suivant", "Next", "Siguiente", "Successivo", "Nachste"],
    "menu_fin_manche_quitter": ["Quitter", "Exit", "Salir", "Uscire", "Verlassen"],
    "menu_fin_partie_fini": ["Partie finie", "Game over", "Juego terminado", "Partita finita", "Spiel beendet"],
    "menu_fin_partie_gagnant": ["Gagnant de la partie", "Winner of the game", "Ganador del juego", "Vincitore del gioco", "Gewinner des Spiels"],
    "menu_pause_pause": ["Pause", "Pause", "Pausa", "Pausa", "Pause"],
    "menu_pause_reprendre": ["Reprendre", "Resume", "Reanudar", "Riprendere", "Fortsetzen"],
    "menu_pause_sauvquit": ["Sauvegarder et quitter", "Save and Quit", "Guardar y salir", "Salva e esci", "Speichern und beenden"],
}

def t(cle: str) -> str:
    """Retourne le texte dans la langue active."""
    return TEXTES[cle][parametres.index_langue]
