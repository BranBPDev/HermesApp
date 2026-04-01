from typing import Callable, Optional

# Definimos un tipo para claridad: recibe un float (0.0 a 1.0) y un string opcional
ProgressCallback = Callable[[float, str], None]

def invoke_progress(callback: Optional[ProgressCallback], value: float, message: str = ""):
    """Invoca el callback de forma segura si existe."""
    if callback:
        try:
            callback(value, message)
        except Exception:
            pass # Los errores de UI no deben romper la lógica de descarga