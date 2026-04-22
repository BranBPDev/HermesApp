import tkinter as tk
from app.gui.styles.styles import COLOR_BG_DARK, COLOR_BG_SIDE, COLOR_PRIMARY

class HermesMainView(tk.Frame):
    def __init__(self, master, app_manager):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.app = app_manager
        
        # Sidebar (Canvas)
        self.sidebar = tk.Canvas(self, width=70, bg=COLOR_BG_SIDE, highlightthickness=0)
        self.sidebar.pack(side="left", fill="y")
        
        # Contenedor de contenido
        self.content_area = tk.Frame(self, bg=COLOR_BG_DARK)
        self.content_area.pack(side="right", expand=True, fill="both")
        
        self._draw_sidebar()

    def _draw_sidebar(self):
        # Dibujamos los iconos como texto o formas en el canvas
        self.sidebar.create_text(35, 50, text="🔍", font=("Roboto", 20), fill=COLOR_PRIMARY)
        self.sidebar.create_text(35, 110, text="🛒", font=("Roboto", 20), fill="white")
        
        # Botón logout abajo
        self.sidebar.create_text(35, self.winfo_height()-40, text="⏻", fill="#FF4444")