# LNCrawler Mobile Ecosystem

## Vision du projet

Créer une plateforme moderne de téléchargement et de gestion de webnovels capable de supporter plusieurs sites grâce à une architecture modulaire extensible.

Le système doit être :

* scalable
* maintenable
* modulaire
* moderne
* orienté UX
* performant
* facilement extensible

L’objectif n’est pas seulement de télécharger des EPUBs, mais de construire un véritable écosystème de lecture et de gestion de webnovels.

---

# Stack Technique

## Frontend Mobile

### Flutter

Pourquoi Flutter :

* UI ultra moderne
* animations fluides
* performances natives
* Android + iOS
* excellente gestion du responsive
* très bon système de thèmes
* énorme communauté
* parfait pour design premium

---

## Backend

### Python + FastAPI

Pourquoi :

* rapidité de développement
* parfait pour scraping
* architecture propre
* async natif
* excellente documentation Swagger
* scalable
* séparation logique/interface

---

## Database

### SQLite

Pourquoi :

* léger
* local
* parfait pour mobile desktop/backend local
* migration facile vers PostgreSQL plus tard

---

# Architecture globale

```text
Mobile App (Flutter)
        ↓
REST API (FastAPI)
        ↓
Download Manager
        ↓
Site Adapter System
        ↓
Novel Sites
```

---

# Backend Architecture

```text
backend/
│
├── app/
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── download.py
│   │   │   ├── favorites.py
│   │   │   ├── history.py
│   │   │   └── library.py
│   │   │
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   ├── downloader.py
│   │   ├── epub_builder.py
│   │   ├── manager.py
│   │   ├── exceptions.py
│   │   └── config.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   ├── models.py
│   │   └── migrations/
│   │
│   ├── helpers/
│   │   ├── cleaner.py
│   │   ├── requests.py
│   │   ├── parser.py
│   │   ├── filename.py
│   │   └── logger.py
│   │
│   ├── sites/
│   │   ├── base.py
│   │   ├── registry.py
│   │   ├── novelfrance.py
│   │   ├── royalroad.py
│   │   ├── scribblehub.py
│   │   └── ...
│   │
│   ├── schemas/
│   │   ├── novel.py
│   │   ├── chapter.py
│   │   └── download.py
│   │
│   └── main.py
│
├── downloads/
├── covers/
├── requirements.txt
└── README.md
```

---

# Architecture Flutter

```text
flutter_app/
│
├── lib/
│   │
│   ├── core/
│   │   ├── constants/
│   │   ├── themes/
│   │   ├── routes/
│   │   └── utils/
│   │
│   ├── services/
│   │   ├── api_service.dart
│   │   ├── download_service.dart
│   │   └── storage_service.dart
│   │
│   ├── models/
│   │   ├── novel.dart
│   │   ├── chapter.dart
│   │   └── download_task.dart
│   │
│   ├── providers/
│   │   ├── download_provider.dart
│   │   ├── history_provider.dart
│   │   ├── favorites_provider.dart
│   │   └── library_provider.dart
│   │
│   ├── screens/
│   │   ├── home/
│   │   ├── downloads/
│   │   ├── library/
│   │   ├── favorites/
│   │   ├── settings/
│   │   └── reader/
│   │
│   ├── widgets/
│   │   ├── cards/
│   │   ├── buttons/
│   │   ├── dialogs/
│   │   ├── animations/
│   │   └── navigation/
│   │
│   └── main.dart
│
└── pubspec.yaml
```

---

# Système de Sites Extensibles

Le cœur du projet.

Chaque site doit être un module indépendant.

---

## Base abstraite

```python
class BaseSite:

    def can_handle(self, url):
        pass

    def fetch_novel_info(self):
        pass

    def fetch_chapters(self):
        pass

    def fetch_chapter_content(self, chapter):
        pass
```

---

## Exemple

```python
class NovelFrance(BaseSite):
```

---

# Registry Pattern

Permet de détecter automatiquement le bon site.

