import traceback
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
        self.root = MainWindow(self)
        center_window(self.root, 1000, 650, resizable=True)
        if LOGO_ICO.exists():
            try: self.root.iconbitmap(str(LOGO_ICO))
            except: pass
        self.auth = None

    def start(self):
        try:
            if not is_latest_version():
                self.show_update()
            elif self._try_autologin():
                self.show_main()
            else:
                self.show_login()
        except:
            self.show_login()
        self.root.mainloop()

    def _try_autologin(self):
        if not SESSION_JSON.exists(): return False
        try:
            data = read_json_local(SESSION_JSON)
            from app.managers.auth_manager import AuthManager
            if not self.auth: self.auth = AuthManager()
            return self.auth.login(decode_from_base64(data["u"]), decode_from_base64(data["p"]))[0]
        except: return False

    def show_update(self):
        from app.gui.components.update import Update
        # Componente único centrado
        instances = self.root.set_layout([{'class': Update, 'relx': 0, 'relw': 1, 'relh': 1}])
        threading.Thread(target=perform_update, args=(instances[0].set_progress,), daemon=True).start()

    def show_login(self):
        from app.gui.components.brand import Brand
        from app.gui.components.auth import Auth
        from app.managers.auth_manager import AuthManager
        if not self.auth: self.auth = AuthManager()

        self.root.set_layout([
            {'class': Brand, 'relx': 0, 'relw': 0.5, 'relh': 1},
            {'class': Auth, 'relx': 0.5, 'relw': 0.5, 'relh': 1, 'args': {'on_submit': self._handle_login}}
        ])
        self.root.bind("<Return>", lambda e: self._handle_login())

    def _handle_login(self):
        auth_comp = self.root.active_instances[1]
        u, p = auth_comp.get_data()
        success, msg = self.auth.login(u, p)
        if success: self.show_main()
        else: auth_comp.show_error(msg)

    def show_main(self):
        self.show_view("search")

    def show_view(self, view_name):
        from app.gui.components.sidebar import Sidebar
        from app.gui.components.header import Header
        user = self.auth.username if self.auth else "Usuario"

        if view_name == "search":
            from app.gui.components.search import Search
            self.root.set_layout([
                {'class': Sidebar, 'relx': 0, 'relw': 0.07, 'relh': 1},
                {'class': Header, 'relx': 0.07, 'relw': 0.93, 'relh': 0.1, 'args': {'username': user}},
                {'class': Search, 'relx': 0.07, 'rely': 0.1, 'relw': 0.93, 'relh': 0.9, 
                 'args': {'on_add': self._handle_add_to_cart}}
            ])
            self.root.bind("<Return>", lambda e: self.root.active_instances[2].execute_search())
        
        elif view_name == "cart":
            from app.gui.components.cart import Cart
            self.root.set_layout([
                {'class': Sidebar, 'relx': 0, 'relw': 0.07, 'relh': 1},
                {'class': Header, 'relx': 0.07, 'relw': 0.93, 'relh': 0.1, 'args': {'username': user}},
                {'class': Cart, 'relx': 0.07, 'rely': 0.1, 'relw': 0.93, 'relh': 0.9}
            ])

    def _handle_add_to_cart(self, product):
        self.log.info(f"Añadido: {product.get('name')}")

    def logout(self):
        if SESSION_JSON.exists(): SESSION_JSON.unlink()
        self.auth = None
        self.show_login()