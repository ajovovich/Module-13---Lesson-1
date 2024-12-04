from flask import request, jsonify
from models.schemas.productSchema import product_schema, products_schema
from services import productService
from marshmallow import ValidationError
from caching import cache
from services.productService import identify_top_selling_products


def save():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    product_save = productService.save(product_data)
    if product_save is not None:
        return jsonify(product_schema.dump(product_save)), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":product_data}), 400
    
@cache.cached(timeout=60)
def find_all():
    products = productService.find_all()
    return products_schema.jsonify(products), 200

#Task 2:

def find_all_pagination():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return products_schema.jsonify(productService.find_all_pagination(page, per_page)), 200

#Task 2: Part 2

def identify_top_selling_products():
    top_selling_products = productService.identify_top_selling_products()
    return jsonify(top_selling_products), 200