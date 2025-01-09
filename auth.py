from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv
from functools import wraps
from flask import request, jsonify

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(' ')[1]
                print("Token:", token)
                payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired', 'error': 'Unauthorized'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token', 'error': 'Unauthorized'}), 401
        if not token:
            return jsonify({'message': 'Token is missing', 'error': 'Unauthorized'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(' ')[1]
            if not token:
                return jsonify({"message": "Token is missing"}), 401
            
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
                if role not in payload['roles']:
                    return jsonify({"message": "You do not have access to this resource"}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired', 'error': 'Unauthorized'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token', 'error': 'Unauthorized'}), 401
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator