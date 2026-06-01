from app.daos.user_dao import UserDAO
from app.utils.logger_util import HermesLogger
from app.utils.paths_util import SESSION_JSON
from app.utils.json_util import save_json, read_json_local
from app.utils.crypto_util import encode_to_base64, decode_from_base64

class AuthManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthManager, cls).__new__(cls)
            cls._instance.user_dao = UserDAO()
            cls._instance.log = HermesLogger.get_logger("AUTH_MANAGER")
            cls._instance.current_user_id = None
            cls._instance.username = None
        return cls._instance

    def attempt_autologin(self):
        """Lógica delegada al AuthManager: intentar recuperar sesión."""
        if not SESSION_JSON.exists(): return False
        try:
            data = read_json_local(SESSION_JSON)
            user = decode_from_base64(data["u"])
            password = decode_from_base64(data["p"])
            success, _ = self.login(user, password)
            return success
        except: return False

    def _save_session(self, identifier, password):
        try:
            data = {"u": encode_to_base64(identifier), "p": encode_to_base64(password)}
            save_json(SESSION_JSON, data)
        except Exception as e:
            self.log.error(f"Error guardando sesión: {e}")

    def login(self, identifier, password, remember=False):
        if not identifier.strip() or not password.strip():
            return False, "Por favor, rellena todos los campos."

        self.log.info(f"Intento de login para usuario: {identifier}")
        try:
            user_id, real_username = self.user_dao.validate_user(identifier, password)
            if user_id:
                self.current_user_id = user_id
                self.username = real_username
                self.log.info(f"LOGIN EXITOSO: ID={self.current_user_id} | User={self.username}")
                if remember:
                    self._save_session(identifier, password)
                return True, "Success"
            
            return False, "Credenciales incorrectas."
        except Exception as e:
            self.log.error(f"Error en login: {e}")
            return False, "Error interno del sistema."

    def register(self, username, email, password, remember=False):
        try:
            user_id = self.user_dao.create_user(username, email, password)
            if user_id:
                self.current_user_id = user_id
                self.username = username
                if remember:
                    self._save_session(username, password)
                return True, "Registro exitoso"
        except Exception as e:
            self.log.error(f"Error en registro: {e}")
            return False, "Error al crear la cuenta"
        return False, "No se pudo crear el usuario"

    def logout(self):
        if SESSION_JSON.exists():
            try: SESSION_JSON.unlink()
            except: pass
        self.current_user_id = None
        self.username = None