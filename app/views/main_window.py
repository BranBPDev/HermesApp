import customtkinter as ctk
from app.views.styles import COLOR_BG_DARK, COLOR_BG_SIDE, COLOR_PRIMARY, COLOR_TEXT_MAIN, FONT_TITLE, FONT_REGULAR, COLOR_INPUT_BG

class HermesMainView(ctk.CTkFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color=COLOR_BG_DARK, corner_radius=0)
        self.app = app_manager
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=COLOR_BG_SIDE)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="HERMES", font=FONT_TITLE, text_color=COLOR_PRIMARY).pack(pady=30)

        self.btn_search = self._create_nav_btn("🔍 BUSCAR", self._show_search)
        self.btn_cart = self._create_nav_btn("🛒 CARRITO", self._show_cart)

        # Main Content Area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self._show_search()

    def _create_nav_btn(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, fg_color="transparent", 
                            text_color=COLOR_TEXT_MAIN, hover_color=COLOR_INPUT_BG,
                            anchor="w", command=command)
        btn.pack(fill="x", padx=10, pady=5)
        return btn

    def _show_search(self):
        for w in self.content_frame.winfo_children(): w.destroy()
        # Aquí cargarás la lógica de búsqueda
        pass

    def _show_cart(self):
        for w in self.content_frame.winfo_children(): w.destroy()
        # Aquí cargarás el frame del carrito
        pass