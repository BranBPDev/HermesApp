import tkinter as tk
from app.gui.styles.styles import COLOR_BG_DARK, COLOR_TEXT_MAIN, FONT_TITLE

class Header(tk.Frame):
    def __init__(self, master, username, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.username = username
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._draw())

    def _draw(self):
        self.canvas.delete("all")
        h = self.canvas.winfo_height()
        self.canvas.create_text(20, h/2, text=f"Hola, {self.username}", fill=COLOR_TEXT_MAIN, font=FONT_TITLE, anchor="w")