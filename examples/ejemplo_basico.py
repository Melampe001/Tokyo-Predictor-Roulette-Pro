"""
Ejemplo Básico: Uso del Sistema de Gestión de Sesiones
Tokyo-Predictor-Roulette-Pro

Este ejemplo demuestra el uso básico del sistema de gestión de sesiones.
"""

import sys
import time
from pathlib import Path

# Agregar el directorio src al path para importar
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from session_manager import SessionManager, SessionConfig


def ejemplo_basico():
    """
    Ejemplo básico de creación y gestión de sesiones.
    """
    print("=" * 60)
    print("Ejemplo Básico: Gestión de Sesiones")
    print("=" * 60)
    
    # Crear configuración personalizada
    config = SessionConfig(
        inactive_timeout=10,  # 10 segundos para demostración
        cleanup_interval=5,    # 5 segundos
        max_sessions_per_user=3,
        enable_auto_cleanup=False  # Manual para este ejemplo
    )
    
    # Crear gestor de sesiones
    manager = SessionManager(config)
    
    # Crear sesiones para diferentes usuarios
    print("\n1. Creando sesiones...")
    session1 = manager.create_session("usuario_001", {"nombre": "Juan", "rol": "jugador"})
    print(f"   ✓ Sesión creada: {session1.session_id}")
    
    session2 = manager.create_session("usuario_002", {"nombre": "María", "rol": "admin"})
    print(f"   ✓ Sesión creada: {session2.session_id}")
    
    session3 = manager.create_session("usuario_001", {"nombre": "Juan", "dispositivo": "móvil"})
    print(f"   ✓ Sesión creada: {session3.session_id}")
    
    # Ver estadísticas
    print("\n2. Estadísticas iniciales:")
    stats = manager.get_stats()
    print(f"   - Sesiones activas: {stats['total_active_sessions']}")
    print(f"   - Usuarios únicos: {stats['unique_users']}")
    
    # Interactuar con sesiones
    print("\n3. Actualizando actividad...")
    session1.set_data("ultima_apuesta", 100)
    session1.set_data("saldo", 5000)
    print(f"   ✓ Datos guardados en sesión {session1.session_id}")
    
    # Recuperar datos
    saldo = session1.get_data("saldo")
    print(f"   ✓ Saldo recuperado: {saldo}")
    
    # Simular inactividad
    print("\n4. Simulando inactividad (esperando 12 segundos)...")
    time.sleep(12)
    
    # Actualizar actividad de session2
    session2.update_activity()
    print(f"   ✓ Actividad actualizada para sesión {session2.session_id}")
    
    # Limpiar sesiones inactivas
    print("\n5. Ejecutando limpieza de sesiones inactivas...")
    terminadas = manager.cleanup_inactive_sessions()
    print(f"   ✓ Sesiones terminadas: {terminadas}")
    
    # Estadísticas finales
    print("\n6. Estadísticas finales:")
    stats = manager.get_stats()
    print(f"   - Sesiones activas: {stats['total_active_sessions']}")
    print(f"   - Usuarios únicos: {stats['unique_users']}")
    
    # Listar sesiones activas
    print("\n7. Sesiones activas:")
    for session in manager.get_all_sessions():
        print(f"   - {session.session_id}: Usuario {session.user_id}")
        print(f"     Inactivo por: {session.get_inactive_duration().total_seconds():.1f}s")
    
    # Cerrar gestor
    print("\n8. Cerrando gestor de sesiones...")
    manager.shutdown()
    print("   ✓ Gestor cerrado correctamente")
    
    print("\n" + "=" * 60)
    print("Ejemplo completado")
    print("=" * 60)


if __name__ == "__main__":
    ejemplo_basico()
