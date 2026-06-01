import time
import concurrent.futures
from app.utils.paths_util import PRODUCT_PATHS
from app.utils.logger_util import HermesLogger 
from app.scrapers.mercadona import MercadonaScraper
from app.scrapers.eroski import EroskiScraper
from app.scrapers.gadis import GadisScraper
from app.utils.json_util import save_json
from app.daos.product_dao import ProductDAO

log = HermesLogger.get_logger("SCRAPER_MANAGER")

SCRAPER_REGISTRY = {
    "mercadona": MercadonaScraper,
    "gadis": GadisScraper,
    "eroski": EroskiScraper
}

def _execute_scraper(name):
    # Definimos ruta fija para que solo haya un archivo por supermercado
    path_objeto = PRODUCT_PATHS[name]
    final_file = path_objeto.with_name(f"{name}_latest.json")
    
    start_time = time.time()
    try:
        # 1. Scrapeo
        scraper_inst = SCRAPER_REGISTRY[name]()
        raw_data = scraper_inst.scrape()
        
        if not raw_data:
            return f"⚠️ {name.upper()}: Sin datos"

        # 2. Procesamiento ligero
        final_products = []
        seen_names = set()

        for item in raw_data:
            nombre = item.get('nombre', '').strip()
            
            if not nombre or nombre in seen_names:
                continue
            
            final_products.append({
                'nombre': nombre,
                'precio': item.get('precio', 0.0),
                'imagen_url': item.get('imagen_url', ''),
                'fecha': time.strftime("%Y-%m-%d")
            })
            seen_names.add(nombre)
        
        # 3. Limpieza y Persistencia
        dao = ProductDAO()
        
        # Guardamos JSON (sobrescribe) e insertamos en DB
        save_json(final_file, final_products)
        dao.upsert_batch(name, final_products)
        
        log.info(f"✅ {name.upper()} ok ({round(time.time()-start_time, 2)}s) -> {len(final_products)} prods")
        return f"{name.upper()} finalizado"

    except Exception as e:
        log.error(f"❌ Error en {name}: {e}")
        return f"❌ {name.upper()} falló"

def run_all_scrapers_parallel():
    log.info("--- INICIANDO SCRAPING PARALELO ---")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(_execute_scraper, n) for n in SCRAPER_REGISTRY]
        concurrent.futures.wait(futures)