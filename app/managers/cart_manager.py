from app.daos.cart_dao import CartDAO
from app.utils.logger_util import HermesLogger

class CartManager:
    def __init__(self):
        self.dao = CartDAO()
        self.log = HermesLogger.get_logger("CART_MANAGER")

    def add_to_cart(self, user_id, product_id, quantity=1):
        self.log.debug(f"Intentando añadir: User={user_id}, Prod={product_id}, Qty={quantity}")
        if not user_id:
            self.log.warning("Intento de añadir al carrito sin user_id válido.")
            return False
        res = self.dao.add_to_cart(user_id, product_id, quantity)
        self.log.info(f"Resultado DAO add_to_cart: {res}")
        return res

    def remove_from_cart(self, user_id, product_id):
        self.log.debug(f"Intentando eliminar: User={user_id}, Prod={product_id}")
        if not user_id: return False
        return self.dao.remove_from_cart(user_id, product_id)

    def get_items(self, user_id):
        self.log.debug(f"TRAZA: get_items solicitado para user_id: {user_id}")
        if user_id is None:
            self.log.error("TRAZA: user_id es NONE.")
            return []
        items = self.dao.get_user_cart(user_id)
        return items

    def get_suggestions(self, user_id):
        self.log.info(f"Generando sugerencias de ahorro para el usuario {user_id}")
        return self.dao.get_savings_suggestions(user_id)

    def empty_cart(self, user_id):
        self.log.info(f"Vaciando carrito del usuario {user_id}")
        return self.dao.clear_cart(user_id)