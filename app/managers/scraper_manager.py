import time, concurrent.futures
from pathlib import Path
from app.utils.paths_util import PRODUCT_PATHS, SCRAPERS_DIR
from app.utils.dates_util import get_current_date_str
from app.utils.logger_util import HermesLogger 
from app.scrapers.mercadona import MercadonaScraper
from app.scrapers.eroski import EroskiScraper
from app.scrapers.gadis import GadisScraper
from app.utils.json_util import save_json
from app.managers.product_manager import ProductManager

log = HermesLogger.get_logger("SCRAPER_MANAGER")

SCRAPER_REGISTRY = {
    "mercadona": MercadonaScraper,
    "gadis": GadisScraper,
    "eroski": EroskiScraper
}

def _execute_scraper(name):
    today = Path(f"{PRODUCT_PATHS[name]}_{get_current_date_str()}.json")

    # Si ya existe localmente, saltamos el scrapeo
    if today.exists() and today.stat().st_size > 0:
        return f"⏭️ {name.upper()}: Ya existe archivo local"

    start = time.time()
    try:
        scraper_inst = SCRAPER_REGISTRY[name]()
        data = scraper_inst.scrape()
        
        if data:
            # Limpiar archivos antiguos del mismo scraper
            for f in SCRAPERS_DIR.iterdir():
                if f.name.startswith(name) and f != today:
                    try: f.unlink()
                    except: pass
            
            # 1. Guardar local
            save_json(today, data)
            
            # 2. Sincronizar Nube (Aquí ocurre la magia)
            log.info(f"☁️ {name.upper()}: Subiendo datos a la nube...")
            pm = ProductManager()
            pm.sync_with_cloud(name, data)
            
            return f"✅ {name.upper()}: {len(data)} prods ({round(time.time() - start, 2)}s) -> Sincronizado"
        
        return f"⚠️ {name.upper()}: El scraper no devolvió datos"
    except Exception as e:
        log.error(f"❌ Error en {name}: {e}")
        return f"❌ {name.upper()}: Fallo crítico"

def run_all_scrapers_parallel():
    log.info("--- INICIO DE SCRAPPING Y SINCRONIZACIÓN ---")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(_execute_scraper, n) for n in SCRAPER_REGISTRY]
        for f in concurrent.futures.as_completed(futures):
            log.info(f.result())