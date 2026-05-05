import tkinter as tk
from app.gui.styles.styles import COLOR_BG_DARK
from app.utils.paths_util import LOGO_ICO  # Asegúrate de importar la ruta
from app.utils.logger_util import HermesLogger

log = HermesLogger.get_logger("MAIN_WINDOW")

class MainWindow(tk.Tk):
    def __init__(self, app_manager):
        super().__init__()
        self.app = app_manager
        self.title("HermesApp")
        self.configure(bg=COLOR_BG_DARK)
        self.active_instances = []

        # FORZAR ICONO EN BARRA DE TAREAS
        if LOGO_ICO.exists():
            try:
                icon_path = str(LOGO_ICO.absolute()) # Usamos ruta absoluta
                log.info(f"Intentando cargar iconbitmap desde: {icon_path}")
                self.iconbitmap(icon_path)
                self.wm_iconbitmap(icon_path)
                log.info("Icono aplicado correctamente a MainWindow")
            except Exception as e:
                log.error(f"Error al aplicar icono en Tkinter: {e}")
        else:
            log.warning(f"LOGO_ICO no encontrado en la ruta esperada: {LOGO_ICO}")

    def reset_layout(self):
        self.unbind("<Return>")
        for widget in self.winfo_children():
            widget.destroy()
        self.active_instances = []

    def set_layout(self, components_config):
        self.reset_layout()
        for conf in components_config:
            container = tk.Frame(self, bg=COLOR_BG_DARK)
            container.place(
                relx=conf.get('relx', 0), rely=conf.get('rely', 0),
                relwidth=conf.get('relw', 1), relheight=conf.get('relh', 1)
            )
            instance = conf['class'](container, **conf.get('args', {}))
            instance.pack(fill="both", expand=True)
            self.active_instances.append(instance)
        return self.active_instances