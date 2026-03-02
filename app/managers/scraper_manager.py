import concurrent.futures
import time
from typing import Dict, Type
from app.models.scraper_base import BaseScraper
from app.utils.json_util import save_json
from app.utils.paths_util import PRODUCT_PATHS
from app.utils.logger_util import HermesLogger  # Importamos nuestro nuevo util
from app.scrapers.mercadona import MercadonaScraper
from app.scrapers.gadis import GadisScraper
from app.scrapers.eroski import EroskiScraper

# Logger central para el manager
log = HermesLogger.get_logger("SCRAPER_MANAGER")

SCRAPER_REGISTRY: Dict[str, Type[BaseScraper]] = {
    "mercadona": MercadonaScraper,
    "gadis": GadisScraper,
    "eroski": EroskiScraper
}

def _execute_scraper(name: str):
    """Lógica interna de ejecución con logging integrado."""
    if name not in SCRAPER_REGISTRY:
        error_msg = f"Scraper {name} no registrado en el REGISTRY."
        log.error(error_msg)
        return f"❌ {name.upper()}: No registrado."
    
    start_time = time.time()
    log.info(f"Iniciando proceso para: {name.upper()}")

    try:
        # Instanciamos el scraper dinámicamente
        scraper_inst = SCRAPER_REGISTRY[name]()
        
        # Ejecutamos el scrape (que ya solo se preocupa de los datos)
        data = scraper_inst.scrape()
        
        duration = round(time.time() - start_time, 2)

        if data and len(data) > 0:
            save_json(PRODUCT_PATHS[name], data)
            success_msg = f"{name.upper()}: {len(data)} prods recuperados con éxito"
            
            # Logueamos el éxito en el archivo con detalle de tiempo
            log.info(f"{success_msg} en {duration}s")
            
            # Retornamos para la consola (formato limpio)
            return f"✅ {name.upper()}: {len(data)} prods en {duration}s"
        
        log.warning(f"{name.upper()}: Finalizado sin datos tras {duration}s")
        return f"⚠️ {name.upper()}: Sin datos"

    except Exception as e:
        # Capturamos el error con el traceback completo en el log
        log.exception(f"Error crítico en el scraper {name}")
        return f"❌ {name.upper()}: Error crítico (ver hermes.log)"

def run_all_scrapers_parallel():
    """Ejecuta todos los scrapers y maneja la salida de consola de forma ordenada."""
    log.info("--- NUEVA SESIÓN DE SCRAPPING EN PARALELO ---")
    
    # Usamos ThreadPoolExecutor para no bloquear el hilo principal
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(SCRAPER_REGISTRY)) as executor:
        # Mapeamos las ejecuciones
        futures = {executor.submit(_execute_scraper, name): name for name in SCRAPER_REGISTRY}
        
        # Recogemos resultados conforme terminan
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            # Este print es el único que verá el usuario en consola
            print(result)

    log.info("--- SESIÓN FINALIZADA ---")