import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class DBHandler:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database and create tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT,
                            username TEXT UNIQUE,
                            email TEXT UNIQUE,
                            password TEXT,
                            role TEXT DEFAULT 'user'
                        )''')
        conn.close()

    def add_user(self, first_name, last_name, username, email, password, role='user'):
        """Add a new user to the database with hashed password and role."""
        hashed_password = generate_password_hash(password)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (first_name, last_name, username, email, password, role) VALUES (?, ?, ?, ?, ?, ?)', 
                           (first_name, last_name, username, email, hashed_password, role))
            conn.commit()
            return True  # Registration successful
        except sqlite3.IntegrityError:
            return False  # Username or email already exists
        finally:
            conn.close()

    def verify_user(self, username, password):
        """Verify a user's credentials."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[0], password):
            return True  # Login successful
        return False  # Login failed

    def get_user_role(self, username):
        """Retrieve the user's role based on their username."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT role FROM users WHERE username = ?', (username,))
        role = cursor.fetchone()
        conn.close()
        return role[0] if role else None

    def get_all_users(self):
        """Retrieve all users from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT first_name, last_name, username, email, role FROM users')
        users = cursor.fetchall()
        conn.close()
        return users
    
    def get_user(self, username):
        """ Retrieve a user from the database by username. """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, last_name, username, email, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user

    def update_user(self, username, updated_data):
        """ Update a user's information in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET first_name = ?, last_name = ?, role = ?
            WHERE username = ?
        """, (updated_data['first_name'], updated_data['last_name'], updated_data['role'], username))
        conn.commit()
        conn.close()

    def delete_user(self, username):
        """ Delete a user from the database by username. """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()
