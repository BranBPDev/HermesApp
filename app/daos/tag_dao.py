from app.managers.db_manager import DBManager

class TagDAO:
    def __init__(self):
        self.db = DBManager()

    def get_matching_tags(self, partial_tag: str):
        sql = "SELECT name FROM tag WHERE name ILIKE %s ORDER BY name ASC LIMIT 10"
        return self.db.execute_query(sql, (f"{partial_tag}%",), fetch=True)

    def get_or_create_tag_id(self, tag_name: str):
        sql = """
            INSERT INTO tag (name) VALUES (%s)
            ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
            RETURNING id
        """
        res = self.db.execute_query(sql, (tag_name,), fetch=True)
        return res[0]['id'] if res else None