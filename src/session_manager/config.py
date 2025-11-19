"""
Módulo de Configuración
Gestiona la configuración del sistema de sesiones.
"""

import json
from typing import Optional
from pathlib import Path


class SessionConfig:
    """
    Clase de configuración para el gestor de sesiones.
    
    Attributes:
        inactive_timeout: Tiempo en segundos antes de que una sesión inactiva sea terminada
        cleanup_interval: Intervalo en segundos para ejecutar la limpieza automática
        max_sessions_per_user: Número máximo de sesiones simultáneas por usuario
        enable_auto_cleanup: Habilita/deshabilita la limpieza automática
    """
    
    # Valores por defecto
    DEFAULT_INACTIVE_TIMEOUT = 1800  # 30 minutos
    DEFAULT_CLEANUP_INTERVAL = 300   # 5 minutos
    DEFAULT_MAX_SESSIONS_PER_USER = 5
    DEFAULT_ENABLE_AUTO_CLEANUP = True
    
    def __init__(
        self,
        inactive_timeout: Optional[int] = None,
        cleanup_interval: Optional[int] = None,
        max_sessions_per_user: Optional[int] = None,
        enable_auto_cleanup: Optional[bool] = None
    ):
        """
        Inicializa la configuración del gestor de sesiones.
        
        Args:
            inactive_timeout: Tiempo límite de inactividad en segundos
            cleanup_interval: Intervalo de limpieza en segundos
            max_sessions_per_user: Máximo de sesiones por usuario
            enable_auto_cleanup: Habilitar limpieza automática
        """
        self.inactive_timeout = inactive_timeout or self.DEFAULT_INACTIVE_TIMEOUT
        self.cleanup_interval = cleanup_interval or self.DEFAULT_CLEANUP_INTERVAL
        self.max_sessions_per_user = max_sessions_per_user or self.DEFAULT_MAX_SESSIONS_PER_USER
        self.enable_auto_cleanup = enable_auto_cleanup if enable_auto_cleanup is not None else self.DEFAULT_ENABLE_AUTO_CLEANUP
    
    @classmethod
    def from_file(cls, config_path: str) -> "SessionConfig":
        """
        Carga la configuración desde un archivo JSON.
        
        Args:
            config_path: Ruta al archivo de configuración
            
        Returns:
            Instancia de SessionConfig con la configuración cargada
        """
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {config_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        return cls(
            inactive_timeout=config_data.get('inactive_timeout'),
            cleanup_interval=config_data.get('cleanup_interval'),
            max_sessions_per_user=config_data.get('max_sessions_per_user'),
            enable_auto_cleanup=config_data.get('enable_auto_cleanup')
        )
    
    def to_dict(self) -> dict:
        """
        Convierte la configuración a un diccionario.
        
        Returns:
            Diccionario con los parámetros de configuración
        """
        return {
            "inactive_timeout": self.inactive_timeout,
            "cleanup_interval": self.cleanup_interval,
            "max_sessions_per_user": self.max_sessions_per_user,
            "enable_auto_cleanup": self.enable_auto_cleanup
        }
    
    def save_to_file(self, config_path: str) -> None:
        """
        Guarda la configuración actual en un archivo JSON.
        
        Args:
            config_path: Ruta donde guardar el archivo de configuración
        """
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    def __repr__(self) -> str:
        return f"SessionConfig(timeout={self.inactive_timeout}s, cleanup={self.cleanup_interval}s)"