```python
site = registry.get_site(url)
```

---

# Fonctionnalités MVP

## Téléchargement EPUB

* téléchargement complet
* téléchargement partiel
* reprise possible
* ordre des chapitres garanti
* nettoyage HTML
* couverture automatique
* CSS premium

---

## Historique

* date téléchargement
* titre
* cover
* statut
* taille

---

## Favoris

* ajout suppression
* cover
* tags
* recherche

---

## Téléchargements parallèles

* queue manager
* max workers configurable
* pause/reprise
* annulation

---

## Bibliothèque locale

* affichage EPUB
* tri
* recherche
* lecture

---

# Design System

## Style général

Direction artistique :

* moderne
* minimaliste
* premium
* sombre
* élégant
* lisible
* inspiré de :

  * Tachiyomi
  * Mihon
  * MoonReader
  * Notion
  * Material 3
  * Spotify
  * Kindle moderne

---

# Palette de couleurs

## Theme principal

### Background

```text
#0F1115
```

### Surface

```text
#1A1D24
```

### Primary

```text
#5B8CFF
```

### Accent

```text
#8B5CF6
```

### Success

```text
#22C55E
```

### Error

```text
#EF4444
```

### Text Primary

```text
#F5F7FA
```

### Text Secondary

```text
#A1A8B3
```

---

# Typographie

## Police

### Inter

Pourquoi :

* moderne
* lisible
* professionnelle
* excellente sur mobile

---

# Règles UI/UX

## Navigation

Bottom Navigation moderne :

* Home
* Downloads
* Library
* Favorites
* Settings

---

## Animations

* fluides
* rapides
* non excessives
* micro-interactions
* transitions Material 3

---

## Cartes

* coins arrondis
* ombres douces
* spacing généreux
* hiérarchie visuelle claire

---

# Écran Home

## Contenu

* champ URL
* bouton analyse
* historique récent
* téléchargements récents
* recommandations

---

# Écran Downloads

## Chaque carte

* cover
* titre
* progression
* vitesse
* taille
* ETA
* pause/reprendre

---

# Écran Library

* grid responsive
* covers haute qualité
* tri dynamique
* recherche instantanée

---

# Reader EPUB

Fonctionnalités :

* mode sombre
* tailles police
* thèmes lecture
* pagination fluide
* historique lecture
* bookmarks

---

# Architecture Téléchargement

## Download Manager

Responsabilités :

* queue
* workers
* reprise
* retry
* cache
* gestion erreurs
* événements temps réel

---

# API Endpoints

## Download

```http
POST /download
```

---

## Downloads

```http
GET /downloads
```

---

## Favorites

```http
GET /favorites
POST /favorites
DELETE /favorites/{id}
```

---

## Library

```http
GET /library
```

---

# Sécurité

* validation URL
* timeout requests
* retry policy
* user-agent rotation possible
* nettoyage HTML
* sandboxing futur

---

# Performance

* async requests
* téléchargement parallèle
* cache covers
* lazy loading
* pagination UI
* compression images

---

# Évolutions futures

## Synchronisation Cloud

* Firebase
* Supabase
* comptes utilisateurs

---

## Multi plateformes

* desktop
* web
* extension navigateur

---

# Priorité de Développement

## Phase 1

* architecture backend
* BaseSite
* NovelFrance
* API FastAPI

---

## Phase 2

* Flutter architecture
* navigation
* design system
* providers

---

## Phase 3

* downloads
* historique
* favoris

---

## Phase 4

* lecteur EPUB
* animations
* optimisation

---

# Règles de Code

* clean architecture
* SOLID
* séparation responsabilités
* services indépendants
* composants réutilisables
* zéro logique métier dans UI

---

# Objectif final

Construire une application moderne capable de devenir :

* un agrégateur de webnovels
* une bibliothèque intelligente
* un lecteur EPUB premium
* un système extensible multi-sites

Le projet doit être pensé comme un produit logiciel durable et évolutif.
