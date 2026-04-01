import customtkinter as ctk
import threading
from app.utils.logger_util import HermesLogger
from app.utils.update_util import is_latest_version, perform_update
from app.utils.paths_util import LOGO_ICO, SESSION_JSON
from app.utils.json_util import read_json_local
from app.utils.crypto_util import decode_from_base64
from app.views.styles import COLOR_BG_DARK

class AppManager:
    def __init__(self):
        self.log = HermesLogger.get_logger("APP_MANAGER")
        
        self.root = ctk.CTk()
        self.root.title("HERMESAPP - INTELIGENCIA DE MERCADO")
        self.root.geometry("1100x700")
        self.root.configure(fg_color=COLOR_BG_DARK)
        
        try:
            if LOGO_ICO.exists():
                self.root.iconbitmap(str(LOGO_ICO))
        except Exception:
            pass
            
        self.current_view = None
        self.auth = None

    def start(self):
        try:
            if not is_latest_version():
                self.show_update()
            elif self._try_autologin():
                self.show_main()
            else:
                self.show_login()
        except Exception as e:
            self.log.error(f"Error en inicio: {e}")
            self.show_login()
        self.root.mainloop()

    def _try_autologin(self):
        """Intenta login automático leyendo el archivo local."""
        if not SESSION_JSON.exists():
            return False
        try:
            # Usamos el util para leer el JSON
            data = read_json_local(SESSION_JSON)
            u = decode_from_base64(data["u"])
            p = decode_from_base64(data["p"])
            
            from app.managers.auth_manager import AuthManager
            # IMPORTANTE: Inicializar auth si no existe
            if not self.auth:
                self.auth = AuthManager()
            
            if self.auth.login(u, p):
                self.log.info(f"Auto-login exitoso para el usuario: {u}")
                return True
            else:
                self.log.warning(f"Credenciales de sesión local ya no son válidas para: {u}")
                return False
        except Exception as e:
            self.log.error(f"Error en proceso de auto-login: {e}")
            return False

    def logout(self):
        if SESSION_JSON.exists():
            SESSION_JSON.unlink()
        self.auth = None
        self.show_login()

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
        self.root.geometry("1200x800")
        from app.views.main_window import HermesMainView
        self.current_view = HermesMainView(self.root, self)
        self.current_view.pack(expand=True, fill="both")