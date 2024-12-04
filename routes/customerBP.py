from flask import Blueprint
from controllers.customerController import save, find_all, determine_customer_lifetime_value


customers_blueprint = Blueprint('customer_bp', __name__)
customers_blueprint.route('/', methods=['POST'])(save)
customers_blueprint.route('/', methods=['GET'])(find_all)
customers_blueprint.route('/lifetime-value', methods=['GET'])(determine_customer_lifetime_value)
