import psycopg2.extras
from app.managers.db_manager import DBManager
from app.utils.logger_util import HermesLogger
from datetime import date

class ProductDAO:
    def __init__(self):
        self.log = HermesLogger.get_logger("PRODUCT_DAO")
        self.db = DBManager()

    def upsert_batch(self, store_name: str, products: list):
        """
        Inserta o actualiza productos masivamente filtrando duplicados en el origen.
        """
        store_res = self.db.execute_query("SELECT id FROM store WHERE name = %s", (store_name.lower(),), fetch=True)
        if not store_res:
            self.log.error(f"No se encontró la tienda {store_name} en la base de datos.")
            return
        
        store_id = store_res[0]['id']
        today = date.today()
        
        # --- FILTRO DE DUPLICADOS (Previene error de PostgreSQL) ---
        unique_products = {}
        for p in products:
            nombre = p.get('nombre')
            if nombre and nombre not in unique_products:
                unique_products[nombre] = p
        
        clean_list = list(unique_products.values())
        # -----------------------------------------------------------

        query = """
            INSERT INTO product (store_id, name, price, quantity, unit_type, image_url, last_update)
            VALUES %s
            ON CONFLICT (name, store_id) 
            DO UPDATE SET 
                last_update = CASE 
                    WHEN product.price <> EXCLUDED.price THEN EXCLUDED.last_update 
                    ELSE product.last_update 
                END,
                image_url = EXCLUDED.image_url,
                quantity = EXCLUDED.quantity,
                unit_type = EXCLUDED.unit_type,
                price = EXCLUDED.price;
        """
        
        conn = self.db._get_connection()
        if not conn: return
        
        try:
            with conn.cursor() as cur:
                data_list = [
                    (
                        store_id, 
                        p['nombre'], 
                        p['precio'], 
                        p['cantidad'], 
                        p['tipo_unidad'], 
                        p['imagen'],
                        today
                    )
                    for p in clean_list
                ]
                psycopg2.extras.execute_values(cur, query, data_list)
                
            conn.commit()
            self.log.info(f"✅ CLOUD: {store_name.upper()} sincronizado ({len(clean_list)} productos únicos).")
            
        except Exception as e:
            self.log.error(f"❌ Error en upsert_batch para {store_name}: {e}")
            conn.rollback()
        finally:
            conn.close()

    def search_by_name(self, query_text: str):
        sql = """
            SELECT p.*, s.name as store_name
            FROM product p
            JOIN store s ON p.store_id = s.id
            WHERE p.name ILIKE %s
            ORDER BY p.price ASC
            LIMIT 100
        """
        formatted_query = f"%{query_text.replace(' ', '%')}%"
        return self.db.execute_query(sql, (formatted_query,), fetch=True)