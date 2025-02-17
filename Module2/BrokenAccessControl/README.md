# Module 2.1
This exercise will expand on a notion we brushed on in the previous exercise. We talked about how the security of the api could be improved using role-based access control, if this access control is poorly designed, unauthorized access is possible.

The file in this exercise is an API for user management. The API includes:

- A user dashboard where users can view their data.
- An admin dashboard where admins can view and manage all users.

The application does not properly enforce access control, allowing any user to access the admin dashboard. 

## Starting and testing the application :

```python broken_access_control.py```

Access the User Dashboard:

Use the following URL to access the dashboard as a regular user: http://127.0.0.1:5000/dashboard?username=user1

Access the Admin Dashboard :
http://127.0.0.1:5000/admin

Even non-admin users can access the admin dashboard, revealing sensitive data.

Implement a fix so that only admin users can access the admin dashboard.

<details>
<summarty><h2>Hint n°1:</h2></summary>

Try adding a condition to the admin dashboard route to limit access to only admin users

</details>

<details>
<summarty><h2>Hint n°2:</h2></summary>

Try using the role of the user as the condition

</details>

<details>
<summary><h2>Solution : </h2></summary>

```py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy user database
users = {
    "user1": {"role": "user", "data": "User 1's data"},
    "user2": {"role": "user", "data": "User 2's data"},
    "admin": {"role": "admin", "data": "Admin's data"}
}

# Insecure authentication (using query parameter for simplicity)
@app.route('/dashboard', methods=['GET'])
def user_dashboard():
    username = request.args.get('username')

    if username not in users:
        return jsonify({"error": "User not found"}), 404

    user_data = users[username]["data"]
    return jsonify({"message": f"Welcome {username}, here is your data: {user_data}"}), 200

# Admin dashboard with access control
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    username = request.args.get('username')

    if username not in users:
        return jsonify({"error": "User not found"}), 404

    # Check if the user has an admin role
    if users[username]["role"] != "admin":
        return jsonify({"error": "Access denied"}), 403

    return jsonify({"message": "Welcome to the Admin Dashboard", "users": users}), 200

if __name__ == '__main__':
    app.run()
```
</details>

Test your code :

http://127.0.0.1:5000/admin?username=admin

<details>
<summary>To go further, what other improvements could we make ?</summary>

- Use a proper authentication mechanism like JWT tokens.
        
- Avoid passing sensitive information like usernames in query parameters.
        
- Implement logging for unauthorized access attempts.

- Log unauthorized access attempts and set up alerts for repeated failures.
</details>

