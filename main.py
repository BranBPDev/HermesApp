from app.utils.update_util import is_latest_version, perform_update
from app.managers.scraper_manager import run_all_scrapers_parallel

def main():
    # 1. El auto-updater siempre primero
    if not is_latest_version():
        perform_update()

    # 2. Lanzamos la recogida de datos paralela (Segundo plano)
    # Esto creará los JSON en data/raw/ sin bloquear el input de abajo
    run_all_scrapers_parallel()

    print("\n[INFO] La aplicación está lista.")
    print("[INFO] Los scrapers están trabajando en segundo plano...")
    
    input("\nPresiona ENTER para salir y detener los procesos...")

if __name__ == "__main__":
    main()