# Pull Requests Abiertos

## Consultar el Pull Request Más Reciente

Para ver el pull request abierto más reciente en este repositorio, puedes usar cualquiera de los siguientes métodos:

### Método 1: Interfaz Web de GitHub
Visita directamente: https://github.com/Melampe001/Tokyo-Predictor-Roulette-Pro/pulls

Los pull requests se muestran ordenados por fecha de actualización por defecto, con el más reciente al principio.

### Método 2: GitHub CLI (gh)
Si tienes instalado GitHub CLI, ejecuta:

```bash
gh pr list --repo Melampe001/Tokyo-Predictor-Roulette-Pro --state open --limit 1
```

Para ver más detalles de un PR específico:

```bash
# Ver detalles del primer PR en la lista
gh pr view --repo Melampe001/Tokyo-Predictor-Roulette-Pro <número-del-pr>

# O listar con formato JSON para procesamiento
gh pr list --repo Melampe001/Tokyo-Predictor-Roulette-Pro --state open --limit 1 --json number,title,author,updatedAt
```

### Método 3: API de GitHub
Usando curl:

```bash
curl -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/Melampe001/Tokyo-Predictor-Roulette-Pro/pulls?state=open&sort=updated&direction=desc&per_page=1
```

### Método 4: Git Command Line
Ver ramas remotas que podrían estar asociadas con PRs:

```bash
git fetch --all
git branch -r
```

## Información del Repositorio
- **Repositorio:** Melampe001/Tokyo-Predictor-Roulette-Pro
- **URL:** https://github.com/Melampe001/Tokyo-Predictor-Roulette-Pro

## Notas
Este documento proporciona métodos para consultar los pull requests abiertos del repositorio. Para información en tiempo real, siempre usa la interfaz web de GitHub o las herramientas de línea de comandos.
