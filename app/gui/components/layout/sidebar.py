import tkinter as tk
from app.gui.styles.styles import COLOR_BG_SIDE, COLOR_PRIMARY

class Sidebar(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_BG_SIDE)
        self.canvas = tk.Canvas(self, bg=COLOR_BG_SIDE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.active_tag = "search"
        self.buttons = {} 

        self._create_buttons()
        self.canvas.bind("<Configure>", lambda e: self._reposition())

    def _create_buttons(self):
        btn_defs = [("🔍", "search"), ("🛒", "cart"), ("⏻", "logout")]
        for icon, tag in btn_defs:
            item = self.canvas.create_text(0, 0, text=icon, font=("Roboto", 20), fill="white", tags=tag)
            self.buttons[tag] = {"id": item}
            self.canvas.tag_bind(tag, "<Enter>", lambda e, i=item: self.canvas.itemconfig(i, font=("Roboto", 26), fill=COLOR_PRIMARY))
            self.canvas.tag_bind(tag, "<Leave>", lambda e, t=tag: self._on_leave(t))
            self.canvas.tag_bind(tag, "<Button-1>", lambda e, t=tag: self._action(t))

    def update_active_visual(self, tag):
        """Actualiza qué icono está resaltado"""
        self.active_tag = tag
        for t, info in self.buttons.items():
            color = COLOR_PRIMARY if t == tag else "white"
            self.canvas.itemconfig(info["id"], fill=color)

    def _on_leave(self, tag):
        if tag == "logout": 
            self.canvas.itemconfig(self.buttons[tag]["id"], font=("Roboto", 20), fill="white")
            return
        is_active = (tag == self.active_tag)
        color = COLOR_PRIMARY if is_active else "white"
        self.canvas.itemconfig(self.buttons[tag]["id"], font=("Roboto", 20), fill=color)

    def _reposition(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if w <= 1: return
        self.canvas.coords(self.buttons["search"]["id"], w/2, 50)
        self.canvas.coords(self.buttons["cart"]["id"], w/2, 110)
        self.canvas.coords(self.buttons["logout"]["id"], w/2, h - 40)

    def _action(self, tag):
        app = self.winfo_toplevel().app
        if tag == "logout": app.logout()
        else: app.show_view(tag)