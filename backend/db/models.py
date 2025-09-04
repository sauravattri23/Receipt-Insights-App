CREATE_RECEIPTS_TABLE = """
CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor TEXT NOT NULL,
    date TEXT,
    amount REAL,
    category TEXT DEFAULT 'Misc'
);
"""
