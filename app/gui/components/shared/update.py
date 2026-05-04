import tkinter as tk
from app.gui.styles.styles import COLOR_PRIMARY

class Update(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="#0F0F0F")
        self.canvas = tk.Canvas(self, bg="#0F0F0F", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.prog, self.txt = 0, "Iniciando..."

    def set_progress(self, val, text):
        self.prog, self.txt = val, text
        self._draw()

    def _draw(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.canvas.create_rectangle(w/2-200, h/2, w/2+200, h/2+10, fill="#222")
        self.canvas.create_rectangle(w/2-200, h/2, w/2-200+(400*self.prog), h/2+10, fill=COLOR_PRIMARY)
        self.canvas.create_text(w/2, h/2+40, text=self.txt, fill="white")