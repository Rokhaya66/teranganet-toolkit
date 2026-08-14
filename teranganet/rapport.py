"""Audit des sites : croisement inventaire / météo et alertes."""

from pathlib import Path
import yaml

CHEMIN_CONFIG = Path(__file__).resolve().parent.parent / "config.yaml"


def charger_seuils(chemin=CHEMIN_CONFIG):
    """Lit les seuils d'alerte dans config.yaml."""
    with open(chemin, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config["seuils"]


def evaluer_alertes(vent, temperature, a_equipement_exterieur, seuils):
    """Renvoie la liste des alertes pour un site donné.

    Fonction pure : aucun appel réseau, aucune lecture de fichier.
    """
    alertes = []
    if a_equipement_exterieur and vent >= seuils["vent_kmh"]:
        alertes.append("ALERTE VENT")
    if temperature >= seuils["temperature_c"]:
        alertes.append("ALERTE TEMPÉRATURE")
    return alertes