from flask import Flask, request, jsonify

app = Flask(__name__)

# --- In-Memory Storage (No Database) ---
# This dictionary stores users while the script is running.
# If you stop the script, new users are lost.
users_db = {
    "admin": "1234",  # Default user
    "alara": "password"
}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "active", 
        "message": "Flask API is running without a database."
    }), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if user exists and password matches
    if username in users_db and users_db[username] == password:
        return jsonify({"success": True, "message": "Login successful!"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password required"}), 400

    if username in users_db:
        return jsonify({"success": False, "message": "User already exists"}), 409

    # Add new user to memory
    users_db[username] = password
    return jsonify({"success": True, "message": "User created successfully"}), 201

if __name__ == '__main__':
    print("Starting Flask Server on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
    