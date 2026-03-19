import time, concurrent.futures
from pathlib import Path
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
    date_str = get_current_date_str()
    # Ahora solo guardamos un archivo final procesado
    final_file = Path(f"{PRODUCT_PATHS[name]}_{date_str}.json")

    start = time.time()
    try:
        scraper_inst = SCRAPER_REGISTRY[name]()
        raw_data = scraper_inst.scrape()
        
        if not raw_data:
            return f"⚠️ {name.upper()}: Sin datos"

        refactorer = HermesRefactorer()
        final_products = []
        seen_names = set() # Para evitar duplicados en el mismo batch

        for item in raw_data:
            nombre = item.get('nombre', '').strip()
            
            # --- FILTRO DE DUPLICADOS EN MEMORIA ---
            # Si el nombre ya lo procesamos en este scrapeo, lo saltamos
            if not nombre or nombre in seen_names:
                continue
            
            new_item = item.copy()
            # Enriquecemos con tags y precios normalizados
            new_item['tag'] = refactorer.get_manual_tag(nombre)
            new_item['price_norm'] = refactorer.get_normalized_data(
                nombre, 
                item.get('precio', 0)
            )
            
            # Añadimos a la lista final y marcamos como visto
            final_products.append(new_item)
            seen_names.add(nombre)
        
        # 1. Guardar archivo único con datos ya procesados (Refactorizados)
        save_json(final_file, final_products)
        
        # 2. 🔥 SUBIDA A LA BASE DE DATOS 🔥
        # Enviamos la lista final_products que ya no tiene duplicados de nombre
        dao = ProductDAO()
        dao.upsert_batch(name, final_products)
        
        duracion = round(time.time() - start, 2)
        log.info(f"✅ {name.upper()} ok ({duracion}s) -> {len(final_products)} prods únicos subidos")
        return f"{name.upper()} finalizado"

    except Exception as e:
        log.error(f"❌ Error en {name}: {e}")
        return f"❌ {name.upper()} falló"

def run_all_scrapers_parallel():
    log.info("--- INICIANDO SCRAPING + ACTUALIZACIÓN DE BASE DE DATOS ---")
    # Mantenemos el paralelismo para que sea rápido
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(_execute_scraper, n) for n in SCRAPER_REGISTRY]
        concurrent.futures.wait(futures)