# Implements the entities described in the Scenario [cite: 9, 13]
class User:
    def __init__(self, username, password_hash, role="staff", user_id=None):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }

class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name