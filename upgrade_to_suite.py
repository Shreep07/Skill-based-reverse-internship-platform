import sqlite3

def upgrade():
    conn = sqlite3.connect("skillhire.db")
    cursor = conn.cursor()

    print("Upgrading database to support Test Suites (Easy, Medium, Hard)...")

    # 1. Add 'level' to task_variants
    try:
        cursor.execute("ALTER TABLE task_variants ADD COLUMN level TEXT DEFAULT 'Easy'")
        print("Added 'level' column to task_variants.")
    except Exception as e:
        print(f"Column 'level' might already exist: {e}")

    # 2. Update assignments to store 3 variant IDs
    try:
        cursor.execute("ALTER TABLE assignments ADD COLUMN variant_easy_id INTEGER")
        cursor.execute("ALTER TABLE assignments ADD COLUMN variant_medium_id INTEGER")
        cursor.execute("ALTER TABLE assignments ADD COLUMN variant_hard_id INTEGER")
        print("Added variant_id columns to assignments.")
    except Exception as e:
        print(f"Columns might already exist in assignments: {e}")

    # 3. Update submissions to store 3 solutions
    try:
        cursor.execute("ALTER TABLE submissions ADD COLUMN solution_easy TEXT")
        cursor.execute("ALTER TABLE submissions ADD COLUMN solution_medium TEXT")
        cursor.execute("ALTER TABLE submissions ADD COLUMN solution_hard TEXT")
        cursor.execute("ALTER TABLE submissions ADD COLUMN autosave_easy TEXT")
        cursor.execute("ALTER TABLE submissions ADD COLUMN autosave_medium TEXT")
        cursor.execute("ALTER TABLE submissions ADD COLUMN autosave_hard TEXT")
        print("Added solution columns to submissions.")
    except Exception as e:
        print(f"Columns might already exist in submissions: {e}")

    # 4. Ensure activity_logs exists
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assignment_id INTEGER,
                event_type TEXT,
                logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (assignment_id) REFERENCES assignments(id)
            )
        ''')
        print("Ensured activity_logs table exists.")
    except Exception as e:
        print(f"Error creating activity_logs: {e}")

    conn.commit()

    conn.close()
    print("Migration complete!")

if __name__ == "__main__":
    upgrade()
