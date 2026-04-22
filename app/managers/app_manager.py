import customtkinter as ctk
import threading
import traceback
from app.utils.logger_util import HermesLogger
from app.utils.update_util import is_latest_version, perform_update
from app.utils.paths_util import LOGO_ICO, SESSION_JSON
from app.utils.json_util import read_json_local
from app.utils.crypto_util import decode_from_base64
from app.utils.window_util import center_window
from app.views.styles import COLOR_BG_DARK

class AppManager:
    def __init__(self):
        self.log = HermesLogger.get_logger("APP_MANAGER")
        self.log.info("--- [START] INICIALIZANDO APP_MANAGER ---")
        
        try:
            ctk.set_appearance_mode("dark")
            self.root = ctk.CTk()
            self.root.title("HERMESAPP - INTELIGENCIA DE MERCADO")
            self.root.configure(fg_color=COLOR_BG_DARK)
            
            # Tamaño inicial 1050x720, centrada y REDIMENSIONABLE
            center_window(self.root, 800, 500, resizable=True)
            self.root.minsize(800, 500)
            
            if LOGO_ICO.exists():
                try:
                    self.root.iconbitmap(str(LOGO_ICO))
                except Exception as e_ico:
                    self.log.warning(f"Error cargando icono: {e_ico}")
                
        except Exception as e:
            self.log.error(f"FALLO CRÍTICO EN CTK INIT: {traceback.format_exc()}")
            
        self.current_view = None
        self.auth = None

    def start(self):
        try:
            verifying_update = is_latest_version()
            if not verifying_update:
                self.show_update()
            elif self._try_autologin():
                self.show_main()
            else:
                self.show_login()
        except Exception:
            self.show_login()
        
        self.root.mainloop()

    def _try_autologin(self):
        if not SESSION_JSON.exists(): return False
        try:
            data = read_json_local(SESSION_JSON)
            u = decode_from_base64(data["u"])
            p = decode_from_base64(data["p"])
            from app.managers.auth_manager import AuthManager
            if not self.auth: self.auth = AuthManager()
            return self.auth.login(u, p)
        except Exception:
            return False

    def _clear_root(self):
        if self.current_view:
            self.current_view.destroy()

    def show_update(self):
        self._clear_root()
        from app.views.update_view import UpdateView
        self.current_view = UpdateView(self.root)
        self.current_view.pack(expand=True, fill="both")
        threading.Thread(target=perform_update, args=(self.current_view.set_progress,), daemon=True).start()

    def show_login(self):
        self._clear_root()
        from app.views.auth_window import AuthView
        from app.managers.auth_manager import AuthManager
        if not self.auth: self.auth = AuthManager()
        self.current_view = AuthView(self.root, self.auth, on_success=self.show_main)
        self.current_view.pack(expand=True, fill="both")

    def show_main(self):
        self._clear_root()
        try:
            from app.views.main_window import HermesMainView
            self.current_view = HermesMainView(self.root, self)
            self.current_view.pack(expand=True, fill="both")
        except Exception:
            self.log.error(f"Error en show_main: {traceback.format_exc()}")

    def logout(self):
        if SESSION_JSON.exists(): SESSION_JSON.unlink()
        self.auth = None 
        self.show_login()