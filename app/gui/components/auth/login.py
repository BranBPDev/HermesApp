import tkinter as tk
from app.gui.components.shared.visual_elements import CButton, CInput, CBadge
from app.gui.styles.styles import (
    COLOR_BG_DARK, COLOR_PRIMARY, COLOR_TEXT_MAIN, COLOR_TEXT_DIM, 
    COLOR_ERROR, FONT_TITLE, FONT_CB, FONT_ERROR, INPUT_W, Y_OFF
)

class Login(tk.Frame):
    def __init__(self, master, auth_manager, on_success, logo, **kwargs):
        super().__init__(master, bg=COLOR_BG_DARK)
        # EL LOGO YA VIENE CARGADO DESDE MAINWINDOW
        self.logo = logo
        self.auth, self.on_success = auth_manager, on_success
        self.pass_visible, self.remember_me = False, tk.BooleanVar(value=False)
        self.error_message = ""
        
        self.canvas = tk.Canvas(self, bg=COLOR_BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.badge_auto = CBadge(self.canvas, "⚠ Auto-login habilitado", color=COLOR_PRIMARY)
        self.input_user = CInput(self.canvas, "USUARIO / EMAIL", "Introduce usuario o email")
        self.input_pass = CInput(self.canvas, "CONTRASEÑA", "Introduce tu contraseña", True, self._toggle_pass)
        self.btn_login = CButton(self.canvas, "ENTRAR AL SISTEMA", self._handle_login)
        
        self.canvas.bind("<Configure>", lambda e: self._render())
        self.winfo_toplevel().bind("<Return>", lambda e: self._handle_login())

    def _render(self, event=None):
        self.canvas.delete("all")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        cx, cy = w / 2, h / 2
        sx = cx - (INPUT_W / 2)
        
        if self.logo:
            self.canvas.create_image(cx, h * 0.15, image=self.logo, anchor="center")
            
        self.canvas.create_text(cx, cy + Y_OFF["TITLE"], text="Acceso al Sistema", 
                               fill=COLOR_TEXT_MAIN, font=FONT_TITLE, anchor="center")
        
        if self.remember_me.get():
            self.badge_auto.draw(sx, cy + Y_OFF["BADGES"])

        self.input_user.draw(sx, cy + Y_OFF["USER"])
        self.input_pass.draw(sx, cy + Y_OFF["PASS"], self.pass_visible)

        cb_y = cy + Y_OFF["CB"]
        cb_tag = "checkbox_group"
        self.canvas.create_rectangle(sx, cb_y, sx + INPUT_W, cb_y + 16, fill=COLOR_BG_DARK, outline=COLOR_BG_DARK, tags=cb_tag)
        self.canvas.create_rectangle(sx, cb_y, sx+16, cb_y+16, outline=COLOR_PRIMARY, width=2, tags=cb_tag)
        if self.remember_me.get():
            self.canvas.create_text(sx+8, cb_y+8, text="✔", fill=COLOR_PRIMARY, font=FONT_CB, tags=cb_tag)
        self.canvas.create_text(sx+25, cb_y+8, text="Recordar mis credenciales", 
                               fill=COLOR_TEXT_DIM, font=FONT_CB, anchor="w", tags=cb_tag)
        self.canvas.tag_bind(cb_tag, "<Button-1>", lambda e: self._toggle_rem())

        self.btn_login.draw(sx, cy + Y_OFF["BTN"])

        if self.error_message:
            self.canvas.create_text(cx, cy + Y_OFF["ERROR"], text=self.error_message,
                                    fill=COLOR_ERROR, font=FONT_ERROR, anchor="center")

    def _toggle_rem(self): self.remember_me.set(not self.remember_me.get()); self._render()
    def _toggle_pass(self): self.pass_visible = not self.pass_visible; self._render()
    
    def _handle_login(self):
        u, p = self.input_user.get(), self.input_pass.get()
        success, message = self.auth.login(u, p, remember=self.remember_me.get())
        if success:
            self.winfo_toplevel().unbind("<Return>")
            self.on_success()
        else:
            self.error_message = message
            self._render()