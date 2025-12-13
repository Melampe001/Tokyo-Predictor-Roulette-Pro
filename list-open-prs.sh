#!/bin/bash
set -u

# Script para listar los pull requests abiertos más recientes
# Script to list the most recent open pull requests

REPO="Melampe001/Tokyo-Predictor-Roulette-Pro"

echo "======================================"
echo "Pull Requests Abiertos / Open PRs"
echo "Repositorio / Repository: $REPO"
echo "======================================"
echo ""

# Verificar si gh CLI está instalado
if command -v gh &> /dev/null; then
    echo "Usando GitHub CLI (gh)..."
    echo ""
    if gh pr list --repo "$REPO" --state open --limit 5 2>/dev/null; then
        echo ""
        echo "Para ver más detalles de un PR específico, usa:"
        echo "  gh pr view <número> --repo $REPO"
    else
        echo "No se pudo acceder a GitHub. Verifica que tengas credenciales configuradas."
        echo "Ejecuta: gh auth login"
        echo ""
        echo "O establece el token GH_TOKEN en tu entorno."
    fi
else
    echo "GitHub CLI (gh) no está instalado."
    echo ""
    echo "Opciones alternativas:"
    echo "1. Visita: https://github.com/$REPO/pulls"
    echo "2. Instala GitHub CLI: https://cli.github.com/"
    echo "3. Usa la API:"
    echo "   curl -H 'Accept: application/vnd.github+json' \\"
    echo "     'https://api.github.com/repos/$REPO/pulls?state=open'"
fi

echo ""
echo "======================================"
