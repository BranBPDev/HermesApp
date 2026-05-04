import tkinter as tk
from app.gui.components.sections.shared.product_list import ProductList
from app.gui.styles.styles import COLOR_BG_DARK, COLOR_TEXT_MAIN, FONT_TITLE

class CartSection(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        
        # Título simple
        lbl = tk.Label(self, text="MI CARRITO", fg=COLOR_TEXT_MAIN, bg=COLOR_BG_DARK, font=FONT_TITLE)
        lbl.pack(pady=20)

        # Reutilizamos ProductList con datos del carrito (ejemplo mock o manager)
        self.list_view = ProductList(
            self, 
            get_items_func=lambda h: [], # Aquí llamarías a CartManager.get_items()
            on_action=lambda p: print("Eliminar"),
            empty_text="Tu carrito está vacío"
        )
        self.list_view.pack(fill="both", expand=True)