"""
Guía de Inicio Rápido - Tokyo-Predictor-Roulette-Pro
Sistema de Gestión de Sesiones

Este script proporciona una demostración interactiva del sistema.
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from session_manager import SessionManager, SessionConfig


def quick_start():
    """Demostración rápida del sistema"""
    
    print("=" * 70)
    print("BIENVENIDO AL SISTEMA DE GESTIÓN DE SESIONES")
    print("Tokyo-Predictor-Roulette-Pro v1.0.0")
    print("=" * 70)
    
    print("\n📚 Esta es una guía de inicio rápido del sistema.")
    print("Para ejemplos completos, ejecuta los scripts en el directorio 'examples/'")
    
    # Crear gestor con configuración básica
    print("\n1️⃣  Creando gestor de sesiones con configuración por defecto...")
    config = SessionConfig(
        inactive_timeout=1800,  # 30 minutos
        cleanup_interval=300,   # 5 minutos
        max_sessions_per_user=5,
        enable_auto_cleanup=True
    )
    
    manager = SessionManager(config)
    print("   ✅ Gestor creado exitosamente")
    print(f"   ⏱️  Timeout de inactividad: {config.inactive_timeout} segundos")
    print(f"   🔄 Intervalo de limpieza: {config.cleanup_interval} segundos")
    
    # Crear sesión de ejemplo
    print("\n2️⃣  Creando sesión de ejemplo para usuario 'demo_user'...")
    session = manager.create_session("demo_user", {
        "nombre": "Usuario Demo",
        "rol": "jugador",
        "saldo_inicial": 1000
    })
    print(f"   ✅ Sesión creada con ID: {session.session_id}")
    
    # Almacenar datos en la sesión
    print("\n3️⃣  Almacenando datos en la sesión...")
    session.set_data("ultima_apuesta", 50)
    session.set_data("juego_actual", "Ruleta Tokyo")
    session.set_data("nivel", 5)
    print("   ✅ Datos almacenados correctamente")
    
    # Recuperar datos
    print("\n4️⃣  Recuperando datos de la sesión...")
    apuesta = session.get_data("ultima_apuesta")
    juego = session.get_data("juego_actual")
    print(f"   📊 Última apuesta: {apuesta}")
    print(f"   🎮 Juego actual: {juego}")
    
    # Mostrar estadísticas
    print("\n5️⃣  Estadísticas del sistema:")
    stats = manager.get_stats()
    print(f"   👥 Sesiones activas: {stats['total_active_sessions']}")
    print(f"   🔢 Usuarios únicos: {stats['unique_users']}")
    print(f"   🤖 Limpieza automática: {'Activa' if stats['auto_cleanup_running'] else 'Inactiva'}")
    
    # Información de la sesión
    print("\n6️⃣  Información completa de la sesión:")
    session_info = session.to_dict()
    print(f"   🆔 Session ID: {session_info['session_id']}")
    print(f"   👤 User ID: {session_info['user_id']}")
    print(f"   📅 Creada: {session_info['created_at']}")
    print(f"   ⏰ Última actividad: {session_info['last_activity']}")
    print(f"   ✅ Activa: {session_info['is_active']}")
    print(f"   💾 Datos guardados: {len(session_info['data'])} elementos")
    
    # Cerrar el gestor
    print("\n7️⃣  Cerrando el gestor de sesiones...")
    manager.shutdown()
    print("   ✅ Gestor cerrado correctamente")
    
    print("\n" + "=" * 70)
    print("🎉 DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)
    
    print("\n📖 PRÓXIMOS PASOS:")
    print("   1. Ejecuta: python examples/ejemplo_basico.py")
    print("   2. Ejecuta: python examples/ejemplo_avanzado.py")
    print("   3. Ejecuta: python examples/ejemplo_configuracion.py")
    print("   4. Lee la documentación completa en README.md")
    print("   5. Ejecuta los tests: python tests/test_session_manager.py")
    
    print("\n💡 CONSEJOS:")
    print("   • Ajusta el timeout según tus necesidades (config)")
    print("   • Usa callbacks para acciones personalizadas al terminar sesiones")
    print("   • Implementa logging para auditoría en producción")
    print("   • Considera persistir sesiones en BD para aplicaciones críticas")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    try:
        quick_start()
    except KeyboardInterrupt:
        print("\n\n❌ Ejecución cancelada por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
