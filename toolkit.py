"""Point d'entrée en ligne de commande du TerangaNet Ops Toolkit."""

import argparse

from teranganet.inventaire import charger_inventaire
from teranganet.meteo import meteo_actuelle


def cmd_inventaire(args):
    """Affiche la liste des équipements de l'inventaire."""
    sites, equipements = charger_inventaire()
    print(f"=== Inventaire TerangaNet — {len(equipements)} équipements, "
          f"{len(sites)} sites ===")
    for eq in equipements:
        print(f"{eq.site} {eq.nom} {eq.type_equipement} {eq.ip} {eq.statut}")


def cmd_meteo(args):
    """Affiche la météo actuelle d'un site."""
    sites, _ = charger_inventaire()
    if args.code not in sites:
        print(f"Erreur : aucun site nommé '{args.code}' dans l'inventaire.")
        return
    site = sites[args.code]
    m = meteo_actuelle(site.latitude, site.longitude)
    print(f"Météo actuelle — {site.nom} ({site.latitude}, {site.longitude})")
    print(f"  Température : {m['temperature']} °C")
    print(f"  Vent : {m['vent']} km/h")
    print(f"  (source : API Open-Meteo, code HTTP {m['code_http']})")
def main():
    """Construit l'analyseur d'arguments et exécute la commande demandée."""
    parser = argparse.ArgumentParser(description="TerangaNet Ops Toolkit")
    sous = parser.add_subparsers(dest="commande", required=True)

    p_inv = sous.add_parser("inventaire", help="Lister les équipements")
    p_inv.set_defaults(fonction=cmd_inventaire)
    p_met = sous.add_parser("meteo", help="Météo actuelle d'un site")
    p_met.add_argument("code", help="Code du site (DKR, THS, STL)")
    p_met.set_defaults(fonction=cmd_meteo)

    args = parser.parse_args()
    args.fonction(args)


if __name__ == "__main__":
    main()