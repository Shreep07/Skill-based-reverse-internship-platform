import sqlite3
from werkzeug.security import generate_password_hash
import os

def reset_user_password():
    print("─── SKILLHIRE PASSWORD RESET TOOL ───")
    email = input("Enter the user's Email: ").strip()
    new_password = input("Enter the NEW Password: ").strip()

    if not email or not new_password:
        print("Error: Email and Password cannot be empty.")
        return

    db_path = 'skillhire.db'
    
    if not os.path.exists(db_path):
        print(f"Error: {db_path} not found. Are you in the project root directory?")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT name FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    if not user:
        print(f"Error: No user found with email '{email}'.")
        conn.close()
        return

    hashed_pw = generate_password_hash(new_password)
    
    try:
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_pw, email))
        conn.commit()
        print(f"Success! Password for {user[0]} ({email}) has been updated.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    reset_user_password()
