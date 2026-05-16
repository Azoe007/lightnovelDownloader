# 🚀 Déployer le Backend sur Render.com

Guide étape par étape pour héberger gratuitement le backend LNCrawler sur Render.

## 📋 Prérequis

- Un compte Render.com (créé ✅)
- Un compte GitHub
- Git installé sur votre ordinateur

## 🛠️ Étape 1 : Préparer le projet pour Render

### 1.1 Créer un dépôt GitHub

```bash
# Initialiser git dans le projet
cd /home/aymanzara/Documents/Projet\ perso/Ln/ln_scalable
git init

# Ajouter tous les fichiers
git add .

# Faire un commit
git commit -m "Initial commit - LNCrawler project"

# Créer un dépôt sur GitHub (à faire sur github.com)
# Puis ajouter le remote
git remote add origin https://github.com/VOTRE_PSEUDO/lncrawler.git

# Pousser le code
git push -u origin main
```

### 1.2 Ajouter un fichier `render.yaml` à la racine

Créez un fichier `render.yaml` à la racine du projet :

```yaml
services:
  - type: web
    name: lncrawler-backend
    env: python
    region: frankfurt
    plan: free
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        value: sqlite+aiosqlite:///./lncrawler.db
      - key: DOWNLOAD_DIR
        value: ./downloads
      - key: COVER_DIR
        value: ./covers
    disk:
      name: data
      mountPath: /opt/render/project/src
      sizeGB: 1
```

### 1.3 Ajouter un `.gitignore`

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build
build/
dist/
*.egg-info/
```

## 🌐 Étape 2 : Déployer sur Render

### 2.1 Connecter GitHub à Render

1. Allez sur [dashboard.render.com](https://dashboard.render.com)
2. Cliquez sur **"New +"** → **"Web Service"**
3. Connectez votre compte GitHub
4. Sélectionnez le dépôt `lncrawler`

### 2.2 Configurer le service

Remplissez les champs :

| Champ | Valeur |
|-------|--------|
| **Name** | `lncrawler-backend` |
| **Region** | `Frankfurt` (le plus proche) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

### 2.3 Variables d'environnement

Ajoutez ces variables dans la section "Environment" :

```
DATABASE_URL=sqlite+aiosqlite:///./lncrawler.db
DOWNLOAD_DIR=./downloads
COVER_DIR=./covers
MAX_CONCURRENT_DOWNLOADS=3
CHAPTER_DELAY=1
```

### 2.4 Lancer le déploiement

Cliquez sur **"Create Web Service"** et attendez la fin du déploiement (~2-5 minutes).

## 🔗 Étape 3 : Récupérer l'URL

Une fois déployé, Render vous donnera une URL du type :
```
https://lncrawler-backend-xxxx.onrender.com
```

**Notez cette URL !**

## 📱 Étape 4 : Configurer l'application Flutter

Modifiez `flutter_app/lib/core/constants/app_constants.dart` :

```dart
class AppConstants {
  // Remplacer par l'URL Render
  static const String baseUrl = 'https://lncrawler-backend-xxxx.onrender.com';
  static const String apiBaseUrl = '$baseUrl/api';
  
  // ... le reste reste identique
}
```

## 🔄 Étape 5 : Reconstruire l'APK

```bash
cd flutter_app
flutter clean
flutter pub get
flutter build apk --release
```

L'APK sera dans `build/app/outputs/flutter-apk/app-release.apk`.

## ✅ Tester

1. Installez le nouvel APK sur votre téléphone
2. Allez dans l'écran d'accueil
3. Collez une URL de novel
4. Lancez un téléchargement

## ⚠️ Limitations du plan gratuit

- **750 heures/mois** (le service se met en veille après 15min d'inactivité)
- **1 Go de stockage** pour les fichiers
- **CPU limité** (les téléchargements peuvent être lents)
- **Temps de réponse** : le premier appel après une période d'inactivité peut prendre 30-50 secondes

## 💡 Astuces

### Garder le service actif
Le service gratuit se met en veille. Pour le réveiller :
- Envoyez une requête toutes les 10 minutes
- Ou utilisez un service comme [UptimeRobot](https://uptimerobot.com) pour ping toutes les 5 minutes

### Surveiller les logs
Dans le dashboard Render :
- Allez sur votre service
- Cliquez sur **"Logs"** pour voir les erreurs

### Mettre à jour le code
```bash
# Après avoir modifié le code
git add .
git commit -m "Update"
git push

# Render redéploiera automatiquement
```

## 🆘 Problèmes courants

### "Build failed"
Vérifiez les logs dans Render. Souvent c'est un problème de dépendances.

### "Module not found"
Assurez-vous que le `Root Directory` est bien `backend` dans Render.

### "Port not found"
Le start command doit utiliser `$PORT` (variable d'environnement Render).

### "Database locked"
SQLite peut avoir des problèmes de concurrence. Pour production, envisagez PostgreSQL (aussi gratuit sur Render).

## 📞 Besoin d'aide ?

- Documentation Render : https://render.com/docs
- Logs du service dans le dashboard
- Support Render : support@render.com

---

**Votre backend est maintenant en ligne !** 🎉