import tkinter as tk
from app.gui.styles.styles import COLOR_BG_SIDE, COLOR_PRIMARY

class Sidebar(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=COLOR_BG_SIDE)
        self.canvas = tk.Canvas(self, bg=COLOR_BG_SIDE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.active_tag = "search"
        self.active_setter = None  # guardará la función set_active del botón activo
        self.canvas.bind("<Configure>", lambda e: self._draw())

    def _draw(self):
        self.canvas.delete("all")
        h = self.canvas.winfo_height()
        
        # Guardamos los setters devueltos por _btn
        setter_search = self._btn(35, 50, "🔍", "search")
        setter_cart = self._btn(35, 110, "🛒", "cart")
        setter_logout = self._btn(35, h-40, "⏻", "logout")
        
        # Al inicio, activamos el search
        self.active_setter = setter_search
        self.active_setter(True)  # activamos el search

    def _btn(self, x, y, icon, tag):
        # Creamos el texto
        item = self.canvas.create_text(
            x, y, 
            text=icon, 
            font=("Roboto", 20), 
            fill="white",  # inicialmente blanco
            tags=tag,
            anchor="center"
        )
        
        # Función para activar/desactivar ESTE botón
        def set_active(active):
            color = COLOR_PRIMARY if active else "white"
            self.canvas.itemconfig(item, fill=color)
        
        # Hover: solo cambia el tamaño y color temporal
        def on_enter(e):
            self.canvas.itemconfig(item, font=("Roboto", 26), fill=COLOR_PRIMARY)
        
        def on_leave(e):
            # Al salir, restauramos tamaño y color según estado activo actual
            # ¿Cómo saber si está activo? Necesitamos saber si este tag es el activo global
            # Para no complicar, podemos guardar el estado activo en una variable local
            # Pero como set_active ya sabe si está activo, lo mejor es que on_leave pregunte
            # si el tag actual es igual a self.active_tag. Para eso necesitamos capturar tag
            es_activo = (tag == self.active_tag)
            color_final = COLOR_PRIMARY if es_activo else "white"
            self.canvas.itemconfig(item, font=("Roboto", 20), fill=color_final)
        
        self.canvas.tag_bind(tag, "<Enter>", on_enter)
        self.canvas.tag_bind(tag, "<Leave>", on_leave)
        self.canvas.tag_bind(tag, "<Button-1>", lambda e: self._action(tag, set_active))
        
        # Devolvemos la función set_active para que el sidebar la use
        return set_active

    def _action(self, tag, set_active_self):
        app = self.master.master.app # AppManager
        if tag == "logout":
            app.logout()
        elif tag != self.active_tag:
            if self.active_setter: self.active_setter(False)
            set_active_self(True)
            self.active_tag = tag
            self.active_setter = set_active_self
            app.show_view(tag) # Esto llamará a MainWindow.set_layout con CartSection o SearchSection