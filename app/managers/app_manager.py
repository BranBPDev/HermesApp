import threading
from app.gui.main_window import MainWindow
from app.utils.logger_util import HermesLogger
from app.utils.window_util import center_window
from app.utils.paths_util import LOGO_ICO, SESSION_JSON
from app.utils.json_util import read_json_local
from app.utils.crypto_util import decode_from_base64
from app.utils.update_util import is_latest_version, perform_update

class AppManager:
    def __init__(self):
        self.log = HermesLogger.get_logger("APP_MANAGER")
        self.log.info("Inicializando AppManager...")
        
        self.root = MainWindow(self)
        self.log.info("MainWindow instanciada correctamente.")
        
        center_window(self.root, 800, 500, resizable=True)
        self.root.minsize(800, 500)
        
        if LOGO_ICO.exists():
            try: 
                self.root.iconbitmap(str(LOGO_ICO))
                self.log.info(f"Icono de aplicación cargado desde: {LOGO_ICO}")
            except Exception as e: 
                self.log.error(f"Error al cargar el icono: {e}")
        
        self.auth = None

    def start(self):
        self.log.info("Iniciando flujo de la aplicación...")
        try:
            if not is_latest_version(): 
                self.log.info("Versión desactualizada detectada. Redirigiendo a pantalla de actualización.")
                self.show_update()
            elif self._try_autologin(): 
                self.log.info("Autologin exitoso. Entrando a la vista principal.")
                self.show_main()
            else: 
                self.log.info("Autologin fallido o inexistente. Redirigiendo a login.")
                self.show_login()
        except Exception as e: 
            self.log.error(f"Error crítico en el inicio: {e}")
            self.show_login()
            
        self.log.info("Lanzando bucle principal (mainloop) de la interfaz.")
        self.root.mainloop()

    def _try_autologin(self):
        self.log.info("Intentando autologin desde sesión guardada...")
        if not SESSION_JSON.exists(): 
            self.log.info("No existe archivo de sesión local.")
            return False
        try:
            data = read_json_local(SESSION_JSON)
            self.log.info("Archivo de sesión leído. Decodificando credenciales...")
            
            from app.managers.auth_manager import AuthManager
            if not self.auth: 
                self.auth = AuthManager()
                self.log.info("AuthManager inicializado para autologin.")
            
            user = decode_from_base64(data["u"])
            password = decode_from_base64(data["p"])
            
            success, message = self.auth.login(user, password)
            if success:
                self.log.info(f"Autologin exitoso para el usuario: {user}")
            else:
                self.log.warning(f"Autologin rechazado: {message}")
            return success
        except Exception as e: 
            self.log.error(f"Error durante el proceso de autologin: {e}")
            return False

    def show_update(self):
        self.log.info("Cargando componente de actualización en la interfaz...")
        from app.gui.components.shared.update import Update
        instances = self.root.set_layout([{'class': Update, 'relx': 0, 'relw': 1, 'relh': 1}])
        
        self.log.info("Iniciando hilo secundario para la ejecución de la actualización (daemon=True).")
        threading.Thread(target=perform_update, args=(instances[0].set_progress,), daemon=True).start()

    def show_login(self):
        self.log.info("Cargando vista de autenticación (Registro y Login)...")
        from app.gui.components.auth.register import Register
        from app.gui.components.auth.login import Login
        from app.managers.auth_manager import AuthManager
        from app.utils.paths_util import LOGO_PNG

        if not self.auth: 
            self.auth = AuthManager()
            self.log.info("AuthManager inicializado para la vista de login.")

        self.root.set_layout([
            {'class': Register, 'relx': 0, 'rely': 0, 'relw': 0.5, 'relh': 1,
             'args': {'auth_manager': self.auth, 'on_register_success': self.show_main, 'logo': LOGO_PNG}},
            {'class': Login, 'relx': 0.5, 'rely': 0, 'relw': 0.5, 'relh': 1,
             'args': {'auth_manager': self.auth, 'on_success': self.show_main, 'logo': LOGO_PNG}}
        ])
        self.log.info("Layout de login aplicado correctamente.")

    def show_main(self):
        self.log.info("Redirigiendo a la vista principal (search).")
        self.show_view("search")

    def show_view(self, view_name):
        self.log.info(f"Cambiando vista activa a: {view_name}")
        from app.gui.components.layout.sidebar import Sidebar
        from app.gui.components.header import Header
        user = self.auth.username if self.auth else "Usuario"

        if view_name == "search":
            from app.gui.components.sections.search.search_section import Search
            self.root.set_layout([
                {'class': Sidebar, 'relx': 0, 'relw': 0.07, 'relh': 1},
                {'class': Header, 'relx': 0.07, 'relw': 0.93, 'relh': 0.12, 'args': {'username': user}},
                {'class': Search, 'relx': 0.07, 'rely': 0.12, 'relw': 0.93, 'relh': 0.88, 
                 'args': {'on_add': self._handle_add_to_cart}}
            ])
            self.log.info("Vista 'search' renderizada.")
        elif view_name == "cart":
            from app.gui.components.sections.cart.cart_section import Cart
            self.root.set_layout([
                {'class': Sidebar, 'relx': 0, 'relw': 0.07, 'relh': 1},
                {'class': Header, 'relx': 0.07, 'relw': 0.93, 'relh': 0.12, 'args': {'username': user}},
                {'class': Cart, 'relx': 0.07, 'rely': 0.12, 'relw': 0.93, 'relh': 0.88}
            ])
            self.log.info("Vista 'cart' renderizada.")

    def _handle_add_to_cart(self, product):
        product_name = product.get('name', 'Desconocido')
        self.log.info(f"Producto añadido al carrito: {product_name}")

    def logout(self):
        self.log.info("Iniciando proceso de cierre de sesión...")
        if SESSION_JSON.exists(): 
            try:
                SESSION_JSON.unlink()
                self.log.info(f"Archivo de sesión eliminado: {SESSION_JSON}")
            except Exception as e:
                self.log.error(f"Error al eliminar el archivo de sesión: {e}")
        
        self.auth = None
        self.log.info("Estado de autenticación reseteado. Volviendo a login.")
        self.show_login()