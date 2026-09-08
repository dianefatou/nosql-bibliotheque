"""
test_project.py
----------------
Vérifications simples de bout en bout. Nécessite une base MongoDB
accessible et déjà initialisée via `python src/init_database.py`.

Exécution : python tests/test_project.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import config
from database import get_database, close_connection
import crud
import aggregations
import indexes


def test_connection():
    db = get_database()
    assert db.name == config.DATABASE_NAME
    print("test_connection : OK")


def test_data_inserted():
    db = get_database()
    assert db[config.COLLECTION_BOOKS].count_documents({}) >= 5
    assert db[config.COLLECTION_AUTHORS].count_documents({}) >= 1
    assert db[config.COLLECTION_LOANS].count_documents({}) >= 1
    print("test_data_inserted : OK")


def test_books_are_retrieved():
    db = get_database()
    books = crud.get_all_books(db)
    assert len(books) > 0
    print("test_books_are_retrieved : OK")


def test_update_availability():
    db = get_database()
    book = db[config.COLLECTION_BOOKS].find_one()
    book_id = str(book["_id"])
    original_value = book["disponible"]

    updated = crud.update_book_availability(db, book_id, not original_value)
    assert updated is True

    crud.update_book_availability(db, book_id, original_value)
    print("test_update_availability : OK")


def test_aggregations_return_results():
    db = get_database()
    by_author = aggregations.books_count_by_author(db)
    assert isinstance(by_author, list) and len(by_author) > 0

    borrowed = aggregations.books_currently_borrowed(db)
    assert isinstance(borrowed, list)
    print("test_aggregations_return_results : OK")


def test_indexes_exist():
    db = get_database()
    index_names = [i["name"] for i in indexes.list_indexes(db)]
    assert "idx_titre" in index_names
    assert "idx_disponible_date_publication" in index_names
    print("test_indexes_exist : OK")


if __name__ == "__main__":
    test_connection()
    test_data_inserted()
    test_books_are_retrieved()
    test_update_availability()
    test_aggregations_return_results()
    test_indexes_exist()
    close_connection()
    print("\nTous les tests ont réussi.")