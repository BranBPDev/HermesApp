import customtkinter as ctk
from PIL import Image
from app.utils.paths_util import LOGO_PNG, DATA_DIR
from app.utils.json_util import save_json
from app.utils.crypto_util import encode_to_base64
from app.views.styles import (
    COLOR_BG_DARK, COLOR_TEXT_MAIN, COLOR_ERROR, FONT_TITLE, FONT_REGULAR,
    STYLE_BADGE, STYLE_BADGE_TEXT, STYLE_INPUT, STYLE_BUTTON_PRIMARY, STYLE_LABEL_BRAND, COLOR_PRIMARY 
)

class AuthView(ctk.CTkFrame):
    def __init__(self, master, auth_manager, on_success):
        super().__init__(master, fg_color=COLOR_BG_DARK, corner_radius=0)
        self.auth = auth_manager
        self.on_success = on_success
        self.session_file = DATA_DIR / "session.json"
        self.remember_var = ctk.BooleanVar(value=False)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._render_left_panel()
        self._render_right_panel()

    def _render_left_panel(self):
        left_frame = ctk.CTkFrame(self, fg_color="#181818", corner_radius=0)
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        try:
            img = ctk.CTkImage(Image.open(str(LOGO_PNG)), size=(140, 140))
            ctk.CTkLabel(left_frame, image=img, text="").pack(pady=(120, 10))
        except Exception: pass
        
        ctk.CTkLabel(left_frame, text="HERMESAPP", font=FONT_TITLE, text_color=COLOR_TEXT_MAIN).pack()
        ctk.CTkLabel(left_frame, text="INTELIGENCIA DE MERCADO", **STYLE_LABEL_BRAND).pack(pady=(10, 0))

    def _render_right_panel(self):
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=60)
        
        ctk.CTkLabel(right_frame, text="Acceso al Sistema", font=FONT_TITLE, text_color=COLOR_TEXT_MAIN, anchor="w").pack(fill="x", pady=(70, 10))
        
        # Contenedor de Badges con altura fija para que no salten los inputs
        self.badges_container = ctk.CTkFrame(right_frame, fg_color="transparent", height=35)
        self.badges_container.pack(fill="x", pady=(0, 15))
        self.badges_container.pack_propagate(False)

        self.badge_info = ctk.CTkFrame(self.badges_container, **STYLE_BADGE)
        ctk.CTkLabel(self.badge_info, text="ⓘ Sin cuenta, se creará al entrar", **STYLE_BADGE_TEXT).pack(padx=10, pady=2)
        self.badge_info.pack(side="left", padx=(0, 10))

        self.badge_auto_reg = ctk.CTkFrame(self.badges_container, **STYLE_BADGE)
        ctk.CTkLabel(self.badge_auto_reg, text="ⓘ Auto-registro habilitado", **STYLE_BADGE_TEXT).pack(padx=10, pady=2)

        self.user_entry = ctk.CTkEntry(right_frame, placeholder_text="Usuario", **STYLE_INPUT)
        self.user_entry.pack(fill="x", pady=5)
        
        self.pass_entry = ctk.CTkEntry(right_frame, placeholder_text="Contraseña", show="*", **STYLE_INPUT)
        self.pass_entry.pack(fill="x", pady=(5, 10))
        
        # Botón para mostrar/ocultar contraseña dentro del input
        self.show_pass_btn = ctk.CTkButton(
            self.pass_entry, text="👁", width=30, height=30,
            fg_color="transparent", hover_color="#333333",
            text_color=COLOR_TEXT_MAIN, font=FONT_REGULAR,
            command=self._toggle_password_visibility
        )
        self.show_pass_btn.place(relx=1.0, rely=0.5, anchor="e", x=-5)
        
        self.user_entry.bind("<Return>", lambda e: self._handle_auth())
        self.pass_entry.bind("<Return>", lambda e: self._handle_auth())

        ctk.CTkCheckBox(
            right_frame, text="Recordarme y acceder automáticamente", variable=self.remember_var,
            command=self._toggle_badges, fg_color=COLOR_PRIMARY, text_color=COLOR_TEXT_MAIN, font=FONT_REGULAR
        ).pack(anchor="w", pady=5)

        self.error_label = ctk.CTkLabel(right_frame, text="", text_color=COLOR_ERROR, font=FONT_REGULAR)
        self.error_label.pack(pady=5)

        ctk.CTkButton(right_frame, text="ENTRAR AL TABLERO", command=self._handle_auth, **STYLE_BUTTON_PRIMARY).pack(fill="x", pady=(10, 40))
        self._toggle_badges()

    def _toggle_password_visibility(self):
        if self.pass_entry.cget("show") == "*":
            self.pass_entry.configure(show="")
            self.show_pass_btn.configure(text="🔒")
        else:
            self.pass_entry.configure(show="*")
            self.show_pass_btn.configure(text="👁")

    def _toggle_badges(self):
        if self.remember_var.get():
            self.badge_auto_reg.pack(side="left")
        else:
            self.badge_auto_reg.pack_forget()

    def _handle_auth(self):
        u, p = self.user_entry.get().strip(), self.pass_entry.get().strip()
        if not u or not p:
            self.error_label.configure(text="⚠️ Rellena todos los campos")
            return
        
        if self.auth.login(u, p) or self.auth.register(u, p):
            if self.remember_var.get():
                save_json(self.session_file, {"u": encode_to_base64(u), "p": encode_to_base64(p)})
            elif self.session_file.exists():
                self.session_file.unlink()
            self.on_success()
        else:
            self.error_label.configure(text="❌ Credenciales incorrectas")