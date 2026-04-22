import tkinter as tk
from app.gui.components.visual_elements import CButton, CInput
from app.gui.styles.styles import COLOR_BG_DARK, COLOR_PRIMARY
from app.daos.product_dao import ProductDAO

class SearchView(tk.Frame):
    def __init__(self, master, on_add_to_cart):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.on_add_to_cart = on_add_to_cart
        self.products = []
        self.dao = ProductDAO()
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._render)

    def _render(self, event=None):
        self.canvas.delete("all")
        self.search_input = CInput(self.canvas, 30, 40, 400, 40, "BUSCAR PRODUCTO")
        self.search_input.draw()
        
        CButton(self.canvas, 450, 40, 100, 40, "BUSCAR", self.execute_search).draw()
        
        if self.products:
            self.render_results(self.products)
        else:
            self.canvas.create_text(30, 120, text="Escribe algo y pulsa buscar...", fill="#555555", anchor="w")

    def execute_search(self):
        query = self.search_input.get_value()
        if query:
            self.products = self.dao.search_by_tag(query)
            self._render()

    def render_results(self, products):
        for i, prod in enumerate(products):
            y_pos = 120 + (i * 65)
            self._draw_product_row(prod, y_pos)

    def _draw_product_row(self, prod, y):
        tag = f"row_{id(prod)}"
        # Fondo estilizado
        self.canvas.create_rectangle(30, y, 750, y+55, fill="#181818", outline="", tags=tag)
        # Datos
        self.canvas.create_text(50, y+27, text=prod['name'], fill="white", anchor="w", font=("Roboto", 11))
        self.canvas.create_text(500, y+27, text=f"{prod['price']} €", fill=COLOR_PRIMARY, font=("Roboto", 12, "bold"))
        self.canvas.create_text(600, y+27, text=prod.get('store_name', '').upper(), fill="#888888", font=("Roboto", 9))
        
        CButton(self.canvas, 660, y+12, 80, 30, "Añadir", lambda p=prod: self.on_add_to_cart(p)).draw()