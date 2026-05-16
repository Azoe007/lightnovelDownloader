# Guide d'Installation Complet - LNCrawler

Ce guide vous explique comment installer et lancer l'application complète LNCrawler (backend + frontend).

## 📋 Prérequis

- **Python 3.10+** (pour le backend)
- **Flutter SDK 3.0+** (pour l'application mobile)
- **Git** (optionnel, pour cloner le projet)

---

## 🖥️ Étape 1 : Installer le Backend

### 1.1 Créer et activer l'environnement virtuel

```bash
# Se placer dans le dossier backend
cd backend

# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement (Linux/Mac)
source venv/bin/activate

# Activer l'environnement (Windows)
# venv\Scripts\activate
```

### 1.2 Installer les dépendances

```bash
pip install -r requirements.txt
```

### 1.3 Lancer le serveur backend

```bash
# Depuis le dossier backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Vérification :** Ouvrez votre navigateur et allez sur http://localhost:8000/health
Vous devriez voir : `{"status": "healthy"}`

**Documentation API :** http://localhost:8000/docs

---

## 📱 Étape 2 : Installer l'Application Flutter

### 2.1 Installer Flutter (si ce n'est pas déjà fait)

**Sur Linux :**
```bash
# Télécharger Flutter
cd ~
wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.19.0-stable.tar.xz

# Extraire
tar xf flutter_linux_3.19.0-stable.tar.xz

# Ajouter à PATH (dans ~/.bashrc ou ~/.zshrc)
export PATH="$PATH:`pwd`/flutter/bin"

# Vérifier l'installation
flutter doctor
```

**Sur Windows :**
- Télécharger l'archive Flutter sur https://docs.flutter.dev/get-started/install/windows
- Extraire dans C:\src\flutter
- Ajouter C:\src\flutter\bin au PATH

**Sur Mac :**
```bash
brew install --cask flutter
flutter doctor
```

### 2.2 Configurer l'application Flutter

```bash
# Se placer dans le dossier flutter_app
cd flutter_app

# Installer les dépendances
flutter pub get

# Vérifier la configuration
flutter doctor
```

### 2.3 Configurer l'URL du backend

Ouvrez le fichier `lib/core/constants/app_constants.dart` et modifiez l'URL :

```dart
// Remplacer localhost par l'IP de votre machine si vous testez sur un appareil physique
static const String baseUrl = 'http://10.0.2.2:8000'; // Pour émulateur Android
// ou
static const String baseUrl = 'http://localhost:8000'; // Pour web/desktop
```

**Notes importantes :**
- **Émulateur Android** : Utilisez `10.0.2.2` au lieu de `localhost`
- **Émulateur iOS** : Utilisez `localhost`
- **Appareil physique** : Utilisez l'IP locale de votre ordinateur (ex: `192.168.1.100`)

### 2.4 Lancer l'application

```bash
# Pour voir les appareils disponibles
flutter devices

# Lancer sur un émulateur/device spécifique
flutter run

# Ou lancer sur Chrome (version web)
flutter run -d chrome

# Ou lancer sur un appareil Android connecté
flutter run -d <device_id>
```

---

## 🚀 Étape 3 : Tester l'Application

### 3.1 Tester le backend seul (sans Flutter)

Vous pouvez tester l'API directement depuis votre navigateur ou avec curl :

```bash
# Vérifier que le backend fonctionne
curl http://localhost:8000/health

# Démarrer un téléchargement (exemple)
curl -X POST http://localhost:8000/api/downloads \
  -H "Content-Type: application/json" \
  -d '{"url": "https://novelfrance.fr/novel/example"}'

# Voir la liste des téléchargements
curl http://localhost:8000/api/downloads
```

### 3.2 Tester avec l'application Flutter

1. **Lancez le backend** (étape 1.3)
2. **Lancez l'application Flutter** (étape 2.4)
3. **Dans l'application :**
   - Allez dans l'onglet "Accueil"
   - Collez une URL de novel (ex: `https://novelfrance.fr/novel/nom-du-novel`)
   - Cliquez sur "Démarrer le téléchargement"
   - Suivez la progression dans l'onglet "Downloads"

---

## 🔧 Dépannage

### Problème : "flutter: command not found"
**Solution :** Flutter n'est pas dans votre PATH. Redémarrez le terminal ou ajoutez Flutter manuellement.

### Problème : "No devices found"
**Solution :** 
- Pour tester sur ordinateur : `flutter run -d linux` ou `flutter run -d windows` ou `flutter run -d macos`
- Pour tester sur web : `flutter run -d chrome`
- Pour Android/iOS : Connectez un appareil ou lancez un émulateur

### Problème : "Connection refused" ou "Failed to connect to backend"
**Solution :**
1. Vérifiez que le backend est lancé : `curl http://localhost:8000/health`
2. Vérifiez l'URL dans `lib/core/constants/app_constants.dart`
3. Si vous utilisez un appareil physique, assurez-vous que l'ordinateur et l'appareil sont sur le même réseau WiFi

### Problème : "Pub get failed"
**Solution :**
```bash
flutter clean
flutter pub get
```

### Problème : Le backend ne démarre pas
**Solution :**
```bash
# Vérifier que Python est installé
python3 --version

# Réinstaller les dépendances
cd backend
pip install -r requirements.txt --force-reinstall
```

---

## 📦 Construire une version de production

### Backend (optionnel avec Gunicorn)

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Flutter APK

```bash
cd flutter_app

# Build APK de release
flutter build apk --release

# L'APK sera dans build/app/outputs/flutter-apk/app-release.apk
```

### Flutter iOS

```bash
cd flutter_app
flutter build ios
```

---

## 📞 Besoin d'aide ?

- Documentation API : http://localhost:8000/docs
- README principal : [README.md](README.md)
- Issues GitHub : (à créer si vous hébergez le projet)

---

**Profitez de LNCrawler !** 🎉