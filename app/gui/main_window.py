import tkinter as tk
from app.gui.styles.styles import COLOR_BG_DARK
from app.utils.paths_util import LOGO_ICO
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

        # FORZAR ICONO - ESTRATEGIA INVERTIDA (Primero en memoria, luego archivo)
        if LOGO_ICO.exists():
            icon_path = str(LOGO_ICO.absolute())
            log.info(f"Ruta de icono confirmada: {icon_path}")
            try:
                # MÉTODO 1: Forzar PhotoImage (Inmune al caché de .ico de Windows)
                from PIL import Image, ImageTk
                log.debug("Intentando cargar icono vía PIL (ImageTk.PhotoImage)...")
                img = Image.open(LOGO_ICO)
                self._icon_photo = ImageTk.PhotoImage(img)
                self.iconphoto(True, self._icon_photo)
                log.info("ÉXITO: self.iconphoto() aplicado correctamente. (Método en memoria)")
            except Exception as e:
                log.error(f"FALLO en iconphoto (PIL): {e}. Procediendo a Plan B (iconbitmap)...")
                try:
                    # MÉTODO 2: Estándar clásico de Windows
                    self.iconbitmap(icon_path)
                    log.info("ÉXITO: self.iconbitmap() aplicado correctamente. (Método archivo)")
                except Exception as ex:
                    log.error(f"FALLO CRÍTICO en iconbitmap: {ex}. Imposible aplicar icono.")
        else:
            log.error(f"FATAL: LOGO_ICO NO EXISTE EN LA RUTA: {LOGO_ICO}")

    def reset_layout(self):
        log.debug(f"Reset de layout. Destruyendo {len(self.active_instances)} instancias activas...")
        self.unbind("<Return>")
        for widget in self.winfo_children():
            widget.destroy()
        self.active_instances = []
        log.debug("Reset de layout completado.")

    def set_layout(self, components_config):
        log.info(f"Aplicando nuevo layout con {len(components_config)} componentes...")
        self.reset_layout()
        for i, conf in enumerate(components_config):
            log.debug(f"Montando componente {i+1}/{len(components_config)}: {conf.get('class').__name__}")
            container = tk.Frame(self, bg=COLOR_BG_DARK)
            container.place(
                relx=conf.get('relx', 0), rely=conf.get('rely', 0),
                relwidth=conf.get('relw', 1), relheight=conf.get('relh', 1)
            )
            instance = conf['class'](container, **conf.get('args', {}))
            instance.pack(fill="both", expand=True)
            self.active_instances.append(instance)
        log.info("Layout aplicado correctamente.")
        return self.active_instances