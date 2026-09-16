import sqlite3
import os

db_path = "skillhire.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"Current columns in users table: {columns}")
    
    needed = ["website", "contact", "tax_id", "verification_status"]
    missing = [c for c in needed if c not in columns]
    
    if missing:
        print(f"Missing columns: {missing}. Adding them...")
        for col in missing:
            if col == "verification_status":
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT DEFAULT 'Pending'")
            else:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT")
        conn.commit()
        print("Migration complete.")
    else:
        print("Schema is up to date.")
    conn.close()
else:
    print("Database does not exist yet. Running init_db from database.py...")
    from database import init_db
    init_db()
