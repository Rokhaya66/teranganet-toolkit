"""Chargement de l'inventaire TerangaNet depuis un fichier YAML."""

from pathlib import Path
import yaml

CHEMIN_DEFAUT = Path(__file__).resolve().parent.parent / "data" / "equipements.yaml"
class Site:
    """Représente un point de présence (POP) de TerangaNet."""

    def __init__(self, code, nom, latitude, longitude):
        self.code = code
        self.nom = nom
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"{self.code} ({self.nom})"


class Equipement:
    """Représente un équipement réseau installé sur un site."""

    def __init__(self, nom, type_equipement, ip, statut, site, exterieur):
        self.nom = nom
        self.type_equipement = type_equipement
        self.ip = ip
        self.statut = statut
        self.site = site
        self.exterieur = exterieur 
def charger_inventaire(chemin=CHEMIN_DEFAUT):
    """Charge le YAML et renvoie (sites, equipements)."""
    with open(chemin, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    sites = {}
    for s in data["sites"]:
        sites[s["code"]] = Site(s["code"], s["nom"], s["latitude"], s["longitude"])

    equipements = []
    for e in data["equipements"]:
        equipements.append(Equipement(e["nom"], e["type"], e["ip"], e["statut"], sites[e["site"]], e["exterieur"]))

    return sites, equipements