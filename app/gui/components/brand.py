import tkinter as tk
from PIL import Image, ImageTk
from app.utils.paths_util import LOGO_PNG
from app.gui.styles.styles import COLOR_BG_SIDE, COLOR_TEXT_MAIN, FONT_BRAND, SIDEBAR_RATIO, Y_OFF

class Brand(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_BG_SIDE)
        self.canvas = tk.Canvas(self, bg=COLOR_BG_SIDE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.logo_img_tk = None
        self._load_assets()
        self.canvas.bind("<Configure>", lambda e: self._render())

    def _load_assets(self):
        try:
            # Reutilizamos tu lógica de carga de imagen
            img = Image.open(str(LOGO_PNG)).resize((180, 180), Image.Resampling.LANCZOS)
            self.logo_img_tk = ImageTk.PhotoImage(img)
        except: pass

    def _render(self, event=None):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        cy = h / 2

        # Dibujar logo y texto de marca usando tus offsets
        if self.logo_img_tk:
            self.canvas.create_image(w / 2, cy + Y_OFF["LOGO"], image=self.logo_img_tk)
        
        self.canvas.create_text(w / 2, cy + Y_OFF["BRAND"], text="HERMESAPP", 
                               fill=COLOR_TEXT_MAIN, font=FONT_BRAND)