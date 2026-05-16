# Modification Architecture — Suppression du lecteur intégré

## Nouvelle direction du projet

L’application ne doit PAS intégrer un lecteur EPUB interne.

Le rôle de l’application est désormais :

* récupérer les novels
* générer les EPUBs
* gérer les téléchargements
* organiser la bibliothèque locale
* ouvrir les fichiers avec une application externe

Exemple :

* MoonReader
* ReadEra
* Lithium
* KOReader
* Kindle
* Play Books

L’application devient donc un :

> gestionnaire intelligent de téléchargement de webnovels.

Cela simplifie énormément :

* l’architecture
* les performances
* la maintenance
* le développement UI

Et honnêtement, c’est une décision très pragmatique.

Les lecteurs EPUB sont un gouffre technique :

* pagination
* moteurs de rendu
* thèmes
* bookmarks
* compatibilité EPUB2/3
* mémoire
* bugs Android

Pendant ce temps, MoonReader existe déjà et est extrêmement mature.

L’application doit se concentrer sur :

* UX
* scraping
* téléchargement
* organisation
* performance

---

# Changements Architecture Flutter

## Supprimer

```text id="4ok5b7"
screens/reader/
```

---

## Nouvelle structure

```text id="g1v6fv"
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
│   │   ├── storage_service.dart
│   │   └── opener_service.dart
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
│   │   ├── settings_provider.dart
│   │   └── library_provider.dart
│   │
│   ├── screens/
│   │   ├── home/
│   │   ├── downloads/
│   │   ├── library/
│   │   ├── favorites/
│   │   └── settings/
│   │
│   ├── widgets/
│   │   ├── cards/
│   │   ├── buttons/
│   │   ├── dialogs/
│   │   ├── animations/
│   │   └── navigation/
│   │
│   └── main.dart
```

---

# Fonctionnement Bibliothèque

## L’application stocke :

* chemin fichier
* cover
* titre
* auteur
* taille
* date téléchargement

Mais PAS le contenu EPUB.

---

# Dossier de téléchargement personnalisable

Fonctionnalité obligatoire.

## Settings

L’utilisateur choisit :

```text id="ctgqpt"
/storage/emulated/0/Books/Webnovels
```

ou :

```text id="iwx4cq"
/Downloads/LNCrawler
```

---

# Permissions Android

À prévoir :

* storage access
* manage external storage (si nécessaire)
* SAF (Storage Access Framework)

Important pour Android 13+.

---

# UX Téléchargement

Après téléchargement :

## Boutons

* Ouvrir
* Ouvrir le dossier
* Partager
* Supprimer

---

# Ouverture EPUB

Utiliser :

## Flutter packages

```yaml id="o25vr3"
open_filex
file_picker
path_provider
permission_handler
```

---

# Library Screen

## Objectif

Agir comme une bibliothèque locale moderne.

### Chaque carte :

* cover
* titre
* auteur
* taille
* date
* bouton ouvrir

---

# Nouveau flow utilisateur

## 1

Coller URL.

---

## 2

Téléchargement backend.

---

## 3

EPUB généré.

---

## 4

Sauvegarde dans dossier choisi.

---

## 5

Ouverture avec application externe.

---

# Design UX

Le design doit évoquer :

* gestionnaire média premium
* bibliothèque numérique moderne
* fluidité
* simplicité

Pas une interface “dev tool”.

---

# Inspirations UI

* Mihon
* TachiyomiSY
* Spotify
* Kindle moderne
* Notion
* Material 3

---

# Philosophie produit

L’application ne lit pas.

Elle orchestre.

Comme :

* Plex organise les médias
* Steam organise les jeux
* Mihon organise les mangas

LNCrawler organise les webnovels.
