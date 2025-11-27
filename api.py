from flask import Flask, request, jsonify
from database import Database
from auth import AuthManager
from analytics import calculate_risk

app = Flask(__name__)
db = Database("wellbeing.db")
auth_system = AuthManager(db)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    success, message, role = auth_system.login(data.get('username'), data.get('password'))
    return jsonify({"success": success, "message": message, "role": role})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    success, message = auth_system.register(data.get('username'), data.get('password'), role=data.get('role', 'staff'))
    return jsonify({"success": success, "message": message})

@app.route('/generate_data', methods=['POST'])
def generate_data():
    db.generate_synthetic_data()
    return jsonify({"success": True, "message": "Synthetic Data Created"})

@app.route('/dashboard', methods=['GET'])
def get_dashboard():
    students = db.get_student_averages()
    results = []
    for s in students:
        risk = calculate_risk(s['avg_stress'], s['avg_sleep'])
        results.append({
            "name": s['name'],
            "id": s['id'],
            "avg_stress": round(s['avg_stress'], 2),
            "status": risk['status'],
            "reason": risk['reason']
        })
    return jsonify(results)

@app.route('/student/<int:student_id>', methods=['GET'])
def get_student_details(student_id):
    history = db.get_student_history(student_id)
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True, port=5000)