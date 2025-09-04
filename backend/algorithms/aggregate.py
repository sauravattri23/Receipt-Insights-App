import sqlite3
import statistics
from collections import Counter, defaultdict
from backend.db.db_utils import DB_PATH
from backend.utils.logger import logger

def compute_basic_stats():
    logger.info("Computing basic stats")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM receipts")
        amounts = [row[0] for row in cursor.fetchall()]

        stats = {
            "sum": round(sum(amounts), 2),
            "mean": round(statistics.mean(amounts), 2) if amounts else 0,
            "median": round(statistics.median(amounts), 2) if amounts else 0,
            "mode": round(statistics.mode(amounts), 2) if len(set(amounts)) > 1 else "N/A"
        }
        return stats

def vendor_frequency():
    logger.info("Calculating vendor frequency")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT vendor FROM receipts")
        vendors = [v[0] for v in cursor.fetchall()]
        return dict(Counter(vendors))

def monthly_trend():
    logger.info("Generating monthly spend trend")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT date, amount FROM receipts")
        month_totals = defaultdict(float)
        for date, amt in cursor.fetchall():
            if "-" in date:
                month = "-".join(date.split("-")[:2]) 
                month_totals[month] += amt
        return dict(sorted(month_totals.items()))
