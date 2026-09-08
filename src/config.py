"""
config.py
---------
Charge la configuration de l'application depuis les variables d'environnement.
"""

import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "bibliotheque_nosql")

COLLECTION_BOOKS = "books"
COLLECTION_AUTHORS = "authors"
COLLECTION_LOANS = "loans"
COLLECTION_USERS = "users"


def validate_config() -> None:
    """Vérifie que MONGODB_URI est bien défini avant toute connexion."""
    if not MONGODB_URI:
        raise EnvironmentError(
            "La variable d'environnement MONGODB_URI est manquante. "
            "Copiez .env.example vers .env et renseignez votre URI."
        )