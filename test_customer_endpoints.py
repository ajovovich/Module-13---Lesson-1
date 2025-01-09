import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
import unittest.mock as mock

from services.customerService import save, find_all, determine_customer_lifetime_value
from models.customer import Customer, db 
from models.order import Order

class TestCustomerEndpoints(unittest.TestCase):

    def setUp(self):
        """Setup before each test."""
        self.db_session_mock = MagicMock(spec=Session)
        db.session = self.db_session_mock 

    def tearDown(self):
        """Cleanup after each test."""
        self.db_session_mock.reset_mock()

    def test_save_customer_success(self):
        customer_data = {'name': 'Test User', 'phone': '1234567890', 'email': 'test@example.com'}
        
        # Mock the database response
        self.db_session_mock.add.return_value = None 
        self.db_session_mock.commit.return_value = None
        self.db_session_mock.refresh.return_value = None

        # Call the function
        result = save(customer_data)

        # Assertions
        self.assertEqual(result.name, 'Test User')
        self.assertEqual(result.phone, '1234567890')
        self.assertEqual(result.email, 'test@example.com')

    def test_save_customer_failure(self):
        customer_data = {'namer': 'failure', 'phone': '1234567890', 'email': 'test@example.com'}
        with self.assertRaises(Exception) as context:
            save(customer_data)

        self.assertEqual(str(context.exception), 'Failure condition triggered')

    @mock.patch('customerService.db.session.execute')
    def test_find_all_customers(self, mock_execute):
        # Mock Data
        mock_customer1 = Customer(name='Customer 1', phone='1111111111', email='customer1@example.com')
        mock_customer2 = Customer(name='Customer 2', phone='2222222222', email='customer2@example.com')
    
        # Configure the mock to return the mock data
        mock_execute.return_value.scalars.return_value.all.return_value = [mock_customer1, mock_customer2]
    
        # Call the function
        customers = find_all()
    
        # Assertions
        self.assertEqual(len(customers), 2) 
        self.assertEqual(customers[0].name, 'Customer 1')
        self.assertEqual(customers[1].name, 'Customer 2')

    @mock.patch('customerService.db.session.query')
    def test_determine_customer_lifetime_value(self, mock_query):
        # Mock Data
        mock_results = [('Valuable Customer', 1500.00), ('Another Good Customer', 1200.00)] 

        # Configure the mock query to return the desired data
        mock_query.return_value.join.return_value.group_by.return_value.having.return_value.all.return_value = mock_results

        # Call the function
        result = determine_customer_lifetime_value()

        # Assertions
        self.assertEqual(result, mock_results)

if __name__ == '__main__':
    unittest.main()