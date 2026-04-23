import tkinter as tk
from app.gui.styles.styles import COLOR_BG_DARK

class MainWindow(tk.Tk):
    def __init__(self, app_manager):
        super().__init__()
        self.app = app_manager
        self.configure(bg=COLOR_BG_DARK)
        self.active_instances = []

    def reset_layout(self):
        self.unbind("<Return>")
        for widget in self.winfo_children():
            widget.destroy()
        self.active_instances = []

    def set_layout(self, components_config):
        """
        config: lista de dicts {'class': Clase, 'relx': f, 'rely': f, 'relw': f, 'relh': f, 'args': {}}
        """
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