from app.daos.cart_dao import CartDAO
from app.utils.logger_util import HermesLogger

class CartManager:
    def __init__(self):
        self.dao = CartDAO()
        self.log = HermesLogger.get_logger("CART_MANAGER")

    def add_to_cart(self, user_id, product_id, quantity=1):
        self.log.info(f"Añadiendo producto {product_id} al carrito del usuario {user_id}")
        return self.dao.add_to_cart(user_id, product_id, quantity)

    def get_items(self, user_id):
        self.log.info(f"Obteniendo items del carrito para el usuario {user_id}")
        return self.dao.get_user_cart(user_id)

    def get_suggestions(self, user_id):
        self.log.info(f"Generando sugerencias de ahorro para el usuario {user_id}")
        return self.dao.get_savings_suggestions(user_id)

    def empty_cart(self, user_id):
        self.log.info(f"Vaciando carrito del usuario {user_id}")
        return self.dao.clear_cart(user_id)