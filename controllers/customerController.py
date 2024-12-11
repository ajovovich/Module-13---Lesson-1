from flask import request, jsonify
from models.schemas.customerSchema import customer_schema, customers_schema
from services import customerService
from marshmallow import ValidationError
from caching import cache
from services.customerService import determine_customer_lifetime_value
from auth import token_required, role_required


@token_required
@role_required('admin')
def save():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    customer_save = customerService.save(customer_data)
    if customer_save is not None:
        return jsonify(customer_schema.dump(customer_save)), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":customer_data}), 400

def find_all():
    customers = customerService.find_all()
    return customers_schema.jsonify(customers), 200


def determine_customer_lifetime_value():
    threshold = request.args.get('threshold', 1000, type=int)
    customer_lifetime_value = customerService.determine_customer_lifetime_value(threshold)
    return jsonify(customer_lifetime_value), 200

