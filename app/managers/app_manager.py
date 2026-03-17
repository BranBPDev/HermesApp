import sys
import os
import threading
from app.managers.scraper_manager import run_all_scrapers_parallel
from app.managers.product_manager import ProductManager
from app.managers.auth_manager import AuthManager
from app.utils.logger_util import HermesLogger
from app.utils.update_util import is_latest_version, perform_update

class AppManager:
    def __init__(self):
        self.log = HermesLogger.get_logger("APP_MANAGER")
        self.pm = ProductManager()
        self.auth = AuthManager()
        self.last_viewed_results = []

    def start(self):
        try:
            if not is_latest_version():
                print("\n[!] Nueva versión detectada. Actualizando...")
                perform_update()
                os._exit(0)
        except Exception as e:
            self.log.error(f"Error en auto-update: {e}")

        threading.Thread(target=run_all_scrapers_parallel, daemon=True).start()
        self._show_auth_menu()
        self._clear_screen()
        self._run_main_loop()

    def _clear_screen(self):
        """Limpia la terminal según el sistema operativo."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def _show_auth_menu(self):
        print("\n" + "="*50 + "\n            📦 HERMES CLOUD V3\n" + "="*50)
        while not self.auth.current_user_id:
            print("\n1. Login | 2. Registro | 3. Salir")
            op = input("\n> ").strip()

            if op == '1':
                u, p = input("User: "), input("Pass: ")
                if self.auth.login(u, p): 
                    print(f"✅ Bienvenido, {u}")
                else: 
                    print("❌ Error de acceso.")
            elif op == '2':
                u, p = input("Nuevo User: "), input("Nueva Pass: ")
                if self.auth.register(u, p): 
                    print(f"✅ Cuenta creada: {u}")
                else: 
                    print("❌ El usuario ya existe o error en BD.")
            elif op == '3': 
                os._exit(0)

    def _run_main_loop(self):
        print("\n" + "-"*50 + f"\n Sesión: {self.auth.username} | 'salir', 'carrito', 'vaciar', '+'\n" + "-"*50)
        
        while True:
            try:
                query = input(f"\n🔍 Buscar: ").strip()
                if not query: continue

                cmd = query.lower()

                # 1. Comandos de salida
                if cmd in ['salir', 'exit', 'q']:
                    print("👋 Saliendo de Hermes...")
                    os._exit(0)
                
                # 2. Gestión de Carrito
                if cmd == 'carrito':
                    self._show_cart()
                    continue

                if cmd == 'vaciar':
                    from app.daos.cart_dao import CartDAO
                    CartDAO().clear_cart(self.auth.current_user_id)
                    print("🗑️ Carrito vaciado correctamente.")
                    continue

                # 3. Paginación
                if query == '+':
                    if self.pm.has_more(): 
                        self._render_results(self.pm.get_next_page())
                    else: 
                        print("  [INFO] No hay más resultados.")
                    continue

                # 4. Búsqueda normal
                self._render_results(self.pm.search(query))

            except (KeyboardInterrupt, EOFError): 
                os._exit(0)

    def _render_results(self, results):
        if not results:
            print("  ❌ Sin coincidencias en la nube.")
            return

        self.last_viewed_results = results
        print(f"\n{'ID':<3} {'PRECIO':<10} {'TIENDA':<12} {'PRODUCTO'}")
        print("-" * 65)
        
        for idx, p in enumerate(results, 1):
            price_str = f"{p['price']} €"
            store_str = f"[{p['store_name'].upper()}]"
            name_display = (p['name'][:40] + '..') if len(p['name']) > 40 else p['name']
            print(f"{idx:<3} {price_str:<10} {store_str:<12} {name_display}")
        
        print("\n(Número para añadir, '+' para más, o Enter para nueva búsqueda)")
        res = input("> ").strip()
        
        if res.isdigit() and 0 < int(res) <= len(results):
            self._add_to_cart(results[int(res)-1])

    def _add_to_cart(self, product):
        from app.daos.cart_dao import CartDAO
        CartDAO().add_to_cart(self.auth.current_user_id, product['id'])
        print(f"🛒 Añadido: {product['name']} ({product['store_name']})")

    def _show_cart(self):
        from app.daos.cart_dao import CartDAO
        items = CartDAO().get_user_cart(self.auth.current_user_id)
        if not items:
            print("\n🛒 Tu carrito está vacío.")
            return
        
        print("\n🛒 TU LISTA DE LA COMPRA:")
        print("-" * 45)
        total = 0
        for i in items:
            sub = float(i['subtotal'])
            total += sub
            # Formateo de nombre para que no rompa la línea del subtotal
            name_trunc = (i['name'][:30] + '...') if len(i['name']) > 30 else i['name']
            print(f" • {i['quantity']}x {name_trunc:<33} ({i['store_name'].upper():^10}) -> {round(sub, 2):>6}€")
        
        print("-" * 45)
        print(f"💰 TOTAL ESTIMADO: {round(total, 2)}€")