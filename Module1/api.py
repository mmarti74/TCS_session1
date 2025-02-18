from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

# In-memory task storage
tasks = {}

app.config["JWT_SECRET_KEY"] = "myprotectedkey"

jwt = JWTManager(app)

# Route to add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    task_id = request.json.get('id')
    task_description = request.json.get('description')

    if not task_id or not task_description:
        return jsonify({"error": "Task ID and description are required"}), 400

    tasks[task_id] = task_description
    return jsonify({"message": "Task added successfully"}), 201

# Route to list all tasks
@app.route('/tasks', methods=['GET'])
def list_tasks():
    return jsonify(tasks)

# Route to delete a specific task
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return jsonify({"message": "Task deleted successfully"})
    else:
        return jsonify({"error": "Task not found"}), 404

# Admin route
@app.route('/admin/delete_all_tasks', methods=['DELETE'])
@jwt_required()
def delete_all_tasks():
    tasks.clear()
    return jsonify({"message": "All tasks deleted successfully"}), 200

# Login
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    print(username)
    print(password)

    if username == "admin" and password == "admin123":
        token = create_access_token(identity=username)
        print(token)
        return jsonify(access_token=token)

    return jsonify({"error": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

