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
        center_window(self.root, 800, 500, resizable=True)
        self.root.minsize(800, 500)
        if LOGO_ICO.exists():
            try: self.root.iconbitmap(str(LOGO_ICO))
            except: pass
        self.auth = None

    def start(self):
        try:
            if not is_latest_version(): self.show_update()
            elif self._try_autologin(): self.show_main()
            else: self.show_login()
        except: self.show_login()
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
        instances = self.root.set_layout([{'class': Update, 'relx': 0, 'relw': 1, 'relh': 1}])
        threading.Thread(target=perform_update, args=(instances[0].set_progress,), daemon=True).start()

    def show_login(self):
        from app.gui.components.register import Register
        from app.gui.components.login import Login
        from app.managers.auth_manager import AuthManager
        from app.utils.paths_util import LOGO_PNG
        import tkinter as tk

        if not self.auth: self.auth = AuthManager()

        self.root.set_layout([
            {'class': Register, 'relx': 0, 'rely': 0, 'relw': 0.5, 'relh': 1,
             'args': {'auth_manager': self.auth, 'on_register_success': self.show_main}},
            {'class': Login, 'relx': 0.5, 'rely': 0, 'relw': 0.5, 'relh': 1,
             'args': {'auth_manager': self.auth, 'on_success': self.show_main}}
        ])

        try:
            self.img_logo = tk.PhotoImage(file=str(LOGO_PNG))
            logo_lbl = tk.Label(self.root, image=self.img_logo, bg=self.root["bg"], bd=0, highlightthickness=0)
            logo_lbl.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            self.log.error(f"No se pudo cargar el logo central: {e}")

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
                {'class': Header, 'relx': 0.07, 'relw': 0.93, 'relh': 0.12, 'args': {'username': user}},
                {'class': Search, 'relx': 0.07, 'rely': 0.12, 'relw': 0.93, 'relh': 0.88, 
                 'args': {'on_add': self._handle_add_to_cart}}
            ])
        elif view_name == "cart":
            from app.gui.components.cart import Cart
            self.root.set_layout([
                {'class': Sidebar, 'relx': 0, 'relw': 0.07, 'relh': 1},
                {'class': Header, 'relx': 0.07, 'relw': 0.93, 'relh': 0.12, 'args': {'username': user}},
                {'class': Cart, 'relx': 0.07, 'rely': 0.12, 'relw': 0.93, 'relh': 0.88}
            ])

    def _handle_add_to_cart(self, product):
        self.log.info(f"Añadido: {product.get('name')}")

    def logout(self):
        if SESSION_JSON.exists(): SESSION_JSON.unlink()
        self.auth = None
        self.show_login()