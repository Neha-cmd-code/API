import os
from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)

# Dummy authentication credentials
USERNAME = "admin"
PASSWORD = "password123"

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != USERNAME or auth.password != PASSWORD:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Sample drug data
drug_data = [
    {"DrugName": "Opioids", "Category": "Painkiller", "Deaths": 50000, "Year": 2023},
    {"DrugName": "Fentanyl", "Category": "Opioid", "Deaths": 70000, "Year": 2023},
]

@app.route('/drugs', methods=['GET'])
@require_auth
def get_all_drugs():
    return jsonify(drug_data)

# Get port from environment variable
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if not set
    app.run(host="0.0.0.0", port=port)
