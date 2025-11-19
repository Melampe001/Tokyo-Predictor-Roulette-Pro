"""
Módulo del Gestor de Sesiones
Gestiona múltiples sesiones con limpieza automática de sesiones inactivas.
"""

import threading
import time
import logging
from typing import Dict, List, Optional, Callable
from datetime import datetime

from .session import Session
from .config import SessionConfig


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SessionManager:
    """
    Gestor centralizado de sesiones con terminación automática de sesiones inactivas.
    
    Esta clase gestiona el ciclo de vida completo de las sesiones de usuarios,
    incluyendo creación, seguimiento de actividad, y terminación automática
    de sesiones inactivas.
    
    Attributes:
        config (SessionConfig): Configuración del gestor
        sessions (Dict[str, Session]): Diccionario de sesiones activas
        cleanup_thread (threading.Thread): Hilo de limpieza automática
    """
    
    def __init__(self, config: Optional[SessionConfig] = None):
        """
        Inicializa el gestor de sesiones.
        
        Args:
            config: Configuración personalizada (opcional)
        """
        self.config = config or SessionConfig()
        self.sessions: Dict[str, Session] = {}
        self._lock = threading.Lock()
        self._cleanup_thread: Optional[threading.Thread] = None
        self._stop_cleanup = threading.Event()
        self._session_terminated_callbacks: List[Callable[[Session], None]] = []
        
        logger.info(f"SessionManager inicializado con configuración: {self.config}")
        
        if self.config.enable_auto_cleanup:
            self.start_auto_cleanup()
    
    def create_session(self, user_id: str, session_data: Optional[Dict] = None) -> Session:
        """
        Crea una nueva sesión para un usuario.
        
        Args:
            user_id: Identificador del usuario
            session_data: Datos iniciales de la sesión (opcional)
            
        Returns:
            La sesión creada
            
        Raises:
            ValueError: Si el usuario ha alcanzado el máximo de sesiones permitidas
        """
        with self._lock:
            # Verificar límite de sesiones por usuario (sin lock anidado)
            user_sessions = [
                session for session in self.sessions.values()
                if session.user_id == user_id and session.is_active
            ]
            if len(user_sessions) >= self.config.max_sessions_per_user:
                logger.warning(
                    f"Usuario {user_id} ha alcanzado el máximo de sesiones ({self.config.max_sessions_per_user})"
                )
                # Terminar la sesión más antigua
                oldest_session = min(user_sessions, key=lambda s: s.created_at)
                # Terminar sin llamar a terminate_session para evitar lock anidado
                oldest_session.terminate()
                logger.info(f"Sesión terminada: {oldest_session.session_id} (usuario: {oldest_session.user_id})")
                for callback in self._session_terminated_callbacks:
                    try:
                        callback(oldest_session)
                    except Exception as e:
                        logger.error(f"Error en callback de terminación: {e}")
                del self.sessions[oldest_session.session_id]
            
            session = Session(user_id=user_id, data=session_data)
            self.sessions[session.session_id] = session
            
            logger.info(f"Sesión creada: {session.session_id} para usuario {user_id}")
            return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """
        Recupera una sesión por su ID.
        
        Args:
            session_id: ID de la sesión a recuperar
            
        Returns:
            La sesión si existe y está activa, None en caso contrario
        """
        with self._lock:
            session = self.sessions.get(session_id)
            if session and session.is_active:
                return session
            return None
    
    def get_user_sessions(self, user_id: str) -> List[Session]:
        """
        Obtiene todas las sesiones activas de un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Lista de sesiones activas del usuario
        """
        with self._lock:
            return [
                session for session in self.sessions.values()
                if session.user_id == user_id and session.is_active
            ]
    
    def update_session_activity(self, session_id: str) -> bool:
        """
        Actualiza la actividad de una sesión.
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            True si la sesión fue actualizada, False si no existe
        """
        session = self.get_session(session_id)
        if session:
            session.update_activity()
            logger.debug(f"Actividad actualizada para sesión {session_id}")
            return True
        return False
    
    def terminate_session(self, session_id: str) -> bool:
        """
        Termina una sesión específica y limpia sus recursos.
        
        Args:
            session_id: ID de la sesión a terminar
            
        Returns:
            True si la sesión fue terminada, False si no existe
        """
        with self._lock:
            session = self.sessions.get(session_id)
            if session:
                session.terminate()
                logger.info(f"Sesión terminada: {session_id} (usuario: {session.user_id})")
                
                # Ejecutar callbacks de terminación
                for callback in self._session_terminated_callbacks:
                    try:
                        callback(session)
                    except Exception as e:
                        logger.error(f"Error en callback de terminación: {e}")
                
                # Remover de la colección de sesiones activas
                del self.sessions[session_id]
                return True
            return False
    
    def terminate_user_sessions(self, user_id: str) -> int:
        """
        Termina todas las sesiones de un usuario.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Número de sesiones terminadas
        """
        user_sessions = self.get_user_sessions(user_id)
        count = 0
        for session in user_sessions:
            if self.terminate_session(session.session_id):
                count += 1
        
        logger.info(f"Terminadas {count} sesiones para usuario {user_id}")
        return count
    
    def cleanup_inactive_sessions(self) -> int:
        """
        Limpia todas las sesiones inactivas basándose en el timeout configurado.
        
        Returns:
            Número de sesiones terminadas
        """
        inactive_sessions = []
        
        with self._lock:
            for session in list(self.sessions.values()):
                if session.is_inactive_for(self.config.inactive_timeout):
                    inactive_sessions.append(session.session_id)
        
        # Terminar sesiones fuera del lock para evitar deadlocks
        count = 0
        for session_id in inactive_sessions:
            if self.terminate_session(session_id):
                count += 1
        
        if count > 0:
            logger.info(f"Limpieza automática: {count} sesiones inactivas terminadas")
        
        return count
    
    def start_auto_cleanup(self) -> None:
        """
        Inicia el hilo de limpieza automática de sesiones inactivas.
        """
        if self._cleanup_thread and self._cleanup_thread.is_alive():
            logger.warning("La limpieza automática ya está en ejecución")
            return
        
        self._stop_cleanup.clear()
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()
        logger.info(
            f"Limpieza automática iniciada (intervalo: {self.config.cleanup_interval}s, "
            f"timeout: {self.config.inactive_timeout}s)"
        )
    
    def stop_auto_cleanup(self) -> None:
        """
        Detiene el hilo de limpieza automática.
        """
        if self._cleanup_thread and self._cleanup_thread.is_alive():
            self._stop_cleanup.set()
            self._cleanup_thread.join(timeout=5)
            logger.info("Limpieza automática detenida")
    
    def _cleanup_loop(self) -> None:
        """
        Bucle principal del hilo de limpieza automática.
        """
        while not self._stop_cleanup.is_set():
            try:
                self.cleanup_inactive_sessions()
            except Exception as e:
                logger.error(f"Error en limpieza automática: {e}")
            
            # Esperar el intervalo de limpieza o hasta que se detenga
            self._stop_cleanup.wait(timeout=self.config.cleanup_interval)
    
    def register_termination_callback(self, callback: Callable[[Session], None]) -> None:
        """
        Registra una función callback que se ejecutará cuando una sesión sea terminada.
        
        Args:
            callback: Función que recibe una Session como parámetro
        """
        self._session_terminated_callbacks.append(callback)
        logger.debug(f"Callback de terminación registrado")
    
    def get_stats(self) -> Dict:
        """
        Obtiene estadísticas del gestor de sesiones.
        
        Returns:
            Diccionario con estadísticas de sesiones
        """
        with self._lock:
            total_sessions = len(self.sessions)
            users = set(s.user_id for s in self.sessions.values())
            
            inactive_soon = sum(
                1 for s in self.sessions.values()
                if s.get_inactive_duration().total_seconds() > self.config.inactive_timeout * 0.8
            )
            
            return {
                "total_active_sessions": total_sessions,
                "unique_users": len(users),
                "sessions_inactive_soon": inactive_soon,
                "config": self.config.to_dict(),
                "auto_cleanup_running": self._cleanup_thread.is_alive() if self._cleanup_thread else False
            }
    
    def get_all_sessions(self) -> List[Session]:
        """
        Obtiene todas las sesiones activas.
        
        Returns:
            Lista de todas las sesiones activas
        """
        with self._lock:
            return list(self.sessions.values())
    
    def shutdown(self) -> None:
        """
        Cierra el gestor de sesiones, terminando todas las sesiones y deteniendo la limpieza.
        """
        logger.info("Iniciando cierre del SessionManager...")
        
        self.stop_auto_cleanup()
        
        # Terminar todas las sesiones
        session_ids = list(self.sessions.keys())
        for session_id in session_ids:
            self.terminate_session(session_id)
        
        logger.info("SessionManager cerrado correctamente")
    
    def __enter__(self):
        """Soporte para context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Soporte para context manager."""
        self.shutdown()
