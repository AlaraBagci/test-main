import sqlite3
import random
from models import User

class Database:
    def __init__(self, db_name="wellbeing.db"):
        self.db_name = db_name
        self.init_db()

    def _get_conn(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self._get_conn()
        # 1. Users Table (With Role column)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'staff'
            )
        ''')
        # 2. Students Table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        # 3. Surveys Table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS surveys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                week INTEGER,
                stress_level INTEGER,
                hours_sleep REAL,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        ''')
        conn.commit()
        conn.close()

    # --- Synthetic Data (Requirement: Version 0.2 Prototype) ---
    def generate_synthetic_data(self):
        conn = self._get_conn()
        conn.execute("DELETE FROM surveys")
        conn.execute("DELETE FROM students")
        
        names = ["Alice", "Bob", "Charlie", "Diana", "Ethan"]
        for name in names:
            cur = conn.execute("INSERT INTO students (name) VALUES (?)", (name,))
            student_id = cur.lastrowid
            
            for week in range(1, 11):
                # Program "Charlie" to be High Risk for the Demo
                stress = 5 if name == "Charlie" and week > 5 else random.randint(1, 4)
                sleep = random.randint(4, 9)
                
                conn.execute(
                    "INSERT INTO surveys (student_id, week, stress_level, hours_sleep) VALUES (?, ?, ?, ?)", 
                    (student_id, week, stress, sleep)
                )
        conn.commit()
        conn.close()

    # --- Analytics Queries ---
    def get_student_averages(self):
        conn = self._get_conn()
        query = '''
            SELECT s.id, s.name, AVG(sv.stress_level) as avg_stress, AVG(sv.hours_sleep) as avg_sleep
            FROM students s
            JOIN surveys sv ON s.id = sv.student_id
            GROUP BY s.id
        '''
        rows = conn.execute(query).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_student_history(self, student_id):
        conn = self._get_conn()
        rows = conn.execute(
            "SELECT week, stress_level, hours_sleep FROM surveys WHERE student_id = ? ORDER BY week", 
            (student_id,)
        ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # --- Auth Methods ---
    def save_user(self, user: User):
        conn = self._get_conn()
        try:
            conn.execute(
                'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)', 
                (user.username, user.password_hash, user.role)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def find_user_by_username(self, username):
        conn = self._get_conn()
        row = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if row:
            return User(row['username'], row['password_hash'], row['role'], row['id'])
        return None