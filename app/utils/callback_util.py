from typing import Callable, Optional

# Definimos un tipo para claridad: recibe un float (0.0 a 1.0) y un string opcional
ProgressCallback = Callable[[float, str], None]

def invoke_progress(callback: Optional[ProgressCallback], value: float, message: str = ""):
    """Invoca el callback de forma segura si existe."""
    if callback:
        try:
            callback(value, message)
        except Exception as e:
            from app.utils.logger_util import HermesLogger
            HermesLogger.get_logger("CALLBACK").error(f"Error en callback: {e}")