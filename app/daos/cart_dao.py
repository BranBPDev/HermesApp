from app.managers.db_manager import DBManager

class CartDAO:
    def __init__(self):
        self.db = DBManager()

    def add_to_cart(self, user_id, product_id, quantity=1):
        sql = """
            INSERT INTO cart_item (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, product_id)
            DO UPDATE SET quantity = cart_item.quantity + EXCLUDED.quantity
        """
        self.db.execute_query(sql, (user_id, product_id, quantity), fetch=False)

    def get_user_cart(self, user_id):
        sql = """
            SELECT p.name, p.price, c.quantity, (p.price * c.quantity) as subtotal, s.name as store_name
            FROM cart_item c
            JOIN product p ON c.product_id = p.id
            JOIN store s ON p.store_id = s.id
            WHERE c.user_id = %s
        """
        return self.db.execute_query(sql, (user_id,), fetch=True)

    def clear_cart(self, user_id):
        """Elimina todos los productos del carrito de un usuario específico."""
        sql = "DELETE FROM cart_item WHERE user_id = %s"
        return self.db.execute_query(sql, (user_id,), fetch=False)