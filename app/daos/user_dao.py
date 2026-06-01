from app.managers.db_manager import DBManager
from app.utils.crypto_util import hash_password, check_password

class UserDAO:
    def __init__(self):
        self.db = DBManager()

    def create_user(self, username, email, password):
        password_hash = hash_password(password)
        sql = 'INSERT INTO "user" (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id'
        try:
            result = self.db.execute_query(sql, (username.lower(), email.lower(), password_hash), fetch=True)
            return result[0]['id'] if result else None
        except Exception as e:
            from app.utils.logger_util import HermesLogger
            HermesLogger.get_logger("USER_DAO").error(f"Error creando usuario: {e}")
            return None

    def validate_user(self, identifier, password):
        sql = 'SELECT id, username, password_hash FROM "user" WHERE username = %s OR email = %s'
        result = self.db.execute_query(sql, (identifier.lower(), identifier.lower()), fetch=True)
        
        if result:
            if check_password(password, result[0]['password_hash']):
                return result[0]['id'], result[0]['username']
        return None, None