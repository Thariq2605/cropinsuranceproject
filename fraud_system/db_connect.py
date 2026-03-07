import sqlite3
import os

try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "crop_insurance.db")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    
    # Initialize expected tables if they do not exist
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fraud_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmer_lands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id TEXT NOT NULL,
            survey_number TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL
        )
    """)
    conn.commit()
    cursor.close()

    print("✅ Connected successfully to SQLite")
except sqlite3.Error as err:
    print(f"❌ Database connection error: {err}")
    # Create a mock connection object or handle as needed
    class MockConn:
        def cursor(self):
            return MockCursor()
        def commit(self):
            pass
        def close(self):
            pass

    class MockCursor:
        def execute(self, *args, **kwargs):
            pass
        def fetchone(self):
            return None
        def fetchall(self):
            return []
        def close(self):
            pass
            
    conn = MockConn()
    print("⚠️ Using mock database connection due to failure")
