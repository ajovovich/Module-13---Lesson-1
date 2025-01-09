import unittest
from unittest.mock import MagicMock, patch
from flask import json
from app import create_app, db  # Assuming 'app' is where your Flask app is defined
from models.product import Product
from services.productService import save as service_save # Import the service function directly
from controllers.productController import save, find_all, find_all_pagination, identify_top_selling_products

class TestProductService(unittest.TestCase):

    def setUp(self):
        self.app = create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()  
        db.create_all()  
        self.client = self.app.test_client()

        self.test_product = {
            "name": "Test Product",
            "price": 10.99
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.db.session')  # Patch the SQLAlchemy Session
    def test_save_product_success(self, mock_session):
        """Test successful product saving (service layer)."""
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        with self.app.app_context():
            new_product = service_save(self.test_product)

        mock_session_instance.add.assert_called_once() 
        mock_session_instance.commit.assert_called_once()
        self.assertEqual(new_product.name, "Test Product")
        self.assertEqual(new_product.price, 10.99)

    def test_save_product_controller(self):
        """Test product saving via API endpoint."""
        response = self.client.post('/products/', 
                                    data=json.dumps(self.test_product),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201) 
        self.assertEqual(response.json['name'], "Test Product")

    def test_get_all_products(self):
        test_product_2 = {
            "name": "Test Product 2",
            "price": 12.99
        }
        with self.app.app_context():
            db.session.add(Product(name=self.test_product['name'], price=self.test_product['price']))
            db.session.add(Product(name=test_product_2['name'], price=test_product_2['price']))
            db.session.commit()
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)  # Check if two products are returned

    def test_get_products_pagination(self):
        with self.app.app_context():
            for i in range(15):
                product = Product(name=f"Product {i}", price=10.00)
                db.session.add(product)
            db.session.commit()
        response = self.client.get('/products/pagination?page=2&per_page=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 5)

    def test_get_top_selling_products(self):
        response = self.client.get('/products/top-selling')
        self.assertEqual(response.status_code, 200) 

    @patch('app.db.session') 
    def test_save_product_failure(self, mock_session):
        """Test failure scenario with circuit breaker (service layer)."""
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        
        self.test_product['name'] = "failure" # Trigger the failure condition

        product = service_save(self.test_product)

        self.assertIsNone(product) # Check if the fallback function returns None

if __name__ == '__main__':
    unittest.main()