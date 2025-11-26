# Tokyo-Predictor-Roulette-Pro

Sistema profesional de gestión de sesiones con terminación automática de sesiones inactivas.

## 📋 Descripción

Tokyo-Predictor-Roulette-Pro es un sistema completo de gestión de sesiones diseñado para aplicaciones que requieren un control robusto del ciclo de vida de las sesiones de usuario. El sistema incluye detección automática de inactividad, limpieza de recursos y un gestor centralizado de sesiones.

## ✨ Características Principales

- **Gestión Centralizada de Sesiones**: Control completo del ciclo de vida de las sesiones
- **Detección de Inactividad**: Monitoreo automático del tiempo sin actividad
- **Terminación Automática**: Limpieza automática de sesiones inactivas basada en tiempo configurable
- **Limpieza de Recursos**: Liberación automática de recursos asociados a sesiones terminadas
- **Configuración Flexible**: Sistema de configuración basado en archivos JSON
- **Callbacks Personalizados**: Soporte para funciones callback en eventos de terminación
- **Thread-Safe**: Operaciones seguras en entornos multi-hilo
- **Límite de Sesiones**: Control de sesiones simultáneas por usuario

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/Tokyo-Predictor-Roulette-Pro.git
cd Tokyo-Predictor-Roulette-Pro
```

2. Asegúrate de tener Python 3.7 o superior instalado

3. El sistema no requiere dependencias externas (usa solo la biblioteca estándar de Python)

## 📖 Uso Básico

### Ejemplo Simple

```python
from src.session_manager import SessionManager, SessionConfig

# Crear configuración
config = SessionConfig(
    inactive_timeout=1800,  # 30 minutos
    cleanup_interval=300,   # 5 minutos
    max_sessions_per_user=5
)

# Crear gestor de sesiones
manager = SessionManager(config)

# Crear una sesión
session = manager.create_session("usuario_001", {"rol": "admin"})

# Usar la sesión
session.set_data("saldo", 1000)
session.set_data("ultima_apuesta", 50)

# Recuperar datos
saldo = session.get_data("saldo")

# Actualizar actividad
session.update_activity()

# Cerrar el gestor (termina todas las sesiones)
manager.shutdown()
```

### Uso con Context Manager

```python
from src.session_manager import SessionManager, SessionConfig

config = SessionConfig(inactive_timeout=600)

# El gestor se cierra automáticamente al salir del bloque
with SessionManager(config) as manager:
    session = manager.create_session("usuario_001")
    # ... usar la sesión ...
```

## ⚙️ Configuración

### Archivo de Configuración

Crea un archivo `config/session_config.json`:

```json
{
  "inactive_timeout": 1800,
  "cleanup_interval": 300,
  "max_sessions_per_user": 5,
  "enable_auto_cleanup": true
}
```

### Cargar desde Archivo

```python
from src.session_manager import SessionConfig, SessionManager

# Cargar configuración
config = SessionConfig.from_file("config/session_config.json")
manager = SessionManager(config)
```

### Parámetros de Configuración

| Parámetro | Descripción | Valor por Defecto |
|-----------|-------------|-------------------|
| `inactive_timeout` | Tiempo en segundos antes de terminar una sesión inactiva | 1800 (30 min) |
| `cleanup_interval` | Intervalo en segundos para ejecutar la limpieza automática | 300 (5 min) |
| `max_sessions_per_user` | Número máximo de sesiones simultáneas por usuario | 5 |
| `enable_auto_cleanup` | Habilita/deshabilita la limpieza automática | true |

## 📚 Documentación de la API

### SessionManager

**Métodos principales:**

- `create_session(user_id, session_data=None)`: Crea una nueva sesión
- `get_session(session_id)`: Recupera una sesión por ID
- `get_user_sessions(user_id)`: Obtiene todas las sesiones de un usuario
- `update_session_activity(session_id)`: Actualiza la actividad de una sesión
- `terminate_session(session_id)`: Termina una sesión específica
- `terminate_user_sessions(user_id)`: Termina todas las sesiones de un usuario
- `cleanup_inactive_sessions()`: Limpia manualmente sesiones inactivas
- `get_stats()`: Obtiene estadísticas del gestor
- `register_termination_callback(callback)`: Registra callback de terminación
- `shutdown()`: Cierra el gestor y todas las sesiones

### Session

**Propiedades:**

- `session_id`: Identificador único de la sesión
- `user_id`: ID del usuario asociado
- `created_at`: Timestamp de creación
- `last_activity`: Timestamp de última actividad
- `is_active`: Estado de la sesión
- `data`: Diccionario de datos de la sesión

**Métodos:**

- `update_activity()`: Actualiza el timestamp de actividad
- `get_inactive_duration()`: Obtiene duración de inactividad
- `is_inactive_for(timeout_seconds)`: Verifica si excede timeout
- `set_data(key, value)`: Almacena datos
- `get_data(key, default=None)`: Recupera datos
- `terminate()`: Termina la sesión
- `to_dict()`: Convierte a diccionario

## 🔍 Ejemplos

El proyecto incluye varios ejemplos completos en el directorio `examples/`:

### Ejemplo Básico
```bash
python examples/ejemplo_basico.py
```
Demuestra la creación, uso y terminación básica de sesiones.

### Ejemplo Avanzado
```bash
python examples/ejemplo_avanzado.py
```
Muestra limpieza automática, callbacks y gestión avanzada.

### Ejemplo de Configuración
```bash
python examples/ejemplo_configuracion.py
```
Ilustra carga de configuración desde archivo JSON.

## 🧪 Tests

Ejecuta los tests unitarios:

```bash
python tests/test_session_manager.py
```

Los tests cubren:
- Creación y gestión de sesiones
- Detección de inactividad
- Limpieza automática
- Límites de sesiones por usuario
- Callbacks de terminación
- Configuración
- Integración completa del sistema

## 🏗️ Arquitectura del Sistema

```
Tokyo-Predictor-Roulette-Pro/
├── src/
│   └── session_manager/
│       ├── __init__.py          # Módulo principal
│       ├── session.py           # Clase Session
│       ├── session_manager.py   # Gestor de sesiones
│       └── config.py            # Configuración
├── config/
│   └── session_config.json      # Configuración por defecto
├── examples/
│   ├── ejemplo_basico.py        # Ejemplo básico
│   ├── ejemplo_avanzado.py      # Ejemplo avanzado
│   └── ejemplo_configuracion.py # Ejemplo de configuración
├── tests/
│   └── test_session_manager.py  # Tests unitarios
└── README.md
```

## 💡 Casos de Uso

### 1. Aplicación de Juegos en Línea
```python
# Gestionar sesiones de jugadores
session = manager.create_session("jugador_001", {
    "saldo": 1000,
    "nivel": 5,
    "sala": "tokyo_room"
})

