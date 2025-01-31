import unittest
import os
import tempfile
import json

from src.q2_time import q2_time
from src.q2_memory import q2_memory


class TestQ2Functions(unittest.TestCase):
    """Test suite for q2_time and q2_memory functions.
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

    def test_no_empty_quote_new_quote(self):
        """Test with no empty quoted content and new quoted content."""
        test_data = [
            {'content': 'aa a aa a😀aa a', 'id': 1,
                'quotedTweet': {'content': 'aa😋 aa', 'id': 2}
            },
            {'content': '😋', 'id': 3,
                'quotedTweet': {'content': '🛫', 'id': 4}
            }
        ]
        file_path = self.create_test_file(test_data)

        # Run both functions
        result_time = q2_time(file_path)
        result_memory = q2_memory(file_path)

        expected = [('😋', 2), ('😀', 1), ('🛫', 1)]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_no_empty_quote_repeated_quote(self):
        """Test with no empty quoted content and a repeated quoted content."""
        test_data = [
            {'content': 'aa a aa a😀aa a', 'id': 1,
                'quotedTweet': {'content': 'aa😋 aa', 'id': 2}
            },
            {'content': '😋', 'id': 3,
                'quotedTweet': {'content': 'aa a aa a😀aa a', 'id': 1}
            }
        ]
        file_path = self.create_test_file(test_data)

        # Run both functions
        result_time = q2_time(file_path)
        result_memory = q2_memory(file_path)

        expected = [('😋', 2), ('😀', 1)]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_empty_quote(self):
        """Test with empty quoted content."""

        test_data = [
            {'content': 'aa a aa a😀aa a', 'id': 1,
                'quotedTweet': None
            },
            {'content': '😋', 'id': 3,
                'quotedTweet': None
            }
        ]
        file_path = self.create_test_file(test_data)

        # Run both functions
        result_time = q2_time(file_path)
        result_memory = q2_memory(file_path)

        expected = [('😀', 1), ('😋', 1)]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_no_emojis(self):
        """Test with no emojis."""

        test_data = [
            {'content': 'aa a aa aaa a', 'id': 1,
                'quotedTweet': {'content': 'aa aa', 'id': 2}
            },
            {'content': 'aaaba aa', 'id': 3,
                'quotedTweet': {'content': 'aa aaa', 'id': 4}
            }
        ]
        file_path = self.create_test_file(test_data)

        # Run both functions
        result_time = q2_time(file_path)
        result_memory = q2_memory(file_path)

        expected = []

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_many_emojis(self):
        """Test with many emojis."""

        test_data = [
            {'content': '🥳🥳🥳🥳🥳🥳🥳🥳 ❤️❤️❤️❤️❤️❤️❤️ 😁😁😁😁😁😁', 'id': 1,
                'quotedTweet': {'content': '👀👀👀👀👀 🐶🐶🐶🐶', 'id': 2}
            },
            {'content': '🙁😀🙁😀🙁😀🙁😀🙁😀🙁😀🙁😀🙁😀🙁😀🙁', 'id': 3,
                'quotedTweet': {'content': '✈️✈️✈️ 😎😎 👍', 'id': 4}
            },
            {'content': '💻💻💻💻💻💻💻💻💻💻💻', 'id': 5}
        ]
        file_path = self.create_test_file(test_data)

        # Run both functions
        result_time = q2_time(file_path)
        result_memory = q2_memory(file_path)

        expected = [('💻', 11), ('🙁', 10), ('😀', 9), ('🥳', 8),
                    ('❤️', 7), ('😁', 6), ('👀', 5), ('🐶', 4),
                    ('✈️', 3), ('😎', 2)]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

if __name__ == "__main__":
    unittest.main()
