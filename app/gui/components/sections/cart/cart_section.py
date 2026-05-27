import tkinter as tk
from app.gui.components.sections.shared.product_list import ProductList
from app.gui.styles.styles import COLOR_BG_DARK, FONT_TITLE
from app.managers.cart_manager import CartManager
from app.managers.auth_manager import AuthManager

class CartSection(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.cm = CartManager()
        self.auth = AuthManager()
        self.user_id = self.auth.current_user_id

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
            show_action_btn=False,
            empty_text="Tu carrito está vacío."
        )
        self.list_view.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Eliminado self.refresh() directo para evitar el doble dibujado inicial con H=1

    def _get_cart_data(self, height):
        self.user_id = self.auth.current_user_id
        if not self.user_id:
            return []
        return self.cm.get_items(self.user_id)

    def refresh(self):
        self.user_id = self.auth.current_user_id
        self.cm.log.info(f"Refrescando vista de carrito para usuario: {self.user_id}")
        self.update_idletasks()
        
        self.list_view.refresh()