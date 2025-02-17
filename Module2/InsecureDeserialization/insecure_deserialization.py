import pickle
import base64
from flask import Flask, request, make_response

app = Flask(__name__)

# Simulated user database
users = {"admin": "supersecret", "user": "password"}

# Session handling with pickle
@app.route("/set_session", methods=["POST"])
def set_session():
    username = request.form.get("username")
    if username not in users:
        return "User not found", 403

    # Serialize user session using pickle
    session_data = pickle.dumps({"username": username})
    encoded_data = base64.b64encode(session_data).decode()

    response = make_response("Session set!")
    response.set_cookie("session", encoded_data)  # 🔥 Insecure: User controls serialized data!
    return response

@app.route('/get_session', methods=['GET'])
def get_session():
    session_cookie = request.cookies.get('session')  # Get the cookie
    if session_cookie:
        try:
            # Deserialize the session cookie
            decoded_cookie = base64.b64decode(session_cookie)
            session_data = pickle.loads(decoded_cookie)  # Deserialize the data

            # Access the username safely
            if isinstance(session_data, dict) and 'username' in session_data:
                return f"Hello, {session_data['username']}!"
            else:
                return "Invalid session data", 400
        except Exception as e:
            return f"Error: {str(e)}", 500
    else:
        return "No session data", 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
