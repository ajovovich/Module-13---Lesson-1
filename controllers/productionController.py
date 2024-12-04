from flask import request, jsonify
from models.schemas.productionSchema import production_schema, productions_schema
from services import productionService
from marshmallow import ValidationError
from caching import cache
from services.productionService import evaluate_production_efficiency


def save():
    try:
        production_data = production_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    production_save = productionService.save(production_data)
    if production_save is not None:
        return jsonify(production_schema.dump(production_save)), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":production_data}), 400
    
@cache.cached(timeout=60)
def find_all():
    productions = productionService.find_all()
    return productions_schema.jsonify(productions), 200

#Task 2: Part 4

def evaluate_production_efficiency():
    efficiency_data = productionService.evaluate_production_efficiency()
    return jsonify(efficiency_data), 200
