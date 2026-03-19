import os
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
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
            
            if ENV_PATH.exists():
                load_dotenv(str(ENV_PATH))
            
            url = os.getenv("DATABASE_URL")
            if not url:
                cls._instance.log.error("DATABASE_URL no configurada.")
                cls._instance.pool = None
            else:
                try:
                    # Creamos un Pool: min 1 conexión, max 10 (suficiente para 3 scrapers + app)
                    cls._instance.pool = ThreadedConnectionPool(1, 10, url)
                    cls._instance.log.info("Pool de conexiones DB inicializado.")
                except Exception as e:
                    cls._instance.log.error(f"Error creando Pool de conexiones: {e}")
                    cls._instance.pool = None
        return cls._instance

    def get_connection(self):
        """Pide una conexión al pool"""
        if self.pool:
            return self.pool.getconn()
        return None

    def release_connection(self, conn):
        """Devuelve la conexión al pool en lugar de cerrarla"""
        if self.pool and conn:
            self.pool.putconn(conn)

    def execute_query(self, query, params=None, fetch=True):
        """Método de conveniencia para queries rápidas"""
        conn = self.get_connection()
        if not conn: return None
        result = None
        try:
            # Importante: RealDictCursor para que devuelva diccionarios
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                if fetch and cur.description:
                    result = cur.fetchall()
                conn.commit()
        except Exception as e:
            self.log.error(f"Error en query: {e}")
            conn.rollback()
        finally:
            self.release_connection(conn)
        return result