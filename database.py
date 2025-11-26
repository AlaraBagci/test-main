import sqlite3
from models import User

class Database:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self._get_conn()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def save_user(self, user: User):
        """Saves a User object to the database."""
        conn = self._get_conn()
        try:
            conn.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                (user.username, user.password_hash)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def find_user_by_username(self, username):
        """Returns a User object if found, else None."""
        conn = self._get_conn()
        row = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if row:
            # Convert raw SQL data back into a User object
            return User(
                user_id=row['id'], 
                username=row['username'], 
                password_hash=row['password_hash']
            )
        return None