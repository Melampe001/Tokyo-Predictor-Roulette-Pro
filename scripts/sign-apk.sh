#!/bin/bash
# Script para firmar APKs manualmente con jarsigner

set -e

echo "=========================================="
echo "Firmar APK de Android"
echo "=========================================="

# Verificar argumentos
if [ $# -lt 1 ]; then
    echo "Uso: $0 <ruta-al-apk> [keystore] [alias]"
    echo ""
    echo "Ejemplo:"
    echo "  $0 app/build/outputs/apk/release/app-release-unsigned.apk"
    echo "  $0 app-unsigned.apk keystores/release.keystore mi_alias"
    exit 1
fi

APK_PATH="$1"
KEYSTORE_PATH="${2:-keystores/release.keystore}"
ALIAS="${3}"

# Verificar que existe el APK
if [ ! -f "$APK_PATH" ]; then
    echo "❌ Error: No se encuentra el APK: $APK_PATH"
    exit 1
fi

# Verificar que existe el keystore
if [ ! -f "$KEYSTORE_PATH" ]; then
    echo "❌ Error: No se encuentra el keystore: $KEYSTORE_PATH"
    exit 1
fi

# Solicitar alias si no se proporcionó
if [ -z "$ALIAS" ]; then
    read -p "Alias de la clave: " ALIAS
    if [ -z "$ALIAS" ]; then
        echo "❌ El alias es obligatorio"
        exit 1
    fi
fi

# Generar nombre del APK firmado
APK_DIR=$(dirname "$APK_PATH")
APK_FILENAME=$(basename "$APK_PATH")
APK_NAME="${APK_FILENAME%.*}"
SIGNED_APK="$APK_DIR/${APK_NAME}-signed.apk"

echo ""
echo "📦 APK a firmar: $APK_PATH"
echo "🔑 Keystore: $KEYSTORE_PATH"
echo "🏷️  Alias: $ALIAS"
echo "💾 APK firmado: $SIGNED_APK"
echo ""

# Copiar APK
cp "$APK_PATH" "$SIGNED_APK"

# Firmar APK
echo "Firmando APK..."
jarsigner -verbose \
    -keystore "$KEYSTORE_PATH" \
    -signedjar "$SIGNED_APK" \
    "$APK_PATH" \
    "$ALIAS"

# Verificar firma
echo ""
echo "Verificando firma..."
jarsigner -verify -verbose -certs "$SIGNED_APK"

# Alinear APK (zipalign)
if command -v zipalign &> /dev/null; then
    echo ""
    echo "Alineando APK..."
    ALIGNED_APK="$APK_DIR/${APK_NAME}-signed-aligned.apk"
    zipalign -f -v 4 "$SIGNED_APK" "$ALIGNED_APK"
    mv "$ALIGNED_APK" "$SIGNED_APK"
    echo "✅ APK alineado"
fi

echo ""
echo "=========================================="
echo "✅ APK firmado exitosamente!"
echo "📁 Ubicación: $SIGNED_APK"
echo ""
echo "Puedes instalar este APK en dispositivos Android."
echo "=========================================="
