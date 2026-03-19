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
        """Inicia el flujo principal de la aplicación."""
        try:
            # 1. Verificación de actualizaciones
            if not is_latest_version():
                print("\n[!] Nueva versión detectada. Actualizando...")
                perform_update()
                os._exit(0)
        except Exception as e:
            self.log.error(f"Error en auto-update: {e}")

        # 2. Scrapers en segundo plano
        threading.Thread(target=run_all_scrapers_parallel, daemon=True).start()
        
        # 3. Autenticación
        self._show_auth_menu()
        self._clear_screen()
        
        # 4. Bucle principal
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
        """Maneja la lógica de comandos y búsqueda."""
        print("\n" + "-"*50)
        print(f" Sesión: {self.auth.username.upper()}")
        print(" Comandos: 'salir', 'carrito', 'ahorro', 'vaciar', '+'")
        print("-"*50)
        
        while True:
            try:
                query = input(f"\n🔍 Buscar: ").strip()
                if not query: continue

                cmd = query.lower()

                if cmd in ['salir', 'exit', 'q']:
                    print("👋 Saliendo de Hermes...")
                    os._exit(0)
                
                if cmd == 'carrito':
                    self._show_cart()
                    continue

                if cmd == 'ahorro':
                    self._show_savings()
                    continue

                if cmd == 'vaciar':
                    from app.daos.cart_dao import CartDAO
                    CartDAO().clear_cart(self.auth.current_user_id)
                    print("🗑️ Carrito vaciado correctamente.")
                    continue

                if query == '+':
                    if self.pm.has_more(): 
                        self._render_results(self.pm.get_next_page())
                    else: 
                        print("  [INFO] No hay más resultados.")
                    continue

                self._render_results(self.pm.search(query))

            except (KeyboardInterrupt, EOFError): 
                os._exit(0)
            except Exception as e:
                self.log.error(f"Error inesperado en el loop principal: {e}")
                print(f"❌ Ha ocurrido un error: {e}")

    def _render_results(self, results):
        """Muestra los resultados de búsqueda en tabla."""
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
        """Añade un producto al carrito del usuario actual."""
        from app.daos.cart_dao import CartDAO
        CartDAO().add_to_cart(self.auth.current_user_id, product['id'])
        print(f"🛒 Añadido: {product['name']} ({product['store_name']})")

    def _show_cart(self):
        """Muestra el contenido actual del carrito y el total."""
        from app.daos.cart_dao import CartDAO
        items = CartDAO().get_user_cart(self.auth.current_user_id)
        if not items:
            print("\n🛒 Tu carrito está vacío.")
            return
        
        print("\n🛒 TU LISTA DE LA COMPRA:")
        print("-" * 55)
        total = 0
        for i in items:
            sub = float(i['subtotal'])
            total += sub
            name_trunc = (i['name'][:30] + '...') if len(i['name']) > 30 else i['name']
            print(f" • {i['quantity']}x {name_trunc:<33} ({i['store_name'].upper():^10}) -> {round(sub, 2):>6}€")
        
        print("-" * 55)
        print(f"💰 TOTAL ESTIMADO: {round(total, 2)}€")
        print("💡 Escribe 'ahorro' para ver si puedes bajar este total.")

    def _show_savings(self):
        """Ejecuta el comparador inteligente de precios basado en el carrito."""
        from app.daos.cart_dao import CartDAO
        print("\n🔍 Analizando precios en otras tiendas...")
        
        try:
            suggestions = CartDAO().get_savings_suggestions(self.auth.current_user_id)
            
            if not suggestions:
                print("\n✨ ¡Excelente! No hemos encontrado alternativas más baratas para tu carrito actual.")
                return

            print("\n💡 OPORTUNIDADES DE AHORRO:")
            print("-" * 65)
            ahorro_total_posible = 0
            
            for s in suggestions:
                # CORRECCIÓN: Usar los nombres de columna exactos definidos en cart_dao.py
                orig_price = s['original_price_norm']
                sugg_price = s['suggestion_price_norm']
                ahorro_unitario = float(s['saving_per_unit'])
                
                print(f"En carrito: {s['original_name'][:35]} ({orig_price}€/u)")
                print(f"👉 Sugerencia: {s['suggestion_name'][:35]} ({sugg_price}€/u)")
                print(f"   Tienda:    {s['store_alt'].upper()}")
                print(f"   Ahorras:   {round(ahorro_unitario, 2)}€ por unidad")
                print("-" * 40)
                ahorro_total_posible += ahorro_unitario

            print(f"💰 AHORRO POTENCIAL TOTAL: {round(ahorro_total_posible, 2)}€")
            print("-" * 65)
        except Exception as e:
            self.log.error(f"Error en sección ahorro: {e}")
            print(f"❌ Error al procesar sugerencias: {e}")