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

    def show_auth(self, auth_manager, on_login_success):
        from app.gui.components.auth.register import Register
        from app.gui.components.auth.login import Login
        # En login no queremos sidebar, usamos un layout limpio
        for w in self.root.winfo_children(): w.pack_forget(); w.place_forget()
        
        f1 = tk.Frame(self.root, bg="#0F0F0F")
        f1.place(relx=0, relw=0.5, relh=1)
        Register(f1, auth_manager=auth_manager, on_register_success=on_login_success, logo=LOGO_PNG).pack(fill="both", expand=True)
        
        f2 = tk.Frame(self.root, bg="#0F0F0F")
        f2.place(relx=0.5, relw=0.5, relh=1)
        Login(f2, auth_manager=auth_manager, on_success=on_login_success, logo=LOGO_PNG).pack(fill="both", expand=True)

    def show_main_layout(self, auth_manager):
        user = auth_manager.username if auth_manager else "Usuario"
        self.root.set_static_layout(Sidebar, UserHeader, {'username': user})

    def show_view(self, view_name, on_add_func):
        if view_name == "search":
            from app.gui.components.sections.search.search_section import SearchSection
            self.root.set_view(SearchSection, {'on_add': on_add_func})
        elif view_name == "cart":
            from app.gui.components.sections.cart.cart_section import CartSection
            self.root.set_view(CartSection, {})

    def start_loop(self):
        self.root.mainloop()