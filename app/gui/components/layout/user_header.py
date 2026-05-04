import tkinter as tk
from app.gui.components.shared.visual_elements import ShapeDrawer
from app.gui.styles.styles import (
    COLOR_BG_DARK, COLOR_TEXT_MAIN, COLOR_BADGE_BG, 
    COLOR_TEXT_DIM, FONT_TITLE, COLOR_ONLINE
)

class UserHeader(tk.Frame):
    def __init__(self, master, username, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK, height=60, **kwargs)
        self.pack_propagate(False)
        self.username = username 

        self.canvas = tk.Canvas(
            self, 
            bg=COLOR_BG_DARK, 
            highlightthickness=0, 
            height=60
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self._draw())

    def _draw(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w < 10: return

        self.canvas.create_text(
            10, h/2, 
            text=f"Hola, {self.username}!", 
            fill=COLOR_TEXT_MAIN, 
            font=(FONT_TITLE[0], 20, "bold"), 
            anchor="w"
        )

        avatar_size = 40
        padding_right = 10
        ax = w - avatar_size - padding_right
        ay = (h - avatar_size) / 2

        ShapeDrawer.rounded_rect(
            self.canvas, ax, ay, avatar_size, avatar_size, 
            avatar_size/2, fill=COLOR_BADGE_BG, outline=""
        )

        self.canvas.create_text(
            ax + (avatar_size/2), ay + (avatar_size/2),
            text="👤", fill=COLOR_TEXT_DIM, font=("Roboto", 18), anchor="center"
        )

        dot_size = 10
        self.canvas.create_oval(
            ax + 30, ay + 30, ax + 30 + dot_size, ay + 30 + dot_size, 
            fill=COLOR_ONLINE, outline=COLOR_BG_DARK, width=2
        )