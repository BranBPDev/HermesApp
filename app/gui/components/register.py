import tkinter as tk
from app.gui.components.visual_elements import CButton, CInput
from app.gui.styles.styles import (
    COLOR_BG_SIDE, COLOR_TEXT_MAIN, COLOR_ERROR, 
    FONT_TITLE, FONT_ERROR, INPUT_W, Y_OFF
)

class Register(tk.Frame):
    def __init__(self, master, auth_manager, on_register_success, **kwargs):
        super().__init__(master, bg=COLOR_BG_SIDE)
        self.auth = auth_manager
        self.on_success = on_register_success
        self.error_message = ""
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_SIDE, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Campos específicos de registro
        self.input_user = CInput(self.canvas, "USUARIO", "Elige un nombre de usuario")
        self.input_email = CInput(self.canvas, "EMAIL", "tu@email.com")
        self.input_pass = CInput(self.canvas, "CONTRASEÑA", "Crea una contraseña", True)
        self.btn_reg = CButton(self.canvas, "CREAR CUENTA", self._handle_register)
        
        self.canvas.bind("<Configure>", lambda e: self._render())

    def _render(self, event=None):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        cx, cy = w / 2, h / 2
        sx = cx - (INPUT_W / 2)

        self.canvas.create_text(cx, cy + Y_OFF["TITLE"], text="Registro de Usuario", 
                               fill=COLOR_TEXT_MAIN, font=FONT_TITLE, anchor="center")
        
        # Ajustamos los Y_OFF para que quepan 3 inputs en lugar de 2
        self.input_user.draw(sx, cy + Y_OFF["USER"] - 40)
        self.input_email.draw(sx, cy + Y_OFF["USER"] + 30)
        self.input_pass.draw(sx, cy + Y_OFF["PASS"] + 30, False)
        self.btn_reg.draw(sx, cy + Y_OFF["BTN"] + 20)

        if self.error_message:
            self.canvas.create_text(cx, cy + Y_OFF["ERROR"] + 20, text=self.error_message,
                                    fill=COLOR_ERROR, font=FONT_ERROR, anchor="center")

    def _handle_register(self):
        u, e, p = self.input_user.get(), self.input_email.get(), self.input_pass.get()
        if not u or not e or not p:
            self.error_message = "Todos los campos son obligatorios"
            self._render()
            return

        success, message = self.auth.register(u, e, p) # Asumiendo que auth_manager tendrá register
        if success:
            self.on_success()
        else:
            self.error_message = message
            self._render()