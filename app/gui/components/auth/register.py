import tkinter as tk
from app.gui.components.shared.visual_elements import CButton, CInput, CBadge
from app.gui.styles.styles import (
    COLOR_BG_SIDE, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_DIM, 
    COLOR_ERROR, FONT_TITLE, FONT_CB, FONT_ERROR, INPUT_W, Y_OFF
)

class Register(tk.Frame):
    def __init__(self, master, auth_manager, on_register_success, **kwargs):
        super().__init__(master, bg=COLOR_BG_SIDE)
        self.auth, self.on_success = auth_manager, on_register_success
        self.pass_visible, self.remember_me = False, tk.BooleanVar(value=False)
        self.error_message = ""
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_SIDE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.input_user = CInput(self.canvas, "USUARIO", "Nombre de usuario")
        self.input_email = CInput(self.canvas, "EMAIL", "tu@email.com")
        self.input_pass = CInput(self.canvas, "CONTRASEÑA", "Crea una contraseña", True, self._toggle_pass)
        self.btn_reg = CButton(self.canvas, "CREAR CUENTA", self._handle_register)
        self.canvas.bind("<Configure>", lambda e: self._render())

    def _render(self, event=None):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        cx, cy = w / 2, h / 2
        sx, half_w = cx - (INPUT_W / 2), (INPUT_W / 2) - 5

        self.canvas.create_line(w, 40, w, h-40, fill=COLOR_PRIMARY, dash=(2, 20), width=4)
        # YA NO DIBUJAMOS EL LOGO AQUÍ
        self.canvas.create_text(cx, cy + Y_OFF["TITLE"], text="Registro de Usuario", fill=COLOR_TEXT_MAIN, font=FONT_TITLE, anchor="center")
        
        self.input_user.draw(sx, cy + Y_OFF["USER"], w=half_w)
        self.input_email.draw(sx + half_w + 10, cy + Y_OFF["USER"], w=half_w)
        self.input_pass.draw(sx, cy + Y_OFF["PASS"], self.pass_visible)

        cb_y, cb_tag = cy + Y_OFF["CB"], "checkbox_reg"
        self.canvas.create_rectangle(sx, cb_y, sx+16, cb_y+16, outline=COLOR_PRIMARY, width=2, tags=cb_tag)
        if self.remember_me.get():
            self.canvas.create_text(sx+8, cb_y+8, text="✔", fill=COLOR_PRIMARY, tags=cb_tag)
        self.canvas.create_text(sx+25, cb_y+8, text="Recordar credenciales", fill=COLOR_TEXT_DIM, font=FONT_CB, anchor="w", tags=cb_tag)
        self.canvas.tag_bind(cb_tag, "<Button-1>", lambda e: self._toggle_rem())
        self.btn_reg.draw(sx, cy + Y_OFF["BTN"])

        if self.error_message:
            self.canvas.create_text(cx, cy + Y_OFF["ERROR"], text=self.error_message, fill=COLOR_ERROR, font=FONT_ERROR, anchor="center")

    def _toggle_rem(self): self.remember_me.set(not self.remember_me.get()); self._render()
    def _toggle_pass(self): self.pass_visible = not self.pass_visible; self._render()
    def _handle_register(self):
        u, e, p = self.input_user.get(), self.input_email.get(), self.input_pass.get()
        if not u or not e or not p: self.error_message = "Campos obligatorios"; self._render(); return
        success, message = self.auth.register(u, e, p, remember=self.remember_me.get()) 
        if success: self.on_success()
        else: self.error_message = message; self._render()