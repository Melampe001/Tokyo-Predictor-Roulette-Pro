# Guía Rápida de Inicio - Tokyo Predictor Roulette Pro

## ⚡ Inicio en 5 Minutos

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/Tokyo-Predictor-Roulette-Pro.git
cd Tokyo-Predictor-Roulette-Pro
```

### 2. Generar Keystore de Debug
```bash
./scripts/generate-debug-keystore.sh
```
Presiona `s` para confirmar cuando se solicite.

### 3. Compilar APK de Debug
```bash
./gradlew assembleDebug
```

### 4. Instalar en Dispositivo
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

## 🚀 Para Producción

### 1. Generar Keystore de Release
```bash
./scripts/generate-release-keystore.sh
```
Completa todos los campos solicitados y **guarda las credenciales de forma segura**.

### 2. Configurar Credenciales
```bash
cp gradle.properties.example gradle.properties
nano gradle.properties  # o usa tu editor favorito
```

Completa:
```properties
RELEASE_KEYSTORE_PATH=./keystores/release.keystore
RELEASE_KEYSTORE_PASSWORD=tu_password
RELEASE_KEY_ALIAS=tu_alias
RELEASE_KEY_PASSWORD=tu_password
```

### 3. Compilar APK de Release
```bash
./gradlew assembleRelease
```

### 4. El APK Firmado está Listo
```
app/build/outputs/apk/release/app-release.apk
```

## 📱 Comandos Útiles

### Limpiar Build
```bash
./gradlew clean
```

### Ver Tareas Disponibles
```bash
./gradlew tasks
```

### Compilar Bundle para Google Play
```bash
./gradlew bundleRelease
```

### Verificar Firma de APK
```bash
jarsigner -verify -verbose app/build/outputs/apk/release/app-release.apk
```

## 🔍 Solución Rápida de Problemas

### Error: "SDK location not found"
```bash
# Crear archivo local.properties
echo "sdk.dir=/ruta/a/tu/Android/Sdk" > local.properties
```

### Error: "keytool: command not found"
Instala JDK 11 o superior y añade al PATH.

### Error al compilar
```bash
# Limpiar y reintentar
./gradlew clean
./gradlew assembleDebug --stacktrace
```

## 📖 Más Información

- **Documentación Completa**: Ver [README.md](README.md)
- **Guía de Firmas**: Ver [ANDROID_SIGNING.md](ANDROID_SIGNING.md)
- **Estructura de Keystores**: Ver [keystores/README.md](keystores/README.md)

## ⚠️ Recordatorios Importantes

1. ✅ El keystore de debug puede compartirse (no es sensible)
2. 🔒 El keystore de release NUNCA debe versionarse en Git
3. 💾 Haz backup del keystore de release en múltiples lugares seguros
4. 🔑 Usa un gestor de contraseñas para guardar las credenciales

---

¿Necesitas ayuda? Abre un issue en el repositorio.
