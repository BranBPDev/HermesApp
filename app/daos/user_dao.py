from app.managers.db_manager import DBManager
from app.utils.logger_util import HermesLogger
from app.utils.crypto_util import hash_password, check_password

class UserDAO:
    def __init__(self):
        self.db = DBManager()
        self.log = HermesLogger.get_logger("USER_DAO")

    def create_user(self, username, password):
        password_hash = hash_password(password)
        sql = 'INSERT INTO "user" (username, password_hash) VALUES (%s, %s) RETURNING id'
        try:
            result = self.db.execute_query(sql, (username.lower(), password_hash), fetch=True)
            return result[0]['id'] if result else None
        except Exception as e:
            self.log.error(f"Error creando usuario: {e}")
            return None

    def validate_user(self, username, password):
        sql = 'SELECT id, password_hash FROM "user" WHERE username = %s'
        result = self.db.execute_query(sql, (username.lower(),), fetch=True)
        
        if result:
            if check_password(password, result[0]['password_hash']):
                return result[0]['id']
        return None