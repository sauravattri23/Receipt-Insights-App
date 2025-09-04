import sqlite3
from pathlib import Path
from backend.db.models import CREATE_RECEIPTS_TABLE
from backend.utils.logger import logger

DB_PATH = Path("data/db.sqlite3")
DB_PATH.parent.mkdir(exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(CREATE_RECEIPTS_TABLE)
    conn.commit()
    conn.close()
    logger.info("Database initialized.")

def insert_receipt(data: dict):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO receipts (vendor, date, amount, category)
            VALUES (?, ?, ?, ?)
        """, (data["vendor"], data["date"], float(data["amount"].replace(",", "")), data["category"]))

        conn.commit()
        logger.info(f"Inserted receipt for vendor: {data['vendor']}")
    except Exception as e:
        logger.error(f"Error inserting receipt: {str(e)}")
    finally:
        conn.close()
