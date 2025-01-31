import unittest
import os
import tempfile
import json

from src.q3_time import q3_time
from src.q3_memory import q3_memory


class TestQ3Functions(unittest.TestCase):
    """Test suite for q3_time and q3_memory functions.
    """

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
            self.test_data.append(f.name)
            return f.name  # Return the file path

    def tearDown(self):
        """This method will run after each test,
        cleaning up the temporary test environment."""
        for file in self.test_data:
            os.remove(file)

    def test_mentions_all_contents(self):
        """Test with mentions in all contents."""
        test_data = [
            {
                "content": "@user1 @user2",
                "id": 1,
                "user": {"username": "user1"},
                "quotedTweet": {
                    "content": "Hi a@user2",
                    "id": 2
                }
            },
            {
                "content": "@user1",
                "id": 3,
                "user": {"username": "user2"},
                "quotedTweet":  {
                    "content": "a@user2",
                    "id": 4
                }
            }
        ]
        file_path = self.create_test_file(test_data)

        # Run both functions
        result_time = q3_time(file_path)
        result_memory = q3_memory(file_path)

        expected = [('user2', 3), ('user1', 2)]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_repeated_quoted_content(self):
        """Test with repeated quoted content."""
        test_data = [
            {
                "content": "@user1 @user2",
                "id": 1,
                "user": {"username": "user1"},
                "quotedTweet": {
                    "content": "Hi a@user1",
                    "id": 2
                }
            },
            {
                "content": "@user1",
                "id": 3,
                "user": {"username": "user2"},
                "quotedTweet":  {
                    "content": "@user1 @user2",
                    "id": 1
                }
            }
        ]
        file_path = self.create_test_file(test_data)

        # Run both functions
        result_time = q3_time(file_path)
        result_memory = q3_memory(file_path)

        expected = [('user1', 3), ('user2', 1)]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_no_quoted_content(self):
        """Test with no quoted content."""
        test_data = [
            {
                "content": "@user1 @user2",
                "id": 1,
                "user": {"username": "user1"},
                "quotedTweet": None
            },
            {
                "content": "@user1",
                "id": 2,
                "user": {"username": "user2"},
                "quotedTweet":  None
            }
        ]
        file_path = self.create_test_file(test_data)

        # Run both functions
        result_time = q3_time(file_path)
        result_memory = q3_memory(file_path)

        expected = [('user1', 2), ('user2', 1)]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_mention_not_username(self):
        """Test with mention that is not a username."""
        test_data = [
            {
                "content": "@user1 @user2",
                "id": 1,
                "user": {"username": "user1"},
                "quotedTweet": None
            },
            {
                "content": "@user3",
                "id": 2,
                "user": {"username": "user2"},
                "quotedTweet":  None
            }
        ]
        file_path = self.create_test_file(test_data)

        # Run both functions
        result_time = q3_time(file_path)
        result_memory = q3_memory(file_path)

        expected = [('user1', 1), ('user2', 1)]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_no_mention(self):
        """Test with no mention."""

        test_data = [
            {
                "content": "aaa aa aaa",
                "id": 1,
                "user": {"username": "user1"},
                "quotedTweet": {
                    "content": "aaaaa aaaa",
                    "id": 2
                }
            },
            {
                "content": "aaaa aaaa",
                "id": 3,
                "user": {"username": "user2"},
                "quotedTweet":  {
                    "content": "a",
                    "id": 4
                }
            }
        ]
        file_path = self.create_test_file(test_data)

        # Run both functions
        result_time = q3_time(file_path)
        result_memory = q3_memory(file_path)

        expected = []

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)


if __name__ == "__main__":
    unittest.main()
