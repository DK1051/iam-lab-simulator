import sqlite3
import json

def migrate():
    # 1. Connect to (or create) the database file
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # 2. Create the Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            failed_attempts INTEGER DEFAULT 0
        )
    ''')

    # 3. Load data from your existing users.json
    try:
        with open("users.json", "r") as file:
            data = json.load(file)
            users_list = data["users"]
        
        # 4. Insert users into the new SQL table
        for user in users_list:
            # We use .get() so if 'password' is missing, it looks for 'password_hash'
            # If both are missing, it defaults to None instead of crashing
            raw_password = user.get('password') or user.get('password_hash')

            cursor.execute('''
                INSERT OR IGNORE INTO users (username, password_hash, role, status, failed_attempts)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                user['username'], 
                raw_password, 
                user['role'], 
                user['status'], 
                user.get('failed_attempts', 0) # Default to 0 if not found
            ))
        
        conn.commit()
        print("✅ Migration Successful: users.db created and populated.")
    
    except FileNotFoundError:
        print("❌ Error: users.json not found.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()