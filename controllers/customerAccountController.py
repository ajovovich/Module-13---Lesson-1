from models.schemas.customerAccountSchema import customer_accounts_schema
from services import customerAccountService
from flask import jsonify, request

def find_all():
    customer_accounts = customerAccountService.find_all()
    return customer_accounts_schema.jsonify(customer_accounts),200

def login():
    customer = request.json
    user = customerAccountService.login_customer(customer['username'], customer['password'])
    if user:
        return jsonify(user), 200
    else:
        resp = {
            'status': 'fail',
            'message': 'Invalid credentials.'
        }
        return jsonify(resp), 404