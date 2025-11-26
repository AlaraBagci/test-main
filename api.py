from flask import Flask, request, jsonify
from database import Database
from auth import AuthManager

app = Flask(__name__)

# --- OOP Initialization ---
# 1. Create the Database instance
db = Database("users.db")

# 2. Create the AuthManager and inject the database into it
auth_system = AuthManager(db)


@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "active", "architecture": "MVC OOP"}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    success, message = auth_system.register(data.get('username'), data.get('password'))
    
    status_code = 201 if success else 400
    return jsonify({"success": success, "message": message}), status_code

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    success, message = auth_system.login(data.get('username'), data.get('password'))
    
    status_code = 200 if success else 401
    return jsonify({"success": success, "message": message}), status_code

if __name__ == '__main__':
    print("Running OOP Flask API on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)