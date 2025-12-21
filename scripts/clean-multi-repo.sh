#!/bin/bash
set -euo pipefail

################################################################################
# Script de Limpieza Multi-Repositorio / Multi-Repository Cleanup Script
# Organización / Organization: Melampe001
# Repositorio / Repository: Tokyo-Predictor-Roulette-Pro
#
# Descripción / Description:
#   Busca archivos basura, temporales y sensibles en múltiples repositorios
#   locales. Muestra coincidencias por defecto. Puede activarse limpieza
#   automática descomentando la línea indicada.
#
#   Searches for junk, temporary and sensitive files across multiple local
#   repositories. Shows matches by default. Automatic cleanup can be enabled
#   by uncommenting the indicated line.
#
# Uso / Usage:
#   ./scripts/clean-multi-repo.sh
#
# Configuración / Configuration:
#   Editar la lista REPO_PATHS con las rutas absolutas de los repositorios.
#   Edit the REPO_PATHS list with absolute paths to your repositories.
################################################################################

# =============================================================================
# CONFIGURACIÓN / CONFIGURATION
# =============================================================================

# Lista de rutas a repositorios locales (editar según necesidad)
# List of local repository paths (edit as needed)
REPO_PATHS=(
    # Ejemplo / Example: "/home/usuario/proyectos/repo1"
    # Ejemplo / Example: "/home/usuario/proyectos/repo2"
    # Ejemplo / Example: "/home/usuario/proyectos/repo3"
)

# Patrones de archivos a buscar / File patterns to search for
JUNK_PATTERNS=(
    "*.tmp"
    "*.temp"
    "*.bak"
    "*.backup"
    "*.old"
    "*.orig"
    "*.swp"
    "*.swo"
    "*~"
    "*.log"
    "*.cache"
    "Thumbs.db"
    ".DS_Store"
    "desktop.ini"
)

# Patrones de directorios temporales / Temporary directory patterns
TEMP_DIR_PATTERNS=(
    "node_modules"
    "__pycache__"
    ".pytest_cache"
    "*.egg-info"
    "dist"
    "build"
    ".venv"
    "venv"
    "env"
    ".tox"
    ".coverage"
    "htmlcov"
)

# Archivos sensibles a detectar (¡NO BORRAR sin revisar!)
# Sensitive files to detect (DO NOT DELETE without review!)
SENSITIVE_PATTERNS=(
    "*.key"
    "*.pem"
    "*.p12"
    "*.pfx"
    ".env"
    ".env.local"
    "secrets.yml"
    "secrets.yaml"
    "credentials.json"
    "*.credentials"
)

# Modo de limpieza automática (cambiar a "true" para activar)
# Automatic cleanup mode (change to "true" to enable)
AUTO_CLEANUP=false
# DESCOMENTAR LA SIGUIENTE LÍNEA PARA ACTIVAR LIMPIEZA AUTOMÁTICA
# UNCOMMENT THE FOLLOWING LINE TO ENABLE AUTOMATIC CLEANUP
# AUTO_CLEANUP=true

# =============================================================================
# FUNCIONES / FUNCTIONS
# =============================================================================

print_header() {
    echo "======================================================================"
    echo "  Limpieza Multi-Repositorio / Multi-Repository Cleanup"
    echo "  Melampe001 - Tokyo-Predictor-Roulette-Pro"
    echo "======================================================================"
    echo ""
}

print_section() {
    echo ""
    echo "----------------------------------------------------------------------"
    echo "  $1"
    echo "----------------------------------------------------------------------"
}

