import tkinter as tk
from PIL import Image, ImageTk
from app.gui.styles.styles import COLOR_BG_SIDE, COLOR_PRIMARY
from app.utils.paths_util import LOGO_PNG

class Sidebar(tk.Frame):
    def __init__(self, master, current_view="search", app=None, **kwargs):
        super().__init__(master, bg=COLOR_BG_SIDE, **kwargs)
        
        # Guardamos la referencia directa de la app para evitar errores de jerarquía
        self.app = app
        
        # Forzar un ancho fijo inicial para evitar que la vista principal solape el sidebar
        self.config(width=60)
        self.pack_propagate(False)
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_SIDE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.active_tag = current_view
        self.active_setter = None
        self.buttons = {} 

        # Cargar y redimensionar el logo estático propio para la cabecera del sidebar
        self.sidebar_logo_img = None
        if LOGO_PNG.exists():
            try:
                self.sidebar_logo_img = ImageTk.PhotoImage(
                    Image.open(str(LOGO_PNG)).resize((35, 35), Image.Resampling.LANCZOS)
                )
            except Exception as e:
                from app.utils.logger_util import HermesLogger
                HermesLogger.get_logger("SIDEBAR").error(f"Error cargando logo en el Sidebar: {e}")

        self._create_buttons()
        self.canvas.bind("<Configure>", self._reposition)
        
        # Bindeo básico al canvas
        self.canvas.bind("<Button-1>", lambda e: None)

    def _create_buttons(self):
        
        # Dibujar la imagen estática del logo en el tope del Canvas si se cargó correctamente
        if self.sidebar_logo_img:
            self.canvas.create_image(0, 0, image=self.sidebar_logo_img, anchor="center", tags="sidebar_logo")

        # Reajuste de posiciones Y fijas hacia abajo para dar espacio limpio al logotipo (Y=45)
        btn_defs = [("🔍", "search", 120), ("🛒", "cart", 180), ("⏻", "logout", -40)]
        
        for icon, tag, y_pos in btn_defs:
            
            # Hitbox sólido pero del mismo color del fondo
            rect_tag = f"{tag}_bg"
            rect = self.canvas.create_rectangle(
                0, 0, 0, 0, fill=COLOR_BG_SIDE, outline=COLOR_BG_SIDE, tags=(tag, rect_tag)
            )
            
            # Icono/Texto
            txt_tag = f"{tag}_txt"
            item = self.canvas.create_text(
                0, 0, text=icon, font=("Roboto", 20), fill="white", tags=(tag, txt_tag), anchor="center"
            )
            
            def make_setter(i, t):
                def set_active(active):
                    color = COLOR_PRIMARY if active else "white"
                    self.canvas.itemconfig(i, fill=color)
                return set_active

            setter = make_setter(item, tag)
            self.buttons[tag] = {"id": item, "rect": rect, "y": y_pos, "setter": setter}

            # Vincular estado activo inicial si corresponde
            if tag == self.active_tag:
                setter(True)
                self.active_setter = setter

            # Bindeo a nivel de TAG (afecta tanto al texto como al rectangulo)
            self.canvas.tag_bind(tag, "<Enter>", lambda e, i=item, t=tag: self._on_enter(i, t))
            self.canvas.tag_bind(tag, "<Leave>", lambda e, i=item, t=tag: self._on_leave(i, t))
            self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=tag, s=setter: self._action(t, s))

    def _on_enter(self, item_id, tag):
        self.canvas.itemconfig(item_id, font=("Roboto", 26), fill=COLOR_PRIMARY)

    def _on_leave(self, item_id, tag):
        is_active = (tag == self.active_tag)
        color = COLOR_PRIMARY if is_active else "white"
        self.canvas.itemconfig(item_id, font=("Roboto", 20), fill=color)

    def _reposition(self, event=None):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        # Evitar procesamiento si el tamaño es muy pequeño o no ha cargado
        if w <= 1: 
            return
            
        x_center = w / 2
        
        # Ubicar el logo de forma estática en la parte superior central
        if self.sidebar_logo_img:
            self.canvas.coords("sidebar_logo", x_center, 45)
        
        for tag, btn in self.buttons.items():
            y = btn["y"] if btn["y"] > 0 else h + btn["y"]
            
            self.canvas.coords(btn["id"], x_center, y)
            self.canvas.coords(btn["rect"], 0, y-25, w, y+25)

    def _action(self, tag, set_active_self):
        try:
            # Intentar usar la referencia inyectada, si no, fallback seguro a la jerarquía anterior
            app = self.app if self.app is not None else self.master.master.app 
            
            if tag == "logout":
                app.logout()
            elif tag != self.active_tag:
                if self.active_setter: 
                    self.active_setter(False)
                
                set_active_self(True)
                self.active_tag = tag
                self.active_setter = set_active_self
                
                app.show_view(tag)
                
        except AttributeError as ae:
            from app.utils.logger_util import HermesLogger
            HermesLogger.get_logger("SIDEBAR").error(f"❌ ERROR DE JERARQUÍA (AttributeError): No se encuentra 'app' en master.master. Detalles: {ae}", exc_info=True)
        except Exception as e:
            from app.utils.logger_util import HermesLogger
            HermesLogger.get_logger("SIDEBAR").error(f"❌ ERROR CRÍTICO DESCONOCIDO al procesar click en '{tag}': {e}", exc_info=True)