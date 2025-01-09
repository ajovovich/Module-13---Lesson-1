import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
import unittest.mock as mock
from datetime import date

from services.productionService import save, find_all, evaluate_production_efficiency
from models.production import Production, db
from models.product import Product

class TestProductionEndpoints(unittest.TestCase):

    def setUp(self):
        """Setup before each test."""
        self.db_session_mock = MagicMock(spec=Session)
        db.session = self.db_session_mock  

    def tearDown(self):
        """Cleanup after each test."""
        self.db_session_mock.reset_mock()

    def test_save_production_success(self):
        production_data = {'product_id': 1, 'quantity_produced': 100, 'date_produced': date(2024, 1, 9)}

        # Mock the database response
        self.db_session_mock.add.return_value = None
        self.db_session_mock.commit.return_value = None
        self.db_session_mock.refresh.return_value = None

        # Call the function
        result = save(production_data)

        self.assertEqual(result.product_id, 1)
        self.assertEqual(result.quantity_produced, 100)
        self.assertEqual(result.date_produced, date(2024, 1, 9))

    def test_save_production_failure(self):
        production_data = {'name': 'failure', 'product_id': 1, 'quantity_produced': 100, 'date_produced': date(2024, 1, 9)}
        with self.assertRaises(Exception) as context:
            save(production_data)

        self.assertEqual(str(context.exception), 'Failure condition triggered')

    @mock.patch('productionService.db.session.execute')
    def test_find_all_productions(self, mock_execute):
        # Mock Data
        mock_production1 = Production(product_id=1, quantity_produced=50, date_produced=date(2024, 1, 8))
        mock_production2 = Production(product_id=2, quantity_produced=150, date_produced=date(2024, 1, 9))

        # Configure the mock to return the mock data
        mock_execute.return_value.scalars.return_value.all.return_value = [mock_production1, mock_production2]

        # Call the function
        productions = find_all()

        self.assertEqual(len(productions), 2)
        self.assertEqual(productions[0].product_id, 1)
        self.assertEqual(productions[1].quantity_produced, 150)

    @mock.patch('productionService.db.session.query')
    def test_evaluate_production_efficiency(self, mock_query):
        # Mock Data
        mock_results = [('Product A', 150), ('Product B', 250)]
        specific_date = date(2024, 1, 9) 

        # Configure the mock query to return the desired data
        mock_query.return_value.join.return_value.filter.return_value.group_by.return_value.all.return_value = mock_results

        # Call the function
        result = evaluate_production_efficiency(specific_date)

        # Assertions
        self.assertEqual(result, mock_results)

if __name__ == '__main__':
    unittest.main()