check_repo_paths() {
    if [ ${#REPO_PATHS[@]} -eq 0 ]; then
        echo "⚠️  ADVERTENCIA / WARNING:"
        echo "    No hay rutas de repositorios configuradas."
        echo "    No repository paths configured."
        echo ""
        echo "    Edita este script y agrega rutas en el array REPO_PATHS."
        echo "    Edit this script and add paths to the REPO_PATHS array."
        echo ""
        exit 1
    fi
    
    echo "📁 Repositorios configurados / Configured repositories:"
    for repo_path in "${REPO_PATHS[@]}"; do
        if [ -d "$repo_path" ]; then
            echo "   ✓ $repo_path"
        else
            echo "   ✗ $repo_path (no existe / does not exist)"
        fi
    done
    echo ""
}

scan_junk_files() {
    print_section "1. Archivos basura y temporales / Junk and temporary files"
    
    local found_count=0
    
    for repo_path in "${REPO_PATHS[@]}"; do
        if [ ! -d "$repo_path" ]; then
            continue
        fi
        
        echo "Escaneando / Scanning: $repo_path"
        
        for pattern in "${JUNK_PATTERNS[@]}"; do
            while IFS= read -r -d '' file; do
                echo "  🗑️  $file"
                found_count=$((found_count + 1))
                
                if [ "$AUTO_CLEANUP" = true ]; then
                    rm -f "$file"
                    echo "     → Eliminado / Deleted"
                fi
            done < <(find "$repo_path" -type f -name "$pattern" -print0 2>/dev/null)
        done
    done
    
    if [ $found_count -eq 0 ]; then
        echo "  ✓ No se encontraron archivos basura / No junk files found"
    else
        echo ""
        echo "  Total encontrados / Total found: $found_count"
        if [ "$AUTO_CLEANUP" = false ]; then
            echo "  ℹ️  Modo solo lectura / Read-only mode (no se eliminó nada / nothing deleted)"
        fi
    fi
}

scan_temp_directories() {
    print_section "2. Directorios temporales / Temporary directories"
    
    local found_count=0
    
    for repo_path in "${REPO_PATHS[@]}"; do
        if [ ! -d "$repo_path" ]; then
            continue
        fi
        
        echo "Escaneando / Scanning: $repo_path"
        
        for pattern in "${TEMP_DIR_PATTERNS[@]}"; do
            while IFS= read -r -d '' dir; do
                echo "  📂 $dir"
                found_count=$((found_count + 1))
                
                if [ "$AUTO_CLEANUP" = true ]; then
                    rm -rf "$dir"
                    echo "     → Eliminado / Deleted"
                fi
            done < <(find "$repo_path" -type d -name "$pattern" -print0 2>/dev/null)
        done
    done
    
    if [ $found_count -eq 0 ]; then
        echo "  ✓ No se encontraron directorios temporales / No temporary directories found"
    else
        echo ""
        echo "  Total encontrados / Total found: $found_count"
        if [ "$AUTO_CLEANUP" = false ]; then
            echo "  ℹ️  Modo solo lectura / Read-only mode (no se eliminó nada / nothing deleted)"
        fi
    fi
}

scan_sensitive_files() {
    print_section "3. Archivos sensibles detectados / Sensitive files detected"
    
    local found_count=0
    
    for repo_path in "${REPO_PATHS[@]}"; do
        if [ ! -d "$repo_path" ]; then
            continue
        fi
        
        echo "Escaneando / Scanning: $repo_path"
        
        for pattern in "${SENSITIVE_PATTERNS[@]}"; do
            while IFS= read -r -d '' file; do
                echo "  🔐 $file"
                found_count=$((found_count + 1))
            done < <(find "$repo_path" -type f -name "$pattern" -print0 2>/dev/null)
        done
    done
    
    if [ $found_count -eq 0 ]; then
        echo "  ✓ No se encontraron archivos sensibles / No sensitive files found"
    else
        echo ""
        echo "  Total encontrados / Total found: $found_count"
        echo "  ⚠️  ADVERTENCIA / WARNING: Revisar manualmente estos archivos"
        echo "      Manually review these files before deletion"
        echo "      Este script NUNCA eliminará archivos sensibles automáticamente"
        echo "      This script will NEVER automatically delete sensitive files"
    fi
}

print_summary() {
    print_section "Resumen / Summary"
    
    if [ "$AUTO_CLEANUP" = true ]; then
        echo "✅ Limpieza automática ACTIVADA / Automatic cleanup ENABLED"
        echo "   Los archivos basura y directorios temporales fueron eliminados."
        echo "   Junk files and temporary directories were deleted."
    else
        echo "ℹ️  Limpieza automática DESACTIVADA / Automatic cleanup DISABLED"
        echo "   Solo se mostraron coincidencias, no se eliminó nada."
        echo "   Only matches were shown, nothing was deleted."
        echo ""
        echo "   Para activar limpieza automática:"
        echo "   To enable automatic cleanup:"
        echo "   1. Edita este script / Edit this script"
        echo "   2. Descomenta: AUTO_CLEANUP=true / Uncomment: AUTO_CLEANUP=true"
        echo "   3. O cambia la línea existente / Or change the existing line"
    fi
    
    echo ""
    echo "💡 Tip: Configura un cronjob para ejecución periódica"
    echo "    Tip: Set up a cronjob for periodic execution"
    echo "    Ejemplo / Example: 0 2 * * 0 /ruta/a/clean-multi-repo.sh"
    echo "    (Cada domingo a las 2am / Every Sunday at 2am)"
}

# =============================================================================
# PROGRAMA PRINCIPAL / MAIN PROGRAM
# =============================================================================

main() {
    print_header
    check_repo_paths
    scan_junk_files
    scan_temp_directories
    scan_sensitive_files
    print_summary
    
    echo ""
    echo "======================================================================"
    echo "✅ Escaneo completado / Scan completed"
    echo "======================================================================"
}

# Ejecutar programa principal / Run main program
main
