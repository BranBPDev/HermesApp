import concurrent.futures
import threading
import time
from app.utils.json_util import save_json
from app.utils.paths_util import MERCADONA_PRODUCTS_JSON, LIDL_PRODUCTS_JSON, GADIS_PRODUCTS_JSON, EROSKI_PRODUCTS_JSON
from app.scrapers import mercadona, lidl, gadis, eroski

SCRAPER_CONFIG = {
    "mercadona": (mercadona.scrape, MERCADONA_PRODUCTS_JSON),
    "lidl": (lidl.scrape, LIDL_PRODUCTS_JSON),
    "gadis": (gadis.scrape, GADIS_PRODUCTS_JSON),
    "eroski": (eroski.scrape, EROSKI_PRODUCTS_JSON),
}

def _task_wrapper(name, func, path):
    print(f"[DEBUG-MANAGER] Lanzando tarea: {name}")
    start_time = time.time()
    try:
        data = func()
        if data:
            save_json(path, data)
            duration = round(time.time() - start_time, 2)
            return f"[SUCCESS] {name}: {len(data)} productos en {duration}s."
        return f"[EMPTY] {name}: No se obtuvieron datos (posible fallo en el scraper)."
    except Exception as e:
        return f"[FAILED] {name}: {str(e)}"

def run_all_scrapers_parallel():
    def executor_logic():
        print("[DEBUG-MANAGER] Hilo de ejecución paralelo iniciado.")
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_name = {
                executor.submit(_task_wrapper, n, cfg[0], cfg[1]): n 
                for n, cfg in SCRAPER_CONFIG.items()
            }
            for future in concurrent.futures.as_completed(future_to_name):
                try:
                    print(future.result())
                except Exception as e:
                    print(f"[DEBUG-MANAGER] Error en hilo de {future_to_name[future]}: {e}")

    threading.Thread(target=executor_logic, daemon=True).start()