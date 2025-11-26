class User:
    def __init__(self, username, password_hash, user_id=None):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash

    def to_dict(self):
        """Converts user object to a dictionary for API responses."""
        return {
            "id": self.id,
            "username": self.username
        }
    
    def __repr__(self):
        return f"<User {self.username}>"