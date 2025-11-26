import hashlib
from models import User

class AuthManager:
    def __init__(self, db_instance):
        # Dependency Injection: We pass the database into the manager
        self.db = db_instance

    def _hash_password(self, password):
        """Private method to hash passwords."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        """Logic for registering a user."""
        if not username or not password:
            return False, "Username and password required"

        if len(password) < 4:
            return False, "Password must be at least 4 characters"

        # Check if user already exists
        if self.db.find_user_by_username(username):
            return False, "User already exists"

        # Create new User object
        hashed_pw = self._hash_password(password)
        new_user = User(username=username, password_hash=hashed_pw)

        # Save to DB
        if self.db.save_user(new_user):
            return True, "User registered successfully"
        else:
            return False, "Database error"

    def login(self, username, password):
        """Logic for logging in."""
        user = self.db.find_user_by_username(username)

        if not user:
            return False, "User not found"

        # Verify password
        input_hash = self._hash_password(password)
        
        if input_hash == user.password_hash:
            return True, "Login successful"
        else:
            return False, "Invalid password"