from flask import Blueprint
from controllers.customerController import save, find_all


customers_blueprint = Blueprint('customer_bp', __name__)
customers_blueprint.route('/', methods=['POST'])(save)
customers_blueprint.route('/', methods=['GET'])(find_all)
