import tkinter as tk
from app.gui.styles.styles import COLOR_BG_DARK

class CartView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLOR_BG_DARK)
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.bind("<Configure>", self._draw_empty_state)

    def _draw_empty_state(self, event=None):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        
        self.canvas.create_text(
            w/2, h/2 - 20, 
            text="🛒 Tu carrito está vacío", 
            font=("Roboto", 18, "bold"), fill="#666666"
        )
        
        self.canvas.create_text(
            w/2, h/2 + 20, 
            text="Añade productos desde la búsqueda para empezar.", 
            font=("Roboto", 12), fill="#444444"
        )