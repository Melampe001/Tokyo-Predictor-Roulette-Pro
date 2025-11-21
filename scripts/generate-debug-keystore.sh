#!/bin/bash
# Script para generar el keystore de debug de Android

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
KEYSTORES_DIR="$PROJECT_ROOT/keystores"

echo "=========================================="
echo "Generando Keystore de Debug"
echo "=========================================="

# Crear directorio de keystores si no existe
mkdir -p "$KEYSTORES_DIR"

# Configuración del keystore de debug (estándar de Android)
KEYSTORE_PATH="$KEYSTORES_DIR/debug.keystore"
ALIAS="androiddebugkey"
PASSWORD="android"
VALIDITY_DAYS=10000

# Verificar si ya existe
if [ -f "$KEYSTORE_PATH" ]; then
    echo "⚠️  El keystore de debug ya existe en: $KEYSTORE_PATH"
    read -p "¿Deseas sobrescribirlo? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Operación cancelada."
        exit 0
    fi
    rm "$KEYSTORE_PATH"
fi

# Generar el keystore
echo "Generando keystore de debug..."
keytool -genkeypair \
    -keystore "$KEYSTORE_PATH" \
    -alias "$ALIAS" \
    -keyalg RSA \
    -keysize 2048 \
    -validity $VALIDITY_DAYS \
    -storepass "$PASSWORD" \
    -keypass "$PASSWORD" \
    -dname "CN=Android Debug,O=Android,C=US"

echo ""
echo "✅ Keystore de debug generado exitosamente!"
echo "📁 Ubicación: $KEYSTORE_PATH"
echo "🔑 Alias: $ALIAS"
echo "🔒 Password: $PASSWORD"
echo ""
echo "Este keystore es solo para desarrollo/debug."
echo "NO usar en producción."
echo "=========================================="
