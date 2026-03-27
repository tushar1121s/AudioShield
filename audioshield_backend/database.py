import sqlite3
from datetime import datetime, timedelta

# Database initialize karne ka function
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Rooms table banana
    # room_code: unique id (e.g., AX9-K32)
    # file_path: server pe file kahan saved hai
    # expiry: kab delete karna hai
    # plan: free ya pro
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_code TEXT PRIMARY KEY,
            file_name TEXT NOT NULL,
            expiry_time DATETIME NOT NULL,
            plan TEXT DEFAULT 'free'
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized and Table created!")

if __name__ == "__main__":
    init_db()