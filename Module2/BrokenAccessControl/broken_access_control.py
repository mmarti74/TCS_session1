from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy user database
users = {
    "user1": {"role": "user", "data": "User 1's data"},
    "user2": {"role": "user", "data": "User 2's data"},
    "admin": {"role": "admin", "data": "Admin's data"}
}

# Authentication
@app.route('/dashboard', methods=['GET'])
def user_dashboard():
    username = request.args.get('username')

    if username not in users:
        return jsonify({"error": "User not found"}), 404

    user_data = users[username]["data"]
    return jsonify({"message": f"Welcome {username}, here is your data: {user_data}"}), 200

# Admin dashboard
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    
    username = request.args.get('username')
    if username not in users:
        return jsonify({"error": "Not authorized!"}), 401
    
    user_role = users[username]["role"]
    if (user_role != "admin"):
        return jsonify({"error": "Not authorized!"}), 401
    
    return jsonify({"message": "Welcome to the Admin Dashboard", "users": users}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
