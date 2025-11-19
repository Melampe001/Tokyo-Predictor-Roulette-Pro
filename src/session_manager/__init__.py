"""
Sistema de Gestión de Sesiones con Terminación Automática
Tokyo-Predictor-Roulette-Pro

Este módulo proporciona un sistema completo para gestionar sesiones de usuarios
con detección y terminación automática de sesiones inactivas.
"""

from .session import Session
from .session_manager import SessionManager
from .config import SessionConfig

__version__ = "1.0.0"
__all__ = ["Session", "SessionManager", "SessionConfig"]
