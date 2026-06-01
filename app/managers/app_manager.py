import threading
from app.managers.gui_manager import GUIManager
from app.utils.update_util import is_latest_version, perform_update
from app.managers.scraper_manager import run_all_scrapers_parallel
from app.utils.logger_util import HermesLogger

class AppManager:
    def __init__(self):
        self.log = HermesLogger.get_logger("APP_MANAGER")
        # El AppManager solo crea la interfaz. No le pasa managers, no le pasa datos.
        self.gui = GUIManager()

    def start(self):
        # 1. Orquesta el inicio de los scrapers
        if not is_latest_version():
            self.gui.show_update(perform_update)
        else:
            self.log.info("Iniciando hilo de scraping en background...")
            threading.Thread(target=run_all_scrapers_parallel, daemon=True).start()
            self.gui.start()