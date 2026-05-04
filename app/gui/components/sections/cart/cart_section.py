import tkinter as tk
from app.gui.components.sections.shared.product_list import ProductList
from app.gui.styles.styles import COLOR_BG_DARK, FONT_TITLE
from app.managers.cart_manager import CartManager

class CartSection(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.cm = CartManager()
        
        # Obtenemos el user_id del AuthManager a través del AppManager
        self.user_id = self.master.master.app.auth.user_id

        # Título de la sección
        self.header = tk.Label(
            self, text="Tu Carrito", font=FONT_TITLE, 
            bg=COLOR_BG_DARK, fg="white", pady=10
        )
        self.header.pack(fill="x")

        # Reutilizamos ProductList para mostrar el contenido del carrito
        # Pasamos None en on_add porque en el carrito quizás quieras 'eliminar' o nada
        self.list_view = ProductList(
            self, 
            fetch_func=self._get_cart_data, 
            on_add=None, 
            empty_text="Tu carrito está vacío."
        )
        self.list_view.pack(fill="both", expand=True)

    def _get_cart_data(self, height):
        # Ignoramos height aquí ya que el carrito suele ser una lista corta
        # pero mantenemos la firma para que ProductList no rompa
        return self.cm.get_items(self.user_id)

    def refresh(self):
        self.list_view.refresh()