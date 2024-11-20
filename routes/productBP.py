from flask import Blueprint
from controllers.productController import save, find_all


products_blueprint = Blueprint('product_bp', __name__)
products_blueprint.route('/', methods=['POST'])(save)
products_blueprint.route('/', methods=['GET'])(find_all)
