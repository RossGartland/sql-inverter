import unittest
import sqlparse
from insert_to_delete_processor import delete_processor, modify_comments, generate_delete

class TestInsertToDeleteProcessor(unittest.TestCase):

    def test_delete_processor_with_non_insert(self):
        sql_script = """
        SELECT * FROM users;
        """
        self.assertEqual(delete_processor(sql_script).strip(), sql_script.strip())

    def test_modify_comments(self):
        statement = """
        -- This insert statement should be modified
        /* Multi-line insert
           should also change */
        """
        expected_output = """
        -- This delete statement should be modified
        /* Multi-line delete
           should also change */
        """.strip()
        
        self.assertEqual(modify_comments(statement).strip(), expected_output)

if __name__ == "__main__":
    unittest.main()
