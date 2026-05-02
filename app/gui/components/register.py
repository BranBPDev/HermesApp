import tkinter as tk
from app.gui.components.visual_elements import CButton, CInput, CBadge
from app.gui.styles.styles import (
    COLOR_BG_SIDE, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_DIM, 
    COLOR_ERROR, FONT_TITLE, FONT_CB, FONT_ERROR, INPUT_W, Y_OFF
)

class Register(tk.Frame):
    def __init__(self, master, auth_manager, on_register_success, **kwargs):
        super().__init__(master, bg=COLOR_BG_SIDE)
        self.auth = auth_manager
        self.on_success = on_register_success
        self.pass_visible = False
        self.remember_me = tk.BooleanVar(value=False)
        self.error_message = ""
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_SIDE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.badge_auto = CBadge(self.canvas, "⚠ Auto-login habilitado", color=COLOR_PRIMARY)
        self.input_user = CInput(self.canvas, "USUARIO", "Nombre")
        self.input_email = CInput(self.canvas, "EMAIL", "tu@email.com")
        self.input_pass = CInput(self.canvas, "CONTRASEÑA", "Crea una contraseña", True, self._toggle_pass)
        self.btn_reg = CButton(self.canvas, "CREAR CUENTA", self._handle_register)
        
        self.canvas.bind("<Configure>", lambda e: self._render())

    def _render(self, event=None):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        cx, cy = w / 2, h / 2
        sx = cx - (INPUT_W / 2)

        self.canvas.create_text(cx, cy + Y_OFF["TITLE"], text="Registro de Usuario", 
                                fill=COLOR_TEXT_MAIN, font=FONT_TITLE, anchor="center")
        
        # Badge de auto-login
        if self.remember_me.get():
            self.badge_auto.draw(sx, cy + Y_OFF["BADGES"])

        # Inputs Usuario y Email uno al lado del otro (mitad de ancho cada uno)
        half_w = INPUT_W / 2 - 5
        self.input_user.draw(sx, cy + Y_OFF["USER"], width=half_w)
        self.input_email.draw(sx + half_w + 10, cy + Y_OFF["USER"], width=half_w)
        
        # Contraseña (vuelve al ancho completo)
        self.input_pass.draw(sx, cy + Y_OFF["PASS"], self.pass_visible)

        # Checkbox "Recordar"
        cb_y = cy + Y_OFF["CB"]
        cb_tag = "checkbox_reg"
        self.canvas.create_rectangle(sx, cb_y, sx+16, cb_y+16, outline=COLOR_PRIMARY, width=2, tags=cb_tag)
        if self.remember_me.get():
            self.canvas.create_text(sx+8, cb_y+8, text="✔", fill=COLOR_PRIMARY, font=FONT_CB, tags=cb_tag)
        self.canvas.create_text(sx+25, cb_y+8, text="Recordar mis credenciales", 
                                fill=COLOR_TEXT_DIM, font=FONT_CB, anchor="w", tags=cb_tag)
        self.canvas.tag_bind(cb_tag, "<Button-1>", lambda e: self._toggle_rem())

        self.btn_reg.draw(sx, cy + Y_OFF["BTN"])

        if self.error_message:
            self.canvas.create_text(cx, cy + Y_OFF["ERROR"], text=self.error_message,
                                    fill=COLOR_ERROR, font=FONT_ERROR, anchor="center")

    def _toggle_rem(self):
        self.remember_me.set(not self.remember_me.get())
        self._render()

    def _toggle_pass(self):
        self.pass_visible = not self.pass_visible
        self._render()

    def _handle_register(self):
        u, e, p = self.input_user.get(), self.input_email.get(), self.input_pass.get()
        if not u or not e or not p:
            self.error_message = "Todos los campos son obligatorios"
            self._render()
            return

        success, message = self.auth.register(u, e, p) 
        if success:
            self.on_success()
        else:
            self.error_message = message
            self._render()