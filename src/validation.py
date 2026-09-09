"""
validation.py
--------------
Amélioration : MongoDB n'impose pas de schéma strict au niveau du
moteur (c'est un choix délibéré du modèle documentaire), mais permet
d'appliquer des règles de validation optionnelles via $jsonSchema,
exécutées côté serveur à chaque insertion/mise à jour.

Cela comble une partie du risque signalé dans le rapport ("absence de
contraintes d'intégrité natives, contrairement aux clés étrangères
SQL") : on ne peut pas garantir qu'un auteur_id référencé existe
réellement (MongoDB ne fait pas de contrôle de clé étrangère), mais on
peut au moins garantir que chaque document a la forme attendue.
"""

import config

BOOKS_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["titre", "disponible"],
        "properties": {
            "titre": {"bsonType": "string", "description": "obligatoire, chaîne de caractères"},
            "disponible": {"bsonType": "bool", "description": "obligatoire, booléen"},
            "tags": {"bsonType": "array", "items": {"bsonType": "string"}},
            "auteurs": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["auteur_id"],
                    "properties": {"auteur_id": {"bsonType": "objectId"}},
                },
            },
        },
    }
}

LOANS_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["utilisateur_id", "livre_id", "date_emprunt"],
        "properties": {
            "utilisateur_id": {"bsonType": "objectId"},
            "livre_id": {"bsonType": "objectId"},
            "date_emprunt": {"bsonType": "date"},
            "date_retour": {"bsonType": ["date", "null"]},
        },
    }
}


def _apply_validator(db, collection_name: str, schema: dict) -> None:
    """
    Applique (ou met à jour) un validateur $jsonSchema sur une collection
    existante via collMod. Si la collection n'existe pas encore, on la
    crée directement avec le validateur.
    """
    existing = db.list_collection_names(filter={"name": collection_name})
    if existing:
        db.command("collMod", collection_name, validator=schema, validationLevel="moderate")
    else:
        db.create_collection(collection_name, validator=schema, validationLevel="moderate")
    print(f"Validation $jsonSchema appliquée sur '{collection_name}'.")


def apply_all_validators(db) -> None:
    """Applique les validateurs définis pour 'books' et 'loans'."""
    _apply_validator(db, config.COLLECTION_BOOKS, BOOKS_SCHEMA)
    _apply_validator(db, config.COLLECTION_LOANS, LOANS_SCHEMA)