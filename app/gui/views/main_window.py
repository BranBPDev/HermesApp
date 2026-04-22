import tkinter as tk
from app.gui.styles.styles import COLOR_BG_DARK, COLOR_BG_SIDE, COLOR_PRIMARY
from app.gui.views.user_header import UserHeader

class HermesMainView(tk.Frame):
    def __init__(self, master, app_manager):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.app = app_manager
        
        # Header de usuario (RECUPERADO)
        self.header = UserHeader(self, username="Usuario")
        self.header.pack(side="top", fill="x")
        
        # Sidebar
        self.sidebar = tk.Canvas(self, width=70, bg=COLOR_BG_SIDE, highlightthickness=0)
        self.sidebar.pack(side="left", fill="y")
        
        # Contenedor principal
        self.content_area = tk.Frame(self, bg=COLOR_BG_DARK)
        self.content_area.pack(side="right", expand=True, fill="both")
        
        self.sidebar.bind("<Configure>", lambda e: self._draw_sidebar())

    def _draw_sidebar(self):
        self.sidebar.delete("all")
        w = 70
        h = self.sidebar.winfo_height()
        
        # Iconos de Navegación (Ahora con tags para clics)
        self._create_nav_btn(35, 50, "🔍", "search", COLOR_PRIMARY)
        self._create_nav_btn(35, 110, "🛒", "cart", "white")
        
        # Botón Logout (RECUPERADO)
        self.sidebar.create_text(35, h-40, text="⏻", font=("Roboto", 20), fill="#FF4444", tags="logout")
        self.sidebar.tag_bind("logout", "<Button-1>", lambda e: self.app.logout())
        self.sidebar.tag_bind("logout", "<Enter>", lambda e: self.sidebar.config(cursor="hand2"))
        self.sidebar.tag_bind("logout", "<Leave>", lambda e: self.sidebar.config(cursor=""))

    def _create_nav_btn(self, x, y, icon, view_name, color):
        tag = f"nav_{view_name}"
        self.sidebar.create_text(x, y, text=icon, font=("Roboto", 20), fill=color, tags=tag)
        self.sidebar.tag_bind(tag, "<Button-1>", lambda e: self.app.show_view(view_name))
        self.sidebar.tag_bind(tag, "<Enter>", lambda e: self.sidebar.config(cursor="hand2"))
        self.sidebar.tag_bind(tag, "<Leave>", lambda e: self.sidebar.config(cursor=""))