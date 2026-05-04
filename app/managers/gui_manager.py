import threading
from app.gui.main_window import MainWindow
from app.utils.window_util import center_window
from app.utils.paths_util import LOGO_ICO, LOGO_PNG
from app.gui.components.layout.sidebar import Sidebar
from app.gui.components.layout.user_header import UserHeader

class GUIManager:
    def __init__(self, app_manager):
        self.app = app_manager
        self.root = MainWindow(self.app)
        self._setup_window()

    def _setup_window(self):
        center_window(self.root, 800, 500, resizable=True)
        self.root.minsize(800, 500)
        if LOGO_ICO.exists():
            try: self.root.iconbitmap(str(LOGO_ICO))
            except: pass

    def show_update(self, perform_update_func):
        from app.gui.components.shared.update import Update
        instances = self.root.set_layout([{'class': Update, 'relx': 0, 'relw': 1, 'relh': 1}])
        threading.Thread(target=perform_update_func, args=(instances[0].set_progress,), daemon=True).start()

    def show_auth(self, auth_manager, on_login_success):
        from app.gui.components.auth.register import Register
        from app.gui.components.auth.login import Login
        self.root.set_layout([
            {'class': Register, 'relx': 0, 'rely': 0, 'relw': 0.5, 'relh': 1,
             'args': {'auth_manager': auth_manager, 'on_register_success': on_login_success, 'logo': LOGO_PNG}},
            {'class': Login, 'relx': 0.5, 'rely': 0, 'relw': 0.5, 'relh': 1,
             'args': {'auth_manager': auth_manager, 'on_success': on_login_success, 'logo': LOGO_PNG}}
        ])

    def show_view(self, view_name, auth_manager, on_add_func):
        user = auth_manager.username if auth_manager else "Usuario"
        
        if view_name == "search":
            from app.gui.components.sections.search.search_section import SearchSection
            layout = [
                {'class': Sidebar, 'relx': 0, 'relw': 0.07, 'relh': 1, 'args': {'active_tab': 'search'}},
                {'class': UserHeader, 'relx': 0.07, 'relw': 0.93, 'relh': 0.12, 'args': {'username': user}},
                {'class': SearchSection, 'relx': 0.07, 'rely': 0.12, 'relw': 0.93, 'relh': 0.88, 
                 'args': {'on_add': on_add_func}}
            ]
        elif view_name == "cart":
            from app.gui.components.sections.cart.cart_section import CartSection
            layout = [
                {'class': Sidebar, 'relx': 0, 'relw': 0.07, 'relh': 1, 'args': {'active_tab': 'cart'}},
                {'class': UserHeader, 'relx': 0.07, 'relw': 0.93, 'relh': 0.12, 'args': {'username': user}},
                {'class': CartSection, 'relx': 0.07, 'rely': 0.12, 'relw': 0.93, 'relh': 0.88}
            ]
        
        self.root.set_layout(layout)

    def start_loop(self):
        self.root.mainloop()