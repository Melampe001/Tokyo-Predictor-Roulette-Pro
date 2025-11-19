"""
Tests Unitarios para el Sistema de Gestión de Sesiones
Tokyo-Predictor-Roulette-Pro
"""

import unittest
import time
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from session_manager import Session, SessionManager, SessionConfig


class TestSession(unittest.TestCase):
    """Tests para la clase Session"""
    
    def test_crear_sesion(self):
        """Verifica que una sesión se crea correctamente"""
        session = Session("usuario_test")
        self.assertIsNotNone(session.session_id)
        self.assertEqual(session.user_id, "usuario_test")
        self.assertTrue(session.is_active)
    
    def test_actualizar_actividad(self):
        """Verifica que la actividad se actualiza"""
        session = Session("usuario_test")
        tiempo_inicial = session.last_activity
        time.sleep(0.1)
        session.update_activity()
        self.assertGreater(session.last_activity, tiempo_inicial)
    
    def test_detectar_inactividad(self):
        """Verifica la detección de inactividad"""
        session = Session("usuario_test")
        time.sleep(2)
        self.assertTrue(session.is_inactive_for(1))
        self.assertFalse(session.is_inactive_for(5))
    
    def test_almacenar_datos(self):
        """Verifica el almacenamiento de datos en sesión"""
        session = Session("usuario_test")
        session.set_data("clave", "valor")
        self.assertEqual(session.get_data("clave"), "valor")
        self.assertIsNone(session.get_data("no_existe"))
    
    def test_terminar_sesion(self):
        """Verifica la terminación de sesión"""
        session = Session("usuario_test")
        session.terminate()
        self.assertFalse(session.is_active)
    
    def test_to_dict(self):
        """Verifica la serialización a diccionario"""
        session = Session("usuario_test", data={"test": "data"})
        session_dict = session.to_dict()
        self.assertEqual(session_dict["user_id"], "usuario_test")
        self.assertIn("session_id", session_dict)
        self.assertIn("test", session_dict["data"])


class TestSessionConfig(unittest.TestCase):
    """Tests para la clase SessionConfig"""
    
    def test_valores_por_defecto(self):
        """Verifica que se usan valores por defecto"""
        config = SessionConfig()
        self.assertEqual(config.inactive_timeout, SessionConfig.DEFAULT_INACTIVE_TIMEOUT)
        self.assertEqual(config.cleanup_interval, SessionConfig.DEFAULT_CLEANUP_INTERVAL)
    
    def test_valores_personalizados(self):
        """Verifica valores personalizados"""
        config = SessionConfig(inactive_timeout=100, cleanup_interval=50)
        self.assertEqual(config.inactive_timeout, 100)
        self.assertEqual(config.cleanup_interval, 50)
    
    def test_to_dict(self):
        """Verifica la conversión a diccionario"""
        config = SessionConfig()
        config_dict = config.to_dict()
        self.assertIn("inactive_timeout", config_dict)
        self.assertIn("cleanup_interval", config_dict)


