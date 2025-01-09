from flask import Flask, request, jsonify
from utils.util import encode_token
from models.user import User


def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if user and user.check_password(data['password']):
        token = encode_token(user.id)
        return jsonify({'token': token, 'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401