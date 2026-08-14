"""Tests unitaires du chargement de l'inventaire."""

import unittest

from teranganet.inventaire import charger_inventaire


class TestChargementInventaire(unittest.TestCase):
    """Vérifie que le fichier YAML est correctement transformé en objets."""

    def test_nombre_equipements(self):
        """L'inventaire contient bien 6 équipements."""
        sites, equipements = charger_inventaire()
        self.assertEqual(len(equipements), 6)

    def test_nombre_sites(self):
        """L'inventaire contient bien 3 sites."""
        sites, equipements = charger_inventaire()
        self.assertEqual(len(sites), 3)

    def test_nom_premier_equipement(self):
        """Le premier équipement s'appelle R1-DKR."""
        sites, equipements = charger_inventaire()
        self.assertEqual(equipements[0].nom, "R1-DKR")

    def test_ip_premier_equipement(self):
        """Le premier équipement a la bonne adresse IP."""
        sites, equipements = charger_inventaire()
        self.assertEqual(equipements[0].ip, "10.10.1.1")

    def test_composition_site(self):
        """Un équipement référence un objet Site, pas une chaîne."""
        sites, equipements = charger_inventaire()
        self.assertEqual(equipements[0].site.nom, "Dakar")

    def test_fichier_introuvable(self):
        """Un chemin invalide lève une erreur au lieu de planter."""
        with self.assertRaises(Exception):
            charger_inventaire("data/inexistant.yaml")


if __name__ == "__main__":
    unittest.main()