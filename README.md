# TerangaNet Ops Toolkit

Outil en ligne de commande de surveillance des équipements réseau de TerangaNet,
fournisseur d'accès Internet sénégalais exploitant trois POP (Dakar, Thiès, Saint-Louis).
L'outil croise l'inventaire des équipements avec les conditions météo actuelles afin de
lever des alertes de vent et de température.

Projet d'examen — Parcours DevNet Associate.

## Prérequis

- Python 3.10 ou supérieur
- Git
- Une connexion Internet (API publique Open-Meteo, sans clé)

## Installation

```bash
git clone https://github.com/Rokhaya66/teranganet-toolkit.git
cd teranganet-toolkit
```

Windows :

```bash
python -m venv venv
.\venv\Scripts\activate
```

Linux / macOS :

```bash
python3 -m venv venv
source venv/bin/activate
```

Puis, dans les deux cas :

```bash
pip install -r requirements.txt
```

## Utilisation

Lister les équipements de l'inventaire :

```bash
python toolkit.py inventaire
```

Détailler un équipement :

```bash
python toolkit.py show ANT1-DKR
```

Consulter la météo actuelle d'un site :

```bash
python toolkit.py meteo DKR
```

Les noms inconnus, les fichiers manquants et les coupures réseau affichent un message
d'erreur explicite, jamais un traceback Python.

## Structure du projet

```
teranganet-toolkit/
├── toolkit.py                 # interface CLI uniquement (argparse)
├── config.yaml                # seuils d'alerte
├── data/equipements.yaml      # inventaire des sites et équipements
├── teranganet/
│   ├── inventaire.py          # classes Site et Equipement + chargement YAML
│   ├── meteo.py               # client de l'API Open-Meteo
│   └── rapport.py             # audit et sérialisation JSON
└── tests/                     # tests unitaires
```

La logique applicative vit dans le paquet `teranganet/`, ce qui la rend importable et
testable indépendamment de la ligne de commande.

## Tests

```bash
python -m unittest discover tests
```

## Auteurs et répartition du travail

- **Rokhaya Diallo** — création du dépôt GitHub et de la structure du projet,
  classes `Site` et `Equipement`, logique d'alerte et commande `audit` (F4),
  revues de code et fusion des pull requests

- **Salimata Sow** — chargement YAML de l'inventaire (`charger_inventaire`),
  commandes `inventaire` (F1) et `show` (F2), client de l'API Open-Meteo (F3),
  gestion des erreurs et robustesse (F6)