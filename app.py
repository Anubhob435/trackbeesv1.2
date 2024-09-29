from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database configuration
db = mysql.connector.connect(
    host="buh89x1pi8cgvaw4161i-mysql.services.clever-cloud.com",
    user="ucwyejivetooukiz",
    password="aAo8DieytbUo0FiYV4RY",
    database="buh89x1pi8cgvaw4161i"
)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user['password'], password):
        return jsonify({"success": True, "message": "Login successful"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    role = data.get('role', 'user')  # Default role is 'user'
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    email = data.get('email', '')
    phone_number = data.get('phone_number', '')

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        return jsonify({"success": False, "message": "Username already exists"}), 400
    else:
        hashed_password = generate_password_hash(password, method='sha256')
        cursor.execute("""
            INSERT INTO users (username, password, role, first_name, last_name, email, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (username, hashed_password, role, first_name, last_name, email, phone_number))
        db.commit()

        return jsonify({"success": True, "message": "User registered successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
