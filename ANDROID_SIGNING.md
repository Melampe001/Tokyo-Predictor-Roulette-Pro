# Guía de Firmas de Versiones de Android

Esta guía explica cómo configurar y usar las firmas de aplicaciones Android para el proyecto Tokyo Predictor Roulette Pro.

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Tipos de Firma](#tipos-de-firma)
3. [Configuración Inicial](#configuración-inicial)
4. [Generar Keystores](#generar-keystores)
5. [Configurar Credenciales](#configurar-credenciales)
6. [Compilar APKs Firmados](#compilar-apks-firmados)
7. [Verificar Firmas](#verificar-firmas)
8. [Seguridad](#seguridad)
9. [CI/CD](#cicd)

## 🎯 Introducción

Las aplicaciones Android deben estar firmadas digitalmente antes de poder ser instaladas en dispositivos. Existen dos tipos de configuraciones de firma:

- **Debug**: Para desarrollo y pruebas
- **Release**: Para producción y publicación en Google Play Store

## 🔐 Tipos de Firma

### Debug Keystore

- Usado durante el desarrollo
- Generado automáticamente por Android Studio
- Credenciales estándar conocidas públicamente
- **NO usar en producción**

### Release Keystore

- Usado para versiones de producción
- Debe ser generado manualmente
- Credenciales únicas y secretas
- **Crítico**: Si se pierde, no se pueden publicar actualizaciones en Google Play

## ⚙️ Configuración Inicial

### Requisitos Previos

- Java Development Kit (JDK) 11 o superior
- Android SDK instalado
- Herramienta `keytool` (incluida en JDK)

### Estructura del Proyecto

```
Tokyo-Predictor-Roulette-Pro/
├── app/
│   ├── build.gradle          # Configuración de firma
│   └── proguard-rules.pro    # Reglas de ofuscación
├── keystores/                # Keystores (no versionados)
│   ├── debug.keystore        # Keystore de debug
│   └── release.keystore      # Keystore de release (NO versionar)
├── scripts/                  # Scripts de utilidad
│   ├── generate-debug-keystore.sh
│   ├── generate-release-keystore.sh
│   └── sign-apk.sh
├── gradle.properties.example # Plantilla de configuración
└── .gitignore               # Excluye keystores y credenciales
```

## 🔑 Generar Keystores

### Generar Debug Keystore

El keystore de debug usa credenciales estándar de Android:

```bash
./scripts/generate-debug-keystore.sh
```

**Credenciales de debug:**
- Keystore password: `android`
- Key alias: `androiddebugkey`
- Key password: `android`

### Generar Release Keystore

⚠️ **IMPORTANTE**: Este keystore es crítico para tu aplicación. Si lo pierdes, no podrás actualizar tu app en Google Play.

```bash
./scripts/generate-release-keystore.sh
```

El script te solicitará:
- Nombre del archivo keystore
- Alias de la clave
- Passwords (keystore y clave)
- Información de la organización (CN, OU, O, L, ST, C)

**Ejemplo de información:**
```
CN: Tu Nombre
OU: Desarrollo Android
O: Tokyo Predictor Roulette Pro
L: Ciudad de México
ST: CDMX
C: MX
```

### Generar Keystore Manualmente

Si prefieres usar `keytool` directamente:

```bash
keytool -genkeypair \
    -keystore keystores/release.keystore \
    -alias mi_alias \
    -keyalg RSA \
    -keysize 2048 \
    -validity 10000 \
    -storepass mi_password_seguro \
    -keypass mi_password_seguro \
    -dname "CN=Mi Nombre, OU=Android, O=Mi Empresa, L=Ciudad, ST=Estado, C=MX"
```

## 🔧 Configurar Credenciales

### Opción 1: Archivo gradle.properties Local (Recomendado)

1. Copia el archivo de ejemplo:
```bash
cp gradle.properties.example gradle.properties
```

2. Edita `gradle.properties` con tus credenciales reales:
```properties
RELEASE_KEYSTORE_PATH=./keystores/release.keystore
RELEASE_KEYSTORE_PASSWORD=tu_password_aqui
RELEASE_KEY_ALIAS=tu_alias
RELEASE_KEY_PASSWORD=tu_password_de_clave
```

3. Verifica que `gradle.properties` esté en `.gitignore` (ya está incluido)

### Opción 2: Variables de Entorno

Configura las siguientes variables de entorno:

```bash
export RELEASE_KEYSTORE_PATH="./keystores/release.keystore"
export RELEASE_KEYSTORE_PASSWORD="tu_password"
export RELEASE_KEY_ALIAS="tu_alias"
export RELEASE_KEY_PASSWORD="tu_password_de_clave"
```

Para hacer permanentes las variables (en Linux/macOS), añádelas a `~/.bashrc` o `~/.zshrc`:

```bash
echo 'export RELEASE_KEYSTORE_PATH="./keystores/release.keystore"' >> ~/.bashrc
echo 'export RELEASE_KEYSTORE_PASSWORD="tu_password"' >> ~/.bashrc
echo 'export RELEASE_KEY_ALIAS="tu_alias"' >> ~/.bashrc
echo 'export RELEASE_KEY_PASSWORD="tu_password"' >> ~/.bashrc
source ~/.bashrc
```

## 🏗️ Compilar APKs Firmados

### Compilar Debug APK

```bash
./gradlew assembleDebug
```

El APK firmado estará en: `app/build/outputs/apk/debug/app-debug.apk`

### Compilar Release APK

```bash
./gradlew assembleRelease
```

El APK firmado estará en: `app/build/outputs/apk/release/app-release.apk`

### Compilar Android App Bundle (AAB) para Google Play

```bash
./gradlew bundleRelease
```

El AAB firmado estará en: `app/build/outputs/bundle/release/app-release.aab`

## ✅ Verificar Firmas

### Verificar que un APK está firmado

```bash
jarsigner -verify -verbose -certs app/build/outputs/apk/release/app-release.apk
```

### Ver información de la firma

```bash
keytool -list -v -keystore keystores/release.keystore
```

### Ver información de firma de un APK

```bash
keytool -printcert -jarfile app/build/outputs/apk/release/app-release.apk
```

### Obtener SHA-256 fingerprint (necesario para Google Play, Firebase, etc.)

```bash
keytool -list -v -keystore keystores/release.keystore -alias tu_alias
```

Busca la línea que dice `SHA256:` y copia el valor hexadecimal.

## 🔒 Seguridad

### ⚠️ Reglas Críticas de Seguridad

1. **NUNCA versionar keystores de producción en Git**
   - Ya está configurado en `.gitignore`
   - Los keystores de release deben mantenerse privados

2. **NUNCA incluir passwords en código**
   - Usar variables de entorno o `gradle.properties` local
   - `gradle.properties` está en `.gitignore`

3. **Hacer backups del keystore de release**
   - Guardar en múltiples ubicaciones seguras
   - Considerar almacenamiento cifrado
   - Guardar contraseñas en un gestor de contraseñas

4. **Usar contraseñas fuertes**
   - Mínimo 12 caracteres
   - Combinación de letras, números y símbolos
   - No usar contraseñas comunes

### Backup del Keystore

Haz copias de seguridad del keystore de release:

```bash
# Hacer backup
cp keystores/release.keystore ~/backups/release.keystore.$(date +%Y%m%d)

# Cifrar el backup (opcional pero recomendado)
gpg -c ~/backups/release.keystore.$(date +%Y%m%d)
```

### Rotar Credenciales

Si crees que tus credenciales están comprometidas:

1. Para keystores de debug: simplemente regenera con el script
2. Para keystores de release: **NO puedes cambiarlos** si ya publicaste en Google Play
   - Google Play requiere que uses el mismo keystore para todas las actualizaciones
   - Considera usar [Google Play App Signing](https://support.google.com/googleplay/android-developer/answer/9842756)

## 🚀 CI/CD

### GitHub Actions

Ejemplo de configuración para firmar APKs en GitHub Actions:

```yaml
name: Build and Sign APK

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up JDK
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Decode Keystore
        env:
          KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
        run: |
          echo $KEYSTORE_BASE64 | base64 -d > keystores/release.keystore
      
      - name: Build Release APK
        env:
          RELEASE_KEYSTORE_PATH: ./keystores/release.keystore
          RELEASE_KEYSTORE_PASSWORD: ${{ secrets.RELEASE_KEYSTORE_PASSWORD }}
          RELEASE_KEY_ALIAS: ${{ secrets.RELEASE_KEY_ALIAS }}
          RELEASE_KEY_PASSWORD: ${{ secrets.RELEASE_KEY_PASSWORD }}
        run: ./gradlew assembleRelease
      
      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: app-release
          path: app/build/outputs/apk/release/app-release.apk
```

Para configurar los secretos en GitHub:

1. Codifica tu keystore en base64:
```bash
base64 -i keystores/release.keystore | pbcopy  # macOS
base64 -i keystores/release.keystore | xclip    # Linux
```

2. Ve a Settings → Secrets and variables → Actions
3. Añade los secretos:
   - `KEYSTORE_BASE64`: el keystore codificado en base64
   - `RELEASE_KEYSTORE_PASSWORD`: password del keystore
   - `RELEASE_KEY_ALIAS`: alias de la clave
   - `RELEASE_KEY_PASSWORD`: password de la clave

## 📚 Recursos Adicionales

- [Documentación oficial de Android sobre App Signing](https://developer.android.com/studio/publish/app-signing)
- [Google Play App Signing](https://support.google.com/googleplay/android-developer/answer/9842756)
- [Configuración de Gradle para firma](https://developer.android.com/studio/build/gradle-tips#sign-your-app)
- [Mejores prácticas de seguridad](https://developer.android.com/topic/security/best-practices)

## 🆘 Solución de Problemas

### Error: "keystore was tampered with, or password was incorrect"

- Verifica que el password sea correcto
- Asegúrate de usar el archivo keystore correcto
- El archivo keystore puede estar corrupto (restaura del backup)

### Error: "Alias does not exist"

- Verifica que el alias sea correcto
- Lista los alias disponibles: `keytool -list -v -keystore keystores/release.keystore`

### Error: "Could not find or load main class"

- Asegúrate de tener JDK instalado (no solo JRE)
- Verifica la variable de entorno JAVA_HOME

### No puedo actualizar mi app en Google Play

- Debes usar el mismo keystore que usaste en la primera versión
- Si perdiste el keystore original, NO puedes actualizar la app
- Tendrías que publicar una nueva app con un nuevo paquete

## 📞 Soporte

Para problemas o preguntas sobre firmas de Android en este proyecto:

1. Revisa esta documentación
2. Consulta la documentación oficial de Android
3. Abre un issue en el repositorio con la etiqueta `android-signing`

---

**Última actualización**: 2025-11-21
**Versión del documento**: 1.0.0
