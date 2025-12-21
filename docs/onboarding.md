# Onboarding - Tokyo-Predictor-Roulette-Pro

## Bienvenida / Welcome

Este documento proporciona información esencial para nuevos colaboradores del proyecto.

This document provides essential information for new project collaborators.

---

## Estructura del Proyecto / Project Structure

```
Tokyo-Predictor-Roulette-Pro/
├── .github/           # Configuración de GitHub Actions y workflows
├── docs/              # Documentación del proyecto
├── scripts/           # Scripts de automatización y utilidades
├── .gitignore         # Archivos excluidos del control de versiones
└── README.md          # Información principal del proyecto
```

---

## Automatización de Limpieza Multi-Repositorio / Multi-Repository Cleanup Automation

### 📋 Descripción / Description

El script `scripts/clean-multi-repo.sh` permite buscar y limpiar archivos basura, temporales y sensibles en múltiples repositorios locales de manera centralizada.

The `scripts/clean-multi-repo.sh` script allows you to search for and clean junk, temporary, and sensitive files across multiple local repositories in a centralized way.

### 🚀 Uso Básico / Basic Usage

1. **Configurar rutas de repositorios / Configure repository paths**

   Edita el script y modifica el array `REPO_PATHS`:
   
   Edit the script and modify the `REPO_PATHS` array:

   ```bash
   REPO_PATHS=(
       "/home/usuario/proyectos/Tokyo-Predictor-Roulette-Pro"
       "/home/usuario/proyectos/otro-repo"
       "/home/usuario/proyectos/repo-adicional"
   )
   ```

2. **Ejecutar en modo de solo lectura (por defecto) / Run in read-only mode (default)**

   ```bash
   ./scripts/clean-multi-repo.sh
   ```

   Este modo **solo muestra** los archivos encontrados, **no elimina nada**.
   
   This mode **only shows** the files found, **does not delete anything**.

3. **Activar limpieza automática / Enable automatic cleanup**

   Para activar la eliminación automática, edita el script y descomenta la línea:
   
   To enable automatic deletion, edit the script and uncomment the line:

   ```bash
   # AUTO_CLEANUP=true  # ← Descomentar esta línea / Uncomment this line
   ```

   ⚠️ **ADVERTENCIA / WARNING**: Revisa siempre la lista de archivos antes de activar la limpieza automática.
   
   Always review the file list before enabling automatic cleanup.

### 📝 Flujo Recomendado / Recommended Workflow

1. **Primera ejecución / First run**
   - Ejecuta el script en modo solo lectura
   - Revisa la lista de archivos y directorios detectados
   - Verifica que no haya archivos importantes en la lista

2. **Configuración personalizada / Custom configuration**
   - Edita los arrays `JUNK_PATTERNS`, `TEMP_DIR_PATTERNS` y `SENSITIVE_PATTERNS`
   - Agrega o elimina patrones según tus necesidades
   - Vuelve a ejecutar para validar los cambios

3. **Activación de limpieza / Enable cleanup**
   - Una vez validado, activa `AUTO_CLEANUP=true`
   - Ejecuta el script para limpiar los archivos
   - Revisa el resumen final

### 🔄 Integración con Cronjob / Cronjob Integration

Para ejecutar la limpieza automáticamente de forma periódica:

To run the cleanup automatically on a periodic basis:

```bash
# Editar crontab / Edit crontab
crontab -e

# Agregar línea para ejecutar cada domingo a las 2am
# Add line to run every Sunday at 2am
0 2 * * 0 /ruta/completa/a/Tokyo-Predictor-Roulette-Pro/scripts/clean-multi-repo.sh >> /var/log/cleanup-multi-repo.log 2>&1
```

**Ejemplos de programación / Scheduling examples:**
- `0 2 * * 0` - Cada domingo a las 2am / Every Sunday at 2am
- `0 3 * * 1` - Cada lunes a las 3am / Every Monday at 3am
- `0 1 1 * *` - El primer día de cada mes a la 1am / First day of each month at 1am
- `0 0 * * *` - Todos los días a medianoche / Every day at midnight

### 🛡️ Seguridad / Security

El script **nunca** elimina automáticamente archivos sensibles detectados (`.env`, `*.key`, `*.pem`, etc.). Estos siempre requieren revisión manual.

The script **never** automatically deletes detected sensitive files (`.env`, `*.key`, `*.pem`, etc.). These always require manual review.

### 📊 Tipos de Archivos Detectados / Types of Files Detected

| Categoría / Category | Ejemplos / Examples | Limpieza Auto / Auto Cleanup |
|----------------------|---------------------|------------------------------|
| Archivos basura / Junk files | `*.tmp`, `*.bak`, `*.log` | ✅ Si está activado / If enabled |
| Directorios temporales / Temp dirs | `node_modules`, `__pycache__`, `dist` | ✅ Si está activado / If enabled |
| Archivos sensibles / Sensitive files | `*.key`, `.env`, `credentials.json` | ❌ Nunca / Never |

---

## .gitignore Institucional / Institutional .gitignore

El archivo `.gitignore` en la raíz del proyecto excluye automáticamente:

The `.gitignore` file at the project root automatically excludes:

- 📦 Backups y archivos temporales / Backups and temporary files
- 📝 Logs y registros / Logs and records
- 🏗️ Archivos compilados y binarios / Compiled files and binaries
- 📂 Directorios de distribución (`dist/`, `build/`) / Distribution directories
- 🔗 Dependencias (`node_modules/`, `vendor/`) / Dependencies
- 🐍 Entornos virtuales Python / Python virtual environments
- 🔐 Archivos sensibles y secretos / Sensitive files and secrets
- 💻 Configuraciones de IDEs / IDE configurations
- 🖥️ Archivos del sistema operativo / Operating system files

---

## Recursos Adicionales / Additional Resources

- **GitHub Repository**: https://github.com/Melampe001/Tokyo-Predictor-Roulette-Pro
- **Pull Requests**: [PULL_REQUESTS.md](../PULL_REQUESTS.md)
- **README Principal**: [README.md](../README.md)

---

## Soporte / Support

Para preguntas o problemas, abre un issue en el repositorio o contacta al equipo de desarrollo.

For questions or issues, open an issue in the repository or contact the development team.
