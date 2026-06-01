import tkinter as tk
from app.gui.components.common.product_list import ProductList
from app.gui.components.common.feedback_toast import FeedbackToast
from app.gui.styles.styles import COLOR_BG_DARK, FONT_TITLE
from app.managers.cart_manager import CartManager
from app.managers.auth_manager import AuthManager
from app.managers.product_manager import ProductManager

class CartSection(tk.Frame):
    def __init__(self, master, on_select, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.cm = CartManager()
        self.auth = AuthManager()
        self.pm = ProductManager()
        self.user_id = self.auth.current_user_id
        self.on_select = on_select

        # Título
        self.header = tk.Label(
            self, text="Tu Carrito", font=FONT_TITLE, 
            bg=COLOR_BG_DARK, fg="white", pady=10
        )
        self.header.pack(fill="x")

        # Toast para feedback
        self.toast = FeedbackToast(self)
        self.toast.pack(fill="x", side="bottom")

        # Lista de productos
        self.list_view = ProductList(
            self, 
            get_items_func=self._get_cart_data, 
            on_action=self._handle_remove,
            on_select=self.on_select,
            show_action_btn=True,
            action_icon="-",
            pm_ref=None,
            empty_text="Tu carrito está vacío."
        )
        self.list_view.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.after(100, self.refresh)

    def _get_cart_data(self, height):
        self.user_id = self.auth.current_user_id
        if not self.user_id: return []
        
        all_items = self.cm.get_items(self.user_id)
        page_size = max(1, int((height - 120) // 65))
        
        # Sincronizamos límites con la página actual del componente
        total_pages = (len(all_items) + page_size - 1) // page_size
        self.list_view.total_pages = max(1, total_pages)
        
        # Si la página actual es inválida tras eliminar, volvemos a la anterior
        if self.list_view.current_page >= self.list_view.total_pages:
            self.list_view.current_page = max(0, self.list_view.total_pages - 1)
            
        start = self.list_view.current_page * page_size
        end = start + page_size
        
        return all_items[start:end]

    def _handle_remove(self, prod):
        if self.user_id:
            success = self.cm.remove_from_cart(self.user_id, prod.get('product_id'))
            if success:
                self.toast.show(f"✓ Eliminado: {prod.get('name', 'Producto')[:25]}...")
                self.refresh()

    def refresh(self):
        self.update_idletasks()
        self.list_view.refresh()