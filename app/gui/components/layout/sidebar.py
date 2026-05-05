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
        import logging
        self.log = logging.getLogger("SIDEBAR")
        btn_defs = [("🔍", "search", 50), ("🛒", "cart", 110), ("⏻", "logout", -40)]
        
        for icon, tag, y_pos in btn_defs:
            # 1. Crear un rectángulo invisible que cubra todo el ancho del sidebar
            # Esto asegura que el click funcione en toda la zona, no solo sobre la letra
            rect = self.canvas.create_rectangle(
                0, 0, 0, 0, fill="", outline="", tags=(tag, f"{tag}_bg")
            )
            
            item = self.canvas.create_text(
                0, 0, text=icon, font=("Roboto", 20), fill="white", tags=(tag, f"{tag}_txt"), anchor="center"
            )
            
            def make_setter(i, t):
                def set_active(active):
                    color = COLOR_PRIMARY if active else "white"
                    self.canvas.itemconfig(i, fill=color)
                return set_active

            setter = make_setter(item, tag)
            self.buttons[tag] = {"id": item, "rect": rect, "y": y_pos, "setter": setter}

            # Bindeamos los eventos al TAG (que ahora incluye al rectángulo y al texto)
            self.canvas.tag_bind(tag, "<Enter>", lambda e, i=item: self.canvas.itemconfig(i, font=("Roboto", 26), fill=COLOR_PRIMARY))
            self.canvas.tag_bind(tag, "<Leave>", lambda e, i=item, t=tag: self._on_leave(i, t))
            self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=tag, s=setter: self._action(t, s))

    def _on_leave(self, item_id, tag):
        is_active = (tag == self.active_tag)
        color = COLOR_PRIMARY if is_active else "white"
        self.canvas.itemconfig(item_id, font=("Roboto", 20), fill=color)

    def _reposition(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1: return
        x_center = w / 2
        
        for tag, btn in self.buttons.items():
            y = btn["y"] if btn["y"] > 0 else h + btn["y"]
            # Centrar texto
            self.canvas.coords(btn["id"], x_center, y)
            # Ajustar rectángulo de colisión (toda la franja del botón)
            self.canvas.coords(btn["rect"], 0, y-25, w, y+25)

    def _action(self, tag, set_active_self):
        self.log.info(f"CLICK DETECTADO en Sidebar: {tag}") # <--- LOG CRÍTICO
        app = self.master.master.app 
        if tag == "logout":
            app.logout()
        elif tag != self.active_tag:
            self.log.debug(f"Cambiando vista de {self.active_tag} a {tag}")
            if self.active_setter: self.active_setter(False)
            set_active_self(True)
            self.active_tag = tag
            self.active_setter = set_active_self
            app.show_view(tag)