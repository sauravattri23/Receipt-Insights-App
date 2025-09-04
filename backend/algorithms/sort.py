import sqlite3
from backend.db.db_utils import DB_PATH
from backend.utils.logger import logger

def sort_by_field(field: str, ascending=True):
    if field not in ["vendor", "date", "amount", "category"]:
        raise ValueError("Invalid sort field")

    order = "ASC" if ascending else "DESC"
    logger.info(f"Sorting by {field} in {order} order")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM receipts ORDER BY {field} {order}"
        cursor.execute(query)
        return cursor.fetchall()
