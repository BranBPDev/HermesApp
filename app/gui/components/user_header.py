import tkinter as tk
from app.gui.styles.styles import FONT_TITLE, COLOR_BG_DARK

class UserHeader(tk.Frame):
    def __init__(self, master, username, **kwargs):
        # Cambiado a tk.Frame estándar
        super().__init__(master, bg=COLOR_BG_DARK, height=60, **kwargs)
        self.pack_propagate(False)
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.username = username
        self.bind("<Configure>", lambda e: self._draw())

    def _draw(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        mid_y = 30

        # Texto de bienvenida
        self.canvas.create_text(
            10, mid_y, 
            text=f"Hola, {self.username}!", 
            font=(FONT_TITLE[0], 18, "bold"), 
            fill="white", anchor="w"
        )

        # Avatar
        avatar_x = w - 30
        self.canvas.create_oval(avatar_x-20, mid_y-20, avatar_x+20, mid_y+20, fill="#252525", outline="")
        self.canvas.create_text(avatar_x, mid_y, text="👤", font=("Roboto", 20), fill="white")