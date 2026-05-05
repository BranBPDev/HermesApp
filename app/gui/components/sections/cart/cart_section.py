import tkinter as tk
from app.gui.components.sections.shared.product_list import ProductList
from app.gui.styles.styles import COLOR_BG_DARK, FONT_TITLE
from app.managers.cart_manager import CartManager
from app.managers.auth_manager import AuthManager # Importamos el manager

class CartSection(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.cm = CartManager()
        self.auth = AuthManager() # Acceso al Singleton
        
        self.user_id = self.auth.current_user_id

        # Título
        self.header = tk.Label(
            self, text="Tu Carrito", font=FONT_TITLE, 
            bg=COLOR_BG_DARK, fg="white", pady=10
        )
        self.header.pack(fill="x")

        # Lista de productos
        self.list_view = ProductList(
            self, 
            fetch_func=self._get_cart_data, 
            on_add=None, 
            empty_text="Tu carrito está vacío."
        )
        self.list_view.pack(fill="both", expand=True, padx=20, pady=10)
        
        # FORZAR REFRESCO INICIAL
        self.refresh()

    def _get_cart_data(self, height):
        if not self.user_id:
            return []
        return self.cm.get_items(self.user_id)

    def refresh(self):
        self.user_id = self.auth.current_user_id
        self.cm.log.info(f"Refrescando CartSection para el usuario: {self.user_id}")
        if not self.user_id:
            self.cm.log.error("CartSection intentó refrescar pero current_user_id es None")
        self.list_view.refresh()