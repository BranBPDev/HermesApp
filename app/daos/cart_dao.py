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
            SELECT p.id as product_id, p.name, p.price, p.price_norm, 
                   c.quantity, (p.price * c.quantity) as subtotal, s.name as store_name
            FROM cart_item c
            JOIN product p ON c.product_id = p.id
            JOIN store s ON p.store_id = s.id
            WHERE c.user_id = %s
            ORDER BY p.name ASC
        """
        return self.db.execute_query(sql, (user_id,), fetch=True)

    def get_savings_suggestions(self, user_id):
        """
        Busca productos con el MISMO TAG pero menor PRECIO NORMALIZADO 
        en otras tiendas.
        """
        sql = """
            WITH current_items AS (
                SELECT p.tag, p.price_norm as curr_price_norm, p.name as curr_name, p.store_id
                FROM cart_item c
                JOIN product p ON c.product_id = p.id
                WHERE c.user_id = %s AND p.tag != 'otros'
            )
            SELECT DISTINCT ON (ci.curr_name)
                ci.curr_name as original_name,
                ci.curr_price_norm as original_price_norm,
                alt.name as suggestion_name,
                alt.price_norm as suggestion_price_norm,
                s.name as store_alt,
                (ci.curr_price_norm - alt.price_norm) as saving_per_unit
            FROM current_items ci
            JOIN product alt ON alt.tag = ci.tag 
            JOIN store s ON alt.store_id = s.id
            WHERE alt.price_norm < ci.curr_price_norm 
              AND alt.store_id != ci.store_id
            ORDER BY ci.curr_name, alt.price_norm ASC
        """
        return self.db.execute_query(sql, (user_id,), fetch=True)

    def clear_cart(self, user_id):
        sql = "DELETE FROM cart_item WHERE user_id = %s"
        return self.db.execute_query(sql, (user_id,), fetch=False)