import tkinter as tk
from app.gui.styles.styles import COLOR_BG_SIDE, COLOR_PRIMARY

class Sidebar(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_BG_SIDE)
        self.canvas = tk.Canvas(self, bg=COLOR_BG_SIDE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._draw())

    def _draw(self):
        self.canvas.delete("all")
        self.canvas.create_text(35, 50, text="🔍", font=("Roboto", 20), fill=COLOR_PRIMARY, tags="s")
        self.canvas.create_text(35, 110, text="🛒", font=("Roboto", 20), fill="white", tags="c")
        self.canvas.tag_bind("s", "<Button-1>", lambda e: self.master.master.app.show_view("search"))
        self.canvas.tag_bind("c", "<Button-1>", lambda e: self.master.master.app.show_view("cart"))