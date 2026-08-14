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
def cmd_show(args):
    """Affiche le détail d'un équipement donné."""
    sites, equipements = charger_inventaire()
    for eq in equipements:
        if eq.nom == args.nom:
            print(f"{eq.nom} — {eq.type_equipement}")
            print(f"  Site : {eq.site} · lat {eq.site.latitude}, lon {eq.site.longitude}")
            print(f"  IP : {eq.ip}")
            print(f"  Statut : {eq.statut}")
            print(f"  Exposé : {'oui' if eq.exterieur else 'non'}")
            return
    print(f"Erreur : aucun équipement nommé '{args.nom}' dans l'inventaire.")
def main():
    """Construit l'analyseur d'arguments et exécute la commande demandée."""
    parser = argparse.ArgumentParser(description="TerangaNet Ops Toolkit")
    sous = parser.add_subparsers(dest="commande", required=True)

    p_inv = sous.add_parser("inventaire", help="Lister les équipements")
    p_inv.set_defaults(fonction=cmd_inventaire)
    p_met = sous.add_parser("meteo", help="Météo actuelle d'un site")
    p_met.add_argument("code", help="Code du site (DKR, THS, STL)")
    p_met.set_defaults(fonction=cmd_meteo)
    p_show = sous.add_parser("show", help="Détailler un équipement")
    p_show.add_argument("nom", help="Nom de l'équipement")
    p_show.set_defaults(fonction=cmd_show)

    args = parser.parse_args()
    try:
        args.fonction(args)
    except ValueError as err:
        print(f"Erreur : {err}")


if __name__ == "__main__":
    main()