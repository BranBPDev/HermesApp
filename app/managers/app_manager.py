import sys
import threading
from app.managers.scraper_manager import run_all_scrapers_parallel
from app.managers.product_manager import ProductManager
from app.utils.logger_util import HermesLogger
from app.utils.update_util import is_latest_version, perform_update

class AppManager:
    def __init__(self):
        self.log = HermesLogger.get_logger("APP_MANAGER")
        self.pm = ProductManager() # Usamos self.pm consistentemente

    def start(self):
        # 1. Update (Solo imprime si hay acción real)
        try:
            if not is_latest_version():
                print("\n[!] Nueva versión detectada. Actualizando...")
                perform_update()
                sys.exit(0)
        except Exception as e:
            self.log.error(f"Error checking version: {e}")

        # 2. Sync (Una sola línea informativa)
        print("\n[⌛] Sincronizando precios...", end="\r")
        scraper_thread = threading.Thread(target=run_all_scrapers_parallel, daemon=True)
        scraper_thread.start()
        scraper_thread.join()
        
        # 3. Data Load
        self.pm.initialize_data()

        # 4. Interface
        self._run_main_loop()

    def _run_main_loop(self):
        # Limpiamos el rastro del "Sincronizando..."
        print(" " * 40, end="\r")
        print("="*50 + "\n   HERMES - COMPARADOR V3\n" + "="*50)
        print(" > Comandos: 'salir' | '+' (ver más)")

        while True:
            try:
                query = input("\n🔍 Buscar: ").strip()
                
                if query.lower() in ['salir', 'q', 'exit']:
                    break
                
                if not query:
                    continue

                if query == '+':
                    if self.pm.has_more():
                        self._render_results(self.pm.get_next_page())
                    else:
                        print("  [INFO] No hay más resultados.")
                else:
                    # Nueva búsqueda: resetea punteros y busca
                    self._render_results(self.pm.search(query))

            except (KeyboardInterrupt, EOFError):
                break
        
        sys.exit(0)

    def _render_results(self, results):
        found = False
        for store, products in results.items():
            if products:
                found = True
                print(f"\n[{store.upper()}]")
                for p in products:
                    precio = p.get('precio', '?.??')
                    nombre = p.get('nombre', 'Sin nombre')
                    print(f"  {precio}€ - {nombre}")
        
        if not found:
            print("  ❌ Sin coincidencias.")
        elif self.pm.has_more():
            print("\n  (Pulsa '+' para ver más)")