from flask import Blueprint
from controllers.productionController import save, find_all


productions_blueprint = Blueprint('production_bp', __name__)
productions_blueprint.route('/', methods=['POST'])(save)
productions_blueprint.route('/', methods=['GET'])(find_all)
