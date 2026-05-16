# LNCrawler Backend

Backend FastAPI pour LNCrawler - Système de téléchargement de webnovels.

## Installation

1. Créez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancez le serveur :
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera disponible à l'adresse : http://localhost:8000

## Documentation API

Une fois le serveur lancé, la documentation Swagger est disponible à :
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

## Endpoints

### Downloads
- `POST /api/downloads` - Démarrer un téléchargement
- `GET /api/downloads` - Liste des téléchargements
- `GET /api/downloads/{id}` - Détails d'un téléchargement
- `POST /api/downloads/{id}/pause` - Pause
- `POST /api/downloads/{id}/resume` - Reprendre
- `DELETE /api/downloads/{id}` - Annuler

### Library
- `GET /api/library` - Bibliothèque locale
- `GET /api/library/{id}` - Détails d'un novel
- `DELETE /api/library/{id}` - Supprimer un novel

### Favorites
- `GET /api/favorites` - Liste des favoris
- `POST /api/favorites/{novel_id}` - Ajouter aux favoris
- `DELETE /api/favorites/{novel_id}` - Supprimer des favoris

### History
- `GET /api/history` - Historique des téléchargements

## Sites supportés

- NovelFrance.fr

## Structure du projet

```
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── download.py
│   │       ├── library.py
│   │       ├── favorites.py
│   │       └── history.py
│   ├── core/
│   │   ├── downloader.py
│   │   ├── epub_builder.py
│   │   └── exceptions.py
│   ├── database/
│   │   ├── db.py
│   │   └── models.py
│   ├── helpers/
│   │   ├── requests.py
│   │   ├── cleaner.py
│   │   └── epub.py
│   ├── sites/
│   │   ├── base.py
│   │   ├── registry.py
│   │   └── novelfrance.py
│   ├── schemas/
│   │   ├── novel.py
│   │   └── download.py
│   ├── config.py
│   └── main.py
├── downloads/
├── covers/
└── requirements.txt
```

## Configuration

La configuration se fait via le fichier `app/config.py` ou les variables d'environnement.

- `DOWNLOAD_DIR` : Dossier de téléchargement des EPUB
- `COVER_DIR` : Dossier de stockage des couvertures
- `DATABASE_URL` : URL de la base de données SQLite
- `MAX_CONCURRENT_DOWNLOADS` : Nombre max de téléchargements simultanés
- `CHAPTER_DELAY` : Délai entre les chapitres (secondes)