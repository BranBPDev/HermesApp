import tkinter as tk
from app.gui.styles.styles import COLOR_BG_DARK, COLOR_PRIMARY

class UpdateView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.progress = 0

    def set_progress(self, val, text):
        self.progress = val
        self._draw(text)

    def _draw(self, text):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        
        # Barra de progreso
        bw, bh = 400, 10
        x, y = (w-bw)/2, h/2
        
        # Fondo barra
        self.canvas.create_rectangle(x, y, x+bw, y+bh, fill="#222222", outline="")
        # Progreso
        self.canvas.create_rectangle(x, y, x+(bw*self.progress), y+bh, fill=COLOR_PRIMARY, outline="")
        # Texto
        self.canvas.create_text(w/2, y+40, text=text, fill="white")