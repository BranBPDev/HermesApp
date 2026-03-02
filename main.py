from app.utils.update_util import is_latest_version, perform_update
from app.managers.scraper_manager import run_all_scrapers_parallel
from app.utils.logger_util import HermesLogger
import threading
import sys

def main():
    log = HermesLogger.get_logger("MAIN")
    log.info("--- INICIO DE APLICACIÓN ---")

    # 1. Check Update
    if not is_latest_version():
        print("[UPDATE] Nueva versión detectada. Actualizando...")
        perform_update()
        return

    print("="*40)
    print("      HERMES APP - MONITORING")
    print("="*40)
    print("[SYSTEM] Iniciando scrapers en paralelo...")

    # 2. Ejecución y espera
    scraper_thread = threading.Thread(target=run_all_scrapers_parallel, daemon=True)
    scraper_thread.start()
    
    # Esperamos a que el hilo termine para que no se mezclen los prints con el input
    scraper_thread.join()

    print("\n" + "="*40)
    print(" PROCESO FINALIZADO")
    print("="*40)
    input("\nPresiona ENTER para cerrar la aplicación...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)