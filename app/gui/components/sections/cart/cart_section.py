import tkinter as tk
from app.gui.components.common.product_list import ProductList
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

        # Lista de productos: show_action_btn=False porque ya están en el carrito
        self.list_view = ProductList(
            self, 
            get_items_func=self._get_cart_data, 
            on_action=None, 
            on_select=self.on_select,
            show_action_btn=False,
            pm_ref=self.pm,
            empty_text="Tu carrito está vacío."
        )
        self.list_view.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Disparar refresco inicial
        self.after(100, self.refresh)

    def _get_cart_data(self, height):
        self.pm.page_size = max(1, int((height - 60) // 65))
        self.user_id = self.auth.current_user_id
        if not self.user_id:
            return []
        return self.cm.get_items(self.user_id)

    def refresh(self):
        self.user_id = self.auth.current_user_id
        self.cm.log.info(f"Refrescando vista de carrito para usuario: {self.user_id}")
        self.update_idletasks()
        
        self.list_view.refresh()