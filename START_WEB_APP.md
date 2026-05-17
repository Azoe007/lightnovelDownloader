# 🚀 Démarrer l'Application Web LNCrawler

## Prérequis
- Node.js (v18 ou supérieur)
- npm (inclus avec Node.js)

## Installation et Lancement

### 1. Installer les dépendances
```bash
cd web_app
npm install
```

### 2. Démarrer le serveur de développement
```bash
npm run dev
```

L'application sera accessible à l'adresse : **http://localhost:3000**

### 3. (Optionnel) Build pour production
```bash
npm run build
npm run preview
```

## 📱 Fonctionnalités

- **Accueil** : Télécharger des webnovels en collant une URL
- **Bibliothèque** : Explorer les novels disponibles avec recherche
- **Favoris** : Sauvegarder vos novels préférés
- **Historique** : Consulter l'historique

## 🔧 Configuration

L'application est pré-configurée pour se connecter au backend. Si vous souhaitez modifier l'URL du backend, éditez le fichier `web_app/vite.config.ts` (pour le développement) ou `web_app/src/services/api.ts` (pour la production).

## 🎨 Design

L'application utilise un thème sombre moderne avec les couleurs suivantes :
- Background : #0F1115
- Primary : #5B8CFF
- Accent : #8B5CF6

## 📦 Structure du projet

```
web_app/
├── src/
│   ├── components/
│   │   ├── layout/       # Layout principal avec navigation
│   │   └── novel/        # Composants NovelCard et DownloadCard
│   ├── context/          # State management (AppContext)
│   ├── pages/            # Pages (Home, Library, Favorites, History)
│   ├── services/         # API service
│   └── types/            # Types TypeScript
├── index.html
├── package.json
├── vite.config.ts
└── README.md