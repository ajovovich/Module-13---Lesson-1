from flask import Blueprint
from controllers.customerAccountController import find_all, login

customer_account_blueprint = Blueprint('customer_account_bp', __name__)
customer_account_blueprint.route('/', methods=['GET'])(find_all)
customer_account_blueprint.route('/login', methods=['POST'])(login)