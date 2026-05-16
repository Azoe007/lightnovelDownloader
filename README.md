# LNCrawler - Webnovel Download System

Une plateforme moderne de téléchargement et de gestion de webnovels avec backend FastAPI et application mobile Flutter.

## 🎯 Vue d'ensemble

LNCrawler permet de :
- Télécharger des webnovels depuis plusieurs sites (NovelFrance, etc.)
- Générer automatiquement des fichiers EPUB
- Gérer une bibliothèque locale
- Suivre les téléchargements en temps réel
- Organiser les favoris

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │
│  Flutter App    │◄───────►│  FastAPI        │
│  (Mobile)       │         │  (Backend)      │
│                 │         │                 │
└─────────────────┘         └────────┬────────┘
                                      │
                                      ▼
                              ┌─────────────────┐
                              │   SQLite DB     │
                              │                 │
                              └─────────────────┘
```

## 📁 Structure du projet

```
ln_scalable/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── api/          # Routes API
│   │   ├── core/         # Logique métier
│   │   ├── database/     # Modèles et config DB
│   │   ├── helpers/      # Utilitaires
│   │   ├── schemas/      # Validation Pydantic
│   │   └── sites/        # Scrapers (NovelFrance, etc.)
│   ├── downloads/        # EPUB générés
│   ├── covers/           # Couvertures téléchargées
│   └── requirements.txt
│
├── flutter_app/          # Application mobile
│   ├── lib/
│   │   ├── core/         # Thème, constantes, routes
│   │   ├── models/       # Modèles de données
│   │   ├── providers/    # State management
│   │   ├── screens/      # Écrans de l'app
│   │   └── services/     # API service
│   └── pubspec.yaml
│
└── docs/                 # Documentation et ancien code
    ├── Instruction1.md
    ├── Instruction2.md
    └── ...
```

## 🚀 Démarrage rapide

### 1. Backend

```bash
cd backend

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API est accessible sur http://localhost:8000
Documentation Swagger : http://localhost:8000/docs

### 2. Flutter App

```bash
cd flutter_app

# Installer les dépendances
flutter pub get

# Configurer l'URL du backend dans lib/core/constants/app_constants.dart
# Remplacer http://localhost:8000 par l'IP de votre machine

# Lancer l'application
flutter run
```

## 📱 Fonctionnalités

### Backend API

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/api/downloads` | POST | Démarrer un téléchargement |
| `/api/downloads` | GET | Liste des téléchargements |
| `/api/downloads/{id}/pause` | POST | Pause |
| `/api/downloads/{id}/resume` | POST | Reprendre |
| `/api/downloads/{id}` | DELETE | Annuler |
| `/api/library` | GET | Bibliothèque locale |
| `/api/favorites` | GET | Favoris |
| `/api/favorites/{id}` | POST | Ajouter aux favoris |
| `/api/favorites/{id}` | DELETE | Supprimer des favoris |
| `/api/history` | GET | Historique |

### Application Mobile

- **Home** : Champ URL + téléchargements en cours
- **Downloads** : Gestion des téléchargements (pause, resume, cancel)
- **Library** : Grille des novels avec recherche
- **Favorites** : Liste des favoris
- **Settings** : Dossier de téléchargement personnalisable

## 🎨 Design System

### Couleurs
- Background: `#0F1115`
- Surface: `#1A1D24`
- Primary: `#5B8CFF`
- Accent: `#8B5CF6`
- Success: `#22C55E`
- Error: `#EF4444`

### Police
- Inter (Google Fonts)

## 🔧 Configuration

### Backend (.env optionnel)

```env
DATABASE_URL=sqlite+aiosqlite:///./lncrawler.db
DOWNLOAD_DIR=./downloads
COVER_DIR=./covers
MAX_CONCURRENT_DOWNLOADS=3
CHAPTER_DELAY=0.5
```

### Flutter

Modifier `lib/core/constants/app_constants.dart` :
```dart
static const String baseUrl = 'http://VOTRE_IP:8000';
```

## 📦 Sites supportés

- ✅ NovelFrance.fr
- 🔲 RoyalRoad (à venir)
- 🔲 ScribbleHub (à venir)

## 🛠️ Technologies

### Backend
- FastAPI
- SQLAlchemy (Async)
- SQLite
- BeautifulSoup4
- EbookLib

### Frontend
- Flutter
- Provider (State Management)
- Dio (HTTP)
- Cached Network Image

## 📝 License

MIT License

---

Développé avec ❤️ pour les amateurs de webnovels