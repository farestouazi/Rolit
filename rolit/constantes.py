"""Constantes globales du jeu."""
from pathlib import Path

# --- Fichiers locaux -------------------------------------------------------
RACINE = Path(__file__).resolve().parent.parent
FICHIER_CONFIG = RACINE / "config.json"
FICHIER_SAUVEGARDE = RACINE / "save_game.json"

# --- Plateau et joueurs ----------------------------------------------------
TAILLE_PLATEAU = 8
COULEUR_NEUTRE = "non"
COULEURS_SELECTIONNABLES = ("red", "orange", "yellow", "green", "blue", "indigo", "pink")
NOM_CPU = "CPU"

OPTIONS_NOMBRE_JOUEURS = (1, 2, 3, 4)  # 1 = un joueur contre le CPU
OPTIONS_LIMITE_POINTS = (100, 250, 450, 700, 1000)

# Si True, le premier joueur de chaque manche est tiré au sort (sauf contre le CPU).
PREMIER_JOUEUR_ALEATOIRE = False

# --- Saisie du nom ---------------------------------------------------------
TOUCHES_POSSIBLES = "azertyuiopqsdfghjklmwxcvbn0123456789"
LONGUEUR_NOM_MIN = 3
LONGUEUR_NOM_MAX = 8

# --- Interface -------------------------------------------------------------
LANGUES = ("Francais", "English", "Espanol", "Italiano", "Deutsch")
POLICES = ("Rockwell", "Centaur", "Jokerman", "Candara", "Fixedsys")
POLICE_TITRE = "Centaur"
