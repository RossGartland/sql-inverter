import unittest
from unittest.mock import patch
from app import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test client before each test."""
        self.app = app.test_client()
        self.app.testing = True  

    def test_index_page(self):
        """Test if the home page loads successfully."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'SQL Converter', response.data)  

    @patch('app.delete_processor', return_value="DELETE MOCK OUTPUT")
    @patch('app.insert_processor', return_value="INSERT MOCK OUTPUT")
    def test_process_sql_delete_to_insert(self, mock_insert, mock_delete):
        """Test the process endpoint for delete_to_insert conversion."""
        response = self.app.post('/process', data={'sql_input': 'DELETE FROM table;', 'conversion_type': 'delete_to_insert'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'INSERT MOCK OUTPUT', response.data)
        mock_insert.assert_called_once_with('DELETE FROM table;')  

    @patch('app.delete_processor', return_value="DELETE MOCK OUTPUT")
    @patch('app.insert_processor', return_value="INSERT MOCK OUTPUT")
    def test_process_sql_insert_to_delete(self, mock_insert, mock_delete):
        """Test the process endpoint for insert_to_delete conversion."""
        response = self.app.post('/process', data={'sql_input': 'INSERT INTO table VALUES(1);', 'conversion_type': 'insert_to_delete'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'DELETE MOCK OUTPUT', response.data)
        mock_delete.assert_called_once_with('INSERT INTO table VALUES(1);')  

    def test_process_sql_no_input(self):
        """Test process endpoint with empty input."""
        response = self.app.post('/process', data={'sql_input': '', 'conversion_type': 'delete_to_insert'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'No SQL input provided', response.data)

    def test_process_sql_invalid_conversion_type(self):
        """Test process endpoint with an invalid conversion type."""
        response = self.app.post('/process', data={'sql_input': 'SELECT * FROM table;', 'conversion_type': 'invalid_type'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid conversion type selected', response.data)

if __name__ == '__main__':
    unittest.main()
