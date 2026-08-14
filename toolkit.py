"""Point d'entrée en ligne de commande du TerangaNet Ops Toolkit."""

import argparse

from teranganet.inventaire import charger_inventaire


def cmd_inventaire(args):
    """Affiche la liste des équipements de l'inventaire."""
    sites, equipements = charger_inventaire()
    print(f"=== Inventaire TerangaNet — {len(equipements)} équipements, "
          f"{len(sites)} sites ===")
    for eq in equipements:
        print(f"{eq.site} {eq.nom} {eq.type_equipement} {eq.ip} {eq.statut}")
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
    p_show = sous.add_parser("show", help="Détailler un équipement")
    p_show.add_argument("nom", help="Nom de l'équipement")
    p_show.set_defaults(fonction=cmd_show)

    args = parser.parse_args()
    args.fonction(args)


if __name__ == "__main__":
    main()