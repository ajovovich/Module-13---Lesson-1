import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, json, jsonify
from sqlalchemy.orm import Session
from app import db # replace your_app
from models.order import Order # replace your_app.models
from models.schemas.orderSchema import OrderSchema # replace your_app.schemas
from services import orderService # replace your_app.services
from controllers import orderController # replace your_app.controllers

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

class TestOrderEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Tuckerstriker12@localhost/factory_management_db'
        self.client = self.app.test_client()
        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @patch.object(orderService, 'save')
    def test_save_order_success(self, mock_save):

        mock_save.return_value = Order(id=1, customer_id=1, product_id=1, quantity=10, total_price=100.0)
        order_data = {'customer_id': 1, 'product_id': 1, 'quantity': 10, 'total_price': 100.0}
        response = self.client.post('/orders/', data=json.dumps(order_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], 1)

    @patch.object(orderService, 'save')
    def test_save_order_failure(self, mock_save):

        mock_save.side_effect = Exception("Database error")
        order_data = {'name': 'failure', 'customer_id': 1, 'product_id': 1, 'quantity': 10, 'total_price': 100.0}
        response = self.client.post('/orders/', data=json.dumps(order_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], "Fallback method error activated")

    @patch.object(orderService, 'find_all')
    def test_get_all_orders(self, mock_find_all):

        mock_find_all.return_value = [
            Order(id=1, customer_id=1, product_id=1, quantity=10, total_price=100.0),
            Order(id=2, customer_id=2, product_id=2, quantity=5, total_price=50.0)
        ]
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)


if __name__ == '__main__':
    unittest.main()
