from app.utils.update_util import is_latest_version, perform_update
from app.managers.scraper_manager import run_all_scrapers_parallel
from app.utils.logger_util import HermesLogger
import threading

def main():
    log = HermesLogger.get_logger("MAIN")
    log.info("--- INICIO DE APLICACIÓN ---")

    if not is_latest_version():
        print("[UPDATE] Actualizando a la última versión...")
        perform_update()
        return

    # Ejecución paralela
    threading.Thread(target=run_all_scrapers_parallel, daemon=True).start()

    print("\n" + "="*30)
    print(" HERMES APP - MONITORING")
    print("="*30)
    input("Presiona ENTER para cerrar...\n")

if __name__ == "__main__":
    main()