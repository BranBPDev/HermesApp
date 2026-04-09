import customtkinter as ctk
from PIL import Image
from app.utils.paths_util import LOGO_PNG
from app.components.user_header import UserHeader
from app.views.search_view import SearchView
from app.views.cart_view import CartView
from app.views.styles import COLOR_BG_DARK, COLOR_BG_SIDE, COLOR_PRIMARY

class HermesMainView(ctk.CTkFrame):
    def __init__(self, master, app_manager):
        super().__init__(master, fg_color=COLOR_BG_DARK, corner_radius=0)
        self.app = app_manager
        
        # Diccionario para guardar referencias a los botones de navegación
        self.nav_buttons = {}
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._init_sidebar()
        self._init_content_area()

    def _init_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=70, corner_radius=0, fg_color=COLOR_BG_SIDE)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        try:
            logo_img = ctk.CTkImage(Image.open(str(LOGO_PNG)), size=(32, 32))
            ctk.CTkLabel(self.sidebar, image=logo_img, text="").pack(pady=25)
        except: pass

        # Guardamos los botones en el diccionario con una clave identificativa
        self.nav_buttons["search"] = self._create_nav_icon("🔍", self._show_search)
        self.nav_buttons["cart"] = self._create_nav_icon("🛒", self._show_cart)
        
        # Botón de logout (no se resalta como activo)
        ctk.CTkButton(self.sidebar, text="⏻", width=40, height=40, fg_color="transparent", 
                      font=("Roboto", 22), text_color="#888888", hover_color="#332222", 
                      command=self.app.logout).pack(side="bottom", pady=20)

    def _create_nav_icon(self, icon, command):
        btn = ctk.CTkButton(self.sidebar, text=icon, width=50, height=50, fg_color="transparent",
                            font=("Roboto", 20), text_color="white", hover_color="#2b2b2b", 
                            command=command)
        btn.pack(pady=10)
        return btn

    def _init_content_area(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=35, pady=25)
        
        username = getattr(self.app.auth, 'username', 'Usuario')
        self.header = UserHeader(self.main_container, username)
        self.header.pack(fill="x", pady=(0, 20))

        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.pack(expand=True, fill="both")
        
        self._show_search()

    def _update_nav_ui(self, active_key):
        """Resalta el icono de la vista activa y devuelve los demás a su estado original."""
        for key, btn in self.nav_buttons.items():
            if key == active_key:
                btn.configure(text_color=COLOR_PRIMARY)
            else:
                btn.configure(text_color="white")

    def _show_search(self):
        self._update_nav_ui("search") # Actualizar UI
        self._clear_content()
        self.search_view = SearchView(self.content_frame, self._add_to_cart_handler)
        self.search_view.pack(expand=True, fill="both")

    def _show_cart(self):
        self._update_nav_ui("cart") # Actualizar UI
        self._clear_content()
        self.cart_view = CartView(self.content_frame)
        self.cart_view.pack(expand=True, fill="both")

    def _clear_content(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

    def _add_to_cart_handler(self, product):
        print(f"DEBUG: Producto enviado al carrito: {product.get('name')}")