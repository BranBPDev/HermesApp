import tkinter as tk
from app.gui.components.visual_elements import CButton, CInput
from app.gui.styles.styles import COLOR_BG_DARK, COLOR_BG_SIDE, FONT_TITLE

class AuthView(tk.Frame):
    def __init__(self, master, auth_manager, on_success):
        super().__init__(master, bg=COLOR_BG_DARK)
        self.auth = auth_manager
        self.on_success = on_success
        self.pass_visible = False
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._render)

    def _render(self, event=None):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        
        # Panel Izquierdo
        self.canvas.create_rectangle(0, 0, w/2, h, fill=COLOR_BG_SIDE, outline="")
        self.canvas.create_text(w/4, h/2, text="HERMESAPP", font=FONT_TITLE, fill="white")

        # Formulario
        cx = (w * 0.75)
        CInput(self.canvas, cx-150, h/2-80, 300, 45, "USUARIO").draw()
        
        # Password Input
        self.input_pass = CInput(self.canvas, cx-150, h/2, 300, 45, "CONTRASEÑA", is_password=not self.pass_visible)
        self.input_pass.draw()
        
        # Botón Mostrar/Ocultar
        toggle_text = "👁" if self.pass_visible else "🔒"
        btn_show = CButton(self.canvas, cx+120, h/2, 30, 45, toggle_text, self._toggle_pass)
        btn_show.draw()
        
        btn_login = CButton(self.canvas, cx-150, h/2+80, 300, 50, "ENTRAR", self._handle_auth)
        btn_login.draw()

    def _toggle_pass(self):
        self.pass_visible = not self.pass_visible
        self._render()

    def _handle_auth(self):
        self.on_success()