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
                from PIL import Image, ImageTk
                # Método 1: El estándar de Tkinter
                self.iconbitmap(default=str(LOGO_ICO.absolute())) 
                
                # Método 2: Forzar icono de barra de tareas mediante PhotoImage (más robusto)
                img = Image.open(LOGO_ICO)
                self._icon_photo = ImageTk.PhotoImage(img) # Guardamos referencia fuerte
                self.wm_iconphoto(True, self._icon_photo)
                
                log.info("Icono aplicado mediante iconbitmap y wm_iconphoto")
            except Exception as e:
                log.error(f"Error real al aplicar icono: {e}")

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