# Registrar apuesta
session.set_data("ultima_apuesta", 50)
session.set_data("saldo", session.get_data("saldo") - 50)
```

### 2. Sistema de Autenticación
```python
# Callback para limpiar tokens al terminar sesión
def on_logout(session):
    token = session.get_data("auth_token")
    revoke_token(token)  # Revocar token en BD
    log_audit(session.user_id, "session_terminated")

manager.register_termination_callback(on_logout)
```

### 3. API con Rate Limiting
```python
# Rastrear uso de API por sesión
session.set_data("requests_count", 0)
session.set_data("last_request_time", time.time())

# Incrementar contador en cada request
count = session.get_data("requests_count", 0)
session.set_data("requests_count", count + 1)
```

## 🔒 Consideraciones de Seguridad

- Las sesiones se identifican mediante UUID v4 aleatorios
- Los datos de sesión se almacenan en memoria (considera encriptación para datos sensibles)
- El sistema es thread-safe para uso concurrente
- Las sesiones inactivas se terminan automáticamente
- Los callbacks permiten limpieza personalizada de recursos

## 🛠️ Personalización

### Crear un Callback Personalizado

```python
def mi_callback(session):
    """Callback ejecutado al terminar una sesión"""
    print(f"Sesión {session.session_id} terminada")
    
    # Guardar estadísticas
    save_session_stats(session.to_dict())
    
    # Limpiar cache
    clear_user_cache(session.user_id)
    
    # Notificar al usuario
    notify_user(session.user_id, "Tu sesión ha expirado")

manager.register_termination_callback(mi_callback)
```

### Extender la Clase Session

```python
from src.session_manager import Session

class GameSession(Session):
    """Sesión extendida para juegos"""
    
    def __init__(self, user_id, **kwargs):
        super().__init__(user_id, **kwargs)
        self.set_data("score", 0)
        self.set_data("level", 1)
    
    def add_score(self, points):
        current = self.get_data("score", 0)
        self.set_data("score", current + points)
        self.update_activity()
```

## 📊 Monitoreo

### Obtener Estadísticas

```python
stats = manager.get_stats()
print(f"Sesiones activas: {stats['total_active_sessions']}")
print(f"Usuarios únicos: {stats['unique_users']}")
print(f"Limpieza automática: {stats['auto_cleanup_running']}")
```

### Listar Sesiones Activas

```python
for session in manager.get_all_sessions():
    print(f"Usuario: {session.user_id}")
    print(f"Inactivo por: {session.get_inactive_duration().total_seconds()}s")
    print(f"Datos: {session.data}")
```

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está disponible bajo la licencia MIT.

## 👥 Autores

- Equipo de desarrollo Tokyo-Predictor-Roulette-Pro

## 📞 Soporte

Para preguntas, problemas o sugerencias, por favor abre un issue en GitHub.

---

**Versión:** 1.0.0  
**Última actualización:** 2025