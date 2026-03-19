import bcrypt
import psycopg2
from app.managers.db_manager import DBManager
from app.utils.logger_util import HermesLogger

class UserDAO:
    def __init__(self):
        self.db = DBManager()
        self.log = HermesLogger.get_logger("USER_DAO")

    def create_user(self, username, password):
        salt = bcrypt.gensalt()
        # El hash de bcrypt ya incluye el salt, no necesitas guardarlo aparte
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        sql = 'INSERT INTO "user" (username, password_hash) VALUES (%s, %s) RETURNING id'
        try:
            result = self.db.execute_query(sql, (username.lower(), password_hash), fetch=True)
            return result[0]['id'] if result else None
        except Exception as e:
            # Capturamos si el usuario ya existe para no romper la app
            self.log.error(f"Error creando usuario (posible duplicado): {e}")
            return None

    def validate_user(self, username, password):
        sql = 'SELECT id, password_hash FROM "user" WHERE username = %s'
        result = self.db.execute_query(sql, (username.lower(),), fetch=True)
        
        if result:
            stored_hash = result[0]['password_hash'].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                return result[0]['id']
        return None