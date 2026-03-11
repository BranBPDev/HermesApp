import time, concurrent.futures
from pathlib import Path
from app.utils.paths_util import PRODUCT_PATHS, SCRAPERS_DIR
from app.utils.dates_util import get_current_date_str
from app.utils.logger_util import HermesLogger 
from app.scrapers.mercadona import MercadonaScraper
from app.scrapers.eroski import EroskiScraper
from app.scrapers.gadis import GadisScraper
from app.utils.json_util import save_json

log = HermesLogger.get_logger("SCRAPER_MANAGER")

SCRAPER_REGISTRY = {
    "mercadona": MercadonaScraper,
    "gadis": GadisScraper,
    "eroski": EroskiScraper
}

def _execute_scraper(name):
    today = Path(f"{PRODUCT_PATHS[name]}_{get_current_date_str()}.json")

    if today.exists() and today.stat().st_size > 0:
        return f"⏭️ {name.upper()}: Al día"

    start = time.time()
    try:
        if data := SCRAPER_REGISTRY[name]().scrape():
            [f.unlink() for f in SCRAPERS_DIR.iterdir() if f.name.startswith(PRODUCT_PATHS[name].name) and f != today]
            save_json(today, data)
            return f"✅ {name.upper()}: {len(data)} prods ({round(time.time() - start, 2)}s)"
        return f"⚠️ {name.upper()}: Sin datos"
    except Exception:
        log.exception(f"Error en {name}")
        return f"❌ {name.upper()}: Error"

def run_all_scrapers_parallel():
    log.info("--- INICIO DE SCRAPPING PARALELO ---")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(_execute_scraper, n) for n in SCRAPER_REGISTRY]
        for f in concurrent.futures.as_completed(futures):
            # Redirigimos el resultado del scraper al log, no a la terminal
            log.info(f.result())