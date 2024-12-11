from flask import Flask
from database import db
from schema import ma
from limiter import limiter
from caching import cache
from models import db, customer, role, customerManagementRole
from sqlalchemy.orm import Session

from models.employee import Employee
from models.product import Product
from models.order import Order
from models.customer import Customer
from models.production import Production
from models.customerAccount import CustomerAccount
from routes.customerBP import customers_blueprint
from routes.employeeBP import employees_blueprint
from routes.orderBP import orders_blueprint
from routes.productBP import products_blueprint
from routes.productionBP import productions_blueprint
from routes.customerAccountBP import customer_account_blueprint

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
    app.register_blueprint(customer_account_blueprint, url_prefix='/accounts')


def configure_rate_limter():
    limiter.limit("5 per day")(employees_blueprint)
    limiter.limit("5 per day")(products_blueprint)
    limiter.limit("5 per day")(customers_blueprint)
    limiter.limit("5 per day")(orders_blueprint)
    limiter.limit("5 per day")(productions_blueprint)

def init_customer_info_data():
    with Session(db.engine) as session:
        with session.begin():
            customers = [
                Customer(name = "Customer One", email="customer1@example.com", phone="1234567890"),
                Customer(name = "Customer Two", email="customer2@example.com", phone="1234567892"),
                Customer(name = "Customer Three", email="customer3@example.com", phone="1234567891"),            
            ]
            session.add_all(customers)
            session.add_all(customerAccounts)

def init_roles_data():
    with Session(db.engine) as session:
        with session.begin():
            roles = [
                role(role_name="admin"),
                role(role_name="user"),
                role(role_name="guest"),
            ]
            session.add_all(roles)

def init_roles_customers_data():
    with Session(db.engine) as session:
        with session.begin():
            roles_customers = [
                customerManagementRole(customer_management_id=1, role_id=1),
                customerManagementRole(customer_management_id=2, role_id=2),
                customerManagementRole(customer_management_id=3, role_id=3),
            ]
            session.add_all(roles_customers)
    

if __name__ == '__main__':
    app = create_app('DevelopmentConfig')

    blue_print_config(app)
    configure_rate_limter()

    with app.app_context():
        db.drop_all()
        db.create_all()
        init_roles_data()
        init_customer_info_data()
        init_roles_customers_data()

    app.run(debug=True)
