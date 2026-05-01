from app.daos.user_dao import UserDAO
from app.utils.logger_util import HermesLogger
from app.utils.paths_util import SESSION_JSON
from app.utils.json_util import write_json_local
from app.utils.crypto_util import encode_to_base64

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

    def _save_session(self, identifier, password):
        try:
            data = {
                "u": encode_to_base64(identifier),
                "p": encode_to_base64(password)
            }
            write_json_local(SESSION_JSON, data)
        except Exception as e:
            self.log.error(f"Error guardando sesión: {e}")

    def login(self, identifier, password, remember=False):
        if not identifier.strip() or not password.strip():
            return False, "Por favor, rellena todos los campos."

        try:
            user_id, real_username = self.user_dao.validate_user(identifier, password)
            if user_id:
                self.current_user_id = user_id
                self.username = real_username
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
                    # En registro, el identificador suele ser el username
                    self._save_session(username, password)
                return True, "Registro completado"
        except Exception as e:
            self.log.error(f"Error en registro: {e}")
            return False, "Error al crear la cuenta"
        return False, "No se pudo crear el usuario"

    def logout(self):
        self.current_user_id = None
        self.username = None