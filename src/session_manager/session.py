"""
Módulo de Sesión
Representa una sesión individual de usuario con seguimiento de actividad.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


class Session:
    """
    Clase que representa una sesión de usuario individual.
    
    Attributes:
        session_id (str): Identificador único de la sesión
        user_id (str): Identificador del usuario asociado
        created_at (datetime): Timestamp de creación de la sesión
        last_activity (datetime): Timestamp de la última actividad
        data (Dict[str, Any]): Datos adicionales de la sesión
        is_active (bool): Estado de la sesión
    """
    
    def __init__(self, user_id: str, session_id: Optional[str] = None, data: Optional[Dict[str, Any]] = None):
        """
        Inicializa una nueva sesión.
        
        Args:
            user_id: Identificador del usuario
            session_id: ID de sesión personalizado (opcional, se genera automáticamente)
            data: Datos adicionales para almacenar en la sesión
        """
        self.session_id = session_id or str(uuid.uuid4())
        self.user_id = user_id
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.data = data or {}
        self.is_active = True
    
    def update_activity(self) -> None:
        """
        Actualiza el timestamp de última actividad a la hora actual.
        """
        self.last_activity = datetime.now()
    
    def get_inactive_duration(self) -> timedelta:
        """
        Calcula la duración de inactividad desde la última actividad.
        
        Returns:
            timedelta: Tiempo transcurrido desde la última actividad
        """
        return datetime.now() - self.last_activity
    
    def is_inactive_for(self, timeout_seconds: int) -> bool:
        """
        Verifica si la sesión ha estado inactiva por más tiempo del especificado.
        
        Args:
            timeout_seconds: Tiempo límite de inactividad en segundos
            
        Returns:
            bool: True si la sesión ha excedido el tiempo de inactividad
        """
        return self.get_inactive_duration().total_seconds() > timeout_seconds
    
    def terminate(self) -> None:
        """
        Marca la sesión como inactiva y limpia recursos.
        """
        self.is_active = False
        # Aquí se pueden agregar más operaciones de limpieza según sea necesario
    
    def set_data(self, key: str, value: Any) -> None:
        """
        Almacena un dato en la sesión.
        
        Args:
            key: Clave del dato
            value: Valor a almacenar
        """
        self.data[key] = value
        self.update_activity()
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """
        Recupera un dato de la sesión.
        
        Args:
            key: Clave del dato
            default: Valor por defecto si la clave no existe
            
        Returns:
            El valor almacenado o el valor por defecto
        """
        self.update_activity()
        return self.data.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la sesión a un diccionario para serialización.
        
        Returns:
            Diccionario con los datos de la sesión
        """
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "is_active": self.is_active,
            "inactive_seconds": self.get_inactive_duration().total_seconds(),
            "data": self.data
        }
    
    def __repr__(self) -> str:
        return f"Session(id={self.session_id}, user={self.user_id}, active={self.is_active})"