class TestSessionManager(unittest.TestCase):
    """Tests para la clase SessionManager"""
    
    def setUp(self):
        """Configuración antes de cada test"""
        self.config = SessionConfig(
            inactive_timeout=5,
            cleanup_interval=2,
            max_sessions_per_user=3,
            enable_auto_cleanup=False
        )
        self.manager = SessionManager(self.config)
    
    def tearDown(self):
        """Limpieza después de cada test"""
        self.manager.shutdown()
    
    def test_crear_sesion(self):
        """Verifica la creación de sesiones"""
        session = self.manager.create_session("usuario1")
        self.assertIsNotNone(session)
        self.assertEqual(session.user_id, "usuario1")
    
    def test_recuperar_sesion(self):
        """Verifica la recuperación de sesiones"""
        session = self.manager.create_session("usuario1")
        recuperada = self.manager.get_session(session.session_id)
        self.assertEqual(session.session_id, recuperada.session_id)
    
    def test_sesiones_por_usuario(self):
        """Verifica obtener sesiones por usuario"""
        self.manager.create_session("usuario1")
        self.manager.create_session("usuario1")
        sesiones = self.manager.get_user_sessions("usuario1")
        self.assertEqual(len(sesiones), 2)
    
    def test_limite_sesiones_por_usuario(self):
        """Verifica el límite de sesiones por usuario"""
        # Crear más sesiones que el límite
        for i in range(5):
            self.manager.create_session("usuario1")
        
        sesiones = self.manager.get_user_sessions("usuario1")
        self.assertLessEqual(len(sesiones), self.config.max_sessions_per_user)
    
    def test_terminar_sesion(self):
        """Verifica la terminación de sesiones"""
        session = self.manager.create_session("usuario1")
        resultado = self.manager.terminate_session(session.session_id)
        self.assertTrue(resultado)
        
        recuperada = self.manager.get_session(session.session_id)
        self.assertIsNone(recuperada)
    
    def test_terminar_sesiones_usuario(self):
        """Verifica la terminación de todas las sesiones de un usuario"""
        self.manager.create_session("usuario1")
        self.manager.create_session("usuario1")
        self.manager.create_session("usuario2")
        
        count = self.manager.terminate_user_sessions("usuario1")
        self.assertEqual(count, 2)
        
        sesiones = self.manager.get_user_sessions("usuario1")
        self.assertEqual(len(sesiones), 0)
    
    def test_limpieza_inactivas(self):
        """Verifica la limpieza de sesiones inactivas"""
        # Crear sesiones
        session1 = self.manager.create_session("usuario1")
        session2 = self.manager.create_session("usuario2")
        
        # Esperar a que expiren
        time.sleep(6)
        
        # Mantener una activa
        self.manager.update_session_activity(session2.session_id)
        
        # Limpiar
        terminadas = self.manager.cleanup_inactive_sessions()
        
        # Verificar que solo se terminó session1
        self.assertGreater(terminadas, 0)
        self.assertIsNone(self.manager.get_session(session1.session_id))
        self.assertIsNotNone(self.manager.get_session(session2.session_id))
    
    def test_estadisticas(self):
        """Verifica las estadísticas del gestor"""
        self.manager.create_session("usuario1")
        self.manager.create_session("usuario2")
        
        stats = self.manager.get_stats()
        self.assertEqual(stats["total_active_sessions"], 2)
        self.assertEqual(stats["unique_users"], 2)
    
    def test_callback_terminacion(self):
        """Verifica que los callbacks se ejecutan"""
        callback_ejecutado = []
        
        def callback(session):
            callback_ejecutado.append(session.session_id)
        
        self.manager.register_termination_callback(callback)
        
        session = self.manager.create_session("usuario1")
        self.manager.terminate_session(session.session_id)
        
        self.assertIn(session.session_id, callback_ejecutado)
    
    def test_context_manager(self):
        """Verifica el uso como context manager"""
        with SessionManager(self.config) as manager:
            session = manager.create_session("usuario1")
            self.assertIsNotNone(session)
        
        # El manager debe estar cerrado después del context


class TestIntegracion(unittest.TestCase):
    """Tests de integración del sistema completo"""
    
    def test_flujo_completo(self):
        """Test de flujo completo del sistema"""
        config = SessionConfig(
            inactive_timeout=3,
            cleanup_interval=1,
            max_sessions_per_user=2,
            enable_auto_cleanup=True
        )
        
        with SessionManager(config) as manager:
            # Crear sesiones
            s1 = manager.create_session("alice", {"rol": "admin"})
            s2 = manager.create_session("bob", {"rol": "user"})
            
            # Verificar creación
            self.assertEqual(len(manager.get_all_sessions()), 2)
            
            # Actividad en una sesión
            s1.set_data("accion", "apuesta")
            
            # Esperar limpieza automática
            time.sleep(5)
            
            # Actualizar actividad de alice
            manager.update_session_activity(s1.session_id)
            
            # Esperar más
            time.sleep(2)
            
            # Bob debería estar terminado, alice no
            self.assertIsNotNone(manager.get_session(s1.session_id))


def ejecutar_tests():
    """Ejecuta todos los tests"""
    print("=" * 60)
    print("Ejecutando Tests del Sistema de Gestión de Sesiones")
    print("=" * 60)
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestSession))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionManager))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracion))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Éxitos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    exitcode = 0 if ejecutar_tests() else 1
    sys.exit(exitcode)
