# Module 1

## Introduction
In this first exercise we will go more in depth on the concept of attack surface in order to understand what it refers to and how it can be reduced.

In the api.py file is a simple API for a task management application. The API allows users to create, update, delete, and list tasks. During development, an additional admin functionality is accidentally left exposed in the API, allowing users to perform unauthorized actions.

## Testing the application 

```python task_api_secure.py```

The app should be running locally on port 5000

### Adding a task : 

```curl -X POST -H "Content-Type: application/json" -d '{"id": "1", "description": "Complete project report"}' http://127.0.0.1:5000/tasks```

### List all tasks :

```curl http://127.0.0.1:5000/tasks```

### Delete a specific task : 

```curl -X DELETE http://127.0.0.1:5000/tasks/1```

### Delete all tasks :

```curl -X DELETE http://127.0.0.1:5000/admin/delete_all_tasks```

<details>
<summary><h3>Read through the code and test it, can you identify some vulnerabilities ?</h3></summary>

- The /admin/delete_all_tasks route allows anyone who discovers it to delete all tasks, potentially disrupting the system and increasing the attack surface.
- There are no authentication or authorization mechanisms in place to restrict access to sensitive endpoints.
- Running the app in debug mode further increases the attack surface by exposing detailed error messages.
</details>

Implement a solution to reduce the attack surface and fix those vulnerabilities.
<details>
<summary><h3> Hint n°1 : </h3></summary>

You should add authentication and role-based access control to the delete_all_users endpoint.

</details>
<details>
<summary><h3> Hint n°2 : </h3></summary>

Try adding a condition with a bearer token for the authorization

</details>

<details>
<summary><h2>Solution : </h2></summary>

```py

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory task storage
tasks = {}

# Dummy authentication token for simplicity (in production, use a secure method)
ADMIN_TOKEN = "secure_admin_token"

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

# Secure admin route to delete all tasks
@app.route('/admin/delete_all_tasks', methods=['DELETE'])
def delete_all_tasks():
    # Require admin authentication
    auth_token = request.headers.get('Authorization')

    if auth_token != f"Bearer {ADMIN_TOKEN}":
        return jsonify({"error": "Unauthorized access"}), 403

    tasks.clear()
    return jsonify({"message": "All tasks deleted successfully"}), 200

if __name__ == '__main__':
    app.run()
```
</details>

In order to test whether the vulnerability has been fixed, you can try testing to delete all users without using any kind of authorization and you should get an error.
This test, however, should work :
```curl -X DELETE -H "Authorization: Bearer secure_admin_token" http://127.0.0.1:5000/admin/delete_all_tasks```

<details>
<summary>To go further, we can reflect what other improvements could be made</summary>

- Implement rate limiting to prevent brute-force attacks on the admin token.
- Use a secure, scalable authentication mechanism like OAuth 2.0 or JWT.
- Log admin access attempts to monitor potential abuse.
</details>