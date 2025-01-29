import unittest
import tempfile
import json
from datetime import date
from src.q1_time import q1_time
from src.q1_memory import q1_memory


class TestQ1Functions(unittest.TestCase):

    def setUp(self):
        """This method will run before each test, setting up the temporary test environment."""
        self.test_data = []

    def create_test_file(self, test_data):
        """Helper method to create a temporary JSON file for each test."""
        with tempfile.NamedTemporaryFile(delete=False, mode='w',
                                         newline='',
                                         encoding='utf-8') as f:
            for entry in test_data:
                f.write(json.dumps(entry) + '\n')
            return f.name  # Return the file path

    def test_single_date_single_user(self):
        """Test with one date and one user."""
        test_data = [
            {"date": "2025-01-01T00:00:00", "user": {"username": "user_1"}},
            {"date": "2025-01-01T00:00:01", "user": {"username": "user_1"}},
            {"date": "2025-01-01T00:20:02", "user": {"username": "user_1"}},
        ]
        file_path = self.create_test_file(test_data)

        # Run both functions
        result_time = q1_time(file_path)
        result_memory = q1_memory(file_path)

        expected = [(date(2025, 1, 1), "user_1")]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)



if __name__ == "__main__":
    unittest.main()
