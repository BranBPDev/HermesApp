import psycopg2.extras
from app.managers.db_manager import DBManager
from app.utils.dates_util import get_current_date_str

class ProductDAO:
    def __init__(self):
        self.db = DBManager()

    def upsert_batch(self, store_name: str, products: list):
        store_res = self.db.execute_query("SELECT id FROM store WHERE name = %s", (store_name.lower(),), fetch=True)
        if not store_res: 
            from app.utils.logger_util import HermesLogger
            HermesLogger.get_logger("PRODUCT_DAO").error(f"Tienda {store_name} no encontrada")
            return
        
        store_id = store_res[0]['id']
        today_str = get_current_date_str()

        query = """
            INSERT INTO product (store_id, name, tag, price, price_norm, quantity, unit_type, image_url, last_update)
            VALUES %s
            ON CONFLICT (name, store_id) 
            DO UPDATE SET 
                price = EXCLUDED.price,
                price_norm = EXCLUDED.price_norm,
                quantity = EXCLUDED.quantity,
                unit_type = EXCLUDED.unit_type,
                image_url = EXCLUDED.image_url,
                last_update = EXCLUDED.last_update
            WHERE (product.price IS DISTINCT FROM EXCLUDED.price OR 
                   product.price_norm IS DISTINCT FROM EXCLUDED.price_norm OR
                   product.quantity IS DISTINCT FROM EXCLUDED.quantity OR
                   product.unit_type IS DISTINCT FROM EXCLUDED.unit_type OR
                   product.image_url IS DISTINCT FROM EXCLUDED.image_url);
        """
        
        conn = self.db.get_connection()
        if not conn: return
        try:
            with conn.cursor() as cur:
                unique_prods = {}
                for p in products:
                    nombre = p.get('nombre', 'Sin nombre')
                    try:
                        precio = float(p.get('precio', 0.0))
                        p_norm = float(p.get('precio_norm', 0.0))
                        qty = float(p.get('cantidad', 0.0))
                    except (TypeError, ValueError):
                        precio, p_norm, qty = 0.0, 0.0, 0.0

                    # TAG fijado a _temp como pediste para nuevos registros
                    unique_prods[nombre] = (
                        store_id, 
                        nombre, 
                        "_temp", 
                        precio, 
                        p_norm, 
                        qty, 
                        p.get('tipo_unidad', 'ud'), 
                        p.get('imagen_url', ''), # CORREGIDO: ahora busca 'imagen_url'
                        today_str
                    )
                data_list = list(unique_prods.values())
                psycopg2.extras.execute_values(cur, query, data_list)
            conn.commit()
        except Exception as e:
            from app.utils.logger_util import HermesLogger
            HermesLogger.get_logger("PRODUCT_DAO").error(f"Error en upsert_batch: {e}")
            if conn: conn.rollback()
        finally:
            if conn: self.db.release_connection(conn)

    def search_by_tag(self, query_tag: str, order_by: str = "p.price_norm ASC"):
        sql = f"""
            SELECT p.*, s.name as store_name
            FROM product p
            JOIN store s ON p.store_id = s.id
            WHERE p.tag ILIKE %s
            ORDER BY {order_by} LIMIT 150
        """
        return self.db.execute_query(sql, (f"%{query_tag}%",), fetch=True)