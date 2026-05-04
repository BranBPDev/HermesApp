from app.daos.cart_dao import CartDAO

class CartManager:
    def __init__(self):
        self.dao = CartDAO()

    def add_to_cart(self, user_id, product_id, quantity=1):
        return self.dao.add_to_cart(user_id, product_id, quantity)

    def get_items(self, user_id):
        # El DAO ya devuelve la lista de diccionarios necesarios
        return self.dao.get_user_cart(user_id)

    def get_suggestions(self, user_id):
        return self.dao.get_savings_suggestions(user_id)

    def empty_cart(self, user_id):
        return self.dao.clear_cart(user_id)