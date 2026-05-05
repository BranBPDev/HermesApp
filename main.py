import sys
import ctypes
from app.managers.app_manager import AppManager
from app.utils.logger_util import HermesLogger

log = HermesLogger.get_logger("SYSTEM")

def main():
    if sys.platform == "win32": 
        try:
            app_id = 'Hermes.App.v004'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            log.info(f"Windows AppID set to: {app_id}")
        except Exception as e:
            log.error(f"Failed to set Windows AppID: {e}")
    
    log.info("Iniciando AppManager...")
    AppManager().start()

if __name__ == "__main__":
    main()