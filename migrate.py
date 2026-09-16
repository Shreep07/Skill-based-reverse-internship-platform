import sqlite3

def migrate():
    conn = sqlite3.connect("skillhire.db")
    cursor = conn.cursor()

    def add_column_if_missing(table, column, col_type):
        cols = [row[1] for row in cursor.execute(f"PRAGMA table_info({table})").fetchall()]
        if column not in cols:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
            print(f"Added {table}.{column}")
        else:
            print(f"Already exists: {table}.{column}")

    # assignments table
    add_column_if_missing("assignments", "language", "TEXT")

    # submissions table
    add_column_if_missing("submissions", "autosave", "TEXT")

    # verification_questions table (older DB had MCQ columns, needs expected_answer)
    add_column_if_missing("verification_questions", "expected_answer", "TEXT")

    conn.commit()

    # Print final state
    for table in ["assignments", "submissions", "verification_questions"]:
        cols = [row[1] for row in cursor.execute(f"PRAGMA table_info({table})").fetchall()]
        print(f"{table}: {cols}")

    conn.close()
    print("\nMigration complete!")

if __name__ == "__main__":
    migrate()
