import tkinter as tk
from app.gui.components.visual_elements import CInput

class SearchComponent(tk.Frame):
    def __init__(self, master, on_search, **kwargs):
        super().__init__(master, bg="#0F0F0F")
        self.canvas = tk.Canvas(self, bg="#0F0F0F", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.search_input = CInput(self.canvas, "BUSCAR EN EL MERCADO", "Producto...")
        self.canvas.bind("<Configure>", lambda e: self.draw())

    def draw(self):
        self.canvas.delete("all")
        # El buscador se posiciona arriba a la izquierda del área de contenido
        self.search_input.draw(20, 20)

    def get_query(self): return self.search_input.get()