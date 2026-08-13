class Site:
    def __init__(self, code, nom, latitude, longitude):
        self.code = code
        self.nom = nom
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"{self.code} ({self.nom})"


class Equipement:
    def __init__(self, nom, type_equipement, ip, statut, site, exterieur):
        self.nom = nom
        self.type_equipement = type_equipement
        self.ip = ip
        self.statut = statut
        self.site = site
        self.exterieur = exterieur 
