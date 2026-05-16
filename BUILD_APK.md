# 📱 Comment Créer un Fichier APK pour LNCrawler

Ce guide vous explique comment compiler l'application Flutter en un fichier APK installable sur Android.

## 📋 Prérequis

- **Flutter SDK** installé et configuré
- **Android SDK** et **Android Studio** (pour les outils de build)
- **Java Development Kit (JDK)** 11+

## 🛠️ Étape 1 : Configurer l'environnement Android

### 1.1 Installer Android Studio
Téléchargez et installez [Android Studio](https://developer.android.com/studio).

### 1.2 Installer les outils de build
Dans Android Studio :
1. Allez dans **Tools > SDK Manager**
2. Installez **Android SDK Build-Tools** (version 33.0.0 ou plus)
3. Installez **Android SDK Platform-Tools**

### 1.3 Configurer les variables d'environnement
Ajoutez ces chemins à votre PATH :
```bash
# Linux/Mac (~/.bashrc ou ~/.zshrc)
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/platform-tools

# Windows (dans les variables d'environnement)
# ANDROID_HOME = C:\Users\VotreNom\AppData\Local\Android\Sdk
# Ajoutez %ANDROID_HOME%\platform-tools au PATH
```

## 🔧 Étape 2 : Préparer l'application Flutter

### 2.1 Se placer dans le dossier Flutter
```bash
cd flutter_app
```

### 2.2 Nettoyer le projet
```bash
flutter clean
```

### 2.3 Récupérer les dépendances
```bash
flutter pub get
```

### 2.4 Vérifier la configuration
```bash
flutter doctor
```

Assurez-vous que tous les checks sont verts, surtout **Android toolchain**.

## 📦 Étape 3 : Créer l'APK

### 3.1 APK de débogage (pour tests)
```bash
flutter build apk --debug
```
**Emplacement :** `build/app/outputs/flutter-apk/app-debug.apk`

### 3.2 APK de release (pour distribution)
```bash
flutter build apk --release
```
**Emplacement :** `build/app/outputs/flutter-apk/app-release.apk`

### 3.3 APK split par architecture (plus léger)
```bash
flutter build apk --split-per-abi --release
```
**Emplacement :** `build/app/outputs/flutter-apk/`
- `app-armeabi-v7a-release.apk` (pour les anciens téléphones 32-bit)
- `app-arm64-v8a-release.apk` (pour les téléphones récents 64-bit)

## 🔐 Étape 4 : Signer l'APK (optionnel mais recommandé)

Pour publier sur le Play Store ou installer sur certains appareils, vous devez signer l'APK.

### 4.1 Créer une keystore
```bash
keytool -genkey -v -keystore ~/lncrawler-upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias lncrawler
```

### 4.2 Configurer la signature dans `android/app/build.gradle`

Ajoutez dans `android/app/build.gradle` :
```gradle
android {
    ...
    signingConfigs {
        release {
            keyAlias 'lncrawler'
            keyPassword 'votre_mot_de_passe'
            storeFile file('/chemin/vers/lncrawler-upload-keystore.jks')
            storePassword 'votre_mot_de_passe'
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

### 4.3 Reconstruire l'APK signé
```bash
flutter build apk --release
```

## 📲 Étape 5 : Installer l'APK sur un appareil Android

### Méthode 1 : Via ADB (USB)
```bash
# Connectez votre téléphone en USB (débogage USB activé)
adb install build/app/outputs/flutter-apk/app-release.apk
```

### Méthode 2 : Transfert manuel
1. Copiez le fichier APK sur votre téléphone
2. Ouvrez le gestionnaire de fichiers
3. Tapez sur l'APK pour l'installer
4. Autorisez l'installation depuis des sources inconnues si demandé

### Méthode 3 : Via Google Drive / Email
Envoyez-vous l'APK par email ou Google Drive, puis téléchargez-le sur votre téléphone et installez-le.

## ⚠️ Configuration importante avant de build

### Modifier l'URL du backend
Dans `lib/core/constants/app_constants.dart`, remplacez :
```dart
static const String baseUrl = 'http://10.0.2.2:8000'; // Pour émulateur
```
par l'IP publique de votre serveur backend :
```dart
static const String baseUrl = 'http://VOTRE_IP_PUBLIQUE:8000';
// ou
static const String baseUrl = 'https://api.lncrawler.com'; // Si vous avez un domaine
```

### Permissions Android
Le fichier `android/app/src/main/AndroidManifest.xml` inclut déjà :
```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
```

## 🐛 Problèmes courants

### "SDK location not found"
**Solution :** Créez un fichier `local.properties` dans `android/` :
```properties
sdk.dir=/home/votre_nom/Android/Sdk
```

### "Build failed with an exception"
**Solution :**
```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter pub get
flutter build apk --release
```

### "No space left on device"
**Solution :** Libérez de l'espace disque (le build Android prend plusieurs Go).

### L'APK ne s'installe pas
**Solution :** Activez "Sources inconnues" dans Paramètres > Sécurité de votre téléphone.

## 📊 Tailles approximatives des APK

- **APK debug** : ~60-80 MB
- **APK release** : ~40-60 MB
- **APK split par ABI** : ~20-30 MB chacun

## 🚀 Prochaines étapes

Une fois l'APK créé :
1. Testez-le sur plusieurs appareils
2. Vérifiez que le backend est accessible depuis l'extérieur
3. Partagez l'APK avec des testeurs
4. Pour publier sur le Play Store, suivez les directives de Google

---

**Besoin d'aide ?** Consultez la documentation Flutter officielle : https://docs.flutter.dev/deployment/android