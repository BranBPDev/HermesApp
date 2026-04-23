from app.daos.user_dao import UserDAO
from app.utils.logger_util import HermesLogger

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

    def login(self, username, password, remember=False):
        # Validación de campos vacíos
        if not username.strip() or not password.strip():
            return False, "Por favor, rellena todos los campos."

        try:
            # Validación de credenciales
            user_id = self.user_dao.validate_user(username, password)
            if user_id:
                self.current_user_id = user_id
                self.username = username
                # Aquí iría la lógica de 'remember' si fuera necesaria, 
                # por ahora solo evitamos el error de argumento.
                return True, "Success"
            
            return False, f"Contraseña incorrecta para el usuario {username}."
        except Exception as e:
            self.log.error(f"Error en login: {e}")
            return False, "Error interno del sistema."

    def register(self, username, password):
        try:
            user_id = self.user_dao.create_user(username, password)
            if user_id:
                self.current_user_id = user_id
                self.username = username
                return True
        except Exception as e:
            self.log.error(f"Error en registro: {e}")
            return False
        return False

    def logout(self):
        self.current_user_id = None
        self.username = None