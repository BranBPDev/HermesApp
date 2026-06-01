import threading
from app.gui.main_window import MainWindow
from app.utils.window_util import center_window
from app.utils.paths_util import LOGO_ICO
from app.gui.components.layout.sidebar import Sidebar
from app.gui.components.layout.user_header import UserHeader

from app.managers.auth_manager import AuthManager
from app.managers.cart_manager import CartManager
from app.managers.product_manager import ProductManager
from app.managers.rating_manager import RatingManager

class GUIManager:
    def __init__(self):
        self.auth = AuthManager()
        self.cart = CartManager()
        self.product = ProductManager()
        self.rating = RatingManager()
        self.root = MainWindow(self)
        self.last_state = {'view': 'search', 'page': 0, 'query': ''}
        self._setup_window()

    def _setup_window(self):
        center_window(self.root, 800, 500, resizable=True)
        self.root.minsize(800, 500)
        if LOGO_ICO.exists():
            try: self.root.iconbitmap(str(LOGO_ICO))
            except: pass

    def show_update(self, perform_update_func):
        from app.gui.components.update.update import Update
        instances = self.root.set_layout([{'class': Update, 'relx': 0, 'relw': 1, 'relh': 1}])
        threading.Thread(target=perform_update_func, args=(instances[0].set_progress,), daemon=True).start()
        self.root.mainloop()

    def start(self):
        """Punto de entrada de la interfaz, decide entre Login o Main."""
        if self.auth.attempt_autologin():
            self.show_main()
        else:
            self.show_auth()
        self.root.mainloop()

    def show_auth(self):
        from app.gui.components.auth.register import Register
        from app.gui.components.auth.login import Login
        self.root.set_layout([
            {'class': Register, 'relx': 0, 'rely': 0, 'relw': 0.5, 'relh': 1,
             'args': {'auth_manager': self.auth, 'on_register_success': self.show_main}},
            {'class': Login, 'relx': 0.5, 'rely': 0, 'relw': 0.5, 'relh': 1,
             'args': {'auth_manager': self.auth, 'on_success': self.show_main}}
        ])

    def logout(self):
        self.auth.logout()
        self.show_auth()

    def show_main(self):
        self.show_view("search", 0, "")

    def show_view(self, view_name, page=0, query=''):
        self.last_state = {'view': view_name, 'page': page, 'query': query}
        user = self.auth.username if self.auth.username else "Usuario"
        
        layout = []
        if view_name == "search":
            from app.gui.components.sections.search.search_section import SearchSection
            layout = [
                {'class': Sidebar, 'relx': 0, 'relw': 0.07, 'relh': 1, 'args': {'current_view': 'search', 'app': self}},
                {'class': UserHeader, 'relx': 0.07, 'relw': 0.93, 'relh': 0.12, 'args': {'username': user}},
                {'class': SearchSection, 'relx': 0.07, 'rely': 0.12, 'relw': 0.93, 'relh': 0.88, 
                 'args': {'on_add': self._handle_add_to_cart, 'on_select': self.show_product_detail, 'page': page, 'initial_query': query}}
            ]
        elif view_name == "cart":
            from app.gui.components.sections.cart.cart_section import CartSection
            layout = [
                {'class': Sidebar, 'relx': 0, 'relw': 0.07, 'relh': 1, 'args': {'current_view': 'cart', 'app': self}},
                {'class': UserHeader, 'relx': 0.07, 'relw': 0.93, 'relh': 0.12, 'args': {'username': user}},
                {'class': CartSection, 'relx': 0.07, 'rely': 0.12, 'relw': 0.93, 'relh': 0.88,
                 'args': {'on_select': self.show_product_detail, 'page': page}}
            ]
        elif view_name == "featured":
            from app.gui.components.sections.featured.featured_section import FeaturedSection
            layout = [
                {'class': Sidebar, 'relx': 0, 'relw': 0.07, 'relh': 1, 'args': {'current_view': 'featured', 'app': self}},
                {'class': UserHeader, 'relx': 0.07, 'relw': 0.93, 'relh': 0.12, 'args': {'username': user}},
                {'class': FeaturedSection, 'relx': 0.07, 'rely': 0.12, 'relw': 0.93, 'relh': 0.88,
                 'args': {'on_add': self._handle_add_to_cart, 'on_select': self.show_product_detail, 'page': page}}
            ]
        self.root.set_layout(layout)

    def show_product_detail(self, product):
        from app.gui.components.common.product_detail import ProductDetail
        
        # EXTRACCIÓN SEGURA: Previene crashes si venimos de la vista Cart
        p_id = product.get("id") or product.get("product_id")

        if self.auth.current_user_id and p_id is not None:
            product["user_rating"] = self.rating.get_user_rating(self.auth.current_user_id, p_id)

        # Capturamos el estado real actual antes de cambiar de vista
        current_page = self.last_state['page']
        current_query = self.last_state['query']
        current_view = self.last_state['view']

        for instance in self.root.active_instances:
            if hasattr(instance, 'get_current_page'):
                current_page = instance.get_current_page()
            if hasattr(instance, 'get_query'):
                current_query = instance.get_query()

        self.root.set_layout([
            {'class': ProductDetail, 'relx': 0, 'rely': 0, 'relw': 1, 'relh': 1,
             'args': {
                 'product': product, 
                 'on_back': lambda: self.show_view(current_view, current_page, current_query), 
                 'on_rate': self._handle_rate
             }}
        ])

    def _handle_add_to_cart(self, product):
        if self.auth.current_user_id:
            p_id = product.get("id") or product.get("product_id")
            self.cart.add_to_cart(self.auth.current_user_id, p_id)

    def _handle_rate(self, p_id, rating):
        if self.auth.current_user_id and p_id is not None:
            self.rating.set_rating(self.auth.current_user_id, p_id, rating)