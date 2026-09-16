import sqlite3
from werkzeug.security import generate_password_hash

def create_admin():
    conn = sqlite3.connect('skillhire.db')
    cursor = conn.cursor()
    
    name = "Platform Admin"
    email = "admin@skillhire.com"
    password = generate_password_hash("admin123")
    role = "admin"
    
    try:
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", 
                       (name, email, password, role))
        conn.commit()
        print("Successfully created Admin account!")
        print(f"Email: {email}")
        print("Password: admin123")
    except sqlite3.IntegrityError:
        print("Admin account already exists or email is taken.")
    finally:
        conn.close()

if __name__ == "__main__":
    create_admin()
