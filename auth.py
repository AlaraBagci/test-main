import hashlib
from models import User

class AuthManager:
    def __init__(self, db_instance):
        self.db = db_instance

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password, role="staff"):
        if self.db.find_user_by_username(username):
            return False, "User already exists"

        hashed_pw = self._hash_password(password)
        new_user = User(username=username, password_hash=hashed_pw, role=role)

        if self.db.save_user(new_user):
            return True, "User registered successfully"
        else:
            return False, "Database error"

    def login(self, username, password):
        user = self.db.find_user_by_username(username)
        if not user:
            return False, "User not found", None

        if self._hash_password(password) == user.password_hash:
            # Return the ROLE so the UI knows where to send them
            return True, "Login successful", user.role 
        else:
            return False, "Invalid password", None