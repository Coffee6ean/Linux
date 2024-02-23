from flask import Flask, request, jsonify
from middleware import auth  # Import middleware functions
import jwt
from datetime import datetime, timedelta

from app.Keys.secrets import APP_KEY

# Create a Flask app
app = Flask(__name__)

# Register middleware functions
app.before_request(auth.authenticate_request)

# Function to generate a token with user information
def generate_token(user_id, username, role):
    # Define payload with user information
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expiration time
    }
    # Generate and return the token
    token = jwt.encode(payload, APP_KEY, algorithm='HS256')
    return token

# Middleware function to authenticate requests
def authenticate_request():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        payload = jwt.decode(token, APP_KEY, algorithms=['HS256'])
        # Here you can perform additional checks or extract information from the payload
        # For example, if you need to verify user roles, you can access 'payload['role']'
        return jsonify({'message': 'Valid token', 'user_role': payload.get('role')}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Expired token'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
