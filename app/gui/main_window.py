import tkinter as tk
from PIL import Image, ImageTk
from app.gui.styles.styles import COLOR_BG_DARK
from app.utils.paths_util import LOGO_ICO, LOGO_PNG
from app.utils.logger_util import HermesLogger

log = HermesLogger.get_logger("MAIN_WINDOW")

class MainWindow(tk.Tk):
    def __init__(self, app_manager):
        super().__init__()
        self.app = app_manager
        log.debug("Inicializando MainWindow...")
        self.title("HermesApp")
        self.configure(bg=COLOR_BG_DARK)
        self.active_instances = []

        # --- CARGA ÚNICA Y OPTIMIZADA DEL LOGO PNG ---
        self.shared_logo_img = None
        if LOGO_PNG.exists():
            try:
                self.shared_logo_img = ImageTk.PhotoImage(
                    Image.open(str(LOGO_PNG)).resize((100, 100), Image.Resampling.LANCZOS)
                )
                log.info("Logo PNG cargado en memoria correctamente.")
            except Exception as e:
                log.error(f"Error cargando PNG: {e}")

        # --- ICONO DEL SISTEMA (.ICO) ---
        if LOGO_ICO.exists():
            try:
                self.icon_temp = ImageTk.PhotoImage(Image.open(LOGO_ICO))
                self.iconphoto(True, self.icon_temp)
            except:
                try: self.iconbitmap(str(LOGO_ICO))
                except: pass
        
        # Vincular el evento de redimensión para actualizar el logo
        self.bind("<Configure>", self._on_resize)

    def reset_layout(self):
        log.debug("Reset de layout...")
        self.unbind("<Return>")
        for widget in self.winfo_children():
            widget.destroy()
        self.active_instances = []

    def set_layout(self, components_config):
        self.reset_layout()
        
        main_container = tk.Frame(self, bg=COLOR_BG_DARK)
        main_container.pack(fill="both", expand=True)

        for conf in components_config:
            container = tk.Frame(main_container, bg=COLOR_BG_DARK)
            container.place(
                relx=conf.get('relx', 0), rely=conf.get('rely', 0),
                relwidth=conf.get('relw', 1), relheight=conf.get('relh', 1)
            )
            instance = conf['class'](container, **conf.get('args', {}))
            instance.pack(fill="both", expand=True)
            self.active_instances.append(instance)

        # Dibujo inicial seguro
        self.after(100, self._draw_floating_logo)
        log.info("Layout aplicado.")
        return self.active_instances

    def _on_resize(self, event):
        """Manejador para cuando la ventana cambia de tamaño."""
        # CRUCIAL: Detener propagación y procesar SOLO si el evento proviene estrictamente de MainWindow
        if event.widget == self:
            self._draw_floating_logo()

    def _draw_floating_logo(self):
        """Dibuja el logo en los canvas de los hijos manteniendo la transparencia."""
        if not self.shared_logo_img or len(self.active_instances) < 2:
            return

        # Obtenemos los canvas de los componentes activos de forma segura
        try:
            canvas_left = getattr(self.active_instances[0], "canvas", None)
            canvas_right = getattr(self.active_instances[1], "canvas", None)

            if not canvas_left or not canvas_right:
                return

            # Eliminamos versiones anteriores del logo para no solapar
            canvas_left.delete("floating_logo")
            canvas_right.delete("floating_logo")

            # Validar dimensiones mínimas antes de renderizar en posiciones relativas
            w_left = canvas_left.winfo_width()
            if w_left > 1:
                canvas_left.create_image(
                    w_left, 
                    100, 
                    image=self.shared_logo_img, 
                    anchor="center",
                    tags="floating_logo"
                )

                canvas_right.create_image(
                    0, 
                    100, 
                    image=self.shared_logo_img, 
                    anchor="center",
                    tags="floating_logo"
                )
        except (AttributeError, tk.TclError):
            # Si el componente se está destruyendo o mutando estructuralmente
            pass