"""
database.py
-----------
Gère la connexion à MongoDB et expose un point d'accès unique à la
base de données pour le reste de l'application.
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError

import config

_client: MongoClient = None
_database = None


def get_database():
    """
    Retourne l'objet Database MongoDB, en créant la connexion si besoin.
    """
    global _client, _database

    if _database is not None:
        return _database

    config.validate_config()

    try:
        _client = MongoClient(config.MONGODB_URI, serverSelectionTimeoutMS=5000)
        _client.admin.command("ping")
    except (ConnectionFailure, ConfigurationError) as error:
        raise ConnectionFailure(
            f"Impossible de se connecter à MongoDB : {error}"
        ) from error

    _database = _client[config.DATABASE_NAME]
    return _database


def close_connection() -> None:
    """Ferme proprement la connexion au client MongoDB."""
    global _client, _database
    if _client is not None:
        _client.close()
        _client = None
        _database = None