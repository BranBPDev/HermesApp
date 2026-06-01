from app.daos.rating_dao import RatingDAO

class RatingManager:
    def __init__(self):
        self.dao = RatingDAO()

    def set_rating(self, user_id, product_id, rating):
        if user_id:
            return self.dao.save_rating(user_id, product_id, rating)
        return False