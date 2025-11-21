#!/bin/bash
# Script para generar el keystore de release/producción de Android

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
KEYSTORES_DIR="$PROJECT_ROOT/keystores"

echo "=========================================="
echo "Generando Keystore de Release (Producción)"
echo "=========================================="
echo ""
echo "⚠️  IMPORTANTE: Guarda las credenciales en un lugar seguro!"
echo "⚠️  Si pierdes este keystore, NO podrás actualizar tu app en Google Play."
echo ""

# Crear directorio de keystores si no existe
mkdir -p "$KEYSTORES_DIR"

# Solicitar información
read -p "Nombre del archivo keystore (default: release.keystore): " KEYSTORE_NAME
KEYSTORE_NAME=${KEYSTORE_NAME:-release.keystore}
KEYSTORE_PATH="$KEYSTORES_DIR/$KEYSTORE_NAME"

read -p "Alias de la clave: " ALIAS
if [ -z "$ALIAS" ]; then
    echo "❌ El alias es obligatorio"
    exit 1
fi

read -sp "Password del keystore: " STORE_PASSWORD
echo ""
if [ -z "$STORE_PASSWORD" ]; then
    echo "❌ El password del keystore es obligatorio"
    exit 1
fi

read -sp "Password de la clave (puede ser igual al anterior): " KEY_PASSWORD
echo ""
if [ -z "$KEY_PASSWORD" ]; then
    echo "❌ El password de la clave es obligatorio"
    exit 1
fi

read -p "Nombre completo (CN): " CN
read -p "Unidad organizacional (OU): " OU
read -p "Organización (O): " O
read -p "Ciudad (L): " L
read -p "Estado/Provincia (ST): " ST
read -p "Código de país de 2 letras (C): " C

DNAME="CN=$CN, OU=$OU, O=$O, L=$L, ST=$ST, C=$C"
VALIDITY_DAYS=10000

# Verificar si ya existe
if [ -f "$KEYSTORE_PATH" ]; then
    echo "⚠️  El keystore ya existe en: $KEYSTORE_PATH"
    read -p "¿Deseas sobrescribirlo? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Operación cancelada."
        exit 0
    fi
    rm "$KEYSTORE_PATH"
fi

# Generar el keystore
echo ""
echo "Generando keystore de release..."
keytool -genkeypair \
    -keystore "$KEYSTORE_PATH" \
    -alias "$ALIAS" \
    -keyalg RSA \
    -keysize 2048 \
    -validity $VALIDITY_DAYS \
    -storepass "$STORE_PASSWORD" \
    -keypass "$KEY_PASSWORD" \
    -dname "$DNAME"

echo ""
echo "✅ Keystore de release generado exitosamente!"
echo "=========================================="
echo "📁 Ubicación: $KEYSTORE_PATH"
echo "🔑 Alias: $ALIAS"
echo ""
echo "⚠️  GUARDA ESTA INFORMACIÓN DE FORMA SEGURA:"
echo "   - Archivo keystore: $KEYSTORE_PATH"
echo "   - Alias: $ALIAS"
echo "   - Password del keystore: [el que ingresaste]"
echo "   - Password de la clave: [el que ingresaste]"
echo ""
echo "📝 Actualiza tu archivo gradle.properties local con:"
echo "   RELEASE_KEYSTORE_PATH=$KEYSTORE_PATH"
echo "   RELEASE_KEY_ALIAS=$ALIAS"
echo "   RELEASE_KEYSTORE_PASSWORD=[tu password]"
echo "   RELEASE_KEY_PASSWORD=[tu password]"
echo ""
echo "🔒 NUNCA versiones este keystore en Git!"
echo "=========================================="
