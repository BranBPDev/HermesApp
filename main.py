import sys
import ctypes
from app.managers.app_manager import AppManager
from app.utils.logger_util import HermesLogger

log = HermesLogger.get_logger("SYSTEM")

def main():
    log.info("--- INICIO DE APLICACIÓN ---")
    if sys.platform == "win32": 
        try:
            app_id = 'Hermes.App.v004'
            res = ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            log.info(f"Windows AppID set to: {app_id} | Result: {res}")
        except Exception as e:
            log.error(f"CRÍTICO: No se pudo setear AppUserModelID: {e}")
    
    from app.utils.paths_util import LOGO_ICO
    log.info(f"Verificando ruta de icono: {LOGO_ICO} | Existe: {LOGO_ICO.exists()}")
    
    AppManager().start()

if __name__ == "__main__":
    main()