from app.managers.db_manager import DBManager
from app.utils.logger_util import HermesLogger

class RatingDAO:
    def __init__(self):
        self.db = DBManager()
        self.log = HermesLogger.get_logger("RATING_DAO")

    def save_rating(self, user_id, product_id, rating):
        query = """
            INSERT INTO product_rating (user_id, product_id, rating, created_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (user_id, product_id) 
            DO UPDATE SET rating = EXCLUDED.rating, created_at = CURRENT_TIMESTAMP;
        """
        try:
            self.db.execute_query(query, (user_id, product_id, rating))
            self.log.info(f"Valoración guardada: User {user_id} -> Prod {product_id} ({rating})")
            return True
        except Exception as e:
            self.log.error(f"Error al guardar valoración: {e}")
            return False