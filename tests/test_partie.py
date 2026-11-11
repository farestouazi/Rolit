import tempfile
import unittest
from pathlib import Path

from rolit.partie import Partie
from rolit.sauvegarde import charger_partie, sauvegarder_partie

class TestPartie(unittest.TestCase):
    def test_partie_contre_cpu(self):
        partie = Partie.nouvelle(1, 100, ["Alice"], ["red"])
        self.assertTrue(partie.contre_cpu)
        self.assertEqual(partie.nombre_participants, 2)
        self.assertEqual(partie.noms_joueurs, ["Alice", "CPU"])
        self.assertNotEqual(partie.couleurs_joueurs[1], "red")
        self.assertEqual(partie.score_manche, [1, 1])

    def test_alternance_des_tours_contre_cpu(self):
        partie = Partie.nouvelle(1, 100, ["Alice"], ["red"])
        partie.passer_au_joueur_suivant()
        self.assertEqual(partie.couleur_courante, partie.couleurs_joueurs[1])
        partie.passer_au_joueur_suivant()
        self.assertEqual(partie.index_couleur, 1)

    def test_alternance_des_tours_a_trois(self):
        partie = Partie.nouvelle(3, 100, ["a", "b", "c"], ["red", "blue", "green"])
        tours = []
        for _ in range(4):
            tours.append(partie.index_couleur)
            partie.passer_au_joueur_suivant()
        self.assertEqual(tours, [1, 2, 3, 1])

    def test_terminer_manche(self):
        partie = Partie.nouvelle(2, 100, ["a", "b"], ["red", "blue"])
        partie.couleurs_boules[0][0] = "red"
        partie.recalculer_scores()
        self.assertEqual(partie.score_manche, [2, 1])
        self.assertEqual(partie.gagnant_manche, "a")

        partie.terminer_manche()
        self.assertEqual(partie.score_total, [2, 1])
        self.assertEqual(partie.nombre_manches, 2)
        self.assertEqual(partie.score_manche, [1, 1])
        self.assertTrue(partie.statut_manche)
        self.assertIsNone(partie.couleurs_boules[0][0])

    def test_limite_atteinte(self):
        partie = Partie.nouvelle(2, 100, ["a", "b"], ["red", "blue"])
        self.assertFalse(partie.limite_atteinte)
        partie.score_total = [100, 3]
        self.assertTrue(partie.limite_atteinte)

class TestSauvegarde(unittest.TestCase):
    def test_aller_retour(self):
        partie = Partie.nouvelle(4, 250, list("abcd"), ["red", "blue", "green", "pink"])
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "save.json"
            sauvegarder_partie(partie, chemin)
            self.assertEqual(charger_partie(chemin), partie)

    def test_fichier_absent_ou_corrompu(self):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "save.json"
            self.assertIsNone(charger_partie(chemin))
            chemin.write_text("pas du json", encoding="utf-8")
            self.assertIsNone(charger_partie(chemin))
            chemin.write_text('{"nombre_joueurs": 2}', encoding="utf-8")
            self.assertIsNone(charger_partie(chemin))

if __name__ == "__main__":
    unittest.main()
