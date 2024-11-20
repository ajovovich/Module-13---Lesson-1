from flask import Flask
from database import db
from schema import ma
from limiter import limiter
from caching import cache

from models.employee import Employee
from models.product import Product
from models.order import Order
from models.customer import Customer
from models.production import Production
from routes.customerBP import customers_blueprint
from routes.employeeBP import employees_blueprint
from routes.orderBP import orders_blueprint
from routes.productBP import products_blueprint
from routes.productionBP import productions_blueprint

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    return app

def blue_print_config(app):
    app.register_blueprint(employees_blueprint, url_prefix='/employees')
    app.register_blueprint(products_blueprint, url_prefix='/products')
    app.register_blueprint(customers_blueprint, url_prefix='/customers')
    app.register_blueprint(orders_blueprint, url_prefix='/orders')
    app.register_blueprint(productions_blueprint, url_prefix='/productions')


def configure_rate_limter():
    limiter.limit("5 per day")(employees_blueprint)
    limiter.limit("5 per day")(products_blueprint)
    limiter.limit("5 per day")(customers_blueprint)
    limiter.limit("5 per day")(orders_blueprint)
    limiter.limit("5 per day")(productions_blueprint)
    

if __name__ == '__main__':
    app = create_app('DevelopmentConfig')

    blue_print_config(app)
    configure_rate_limter()

    with app.app_context():
        db.drop_all()
        db.create_all()

    app.run(debug=True)
