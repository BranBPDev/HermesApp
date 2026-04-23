import tkinter as tk
from app.gui.components.visual_elements import CButton, CInput
from app.gui.styles.styles import COLOR_BG_DARK
from app.daos.product_dao import ProductDAO

class Search(tk.Frame):
    def __init__(self, master, on_add, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.on_add, self.products, self.dao = on_add, [], ProductDAO()
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.inp = CInput(self.canvas, "BUSCAR PRODUCTO", "Escribe...")
        self.btn = CButton(self.canvas, "BUSCAR", self.execute_search)
        self.canvas.bind("<Configure>", lambda e: self._draw())
        self.master.winfo_toplevel().bind("<Return>", lambda e: self.execute_search())

    def execute_search(self):
        q = self.inp.get()
        if q: self.products = self.dao.search_by_tag(q); self._draw()

    def _draw(self):
        self.canvas.delete("all")
        self.inp.draw(30, 40)
        self.btn.draw(450, 40)
        for i, p in enumerate(self.products):
            y = 120 + (i * 65)
            self.canvas.create_rectangle(30, y, 750, y+55, fill="#181818", outline="")
            self.canvas.create_text(50, y+27, text=p['name'], fill="white", anchor="w")