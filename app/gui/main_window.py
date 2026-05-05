import tkinter as tk
from app.gui.styles.styles import COLOR_BG_DARK
from app.utils.paths_util import LOGO_ICO
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
            icon_path = str(LOGO_ICO.absolute())
            log.info(f"Aplicando icono desde ruta absoluta: {icon_path}")
            try:
                # Método 1: Estándar clásico
                self.iconbitmap(icon_path)
                log.info("self.iconbitmap() ejecutado con éxito.")
            except tk.TclError as e:
                log.error(f"Error de formato iconbitmap: {e}. Probando iconphoto...")
                try:
                    # Método 2: Alternativa con PIL (evitando wm_iconphoto que da problemas en Win11)
                    from PIL import Image, ImageTk
                    img = Image.open(LOGO_ICO)
                    self._icon_photo = ImageTk.PhotoImage(img)
                    self.iconphoto(True, self._icon_photo)
                    log.info("self.iconphoto() ejecutado con éxito.")
                except Exception as ex:
                    log.error(f"Error en método iconphoto: {ex}")
            except Exception as e:
                log.error(f"Error general al aplicar icono: {e}")
        else:
            log.error(f"LOGO_ICO NO EXISTE EN LA RUTA: {LOGO_ICO}")

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