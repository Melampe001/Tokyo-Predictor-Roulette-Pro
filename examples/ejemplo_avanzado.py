"""
Ejemplo Avanzado: Limpieza Automática y Callbacks
Tokyo-Predictor-Roulette-Pro

Este ejemplo demuestra características avanzadas como limpieza automática
y callbacks de terminación de sesiones.
"""

import sys
import time
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from session_manager import SessionManager, SessionConfig, Session


def on_session_terminated(session: Session):
    """
    Callback que se ejecuta cuando una sesión es terminada.
    
    Args:
        session: La sesión que fue terminada
    """
    print(f"\n   [CALLBACK] Sesión terminada: {session.session_id}")
    print(f"              Usuario: {session.user_id}")
    print(f"              Duración total: {(session.last_activity - session.created_at).total_seconds():.1f}s")
    
    # Aquí podrías:
    # - Guardar estadísticas de la sesión
    # - Notificar al usuario
    # - Limpiar recursos externos (conexiones BD, cache, etc.)
    # - Registrar en logs de auditoría


def ejemplo_avanzado():
    """
    Ejemplo avanzado con limpieza automática y callbacks.
    """
    print("=" * 60)
    print("Ejemplo Avanzado: Limpieza Automática y Callbacks")
    print("=" * 60)
    
    # Configuración con limpieza automática habilitada
    config = SessionConfig(
        inactive_timeout=15,  # 15 segundos
        cleanup_interval=8,   # Revisar cada 8 segundos
        max_sessions_per_user=3,
        enable_auto_cleanup=True
    )
    
    # Usar context manager para asegurar limpieza
    with SessionManager(config) as manager:
        
        # Registrar callback de terminación
        manager.register_termination_callback(on_session_terminated)
        print("\n✓ Callback de terminación registrado")
        
        # Crear múltiples sesiones
        print("\n1. Creando sesiones para múltiples usuarios...")
        users = ["alice", "bob", "charlie", "diana"]
        sessions = []
        
        for user in users:
            session = manager.create_session(
                user,
                {"tipo": "premium", "timestamp_login": time.time()}
            )
            sessions.append(session)
            print(f"   ✓ Sesión creada para {user}: {session.session_id}")
        
        # Crear sesión adicional para un usuario
        extra_session = manager.create_session("alice", {"dispositivo": "tablet"})
        print(f"   ✓ Segunda sesión para alice: {extra_session.session_id}")
        
        # Mostrar sesiones por usuario
        print("\n2. Sesiones por usuario:")
        for user in set(users):
            user_sessions = manager.get_user_sessions(user)
            print(f"   - {user}: {len(user_sessions)} sesión(es)")
        
        # Simular actividad en algunas sesiones
        print("\n3. Simulando actividad...")
        time.sleep(5)
        
        # Alice mantiene actividad
        for session in manager.get_user_sessions("alice"):
            session.set_data("ultima_accion", "apuesta realizada")
            print(f"   ✓ Actividad registrada para sesión de alice")
        
        # Bob mantiene actividad
        bob_sessions = manager.get_user_sessions("bob")
        if bob_sessions:
            bob_sessions[0].update_activity()
            print(f"   ✓ Actividad registrada para sesión de bob")
        
        # Esperar a que expire el timeout de algunas sesiones
        print(f"\n4. Esperando limpieza automática (timeout: {config.inactive_timeout}s)...")
        print("   La limpieza automática se ejecutará automáticamente...")
        
        # Monitorear durante 25 segundos
        for i in range(5):
            time.sleep(5)
            stats = manager.get_stats()
            print(f"\n   T+{(i+1)*5}s - Sesiones activas: {stats['total_active_sessions']}")
            
            if i == 1:  # Después de 10 segundos, mantener actividad en alice
                for session in manager.get_user_sessions("alice"):
                    session.update_activity()
                    print("   ✓ Alice mantiene su sesión activa")
        
        # Estadísticas finales
        print("\n5. Estadísticas finales:")
        stats = manager.get_stats()
        print(f"   - Sesiones activas: {stats['total_active_sessions']}")
        print(f"   - Usuarios únicos: {stats['unique_users']}")
        print(f"   - Limpieza automática activa: {stats['auto_cleanup_running']}")
        
        # Listar sesiones restantes
        print("\n6. Sesiones que sobrevivieron:")
        for session in manager.get_all_sessions():
            duration = session.get_inactive_duration().total_seconds()
            print(f"   - Usuario {session.user_id}")
            print(f"     ID: {session.session_id}")
            print(f"     Inactivo por: {duration:.1f}s")
        
        # Terminar manualmente sesiones de un usuario
        print("\n7. Terminando manualmente sesiones de alice...")
        terminated = manager.terminate_user_sessions("alice")
        print(f"   ✓ {terminated} sesión(es) terminada(s)")
    
    # Al salir del context manager, se llama automáticamente a shutdown()
    print("\n" + "=" * 60)
    print("Ejemplo completado (gestor cerrado automáticamente)")
    print("=" * 60)


if __name__ == "__main__":
    ejemplo_avanzado()
