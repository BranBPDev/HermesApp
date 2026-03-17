from app.daos.user_dao import UserDAO
from app.utils.logger_util import HermesLogger

class AuthManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthManager, cls).__new__(cls)
            cls._instance.user_dao = UserDAO()
            cls._instance.current_user_id = None
            cls._instance.username = None
        return cls._instance

    def login(self, username, password):
        user_id = self.user_dao.validate_user(username, password)
        if user_id:
            self.current_user_id = user_id
            self.username = username
            return True
        return False

    def register(self, username, password):
        try:
            user_id = self.user_dao.create_user(username, password)
            if user_id:
                self.current_user_id = user_id
                self.username = username
                return True
        except Exception:
            return False
        return False

    def logout(self):
        self.current_user_id = None
        self.username = None