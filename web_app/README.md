# LNCrawler Web App

Application web moderne pour télécharger des webnovels, développée avec React, TypeScript et Tailwind CSS.

## 🚀 Fonctionnalités

- **Téléchargement de webnovels** - Collez une URL et téléchargez automatiquement
- **Bibliothèque** - Explorez les webnovels disponibles avec recherche
- **Favoris** - Sauvegardez vos webnovels préférés
- **Historique** - Gardez une trace de vos consultations
- **Interface responsive** - Fonctionne sur mobile, tablette et desktop
- **Dark theme** - Design moderne et élégant

## 🛠️ Stack Technique

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool ultra-rapide
- **Tailwind CSS** - Utility-first CSS
- **React Router** - Navigation
- **Axios** - HTTP client
- **Lucide React** - Icônes modernes
- **React Hot Toast** - Notifications

## 📦 Installation

```bash
# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm run dev

# Build pour la production
npm run build

# Prévisualiser la production
npm run preview
```

## 🔧 Configuration

L'application se connecte automatiquement au backend via le proxy Vite configuré dans `vite.config.ts`.

Pour une utilisation en production, vous pouvez modifier l'URL du backend dans `src/services/api.ts`.

## 📱 Pages

- **Accueil** (`/`) - Téléchargement de webnovels
- **Bibliothèque** (`/library`) - Grid des novels disponibles
- **Favoris** (`/favorites`) - Vos novels favoris
- **Historique** (`/history`) - Historique des consultations

## 🎨 Design System

- **Background** : `#0F1115`
- **Surface** : `#1A1D24`
- **Primary** : `#5B8CFF`
- **Accent** : `#8B5CF6`
- **Text Primary** : `#F5F7FA`
- **Text Secondary** : `#A1A8B3`

## 🌐 Déploiement

### Build statique
```bash
npm run build
```

Les fichiers statiques seront générés dans le dossier `dist/`.

### Docker (optionnel)
Vous pouvez utiliser un conteneur Node.js ou Nginx pour servir l'application.

## 📄 Licence

MIT