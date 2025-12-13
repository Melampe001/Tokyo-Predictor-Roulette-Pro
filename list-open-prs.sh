#!/bin/bash

# Script para listar el pull request abierto más reciente
# Script to list the most recent open pull request

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
    gh pr list --repo "$REPO" --state open --limit 5
    echo ""
    echo "Para ver más detalles de un PR específico, usa:"
    echo "  gh pr view <número> --repo $REPO"
else
    echo "GitHub CLI (gh) no está instalado."
    echo ""
    echo "Opciones alternativas:"
    echo "1. Visita: https://github.com/$REPO/pulls"
    echo "2. Instala GitHub CLI: https://cli.github.com/"
    echo "3. Usa la API:"
    echo "   curl -H 'Accept: application/vnd.github.v3+json' \\"
    echo "     https://api.github.com/repos/$REPO/pulls?state=open"
fi

echo ""
echo "======================================"
