import psycopg2.extras
from app.managers.db_manager import DBManager
from app.utils.logger_util import HermesLogger
from app.utils.dates_util import get_current_date_str

class ProductDAO:
    def __init__(self):
        self.log = HermesLogger.get_logger("PRODUCT_DAO")
        self.db = DBManager()

    def upsert_batch(self, store_name: str, products: list):
        store_res = self.db.execute_query("SELECT id FROM store WHERE name = %s", (store_name.lower(),), fetch=True)
        if not store_res: 
            self.log.error(f"Tienda {store_name} no encontrada")
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
                    qty = p.get('cantidad', 0)
                    try: qty = float(qty) if qty else 0.0
                    except: qty = 0.0

                    unique_prods[nombre] = (
                        store_id, nombre, "_temp",
                        float(p.get('precio', 0.0)), float(p.get('price_norm', 0.0)),
                        qty, p.get('tipo_unidad', 'ud'), p.get('imagen', ''), today_str
                    )
                data_list = list(unique_prods.values())
                psycopg2.extras.execute_values(cur, query, data_list)
            conn.commit()
        except Exception as e:
            self.log.error(f"Error en upsert_batch: {e}")
            if conn: conn.rollback()
        finally:
            if conn: self.db.release_connection(conn)

    def search_by_tag(self, query_tag: str, order_by: str = "p.price_norm ASC"):
        """ Búsqueda estricta por similitud en el campo TAG """
        sql = f"""
            SELECT p.*, s.name as store_name
            FROM product p
            JOIN store s ON p.store_id = s.id
            WHERE p.tag ILIKE %s
            ORDER BY {order_by} LIMIT 150
        """
        formatted_query = f"%{query_tag}%"
        return self.db.execute_query(sql, (formatted_query,), fetch=True)