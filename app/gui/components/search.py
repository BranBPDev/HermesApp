import tkinter as tk
from app.gui.components.visual_elements import CInput, CButton
from app.daos.product_dao import ProductDAO

class Search(tk.Frame):
    def __init__(self, master, on_add, **kwargs):
        super().__init__(master, bg="#0F0F0F")
        self.on_add, self.dao = on_add, ProductDAO()
        self.products = []
        self.canvas = tk.Canvas(self, bg="#0F0F0F", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.inp = CInput(self.canvas, "PRODUCTO", "Buscar...")
        self.btn = CButton(self.canvas, "BUSCAR", self.execute_search)
        self.canvas.bind("<Configure>", lambda e: self._draw())

    def execute_search(self):
        query = self.inp.get()
        if query:
            self.products = self.dao.search_by_tag(query)
            self._draw()

    def _draw(self):
        self.canvas.delete("all")
        self.inp.draw(20, 20)
        self.btn.draw(360, 20)
        for i, p in enumerate(self.products):
            y = 100 + (i * 40)
            self.canvas.create_text(20, y, text=p['name'], fill="white", anchor="w")