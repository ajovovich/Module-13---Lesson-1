from flask import Blueprint
from controllers.employeeController import save, find_all, get_employee_performance


employees_blueprint = Blueprint('employee_bp', __name__)
employees_blueprint.route('/', methods=['POST'])(save)
employees_blueprint.route('/', methods=['GET'])(find_all)
employees_blueprint.route('/performance', methods=['GET'])(get_employee_performance)                                                    
