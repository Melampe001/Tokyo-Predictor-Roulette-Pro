# Contribuir

Gracias por contribuir. Sigue estos pasos mínimos antes de cada commit o PR:

Requisitos locales
- Python 3.10+ recomendado
- (Opcional) Virtualenv: `python -m venv .venv && source .venv/bin/activate`
- Instala dependencias: `pip install -r requirements.txt` (si existe)

Antes de cada commit
- Ejecuta `make fmt` para formatear el código (usa black).
- Ejecuta `make test` para validar que los tests pasan.
- Ejecuta `make lint` para comprobar calidad estática (flake8).

Flujo de desarrollo
- Crear branch: `git checkout -b feature/mi-cambio`
- Formatear: `make fmt`
- Ejecutar tests: `make test`
- Abrir PR apuntando a `main` (o la rama base de tu proyecto)

CI local
- `make ci` ejecuta una secuencia básica: `fmt`, `lint`, `test`.

Protoc (si aplica)
- Si el repo incluye Protobufs en `proto/`, añade pasos en `make proto` para generar artefactos.

Ruby
- Si modificas contenido en `ruby/`, actualiza la versión semántica en:
  `ruby/lib/billing-platform/version.rb`

Ganchos (hooks)
- Para instalar pre-commit local:
  `cp scripts/pre-commit.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit`

Notas
- Sigue las guías de estilo de Python (PEP8) y escribe tests table-driven cuando aplique.
- Documenta cambios relevantes en `docs/` o README.
