from ...conf.db import get_db, close_db


class Operations:
    def get_all(self):
        db, c = get_db()
        query = """
        SELECT name, IF(active=1, "Activo", "Desactivado") as estado
        FROM operations
        """
        c.execute(query)
        values = c.fetchall()
        close_db()
        return values
