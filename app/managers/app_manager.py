import threading
from app.managers.gui_manager import GUIManager
from app.managers.cart_manager import CartManager
from app.managers.rating_manager import RatingManager # Import
from app.utils.logger_util import HermesLogger
from app.utils.paths_util import SESSION_JSON
from app.utils.json_util import read_json_local
from app.utils.crypto_util import decode_from_base64
from app.utils.update_util import is_latest_version, perform_update
from app.managers.scraper_manager import run_all_scrapers_parallel

class AppManager:
    def __init__(self):
        self.log = HermesLogger.get_logger("APP_MANAGER")
        self.gui = GUIManager(self)
        self.auth = None
        self.cart_manager = CartManager()
        self.rating_manager = RatingManager() # Init

    def start(self):
        try:
            if not is_latest_version():
                self.gui.show_update(perform_update)
            else:
                self.log.info("Iniciando hilo de scraping en background...")
                threading.Thread(target=run_all_scrapers_parallel, daemon=True).start()
                if self._try_autologin():
                    self.show_main()
                else:
                    self.show_login()
        except Exception as e:
            self.log.error(f"Error crítico: {e}")
            self.show_login()
        self.gui.start_loop()

    def _try_autologin(self):
        if not SESSION_JSON.exists(): return False
        try:
            data = read_json_local(SESSION_JSON)
            from app.managers.auth_manager import AuthManager
            if not self.auth: self.auth = AuthManager()
            user = decode_from_base64(data["u"])
            password = decode_from_base64(data["p"])
            success, _ = self.auth.login(user, password)
            return success
        except: return False

    def show_login(self):
        from app.managers.auth_manager import AuthManager
        if not self.auth: self.auth = AuthManager()
        self.gui.show_auth(self.auth, self.show_main)

    def show_main(self):
        self.show_view("search")

    def show_view(self, view_name):
        self.gui.show_view(view_name, self.auth, self._handle_add_to_cart, self.show_product_detail)

    def show_product_detail(self, product):
        def on_rate_callback(p_id, rating):
            if self.auth and self.auth.current_user_id:
                success = self.rating_manager.set_rating(self.auth.current_user_id, p_id, rating)
                if success: self.log.info(f"Valoración exitosa: {rating} para {p_id}")
            else:
                self.log.warning("Usuario no logueado, no se puede valorar")
        
        self.gui.show_product_detail(product, on_back=self.show_main, on_rate=on_rate_callback)

    def _handle_add_to_cart(self, product):
        if self.auth and self.auth.current_user_id:
            self.cart_manager.add_to_cart(self.auth.current_user_id, product['id'])
            self.log.info(f"DB: Añadido {product['name']} al usuario {self.auth.current_user_id}")

    def logout(self):
        if SESSION_JSON.exists():
            try: SESSION_JSON.unlink()
            except: pass
        self.auth = None
        self.show_login()