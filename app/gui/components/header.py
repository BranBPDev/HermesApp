import tkinter as tk
from app.gui.components.visual_elements import ShapeDrawer
from app.gui.styles.styles import COLOR_BG_DARK, COLOR_TEXT_MAIN, COLOR_BADGE_BG, FONT_TITLE

class Header(tk.Frame):
    def __init__(self, master, username, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.username = username
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._draw())

    def _draw(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.canvas.create_text(20, h/2, text=f"Hola, {self.username}!", fill=COLOR_TEXT_MAIN, font=(FONT_TITLE[0], 20, "bold"), anchor="w")
        ShapeDrawer.rounded_rect(self.canvas, w-50, h/2-20, 40, 40, 20, fill=COLOR_BADGE_BG, outline="")