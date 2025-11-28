from build_connection import BuildConnection
from entities import User
import bcrypt

class UserModel:

    @staticmethod
    def create(user_id, email, role, password_hash):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            INSERT INTO users (user_id, email, role, password_hash)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (user_id, email, role, password_hash))
        conn.commit()

        cur.close()
        conn.close()
        return user_id

    @staticmethod
    def verify(email, password):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row is None:
            return None

        user = User(
            user_id=row[0],
            email=row[1],
            role=row[2],
            password_hash=row[3]
        )

        # compare hashed password 
        if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return user

        return None
