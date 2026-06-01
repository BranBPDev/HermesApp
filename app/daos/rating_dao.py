from app.managers.db_manager import DBManager

class RatingDAO:
    def __init__(self):
        self.db = DBManager()

    def save_rating(self, user_id, product_id, rating):
        query = """
            INSERT INTO product_rating (user_id, product_id, rating, created_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (user_id, product_id) 
            DO UPDATE SET rating = EXCLUDED.rating, created_at = CURRENT_TIMESTAMP;
        """
        try:
            self.db.execute_query(query, (user_id, product_id, rating))
            return True
        except Exception as e:
            from app.utils.logger_util import HermesLogger
            HermesLogger.get_logger("RATING_DAO").error(f"Error al guardar valoración: {e}")
            return False