import time, concurrent.futures
from app.utils.paths_util import PRODUCT_PATHS
from app.utils.dates_util import get_current_date_str
from app.utils.logger_util import HermesLogger 
from app.scrapers.mercadona import MercadonaScraper
from app.scrapers.eroski import EroskiScraper
from app.scrapers.gadis import GadisScraper
from app.utils.json_util import save_json
from app.utils.refactor_util import HermesRefactorer
from app.daos.product_dao import ProductDAO

log = HermesLogger.get_logger("SCRAPER_MANAGER")

SCRAPER_REGISTRY = {
    "mercadona": MercadonaScraper,
    "gadis": GadisScraper,
    "eroski": EroskiScraper
}

def _execute_scraper(name):
    # Construcción de ruta usando strings sobre el objeto Path importado
    path_objeto = PRODUCT_PATHS[name]
    final_file = path_objeto.with_name(f"{path_objeto.name}_{get_current_date_str()}.json")
    
    start = time.time()
    try:
        scraper_inst = SCRAPER_REGISTRY[name]()
        raw_data = scraper_inst.scrape()
        
        if not raw_data:
            return f"⚠️ {name.upper()}: Sin datos"

        refactorer = HermesRefactorer()
        final_products = []
        seen_names = set()

        for item in raw_data:
            nombre = item.get('nombre', '').strip()
            if not nombre or nombre in seen_names:
                continue
            
            new_item = item.copy()
            # OJO: Aquí el manager usa el refactorer para el cálculo de precios, 
            # pero el DAO mandará "_temp" para el TAG.
            
            if item.get('precio_referencia') and item.get('precio_referencia') > 0:
                new_item['price_norm'] = item['precio_referencia']
                new_item['cantidad'] = item.get('cantidad')
                new_item['tipo_unidad'] = item.get('tipo_unidad')
            else:
                p_norm, qty, unit = refactorer.get_normalized_data(nombre, item.get('precio', 0))
                new_item['price_norm'] = p_norm
                new_item['cantidad'] = qty
                new_item['tipo_unidad'] = unit
            
            final_products.append(new_item)
            seen_names.add(nombre)
        
        save_json(final_file, final_products)
        ProductDAO().upsert_batch(name, final_products)
        
        log.info(f"✅ {name.upper()} ok ({round(time.time()-start, 2)}s) -> {len(final_products)} prods")
        return f"{name.upper()} finalizado"

    except Exception as e:
        log.error(f"❌ Error en {name}: {e}")
        return f"❌ {name.upper()} falló"

def run_all_scrapers_parallel():
    log.info("--- INICIANDO SCRAPING PARALELO ---")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(_execute_scraper, n) for n in SCRAPER_REGISTRY]
        concurrent.futures.wait(futures)