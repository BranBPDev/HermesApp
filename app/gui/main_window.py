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
                img = Image.open(str(LOGO_PNG)).resize((100, 100), Image.Resampling.LANCZOS)
                self.shared_logo_img = ImageTk.PhotoImage(img)
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

    def reset_layout(self):
        log.debug("Reset de layout...")
        self.unbind("<Return>")
        for widget in self.winfo_children():
            widget.destroy()
        self.active_instances = []

    def set_layout(self, components_config):
        self.reset_layout()
        
        # Contenedor para los componentes
        main_container = tk.Frame(self, bg=COLOR_BG_DARK)
        main_container.pack(fill="both", expand=True)

        for conf in components_config:
            container = tk.Frame(main_container, bg=COLOR_BG_DARK)
            container.place(
                relx=conf.get('relx', 0), rely=conf.get('rely', 0),
                relwidth=conf.get('relw', 1), relheight=conf.get('relh', 1)
            )
            # Pasamos None al logo de los componentes porque ahora lo gestiona MainWindow
            instance = conf['class'](container, **conf.get('args', {}))
            instance.pack(fill="both", expand=True)
            self.active_instances.append(instance)

        # --- LOGO ÚNICO CENTRADO (FLOTANTE) ---
        # Solo lo mostramos si hay más de un componente (Login/Register)
        if len(components_config) > 1 and self.shared_logo_img:
            logo_label = tk.Label(self, image=self.shared_logo_img, bg=COLOR_BG_DARK, bd=0, highlightthickness=0)
            logo_label.place(relx=0.5, rely=0.15, anchor="center")

        log.info("Layout aplicado con logo centralizado.")
        return self.active_instances