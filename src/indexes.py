"""
indexes.py
----------
Crée et vérifie les index de la collection "books".

1. Index simple sur "titre" : accélère la recherche par titre et évite
   un scan complet de la collection (COLLSCAN).

2. Index composé { "disponible": 1, "date_publication": -1 } : pensé
   pour la requête "livres disponibles, triés par date de publication
   décroissante" (page d'accueil typique). MongoDB peut alors filtrer
   ET trier directement via l'index, sans tri en mémoire supplémentaire.
"""

import config


def create_all_indexes(db) -> None:
    """Crée l'ensemble des index nécessaires au projet."""
    books = db[config.COLLECTION_BOOKS]

    title_index_name = books.create_index("titre", name="idx_titre")

    compound_index_name = books.create_index(
        [("disponible", 1), ("date_publication", -1)],
        name="idx_disponible_date_publication",
    )

    print(f"Index créé : {title_index_name}")
    print(f"Index composé créé : {compound_index_name}")


def list_indexes(db) -> list:
    """Retourne la liste des index existants sur 'books'."""
    return list(db[config.COLLECTION_BOOKS].list_indexes())


def explain_title_search(db, keyword: str) -> dict:
    """Vérifie via explain() que l'index 'idx_titre' est bien utilisé."""
    query = {"titre": {"$regex": f"^{keyword}", "$options": "i"}}
    return db[config.COLLECTION_BOOKS].find(query).explain()