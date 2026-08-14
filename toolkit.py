"""Point d'entrée en ligne de commande du TerangaNet Ops Toolkit."""

import argparse
from datetime import datetime

from teranganet.inventaire import charger_inventaire
from teranganet.meteo import meteo_actuelle
from teranganet.rapport import charger_seuils, evaluer_alertes, ecrire_rapport


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
            print(f"  Site : {eq.site} · lat {eq.site.latitude}, "
                  f"lon {eq.site.longitude}")
            print(f"  IP : {eq.ip}")
            print(f"  Statut : {eq.statut}")
            print(f"  Exposé : {'oui' if eq.exterieur else 'non'}")
            return
    print(f"Erreur : aucun équipement nommé '{args.nom}' dans l'inventaire.")


def cmd_audit(args):
    """Croise l'inventaire et la météo pour lever des alertes."""
    sites, equipements = charger_inventaire()
    seuils = charger_seuils()
    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"=== Audit TerangaNet — {horodatage} ===")

    total_alertes = 0
    for code, site in sites.items():
        exterieurs = [e for e in equipements
                      if e.site.code == code and e.exterieur]
        m = meteo_actuelle(site.latitude, site.longitude)
        alertes = evaluer_alertes(m["vent"], m["temperature"],
                                  len(exterieurs) > 0, seuils)
        total_alertes += len(alertes)
        etat = " ".join(f"[{a}]" for a in alertes) if alertes else "OK"
        print(f"{site}  vent {m['vent']} km/h  "
              f"temp {m['temperature']} °C  {etat}")

    nb_ext = len([e for e in equipements if e.exterieur])
    print(f"\nBilan : {total_alertes} alertes sur {len(sites)} sites. "
          f"Équipements extérieurs exposés au vent : {nb_ext}.")


def cmd_rapport(args):
    """Exporte l'audit dans un fichier JSON horodaté."""
    sites, equipements = charger_inventaire()
    seuils = charger_seuils()
    resultats = []
    for code, site in sites.items():
        exterieurs = [e for e in equipements
                      if e.site.code == code and e.exterieur]
        m = meteo_actuelle(site.latitude, site.longitude)
        alertes = evaluer_alertes(m["vent"], m["temperature"],
                                  len(exterieurs) > 0, seuils)
        resultats.append({
            "site": code,
            "nom": site.nom,
            "vent_kmh": m["vent"],
            "temperature_c": m["temperature"],
            "alertes": alertes,
        })
    donnees = {
        "horodatage": datetime.now().isoformat(timespec="seconds"),
        "seuils": seuils,
        "sites": resultats,
    }
    chemin = ecrire_rapport(donnees)
    print(f"Rapport écrit : {chemin}")


def main():
    """Construit l'analyseur d'arguments et exécute la commande demandée."""
    parser = argparse.ArgumentParser(description="TerangaNet Ops Toolkit")
    sous = parser.add_subparsers(dest="commande", required=True)

    p_inv = sous.add_parser("inventaire", help="Lister les équipements")
    p_inv.set_defaults(fonction=cmd_inventaire)

    p_show = sous.add_parser("show", help="Détailler un équipement")
    p_show.add_argument("nom", help="Nom de l'équipement")
    p_show.set_defaults(fonction=cmd_show)

    p_met = sous.add_parser("meteo", help="Météo actuelle d'un site")
    p_met.add_argument("code", help="Code du site (DKR, THS, STL)")
    p_met.set_defaults(fonction=cmd_meteo)

    p_aud = sous.add_parser("audit", help="Croiser inventaire et météo")
    p_aud.set_defaults(fonction=cmd_audit)

    p_rap = sous.add_parser("rapport", help="Exporter l'audit en JSON")
    p_rap.set_defaults(fonction=cmd_rapport)

    args = parser.parse_args()
    try:
        args.fonction(args)
    except ValueError as err:
        print(f"Erreur : {err}")


if __name__ == "__main__":
    main()