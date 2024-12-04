from flask import Blueprint
from controllers.productController import save, find_all, find_all_pagination, identify_top_selling_products


products_blueprint = Blueprint('product_bp', __name__)
products_blueprint.route('/', methods=['POST'])(save)
products_blueprint.route('/', methods=['GET'])(find_all)
products_blueprint.route('/pagination', methods=['GET'])(find_all_pagination)
products_blueprint.route('/top-selling', methods=['GET'])(identify_top_selling_products)
