import tkinter as tk
from app.gui.components.visual_elements import CInput, CButton
from app.gui.styles.styles import COLOR_BG_DARK, COLOR_ERROR

class Auth(tk.Frame):
    def __init__(self, master, on_submit, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.u = CInput(self.canvas, "USUARIO", "Introduce usuario")
        self.p = CInput(self.canvas, "CONTRASEÑA", "Introduce contraseña", is_pass=True)
        self.btn = CButton(self.canvas, "ENTRAR", on_submit)
        self.err = ""
        self.canvas.bind("<Configure>", lambda e: self._draw())

    def _draw(self):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.u.draw(w/2 - 160, h/2 - 60)
        self.p.draw(w/2 - 160, h/2)
        self.btn.draw(w/2 - 160, h/2 + 80)
        if self.err: self.canvas.create_text(w/2, h/2 + 140, text=self.err, fill=COLOR_ERROR)

    def get_data(self): return self.u.get(), self.p.get()
    def show_error(self, m): self.err = m; self._draw()