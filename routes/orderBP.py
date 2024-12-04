from flask import Blueprint
from controllers.orderController import save, find_all, find_all_pagination


orders_blueprint = Blueprint('order_bp', __name__)
orders_blueprint.route('/', methods=['POST'])(save)
orders_blueprint.route('/', methods=['GET'])(find_all)
orders_blueprint.route('/pagination', methods=['GET'])(find_all_pagination)