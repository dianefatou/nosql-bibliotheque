# Bibliothèque Numérique - Projet NoSQL / MongoDB

## Présentation

Ce projet est réalisé dans le cadre du devoir **« Exploration et Implémentation NoSQL »**.
Il consiste à concevoir et implémenter une base de données documentaire
MongoDB pour la gestion d'une bibliothèque numérique : livres, auteurs,
utilisateurs et emprunts.

Le projet démontre, sur un cas concret, les principes de modélisation
NoSQL (embedding vs referencing, conception orientée requêtes), ainsi
que la mise en œuvre de requêtes CRUD, de pipelines d'agrégation et
d'index avec **PyMongo**.

## Technologies utilisées

- **Python 3.14**
- **MongoDB 7** (via **Docker**)
- **PyMongo** pour l'accès à la base depuis Python
- **python-dotenv** pour la gestion de la configuration

## Architecture du projet
nosql-bibliotheque/
│
├── README.md
├── requirements.txt
├── .env.example # modèle de configuration (sans identifiants réels)
├── .gitignore
│
├── src/
│ ├── config.py # lecture de la configuration (.env)
│ ├── database.py # connexion à MongoDB
│ ├── init_database.py # initialisation et peuplement de la base
│ ├── crud.py # opérations Create / Read / Update / Delete
│ ├── aggregations.py # pipelines d'agrégation
│ ├── indexes.py # création et vérification des index
│ └── main.py # démonstration complète des fonctionnalités
│
├── data/
├── docs/
├── rapport/
│ └── rapport_nosql_fatoumata.pdf
│
└── tests/
└── test_project.py # vérifications de bon fonctionnement


## Installation

### 1. Cloner le dépôt

```bash
git clone <url-du-depot>
cd nosql-bibliotheque
```

### 2. Créer un environnement virtuel

**Windows (PowerShell) :**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS :**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Configuration de MongoDB

Ce projet utilise une instance **MongoDB locale via Docker**.

1. Lancer le conteneur MongoDB :
```bash
docker run -d --name mongo-bibliotheque -p 27017:27017 mongo:7
```

2. Créer le fichier `.env` à la racine du projet, à partir du modèle fourni :
```bash
cp .env.example .env
```

Le fichier `.env` contient déjà la configuration par défaut pour Docker :

MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=bibliotheque_nosql


> Le fichier `.env` ne doit **jamais** être versionné sur GitHub — il est
> déjà exclu via `.gitignore`.

### Alternative : MongoDB Atlas

Il est aussi possible d'utiliser un cluster MongoDB Atlas gratuit (M0)
plutôt que Docker : remplacer `MONGODB_URI` dans `.env` par l'URI
`mongodb+srv://...` fournie par Atlas (Database → Connect → Drivers).

## Exécution du projet

Tous les scripts se lancent depuis le dossier `src/` (sauf les tests).

### 1. Initialiser la base de données

```bash
cd src
python init_database.py
```

### 2. Lancer la démonstration complète

```bash
python main.py
```

### 3. Exécuter les tests

Depuis la racine du projet :
```bash
cd ..
python tests\test_project.py
```

## Fonctionnalités implémentées

- Connexion à MongoDB centralisée, avec vérification de la joignabilité
  du serveur (commande `ping`).
- Insertion d'un jeu de données réaliste (4 auteurs, 3 utilisateurs,
  5 livres aux structures variées, 4 emprunts).
- **CRUD** complet sur la collection `books` :
  - création d'un livre ;
  - lecture de tous les livres, par id, par disponibilité, par titre ;
  - mise à jour de la disponibilité ;
  - suppression d'un document de test.
- **Agrégations** :
  - nombre de livres par auteur ;
  - livres actuellement empruntés et non rendus.
- **Index** :
  - index simple sur `titre` ;
  - index composé sur `{ disponible, date_publication }`.
- Suite de tests de vérification du bon fonctionnement de bout en bout.

## Modélisation — Embedding vs Referencing

| Élément | Choix | Justification |
|---|---|---|
| Auteurs dans un livre | Référence étendue `{auteur_id, nom}` | Évite un `$lookup` systématique pour l'affichage d'une liste, tout en gardant l'`_id` pour la fiche complète. |
| Fiche complète auteur | Collection séparée `authors` | Bio et nationalité consultées seulement sur la fiche détaillée. |
| Utilisateur / livre dans un emprunt | Référence pure | Les emprunts sont nombreux et non bornés ; dupliquer le livre ou l'utilisateur à chaque emprunt serait redondant. |
| Tags d'un livre | Embedding | Toujours lus avec le livre, jamais interrogés seuls. |

Le détail complet des justifications se trouve dans `rapport/Devoir Final Groupe3 NoSQL.pdf`.

## Auteurs

 Master Data Science & Intelligence Artificielle (MSTN), ESMT
 Groupe 3: 
 Fatoumata DIANE
Moussa KEITA
ASIEDU Kevin Y.
Andre Fulgence DIAGNE
Omar Abdilahi SAAD
Ibilaounto AGBOTON