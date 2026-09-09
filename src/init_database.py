"""
init_database.py
-----------------
Initialise la base de données de la bibliothèque numérique :
- vide les collections existantes (pour permettre une exécution répétée) ;
- insère des auteurs, des utilisateurs, des livres et des emprunts
  cohérents entre eux ;
- crée les index et applique les validateurs de schéma, pour que la
  base soit entièrement prête après ce seul script (nécessaire pour
  que le workflow GitHub Actions, qui n'exécute jamais main.py,
  trouve les index déjà en place lors des tests).
"""

from datetime import datetime, timedelta, UTC

import config
from database import get_database, close_connection
from indexes import create_all_indexes
from validation import apply_all_validators


def reset_collections(db) -> None:
    """Supprime le contenu des collections pour repartir d'une base vide."""
    db[config.COLLECTION_BOOKS].delete_many({})
    db[config.COLLECTION_AUTHORS].delete_many({})
    db[config.COLLECTION_LOANS].delete_many({})
    db[config.COLLECTION_USERS].delete_many({})
    print("Collections vidées.")


def insert_authors(db) -> dict:
    """Insère les auteurs et retourne {nom: _id} pour les référencer ensuite."""
    authors = [
        {"nom": "George Orwell", "bio": "Écrivain britannique, œuvres dystopiques.",
         "nationalite": "Britannique"},
        {"nom": "Robert C. Martin", "bio": "Ingénieur logiciel américain, bonnes pratiques.",
         "nationalite": "Américaine"},
        {"nom": "Isaac Asimov", "bio": "Écrivain et biochimiste, science-fiction.",
         "nationalite": "Américaine"},
        {"nom": "Yuval Noah Harari", "bio": "Historien et essayiste israélien.",
         "nationalite": "Israélienne"},
    ]
    result = db[config.COLLECTION_AUTHORS].insert_many(authors)
    ids_by_name = {a["nom"]: _id for a, _id in zip(authors, result.inserted_ids)}
    print(f"{len(result.inserted_ids)} auteurs insérés.")
    return ids_by_name


def insert_users(db) -> dict:
    """Insère les utilisateurs et retourne {nom: _id}."""
    users = [
        {"nom": "Amadou Diallo", "email": "amadou.diallo@example.com"},
        {"nom": "Fatoumata Camara", "email": "fatoumata.camara@example.com"},
        {"nom": "Mamadou Bah", "email": "mamadou.bah@example.com"},
    ]
    result = db[config.COLLECTION_USERS].insert_many(users)
    ids_by_name = {u["nom"]: _id for u, _id in zip(users, result.inserted_ids)}
    print(f"{len(result.inserted_ids)} utilisateurs insérés.")
    return ids_by_name


def build_author_ref(author_id, nom: str) -> dict:
    """Sous-document 'référence étendue' embarqué dans un livre."""
    return {"auteur_id": author_id, "nom": nom}


def insert_books(db, author_ids: dict) -> dict:
    """Insère 5 livres à structures volontairement différentes."""
    books = [
        {
            "titre": "1984",
            "auteurs": [build_author_ref(author_ids["George Orwell"], "George Orwell")],
            "date_publication": datetime(1949, 6, 8),
            "tags": ["Dystopie", "Science-fiction", "Politique"],
            "resume": "Winston Smith tente de préserver sa liberté de pensée sous un régime totalitaire.",
            "disponible": True,
        },
        {
            "titre": "Clean Code",
            "auteurs": [build_author_ref(author_ids["Robert C. Martin"], "Robert C. Martin")],
            "date_publication": datetime(2008, 8, 1),
            "tags": ["Génie logiciel"],
            "resume": "Un guide de référence sur l'écriture d'un code lisible et maintenable.",
            "disponible": False,
        },
        {
            "titre": "Fondation",
            "auteurs": [build_author_ref(author_ids["Isaac Asimov"], "Isaac Asimov")],
            "date_publication": datetime(1951, 5, 1),
            "tags": ["Science-fiction", "Space opera"],
            "resume": "L'effondrement d'un empire galactique donne naissance à un projet scientifique.",
            "disponible": True,
        },
        {
            "titre": "Sapiens",
            "auteurs": [build_author_ref(author_ids["Yuval Noah Harari"], "Yuval Noah Harari")],
            "date_publication": datetime(2011, 1, 1),
            "tags": [],
            "resume": "Une traversée de l'histoire humaine, de l'Homo sapiens à nos jours.",
            "disponible": True,
        },
        {
            "titre": "Le Guide du développeur pragmatique",
            "auteurs": [
                build_author_ref(author_ids["Robert C. Martin"], "Robert C. Martin"),
                build_author_ref(author_ids["George Orwell"], "George Orwell"),
            ],
            "date_publication": datetime(2019, 3, 15),
            "tags": ["Génie logiciel", "Méthodologie"],
            "resume": "Compilation de bonnes pratiques transversales pour le développement logiciel.",
            "disponible": False,
        },
    ]
    result = db[config.COLLECTION_BOOKS].insert_many(books)
    ids_by_title = {b["titre"]: _id for b, _id in zip(books, result.inserted_ids)}
    print(f"{len(result.inserted_ids)} livres insérés.")
    return ids_by_title


def insert_loans(db, book_ids: dict, user_ids: dict) -> None:
    """Insère des emprunts référençant livres et utilisateurs par ObjectId."""
    now = datetime.now(UTC)
    loans = [
        {"utilisateur_id": user_ids["Amadou Diallo"], "livre_id": book_ids["1984"],
         "date_emprunt": now - timedelta(days=10), "date_retour_prevue": now,
         "date_retour": None, "statut": "en_cours"},
        {"utilisateur_id": user_ids["Fatoumata Camara"], "livre_id": book_ids["Clean Code"],
         "date_emprunt": now - timedelta(days=20), "date_retour_prevue": now - timedelta(days=6),
         "date_retour": None, "statut": "en_cours"},
        {"utilisateur_id": user_ids["Mamadou Bah"], "livre_id": book_ids["Fondation"],
         "date_emprunt": now - timedelta(days=30), "date_retour_prevue": now - timedelta(days=16),
         "date_retour": now - timedelta(days=15), "statut": "rendu"},
        {"utilisateur_id": user_ids["Amadou Diallo"], "livre_id": book_ids["Le Guide du développeur pragmatique"],
         "date_emprunt": now - timedelta(days=5), "date_retour_prevue": now + timedelta(days=9),
         "date_retour": None, "statut": "en_cours"},
    ]
    result = db[config.COLLECTION_LOANS].insert_many(loans)
    print(f"{len(result.inserted_ids)} emprunts insérés.")


def main() -> None:
    db = get_database()
    print(f"Connexion établie à la base '{db.name}'.")

    reset_collections(db)
    author_ids = insert_authors(db)
    user_ids = insert_users(db)
    book_ids = insert_books(db, author_ids)
    insert_loans(db, book_ids, user_ids)
    create_all_indexes(db)
    apply_all_validators(db)

    print("Initialisation de la base terminée avec succès.")
    close_connection()


if __name__ == "__main__":
    main()