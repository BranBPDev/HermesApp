import tkinter as tk
import logging
from app.gui.styles.styles import COLOR_BG_SIDE, COLOR_PRIMARY

class Sidebar(tk.Frame):
    def __init__(self, master, current_view="search", **kwargs):
        super().__init__(master, bg=COLOR_BG_SIDE)
        self.log = logging.getLogger("SIDEBAR")
        self.canvas = tk.Canvas(self, bg=COLOR_BG_SIDE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.active_tag = current_view
        self.active_setter = None
        self.buttons = {} 

        self._create_buttons()
        self.canvas.bind("<Configure>", lambda e: self._reposition())
        # Log de respaldo para saber si el canvas registra clicks en áreas vacías
        self.canvas.bind("<Button-1>", lambda e: self.log.debug(f"Click en Canvas (X:{e.x}, Y:{e.y})"))

    def _create_buttons(self):
        btn_defs = [("🔍", "search", 50), ("🛒", "cart", 110), ("⏻", "logout", -40)]
        
        for icon, tag, y_pos in btn_defs:
            # SOLUCIÓN CRÍTICA: fill=COLOR_BG_SIDE y outline=COLOR_BG_SIDE
            # Tkinter ignora los clicks si fill="" (transparente). 
            # Dándole el mismo color del fondo lo hacemos "clicable" pero invisible a la vista.
            rect = self.canvas.create_rectangle(
                0, 0, 0, 0, fill=COLOR_BG_SIDE, outline=COLOR_BG_SIDE, tags=(tag, f"{tag}_bg")
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
            self.canvas.coords(btn["id"], x_center, y)
            self.canvas.coords(btn["rect"], 0, y-25, w, y+25)

    def _action(self, tag, set_active_self):
        self.log.info(f"--- INICIO ACCION SIDEBAR: {tag} ---")
        try:
            app = self.master.master.app 
            if tag == "logout":
                self.log.info("Ejecutando app.logout()...")
                app.logout()
            elif tag != self.active_tag:
                self.log.info(f"Cambiando vista de {self.active_tag} a {tag}")
                if self.active_setter: self.active_setter(False)
                set_active_self(True)
                self.active_tag = tag
                self.active_setter = set_active_self
                self.log.info(f"Llamando a app.show_view('{tag}')...")
                app.show_view(tag)
            else:
                self.log.info("Click en la vista ya activa. Ignorando.")
        except Exception as e:
            self.log.error(f"ERROR CRITICO en _action del sidebar: {e}", exc_info=True)
        self.log.info(f"--- FIN ACCION SIDEBAR: {tag} ---")