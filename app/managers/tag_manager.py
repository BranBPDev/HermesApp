from app.daos.tag_dao import TagDAO

class TagManager:
    def __init__(self):
        self.dao = TagDAO()

    def get_suggestions(self, query):
        if len(query) < 1: return []
        results = self.dao.get_matching_tags(query)
        return [r['name'] for r in results] if results else []