import tkinter as tk
from app.gui.components.sections.shared.product_list import ProductList
from app.gui.styles.styles import COLOR_BG_DARK, FONT_TITLE
from app.managers.cart_manager import CartManager

class CartSection(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.cm = CartManager()
        
        # Obtenemos el user_id de forma segura
        app_manager = self.master.master.app
        self.user_id = app_manager.auth.current_user_id

        # Título
        self.header = tk.Label(
            self, text="Tu Carrito", font=FONT_TITLE, 
            bg=COLOR_BG_DARK, fg="white", pady=10
        )
        self.header.pack(fill="x")

        # El componente de lista debe expandirse para ser visible
        self.list_view = ProductList(
            self, 
            fetch_func=self._get_cart_data, 
            on_add=None, 
            empty_text="Tu carrito está vacío."
        )
        self.list_view.pack(fill="both", expand=True, padx=20, pady=10)

    def _get_cart_data(self, height):
        # El manager ya loguea esta acción
        return self.cm.get_items(self.user_id)

    def refresh(self):
        self.list_view.refresh()