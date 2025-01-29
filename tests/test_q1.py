import unittest
import tempfile
import json
from datetime import date
from src.q1_time import q1_time
from src.q1_memory import q1_memory


class TestQ1Functions(unittest.TestCase):

    def setUp(self):
        """This method will run before each test,
        setting up the temporary test environment.
        """
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

    def test_two_dates_with_distinct_activity(self):
        """Test with two dates where each has a distinct top user."""
        test_data = [
            {"date": "2025-01-01T00:00:00", "user": {"username": "user_1"}},
            {"date": "2025-01-01T00:00:01", "user": {"username": "user_1"}},
            {"date": "2025-01-02T00:00:00", "user": {"username": "user_2"}},
            {"date": "2025-01-02T00:10:00", "user": {"username": "user_2"}},
            {"date": "2025-01-02T00:00:02", "user": {"username": "user_3"}},
        ]
        file_path = self.create_test_file(test_data)

        result_time = q1_time(file_path)
        result_memory = q1_memory(file_path)

        expected = [
            (date(2025, 1, 2), "user_2"),
            (date(2025, 1, 1), "user_1")
        ]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_top_10_dates_with_same_activity(self):
        """Test with more than 10 dates, each having the same activity
        count, but different users.
        """
        test_data = []
        for i in range(1, 11):
            date_str = f"2025-01-{i:02d}T00:00:"
            test_data.extend([
                {"date": date_str+"00", "user": {"username": f"user_{i}"}},
                {"date": date_str+"01", "user": {"username": f"user_{i}"}},
                # Add a user that is not the top user
                {"date": date_str+"03", "user": {"username": "user_not_top"}},
            ])

        # Add an 11th date with one entry, which should not be in the result
        test_data.append({"date": "2025-01-11T00:00:00", "user": 
                          {"username": "user_11"}})

        file_path = self.create_test_file(test_data)

        result_time = q1_time(file_path)
        result_memory = q1_memory(file_path)

        expected = [(date(2025, 1, i), f"user_{i}") for i in range(1, 11)]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)


if __name__ == "__main__":
    unittest.main()
