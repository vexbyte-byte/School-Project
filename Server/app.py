from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Temporary memory storage for accounts (resets when server restarts)
fake_database = {}

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required!"}), 400
        
    if email in fake_database:
        return jsonify({"success": False, "message": "Account already exists!"}), 400
        
    # In a real app, you would hash the password here!
    fake_database[email] = password
    print(f"New user registered: {email}")
    
    return jsonify({"success": True, "message": "Signup successful!"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if fake_database.get(email) == password:
        return jsonify({"success": True, "message": "Login successful!"})
    
    return jsonify({"success": False, "message": "Invalid email or password!"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)