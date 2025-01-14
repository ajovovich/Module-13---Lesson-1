from flask import Blueprint
from controllers.productionController import save, find_all, evaluate_production_efficiency


productions_blueprint = Blueprint('production_bp', __name__)
productions_blueprint.route('/', methods=['POST'])(save)
productions_blueprint.route('/', methods=['GET'])(find_all)
productions_blueprint.route('/efficiency', methods=['GET'])(evaluate_production_efficiency)