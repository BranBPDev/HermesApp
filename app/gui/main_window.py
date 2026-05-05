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

        # --- CARGA OPTIMIZADA DEL LOGO PNG (UNA SOLA VEZ) ---
        self.logo_png_shared = None
        if LOGO_PNG.exists():
            try:
                img = Image.open(str(LOGO_PNG)).resize((100, 100), Image.Resampling.LANCZOS)
                self.logo_png_shared = ImageTk.PhotoImage(img)
                log.info("ÉXITO: Logo PNG cargado en memoria para compartir.")
            except Exception as e:
                log.error(f"Error cargando logo PNG compartido: {e}")

        # --- GESTIÓN DEL ICONO (.ICO) PARA BARRA DE TAREAS Y VENTANA ---
        if LOGO_ICO.exists():
            icon_path = str(LOGO_ICO.absolute())
            try:
                # MÉTODO 1: Forzar PhotoImage para el icono de ventana
                img_ico = Image.open(LOGO_ICO)
                self._icon_photo = ImageTk.PhotoImage(img_ico)
                self.iconphoto(True, self._icon_photo)
                log.info("ÉXITO: self.iconphoto() con .ico aplicado.")
            except Exception as e:
                log.error(f"FALLO en iconphoto: {e}. Probando iconbitmap...")
                try:
                    self.iconbitmap(icon_path)
                except Exception as ex:
                    log.error(f"FALLO CRÍTICO en iconbitmap: {ex}")

    def reset_layout(self):
        log.debug(f"Reset de layout. Destruyendo {len(self.active_instances)} instancias...")
        self.unbind("<Return>")
        for widget in self.winfo_children():
            widget.destroy()
        self.active_instances = []

    def set_layout(self, components_config):
        log.info(f"Aplicando nuevo layout...")
        self.reset_layout()
        for i, conf in enumerate(components_config):
            container = tk.Frame(self, bg=COLOR_BG_DARK)
            container.place(
                relx=conf.get('relx', 0), rely=conf.get('rely', 0),
                relwidth=conf.get('relw', 1), relheight=conf.get('relh', 1)
            )
            # Inyectamos el logo ya cargado en los argumentos si el componente lo necesita
            args = conf.get('args', {})
            if 'logo' in args:
                args['logo'] = self.logo_png_shared

            instance = conf['class'](container, **args)
            instance.pack(fill="both", expand=True)
            self.active_instances.append(instance)
        return self.active_instances