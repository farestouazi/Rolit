import unittest

from rolit import regles

def plateau_vide():
    return regles.creer_plateau_vide()

class TestCoupsValides(unittest.TestCase):
    def test_case_isolee_invalide(self):
        plateau = plateau_vide()
        plateau[3][3] = "red"
        self.assertFalse(regles.coup_valide(plateau, 0, 0))

    def test_case_voisine_valide(self):
        plateau = plateau_vide()
        plateau[3][3] = "red"
        self.assertTrue(regles.coup_valide(plateau, 2, 2))
        self.assertTrue(regles.coup_valide(plateau, 3, 4))

    def test_case_occupee_invalide(self):
        plateau = plateau_vide()
        plateau[3][3] = "red"
        self.assertFalse(regles.coup_valide(plateau, 3, 3))

    def test_hors_plateau_invalide(self):
        self.assertFalse(regles.coup_valide(plateau_vide(), -1, 0))
        self.assertFalse(regles.coup_valide(plateau_vide(), 0, 8))

    def test_jouer_coup_invalide_leve_une_erreur(self):
        with self.assertRaises(ValueError):
            regles.jouer_coup(plateau_vide(), 0, 0, "red")

class TestCaptures(unittest.TestCase):
    def test_capture_horizontale(self):
        plateau = plateau_vide()
        plateau[3][3], plateau[3][4] = "red", "blue"
        modifiees = regles.jouer_coup(plateau, 3, 5, "red")
        self.assertEqual(plateau[3][4], "red")
        self.assertEqual(modifiees[0], (3, 5))
        self.assertIn((3, 4), modifiees)

    def test_capture_diagonale_et_boule_neutre(self):
        plateau = plateau_vide()
        plateau[4][4], plateau[3][3] = "red", "non"
        regles.jouer_coup(plateau, 2, 2, "red")
        self.assertEqual(plateau[3][3], "red")

    def test_pas_de_capture_sans_boule_de_fermeture(self):
        plateau = plateau_vide()
        plateau[3][3] = "blue"
        regles.jouer_coup(plateau, 3, 4, "red")
        self.assertEqual(plateau[3][3], "blue")

    def test_pas_de_capture_a_travers_une_case_vide(self):
        plateau = plateau_vide()
        plateau[3][3], plateau[3][5] = "blue", "red"
        regles.jouer_coup(plateau, 3, 4, "red")
        self.assertEqual(plateau[3][3], "blue")

    def test_pas_de_capture_en_rebouclant_sur_le_bord(self):
        # Régression : l'ancienne version lisait l'indice -1 (dernière colonne).
        plateau = plateau_vide()
        plateau[3][0] = "blue"
        plateau[2][7] = "red"
        regles.jouer_coup(plateau, 4, 1, "red")
        self.assertEqual(plateau[3][0], "blue")

    def test_captures_multiples_dans_plusieurs_directions(self):
        plateau = plateau_vide()
        plateau[3][4], plateau[3][5] = "blue", "red"
        plateau[4][3], plateau[5][3] = "blue", "red"
        regles.jouer_coup(plateau, 3, 3, "red")
        self.assertEqual(plateau[3][4], "red")
        self.assertEqual(plateau[4][3], "red")

class TestPlateauEtScores(unittest.TestCase):
    couleurs = ["red", "blue", "green", "non"]

    def test_plateau_initial_quatre_joueurs(self):
        plateau = regles.plateau_initial(4, self.couleurs)
        self.assertEqual(
            (plateau[3][3], plateau[3][4], plateau[4][4], plateau[4][3]),
            ("red", "blue", "green", "non"),
        )

    def test_plateau_initial_deux_joueurs_diagonales_neutres(self):
        couleurs = ["red", "blue", "non", "non"]
        plateau = regles.plateau_initial(2, couleurs)
        self.assertEqual((plateau[3][3], plateau[4][4]), ("red", "blue"))
        self.assertEqual((plateau[3][4], plateau[4][3]), ("non", "non"))

    def test_scores_ignorent_les_boules_neutres(self):
        plateau = regles.plateau_initial(3, self.couleurs)
        self.assertEqual(regles.calculer_scores(plateau, self.couleurs, 3), [1, 1, 1])

    def test_plateau_plein(self):
        plateau = plateau_vide()
        self.assertFalse(regles.plateau_plein(plateau))
        plateau = [["red"] * 8 for _ in range(8)]
        self.assertTrue(regles.plateau_plein(plateau))

    def test_coup_aleatoire_toujours_valide(self):
        plateau = regles.plateau_initial(2, ["red", "blue", "non", "non"])
        for _ in range(50):
            ligne, colonne = regles.coup_aleatoire(plateau)
            self.assertTrue(regles.coup_valide(plateau, ligne, colonne))

    def test_coup_aleatoire_sans_coup_possible(self):
        self.assertIsNone(regles.coup_aleatoire([["red"] * 8 for _ in range(8)]))

if __name__ == "__main__":
    unittest.main()
