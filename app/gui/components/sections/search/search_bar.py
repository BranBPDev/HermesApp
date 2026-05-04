import tkinter as tk
from app.gui.components.shared.visual_elements import CButton, CInput
from app.gui.styles.styles import COLOR_BG_DARK

class SearchBar(tk.Frame):
    def __init__(self, master, on_search, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK, height=80)
        self.on_search = on_search
        self.pack_propagate(False) # Mantiene el alto fijo
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.inp = CInput(self.canvas, "BUSCAR PRODUCTO", "Escribe el nombre del producto...")
        self.btn = CButton(self.canvas, "BUSCAR", self._trigger_search)
        
        self.canvas.bind("<Configure>", lambda e: self.draw())
        # Vincular la tecla Enter a nivel de ventana para este componente
        self.master.winfo_toplevel().bind("<Return>", lambda e: self._trigger_search())

    def _trigger_search(self):
        query = self.inp.get()
        if query:
            self.on_search(query)

    def get_query(self):
        return self.inp.get()

    def draw(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        # Mantenemos tus coordenadas exactas: x=30, y=40
        self.inp.draw(30, 40, w=w-200)
        self.btn.draw(w-150, 40, w=120)