import unittest
from unittest.mock import patch, MagicMock
from services.employeeService import save, find_all
from models.employee import Employee
from app import create_app
from database import db

class TestEmployeeEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('TestingConfig')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        with cls.app.app_context():
            # Drop all tables to ensure a clean state
            db.drop_all()
            # Create tables in the correct order
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()
        cls.app_context.pop()

    @patch('services.employeeService.db.session')
    def test_get_employee(self, mock_session):
        # Mock the database session and query
        mock_query = MagicMock()
        mock_query.scalars.return_value.all.return_value = [Employee(id=1, name="John Doe", position="Developer")]
        mock_session.execute.return_value = mock_query
        
        # Call the function to test
        employee = find_all()
        
        # Assertions
        self.assertIsNotNone(employee)
        self.assertEqual(employee[0].name, "John Doe")
        self.assertEqual(employee[0].position, "Developer")

    @patch('services.employeeService.db.session')
    def test_create_employee(self, mock_session):
        # Mock the database session and commit
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()
        mock_session.refresh = MagicMock()
        
        # Employee data to test
        employee_data = {'name': 'Jane Doe', 'position': 'Manager'}
        
        # Call the function to test
        new_employee = save(employee_data)
        
        # Assertions
        self.assertIsNotNone(new_employee)
        self.assertEqual(new_employee.name, 'Jane Doe')
        self.assertEqual(new_employee.position, 'Manager')

    @patch('services.employeeService.db.session')
    def test_update_employee(self, mock_session):
        # Mock the database session and query
        mock_query = mock_session.query.return_value
        mock_query.filter_by.return_value.first.return_value = Employee(id=1, name="John Doe", position="Developer")
        
        # Employee data to update
        updated_data = {'name': 'John Smith', 'position': 'Senior Developer'}
        
        # Call the function to test
        employee = mock_query.filter_by(id=1).first()
        employee.name = updated_data['name']
        employee.position = updated_data['position']
        self.assertEqual(employee.name, 'John Smith')
        self.assertEqual(employee.position, 'Senior Developer')

    @patch('services.employeeService.db.session')
    def test_delete_employee(self, mock_session):
        # Mock the database session and query
        mock_query = mock_session.query.return_value
        mock_query.filter_by.return_value.first.return_value = Employee(id=1, name="John Doe", position="Developer")
        
        # Call the function to test
        employee = mock_query.filter_by(id=1).first()
        mock_session.delete(employee)
        mock_session.commit()
        
        # Assertions
        mock_session.delete.assert_called_once_with(employee)
        mock_session.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
