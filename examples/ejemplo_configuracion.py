"""
Ejemplo de Configuración: Carga desde archivo
Tokyo-Predictor-Roulette-Pro

Demuestra cómo cargar la configuración desde un archivo JSON.
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from session_manager import SessionManager, SessionConfig


def ejemplo_configuracion():
    """
    Ejemplo de carga de configuración desde archivo.
    """
    print("=" * 60)
    print("Ejemplo: Configuración desde Archivo")
    print("=" * 60)
    
    # Ruta al archivo de configuración
    config_path = Path(__file__).parent.parent / "config" / "session_config.json"
    
    print(f"\n1. Cargando configuración desde: {config_path}")
    
    try:
        # Cargar configuración desde archivo
        config = SessionConfig.from_file(str(config_path))
        print("   ✓ Configuración cargada correctamente")
        
        # Mostrar configuración
        print("\n2. Parámetros de configuración:")
        print(f"   - Timeout de inactividad: {config.inactive_timeout}s ({config.inactive_timeout/60:.1f} min)")
        print(f"   - Intervalo de limpieza: {config.cleanup_interval}s ({config.cleanup_interval/60:.1f} min)")
        print(f"   - Máx sesiones por usuario: {config.max_sessions_per_user}")
        print(f"   - Limpieza automática: {'Habilitada' if config.enable_auto_cleanup else 'Deshabilitada'}")
        
        # Crear gestor con la configuración cargada
        print("\n3. Creando gestor con configuración del archivo...")
        manager = SessionManager(config)
        
        # Crear algunas sesiones de prueba
        print("\n4. Creando sesiones de prueba...")
        for i in range(3):
            session = manager.create_session(f"test_user_{i}")
            print(f"   ✓ Sesión creada: {session.session_id}")
        
        # Mostrar estadísticas
        print("\n5. Estadísticas:")
        stats = manager.get_stats()
        for key, value in stats.items():
            if key != "config":
                print(f"   - {key}: {value}")
        
        # Cerrar gestor
        manager.shutdown()
        print("\n✓ Gestor cerrado")
        
        # Ejemplo de modificación y guardado de configuración
        print("\n6. Modificando y guardando configuración...")
        config.inactive_timeout = 3600  # 1 hora
        config.cleanup_interval = 600    # 10 minutos
        
        new_config_path = Path(__file__).parent.parent / "config" / "session_config_custom.json"
        config.save_to_file(str(new_config_path))
        print(f"   ✓ Nueva configuración guardada en: {new_config_path}")
        
    except FileNotFoundError as e:
        print(f"   ✗ Error: {e}")
        print("   Asegúrate de que el archivo de configuración existe.")
    except Exception as e:
        print(f"   ✗ Error inesperado: {e}")
    
    print("\n" + "=" * 60)
    print("Ejemplo completado")
    print("=" * 60)


if __name__ == "__main__":
    ejemplo_configuracion()
