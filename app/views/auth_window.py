import customtkinter as ctk
from PIL import Image
from app.utils.paths_util import LOGO_PNG, DATA_DIR
from app.utils.json_util import save_json
from app.utils.crypto_util import encode_to_base64
from app.views.styles import (
    COLOR_BG_DARK, COLOR_TEXT_MAIN, COLOR_ERROR, FONT_TITLE, FONT_REGULAR,
    STYLE_BADGE, STYLE_BADGE_TEXT, STYLE_INPUT, STYLE_BUTTON_PRIMARY, STYLE_LABEL_BRAND
)

class AuthView(ctk.CTkFrame):
    def __init__(self, master, auth_manager, on_success):
        super().__init__(master, fg_color=COLOR_BG_DARK, corner_radius=0)
        self.auth = auth_manager
        self.on_success = on_success
        self.session_file = DATA_DIR / "session.json"

        self._setup_grid()
        self._render_left_panel()
        self._render_right_panel()
        
        self.user_entry.bind("<Return>", lambda e: self._handle_auth())
        self.pass_entry.bind("<Return>", lambda e: self._handle_auth())
        
        self.master.after(100, self._adjust_window_size)

    def _setup_grid(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _adjust_window_size(self):
        self.master.update_idletasks()
        width, height = 900, self.right_frame.winfo_reqheight() + 200
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f"{width}x{int(height)}+{x}+{y}")

    def _render_left_panel(self):
        self.left_frame = ctk.CTkFrame(self, fg_color="#181818", corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        try:
            img = ctk.CTkImage(Image.open(str(LOGO_PNG)), size=(140, 140))
            ctk.CTkLabel(self.left_frame, image=img, text="").pack(pady=(120, 10))
        except Exception: pass
        ctk.CTkLabel(self.left_frame, text="HERMESAPP", font=FONT_TITLE, text_color=COLOR_TEXT_MAIN).pack()
        ctk.CTkLabel(self.left_frame, text="INTELIGENCIA DE MERCADO", **STYLE_LABEL_BRAND).pack(pady=(10, 0))

    def _render_right_panel(self):
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=60)
        
        ctk.CTkLabel(self.right_frame, text="Acceso al Sistema", font=FONT_TITLE, text_color=COLOR_TEXT_MAIN, anchor="w").pack(fill="x", pady=(80, 10))
        
        badge = ctk.CTkFrame(self.right_frame, **STYLE_BADGE)
        badge.pack(anchor="w", pady=(0, 20))
        ctk.CTkLabel(badge, text="ⓘ Auto-registro habilitado", **STYLE_BADGE_TEXT).pack(padx=12, pady=2)

        self.user_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Usuario", **STYLE_INPUT)
        self.user_entry.pack(fill="x", pady=10)
        self.pass_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Contraseña", show="*", **STYLE_INPUT)
        self.pass_entry.pack(fill="x", pady=10)

        self.error_label = ctk.CTkLabel(self.right_frame, text="", text_color=COLOR_ERROR, font=FONT_REGULAR)
        self.error_label.pack(pady=5)

        self.login_btn = ctk.CTkButton(self.right_frame, text="ENTRAR AL TABLERO", command=self._handle_auth, **STYLE_BUTTON_PRIMARY)
        self.login_btn.pack(fill="x", pady=(20, 80))

    def _handle_auth(self):
        u, p = self.user_entry.get().strip(), self.pass_entry.get().strip()
        if not u or not p:
            self.error_label.configure(text="⚠️ Rellena todos los campos")
            return
        
        if self.auth.login(u, p) or self.auth.register(u, p):
            save_json(self.session_file, {
                "u": encode_to_base64(u),
                "p": encode_to_base64(p)
            })
            self.on_success()
        else:
            self.error_label.configure(text="❌ Credenciales incorrectas")