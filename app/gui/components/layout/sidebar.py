import tkinter as tk
from app.gui.styles.styles import COLOR_BG_SIDE, COLOR_PRIMARY

class Sidebar(tk.Frame):
    def __init__(self, master, active_tab="search", **kwargs):
        super().__init__(master, bg=COLOR_BG_SIDE)
        self.canvas = tk.Canvas(self, bg=COLOR_BG_SIDE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.active_tag = active_tab
        self.buttons = {} 

        self._create_buttons()
        self.canvas.bind("<Configure>", lambda e: self._reposition())

    def _create_buttons(self):
        btn_defs = [("🔍", "search"), ("🛒", "cart"), ("⏻", "logout")]
        
        for icon, tag in btn_defs:
            color = COLOR_PRIMARY if tag == self.active_tag else "white"
            item = self.canvas.create_text(
                0, 0, text=icon, font=("Roboto", 20), fill=color, tags=tag, anchor="center"
            )
            
            self.buttons[tag] = {"id": item}

            # Eventos
            self.canvas.tag_bind(tag, "<Enter>", lambda e, i=item: self.canvas.itemconfig(i, font=("Roboto", 26), fill=COLOR_PRIMARY))
            self.canvas.tag_bind(tag, "<Leave>", lambda e, t=tag: self._on_leave(t))
            self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=tag: self._action(t))

    def _on_leave(self, tag):
        item_id = self.buttons[tag]["id"]
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

    def _action(self, tag):
        app = self.master.master.app # Acceso al AppManager
        if tag == "logout":
            app.logout()
        elif tag != self.active_tag:
            app.show_view(tag)