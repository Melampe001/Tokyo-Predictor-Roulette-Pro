# Tokyo-Predictor-Roulette-Pro

Aplicación Android para predicción de ruleta con sistema de firma de versiones configurado.

## 📱 Características

- Configuración completa de firmas de Android (Debug y Release)
- Scripts automatizados para generación de keystores
- Versionado de aplicación configurado
- Sistema de build con Gradle
- Documentación completa en español

## 🚀 Inicio Rápido

### Requisitos Previos

- Java Development Kit (JDK) 11 o superior
- Android SDK
- Gradle 8.2 o superior

### Configuración Inicial

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/Tokyo-Predictor-Roulette-Pro.git
   cd Tokyo-Predictor-Roulette-Pro
   ```

2. **Generar keystore de debug** (para desarrollo)
   ```bash
   ./scripts/generate-debug-keystore.sh
   ```

3. **Generar keystore de release** (para producción)
   ```bash
   ./scripts/generate-release-keystore.sh
   ```
   
   ⚠️ **IMPORTANTE**: Guarda las credenciales del keystore de release en un lugar seguro. Si lo pierdes, no podrás actualizar tu app en Google Play.

4. **Configurar credenciales**
   ```bash
   cp gradle.properties.example gradle.properties
   # Edita gradle.properties con tus credenciales reales
   ```

## 🔧 Compilar la Aplicación

### Compilar APK de Debug
```bash
./gradlew assembleDebug
```
El APK estará en: `app/build/outputs/apk/debug/app-debug.apk`

### Compilar APK de Release
```bash
./gradlew assembleRelease
```
El APK estará en: `app/build/outputs/apk/release/app-release.apk`

### Compilar Android App Bundle (para Google Play)
```bash
./gradlew bundleRelease
```
El AAB estará en: `app/build/outputs/bundle/release/app-release.aab`

## 🔐 Firmas de Android

Este proyecto incluye un sistema completo de firmas de versiones de Android:

### Características de Firma

- **Debug Keystore**: Para desarrollo con credenciales estándar de Android
- **Release Keystore**: Para producción con credenciales personalizadas
- **Versionado Automático**: `versionCode` y `versionName` configurados
- **Scripts de Generación**: Herramientas para crear keystores fácilmente
- **Seguridad**: `.gitignore` configurado para no versionar keystores de producción

### Documentación Completa

Para información detallada sobre firmas de Android, consulta:
📖 **[ANDROID_SIGNING.md](ANDROID_SIGNING.md)** - Guía completa de firmas de Android

Incluye:
- Cómo generar keystores
- Configuración de credenciales
- Firmar APKs manualmente
- Verificar firmas
- Mejores prácticas de seguridad
- Configuración de CI/CD
- Solución de problemas

## 📁 Estructura del Proyecto

```
Tokyo-Predictor-Roulette-Pro/
├── app/
│   ├── build.gradle              # Configuración de build con firmas
│   └── proguard-rules.pro        # Reglas de ofuscación
├── keystores/
│   ├── README.md                 # Información sobre keystores
│   ├── debug.keystore            # Keystore de debug (autogenerado)
│   └── release.keystore          # Keystore de release (NO versionar)
├── scripts/
│   ├── generate-debug-keystore.sh    # Genera keystore de debug
│   ├── generate-release-keystore.sh  # Genera keystore de release
│   └── sign-apk.sh                   # Firma APKs manualmente
├── build.gradle                  # Configuración principal de Gradle
├── settings.gradle               # Configuración de módulos
├── gradle.properties             # Propiedades de Gradle (NO versionar)
├── gradle.properties.example     # Ejemplo de configuración
├── .gitignore                    # Excluye keystores y credenciales
├── ANDROID_SIGNING.md            # Guía completa de firmas
└── README.md                     # Este archivo
```

## 🔒 Seguridad

### ⚠️ Reglas Importantes

1. **NUNCA** versionar keystores de release en Git
2. **NUNCA** incluir contraseñas en el código
3. **SIEMPRE** hacer backups del keystore de release
4. **SIEMPRE** usar contraseñas fuertes

Los archivos sensibles ya están configurados en `.gitignore`:
- `*.keystore` (excepto debug.keystore)
- `*.jks`
- `gradle.properties`

## 📦 Versionado

El versionado de la aplicación se configura en `app/build.gradle`:

```gradle
versionCode 1        // Número de versión interna (incrementar con cada release)
versionName "1.0.0"  // Versión visible para usuarios (formato semántico)
```

### Convención de Versionado

Usamos **Semantic Versioning** (SemVer):
- `MAJOR.MINOR.PATCH` (ej: 1.0.0)
- MAJOR: Cambios incompatibles
- MINOR: Nuevas funcionalidades compatibles
- PATCH: Correcciones de bugs

## 🛠️ Comandos Útiles

### Ver información de un keystore
```bash
keytool -list -v -keystore keystores/release.keystore
```

### Verificar firma de un APK
```bash
jarsigner -verify -verbose -certs app/build/outputs/apk/release/app-release.apk
```

### Obtener SHA-256 fingerprint (para Google Play, Firebase, etc.)
```bash
keytool -list -v -keystore keystores/release.keystore -alias tu_alias | grep SHA256
```

### Firmar APK manualmente
```bash
./scripts/sign-apk.sh app/build/outputs/apk/release/app-release-unsigned.apk
```

## 📚 Recursos

- [Documentación de Firmas de Android](ANDROID_SIGNING.md)
- [Documentación Oficial de Android](https://developer.android.com/studio/publish/app-signing)
- [Google Play App Signing](https://support.google.com/googleplay/android-developer/answer/9842756)
- [Gradle Build Configuration](https://developer.android.com/studio/build/gradle-tips)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## ✉️ Contacto

Para preguntas o soporte, abre un issue en el repositorio.

---

**Versión**: 1.0.0  
**Última actualización**: 2025-11-21