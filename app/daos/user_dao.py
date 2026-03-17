import bcrypt
from app.managers.db_manager import DBManager
from app.utils.logger_util import HermesLogger

class UserDAO:
    def __init__(self):
        self.db = DBManager()
        self.log = HermesLogger.get_logger("USER_DAO")

    def create_user(self, username, password):
        """Hashea la contraseña y crea el usuario."""
        # Generar hash
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        sql = 'INSERT INTO "user" (username, password_hash) VALUES (%s, %s) RETURNING id'
        result = self.db.execute_query(sql, (username, password_hash), fetch=True)
        return result[0]['id'] if result else None

    def validate_user(self, username, password):
        """Verifica si las credenciales son correctas."""
        sql = 'SELECT id, password_hash FROM "user" WHERE username = %s'
        result = self.db.execute_query(sql, (username,), fetch=True)
        
        if result:
            stored_hash = result[0]['password_hash'].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                return result[0]['id'] # Devuelve ID si es válido
        return None