from flask import request, jsonify
from models.schemas.employeeSchema import employee_schema, employees_schema
from services import employeeService
from marshmallow import ValidationError
from caching import cache
from services.employeeService import analyze_employee_performance
from auth import token_required, role_required

@role_required('admin')
def save():
    try:
        employee_data = employee_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    employee_save = employeeService.save(employee_data)
    if employee_save is not None:
        return jsonify(employee_schema.dump(employee_save)), 201
    else:
        return jsonify({"message":"Fallback method error activated","body":employee_data}), 400
    
@cache.cached(timeout=60)
def find_all():
    employees = employeeService.find_all()
    return employees_schema.jsonify(employees), 200

#Task 1: Part 2

def get_employee_performance():
    performance_data = analyze_employee_performance()
    return jsonify(performance_data), 200
