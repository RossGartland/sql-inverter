import unittest
from unittest.mock import patch
import sqlparse
from delete_to_insert_processor import insert_processor, modify_comments_for_inserts, generate_insert

class TestDeleteToInsertProcessor(unittest.TestCase):
    
    def test_invalid_delete_statement(self):
        """Test handling of an invalid DELETE statement."""
        sql = "DELETE WHERE id = 2;"  # No FROM clause
        result = insert_processor(sql)
        self.assertIn("-- Error generating INSERT", result)

    def test_generate_insert_missing_table(self):
        """Test DELETE statement missing table name."""
        sql = "DELETE WHERE id = 3;"
        parsed = sqlparse.parse(sql)[0]
        with self.assertRaises(ValueError):
            generate_insert(parsed)

    def test_generate_insert_missing_where(self):
        """Test DELETE statement missing WHERE clause."""
        sql = "DELETE FROM employees;"
        parsed = sqlparse.parse(sql)[0]
        with self.assertRaises(ValueError):
            generate_insert(parsed)

if __name__ == '__main__':
    unittest.main()