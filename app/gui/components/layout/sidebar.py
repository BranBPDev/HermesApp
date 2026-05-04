import tkinter as tk
from app.gui.styles.styles import COLOR_BG_SIDE, COLOR_PRIMARY

class Sidebar(tk.Frame):
    def __init__(self, master, current_view="search", **kwargs):
        super().__init__(master, bg=COLOR_BG_SIDE)
        self.canvas = tk.Canvas(self, bg=COLOR_BG_SIDE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.active_tag = current_view
        self.active_setter = None
        self.buttons = {} 

        self._create_buttons()
        self.canvas.bind("<Configure>", lambda e: self._reposition())

    def _create_buttons(self):
        btn_defs = [("🔍", "search"), ("🛒", "cart"), ("⏻", "logout")]
        
        for icon, tag in btn_defs:
            item = self.canvas.create_text(
                0, 0, text=icon, font=("Roboto", 20), fill="white", tags=tag, anchor="center"
            )
            
            def make_setter(item_id, t):
                def set_active(active):
                    color = COLOR_PRIMARY if active else "white"
                    self.canvas.itemconfig(item_id, fill=color)
                return set_active

            setter = make_setter(item, tag)
            self.buttons[tag] = {"id": item, "setter": setter}

            # Eventos con clausuras correctas
            self.canvas.tag_bind(tag, "<Enter>", lambda e, i=item: self.canvas.itemconfig(i, font=("Roboto", 26), fill=COLOR_PRIMARY))
            self.canvas.tag_bind(tag, "<Leave>", lambda e, i=item, t=tag: self._on_leave(i, t))
            self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=tag, s=setter: self._action(t, s))

        # Activar visualmente el botón de la vista actual
        if self.active_tag in self.buttons:
            self.active_setter = self.buttons[self.active_tag]["setter"]
            self.active_setter(True)

    def _on_leave(self, item_id, tag):
        is_active = (tag == self.active_tag)
        color = COLOR_PRIMARY if is_active else "white"
        self.canvas.itemconfig(item_id, font=("Roboto", 20), fill=color)

    def _reposition(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1: return
        
        x_center = w / 2
        self.canvas.coords(self.buttons["search"]["id"], x_center, 50)
        self.canvas.coords(self.buttons["cart"]["id"], x_center, 110)
        self.canvas.coords(self.buttons["logout"]["id"], x_center, h - 40)

    def _action(self, tag, set_active_self):
        # Acceso al AppManager: container (master) -> MainWindow (master) -> app
        app = self.master.master.app 
        if tag == "logout":
            app.logout()
        elif tag != self.active_tag:
            # Actualizamos estado interno antes de pedir el cambio de vista
            if self.active_setter: self.active_setter(False)
            set_active_self(True)
            self.active_tag = tag
            self.active_setter = set_active_self
            app.show_view(tag)