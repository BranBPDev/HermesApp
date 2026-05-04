import tkinter as tk
from app.gui.styles.styles import COLOR_BG_DARK, COLOR_BG_SIDE

class MainWindow(tk.Tk):
    def __init__(self, app_manager):
        super().__init__()
        self.app = app_manager
        self.title("HermesApp")
        self.configure(bg=COLOR_BG_DARK)
        
        # 1. Contenedor del Sidebar (Fijo)
        self.sidebar_container = tk.Frame(self, bg=COLOR_BG_SIDE)
        self.sidebar_container.place(relx=0, rely=0, relwidth=0.07, relheight=1)
        
        # 2. Contenedor del Header (Fijo)
        self.header_container = tk.Frame(self, bg=COLOR_BG_DARK)
        self.header_container.place(relx=0.07, rely=0, relwidth=0.93, relheight=0.12)
        
        # 3. Contenedor de Contenido (Dinámico)
        self.content_container = tk.Frame(self, bg=COLOR_BG_DARK)
        self.content_container.place(relx=0.07, rely=0.12, relwidth=0.93, relheight=0.88)
        
        self.sidebar_instance = None
        self.header_instance = None

    def set_static_layout(self, sidebar_class, header_class, header_args):
        """Dibuja los componentes que no cambian"""
        for w in self.sidebar_container.winfo_children(): w.destroy()
        for w in self.header_container.winfo_children(): w.destroy()
        
        self.sidebar_instance = sidebar_class(self.sidebar_container)
        self.sidebar_instance.pack(fill="both", expand=True)
        
        self.header_instance = header_class(self.header_container, **header_args)
        self.header_instance.pack(fill="both", expand=True)

    def set_view(self, view_class, args):
        """Cambia solo el contenido central"""
        for w in self.content_container.winfo_children(): w.destroy()
        self.unbind("<Return>")
        
        instance = view_class(self.content_container, **args)
        instance.pack(fill="both", expand=True)
        
        # Actualizar estado visual del sidebar si existe
        if self.sidebar_instance:
            # Determinamos el tag basado en la clase para mantener el icono encendido
            tag = "search" if "Search" in view_class.__name__ else "cart"
            self.sidebar_instance.update_active_visual(tag)

    def full_reset(self):
        """Limpiar todo para volver al login/update"""
        for widget in self.winfo_children():
            widget.destroy()
        # Re-crear contenedores básicos si es necesario o manejar layouts distintos