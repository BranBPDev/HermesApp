import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from app.utils.logger_util import HermesLogger
from app.utils.paths_util import ENV_PATH

class DBManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance.log = HermesLogger.get_logger("DB_MANAGER")
            
            # Carga del .env desde el path oficial definido en paths_util
            if ENV_PATH.exists():
                load_dotenv(str(ENV_PATH))
            
            cls._instance.url = os.getenv("DATABASE_URL")
        return cls._instance

    def _get_connection(self):
        try:
            if not self.url:
                raise ValueError("DATABASE_URL no configurada en el entorno.")
            return psycopg2.connect(self.url)
        except Exception as e:
            self.log.error(f"Error de conexión: {e}")
            return None

    def execute_query(self, query, params=None, fetch=True):
        conn = self._get_connection()
        if not conn: return None
        result = None
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if fetch and cur.description:
                    result = cur.fetchall()
                conn.commit()
        except Exception as e:
            self.log.error(f"Error en query: {e}")
            conn.rollback()
        finally:
            conn.close()
        return result