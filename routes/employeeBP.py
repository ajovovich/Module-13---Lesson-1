from flask import Blueprint
from controllers.employeeController import save, find_all


employees_blueprint = Blueprint('employee_bp', __name__)
employees_blueprint.route('/', methods=['POST'])(save)
employees_blueprint.route('/', methods=['GET'])(find_all)
