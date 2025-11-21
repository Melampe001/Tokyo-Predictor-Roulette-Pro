# Keystores

Este directorio contiene los keystores de firma para la aplicación Android.

## ⚠️ IMPORTANTE

- **NUNCA versionar keystores de release en Git**
- Los keystores de release contienen claves privadas críticas
- Si pierdes el keystore de release, no podrás actualizar tu app en Google Play

## Contenido

### debug.keystore
- Keystore de desarrollo
- Credenciales estándar de Android
- Puede ser versionado (no es crítico)
- Se regenera automáticamente si se pierde

### release.keystore
- Keystore de producción
- **NO DEBE ser versionado**
- **Hacer backups múltiples**
- Crítico para publicar en Google Play

## Generar Keystores

### Debug Keystore
```bash
../scripts/generate-debug-keystore.sh
```

### Release Keystore
```bash
../scripts/generate-release-keystore.sh
```

## Seguridad

1. Haz backup del keystore de release en ubicaciones seguras
2. Usa un gestor de contraseñas para guardar las credenciales
3. Nunca compartas el keystore de release públicamente
4. Considera cifrar los backups con GPG o similar

## Backup

Ejemplo de comando para hacer backup:

```bash
# Backup simple
cp release.keystore ~/secure-backups/release.keystore.$(date +%Y%m%d)

# Backup cifrado con GPG
gpg -c release.keystore
mv release.keystore.gpg ~/secure-backups/
```

## Ver Información del Keystore

```bash
# Listar alias
keytool -list -v -keystore release.keystore

# Ver certificado
keytool -list -v -keystore release.keystore -alias <tu-alias>

# Obtener SHA-256 fingerprint
keytool -list -v -keystore release.keystore -alias <tu-alias> | grep SHA256
```

Para más información, consulta [ANDROID_SIGNING.md](../ANDROID_SIGNING.md)
