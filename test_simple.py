"""
Test Simple de Verificación
Valida que el sistema de gestión de sesiones funciona correctamente
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

print("Importando módulos...")
from session_manager import SessionManager, SessionConfig, Session

print("✓ Módulos importados correctamente")

# Test 1: Crear configuración
print("\nTest 1: Crear configuración")
config = SessionConfig(inactive_timeout=60, cleanup_interval=30)
print(f"✓ Configuración creada: timeout={config.inactive_timeout}s")

# Test 2: Crear gestor
print("\nTest 2: Crear gestor de sesiones")
manager = SessionManager(SessionConfig(enable_auto_cleanup=False))
print("✓ Gestor creado correctamente")

# Test 3: Crear sesión
print("\nTest 3: Crear sesión")
session = manager.create_session("test_user", {"test": "data"})
print(f"✓ Sesión creada: {session.session_id}")

# Test 4: Almacenar y recuperar datos
print("\nTest 4: Almacenar y recuperar datos")
session.set_data("key1", "value1")
value = session.get_data("key1")
assert value == "value1", "Error al recuperar datos"
print(f"✓ Datos almacenados y recuperados: {value}")

# Test 5: Recuperar sesión
print("\nTest 5: Recuperar sesión por ID")
recovered = manager.get_session(session.session_id)
assert recovered is not None, "Error al recuperar sesión"
print(f"✓ Sesión recuperada: {recovered.session_id}")

# Test 6: Estadísticas
print("\nTest 6: Obtener estadísticas")
stats = manager.get_stats()
print(f"✓ Sesiones activas: {stats['total_active_sessions']}")
print(f"✓ Usuarios únicos: {stats['unique_users']}")

# Test 7: Terminar sesión
print("\nTest 7: Terminar sesión")
result = manager.terminate_session(session.session_id)
assert result == True, "Error al terminar sesión"
print("✓ Sesión terminada correctamente")

# Test 8: Verificar que la sesión fue terminada
print("\nTest 8: Verificar terminación")
recovered = manager.get_session(session.session_id)
assert recovered is None, "La sesión debería estar terminada"
print("✓ Sesión confirmada como terminada")

# Cerrar gestor
print("\nCerrando gestor...")
manager.shutdown()
print("✓ Gestor cerrado")

print("\n" + "="*50)
print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
print("="*50)
print("\n🎉 El sistema de gestión de sesiones está funcionando correctamente!")
