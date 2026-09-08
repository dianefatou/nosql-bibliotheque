"""
crud.py
-------
Implémente les opérations CRUD (Create, Read, Update, Delete) sur la
collection "books" de la bibliothèque numérique.
"""

from bson import ObjectId
from bson.errors import InvalidId

import config


# ---------------------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------------------

def create_book(db, book_data: dict):
    """Insère un nouveau livre. Retourne son ObjectId, ou None en cas d'erreur."""
    try:
        result = db[config.COLLECTION_BOOKS].insert_one(book_data)
        return result.inserted_id
    except Exception as error:
        print(f"Erreur lors de l'insertion du livre : {error}")
        return None


# ---------------------------------------------------------------------------
# READ
# ---------------------------------------------------------------------------

def get_all_books(db) -> list:
    """Retourne la liste de tous les livres."""
    return list(db[config.COLLECTION_BOOKS].find())


def get_book_by_id(db, book_id: str):
    """Retourne un livre à partir de son identifiant (chaîne)."""
    try:
        object_id = ObjectId(book_id)
    except InvalidId:
        print(f"Identifiant invalide : {book_id}")
        return None
    return db[config.COLLECTION_BOOKS].find_one({"_id": object_id})


def get_available_books(db) -> list:
    """Retourne uniquement les livres actuellement disponibles."""
    return list(db[config.COLLECTION_BOOKS].find({"disponible": True}))


def search_books_by_title(db, keyword: str) -> list:
    """Recherche les livres dont le titre contient le mot-clé (insensible à la casse)."""
    regex_query = {"titre": {"$regex": keyword, "$options": "i"}}
    return list(db[config.COLLECTION_BOOKS].find(regex_query))


# ---------------------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------------------

def update_book_availability(db, book_id: str, disponible: bool) -> bool:
    """Met à jour le champ 'disponible' d'un livre. Retourne True si modifié."""
    try:
        object_id = ObjectId(book_id)
    except InvalidId:
        print(f"Identifiant invalide : {book_id}")
        return False

    result = db[config.COLLECTION_BOOKS].update_one(
        {"_id": object_id},
        {"$set": {"disponible": disponible}},
    )
    return result.modified_count > 0


# ---------------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------------

def delete_book(db, book_id: str) -> bool:
    """Supprime un livre à partir de son identifiant. Retourne True si supprimé."""
    try:
        object_id = ObjectId(book_id)
    except InvalidId:
        print(f"Identifiant invalide : {book_id}")
        return False

    result = db[config.COLLECTION_BOOKS].delete_one({"_id": object_id})
    return result.deleted_count > 0