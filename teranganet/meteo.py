"""Client de l'API REST publique Open-Meteo."""

import requests

URL_BASE = "https://api.open-meteo.com/v1/forecast"
TIMEOUT = 10


def meteo_actuelle(lat, lon):
    """Interroge Open-Meteo et renvoie temperature, vent et code HTTP."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m",
    }
    try:
        r = requests.get(URL_BASE, params=params, timeout=TIMEOUT)
    except requests.exceptions.Timeout:
        raise ValueError("Délai dépassé en contactant l'API météo.")
    except requests.exceptions.ConnectionError:
        raise ValueError("Impossible de joindre l'API météo (pas de réseau ?).")

    if r.status_code != 200:
        if 400 <= r.status_code < 500:
            raise ValueError(
                f"Erreur {r.status_code} : vérifiez la requête envoyée à l'API."
            )
        raise ValueError(
            f"Erreur {r.status_code} : le serveur a un problème, réessayez."
        )
    
    data = r.json()
    return {
        "temperature": data["current"]["temperature_2m"],
        "vent": data["current"]["wind_speed_10m"],
        "code_http": r.status_code,
    }