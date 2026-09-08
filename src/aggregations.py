"""
aggregations.py
----------------
Pipelines d'agrégation demandés par le devoir :

1. Nombre de livres par auteur.
2. Livres actuellement empruntés et non rendus.
"""

from datetime import datetime, UTC

import config


def books_count_by_author(db) -> list:
    """
    Pipeline :
      1. $unwind sur 'auteurs' : un livre à plusieurs auteurs est éclaté
         en plusieurs documents temporaires, un par auteur.
      2. $group : compte le nombre de livres par auteur_id.
      3. $lookup : récupère le nom complet de l'auteur.
      4. $unwind : aplatit le tableau retourné par $lookup.
      5. $project : ne garde que les champs utiles à l'affichage.
      6. $sort : trie par nombre de livres décroissant.
    """
    pipeline = [
        {"$unwind": "$auteurs"},
        {"$group": {"_id": "$auteurs.auteur_id", "nombre_livres": {"$sum": 1}}},
        {"$lookup": {
            "from": config.COLLECTION_AUTHORS,
            "localField": "_id",
            "foreignField": "_id",
            "as": "auteur_info",
        }},
        {"$unwind": "$auteur_info"},
        {"$project": {"_id": 0, "auteur": "$auteur_info.nom", "nombre_livres": 1}},
        {"$sort": {"nombre_livres": -1}},
    ]
    return list(db[config.COLLECTION_BOOKS].aggregate(pipeline))


def books_currently_borrowed(db) -> list:
    """
    Pipeline :
      1. $match sur date_retour = null : emprunts non clôturés.
      2. $lookup vers 'books' : récupère le titre du livre.
      3. $lookup vers 'users' : récupère le nom de l'emprunteur.
      4. $unwind sur les deux jointures.
      5. $project : construit un document lisible.
      6. $sort : les plus anciens d'abord.
    """
    pipeline = [
        {"$match": {"date_retour": None}},
        {"$lookup": {
            "from": config.COLLECTION_BOOKS,
            "localField": "livre_id",
            "foreignField": "_id",
            "as": "livre",
        }},
        {"$unwind": "$livre"},
        {"$lookup": {
            "from": config.COLLECTION_USERS,
            "localField": "utilisateur_id",
            "foreignField": "_id",
            "as": "utilisateur",
        }},
        {"$unwind": "$utilisateur"},
        {"$project": {
            "_id": 0,
            "titre_livre": "$livre.titre",
            "emprunteur": "$utilisateur.nom",
            "date_emprunt": 1,
            "date_retour_prevue": 1,
        }},
        {"$sort": {"date_emprunt": 1}},
    ]
    results = list(db[config.COLLECTION_LOANS].aggregate(pipeline))

    today = datetime.now(UTC)
    for loan in results:
        date_prevue = loan["date_retour_prevue"]
        if date_prevue.tzinfo is None:
            date_prevue = date_prevue.replace(tzinfo=UTC)
        loan["en_retard"] = date_prevue < today

    return results