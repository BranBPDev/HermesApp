import tkinter as tk
from app.gui.components.visual_elements import CButton, CInput
from app.gui.styles.styles import COLOR_BG_DARK

class SearchView(tk.Frame):
    def __init__(self, master, on_add_to_cart):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.on_add_to_cart = on_add_to_cart
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.bind("<Configure>", self._render_initial)

    def _render_initial(self, event=None):
        self.canvas.delete("all")
        # Input de búsqueda integrado en el canvas
        self.search_input = CInput(self.canvas, 20, 40, 300, 35, "BUSCAR PRODUCTO")
        self.search_input.draw()
        
        btn_search = CButton(self.canvas, 330, 40, 100, 35, "BUSCAR", self.execute_search)
        btn_search.draw()

    def execute_search(self):
        # Lógica de búsqueda (placeholder)
        pass

    def render_results(self, products):
        # Limpiar solo el área de resultados si fuera necesario
        self.canvas.delete("result_item")
        for i, prod in enumerate(products):
            y_pos = 100 + (i * 50)
            self._draw_product_row(prod, y_pos)

    def _draw_product_row(self, prod, y):
        # Dibujamos directamente en el canvas principal
        self.canvas.create_text(25, y+15, text=prod['name'], fill="white", anchor="w", tags="result_item")
        btn = CButton(self.canvas, 400, y, 80, 30, "Añadir", 
                          lambda p=prod: self.on_add_to_cart(p))
        btn.draw()