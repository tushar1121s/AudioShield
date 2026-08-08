import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_code TEXT PRIMARY KEY,
            file_name TEXT NOT NULL,
            expiry_time TIMESTAMP NOT NULL,
            plan TEXT DEFAULT 'free'
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database initialized and Table created!")

if __name__ == "__main__":
    init_db()