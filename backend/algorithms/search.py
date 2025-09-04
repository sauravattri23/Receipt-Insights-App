import sqlite3
from backend.db.db_utils import DB_PATH
from backend.utils.logger import logger

def search_by_keyword(keyword: str):
    logger.info(f"Search by keyword: {keyword}")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = """
        SELECT * FROM receipts
        WHERE vendor LIKE ? OR category LIKE ?
        """
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        return cursor.fetchall()

def search_by_amount_range(min_amt: float, max_amt: float):
    logger.info(f"Search by amount range: {min_amt}-{max_amt}")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = """
        SELECT * FROM receipts
        WHERE amount BETWEEN ? AND ?
        """
        cursor.execute(query, (min_amt, max_amt))
        return cursor.fetchall()

def search_by_date_pattern(pattern: str):
    logger.info(f"Search by date pattern: {pattern}")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = """
        SELECT * FROM receipts
        WHERE date LIKE ?
        """
        cursor.execute(query, (f"%{pattern}%",))
        return cursor.fetchall()
