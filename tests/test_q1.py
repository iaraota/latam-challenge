import unittest
import os
import tempfile
import json
from datetime import date
from src.q1_time import q1_time
from src.q1_memory import q1_memory


class TestQ1Functions(unittest.TestCase):
    """Test suite for q1_time and q1_memory functions.
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

    def test_single_date_single_user_no_quote(self):
        """Test with one date, one user and no quoted tweet."""
        test_data = [
            {
                'date': '2025-01-01T00:00:00',
                'id': 1,
                'user': {'username': 'user_1'},
                'quotedTweet': None},
            {
                'date': '2025-01-01T00:00:01',
                'id': 2,
                'user': {'username': 'user_1'},
                'quotedTweet': None},
            {
                'date': '2025-01-01T00:20:02',
                'id': 3,
                'user': {'username': 'user_1'},
                'quotedTweet': None},
        ]
        file_path = self.create_test_file(test_data)

        # Run both functions
        result_time = q1_time(file_path)
        result_memory = q1_memory(file_path)

        expected = [(date(2025, 1, 1), 'user_1')]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_two_dates_with_distinct_activity_no_quote(self):
        """Test with two dates where each has a distinct top user and no quoted tweet."""
        test_data = [
            {
                'date': '2025-01-01T00:00:00',
                'id': 1,
                'user': {'username': 'user_1'},
                'quotedTweet': None},
            {
                'date': '2025-01-01T00:00:01',
                'id': 2,
                'user': {'username': 'user_1'},
                'quotedTweet': None},
            {
                'date': '2025-01-02T00:00:00',
                'id': 3,
                'user': {'username': 'user_2'},
                'quotedTweet': None},
            {
                'date': '2025-01-02T00:10:00',
                'id': 4,
                'user': {'username': 'user_2'},
                'quotedTweet': None},
            {
                'date': '2025-01-02T00:00:02',
                'id': 5,
                'user': {'username': 'user_3'},
                'quotedTweet': None},
        ]
        file_path = self.create_test_file(test_data)

        result_time = q1_time(file_path)
        result_memory = q1_memory(file_path)

        expected = [
            (date(2025, 1, 2), 'user_2'),
            (date(2025, 1, 1), 'user_1')
        ]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_top_10_dates_with_same_activity_no_quote(self):
        """Test with more than 10 dates, each having the same activity
        count, but different users. No quoted tweets.
        """
        test_data = []
        id_counter_1 = 1
        id_counter_2 = 11
        id_counter_3 = 111
        for i in range(1, 11):
            # set up the date string, changes day for each step
            # in the loop, don't include seconds
            # the seconds will be different for each activity
            # this ensure we test different times for the same date
            date_str = f'2025-01-{i:02d}T00:00:'
            test_data.extend([
                {
                    'date': date_str+'00',
                    'id': id_counter_1,
                    'user': {'username': f'user_{i}'},
                    'quotedTweet': None},
                {
                    'date': date_str+'01',
                    'id': id_counter_2,
                    'user': {'username': f'user_{i}'},
                    'quotedTweet': None},
                # Add a user that is not the top user
                {
                    'date': date_str+'03',
                    'id': id_counter_3,
                    'user': {'username': 'user_not_top'},
                    'quotedTweet': None},
            ])
            id_counter_1 += 1
            id_counter_2 += 1
            id_counter_3 += 1

        # Add an 11th date with one entry, which should not be in the result
        test_data.append({
            'date': '2025-01-11T00:00:00',
            'id': 999999,
            'user': {'username': 'user_11'},
            'quotedTweet': None,
            })

        file_path = self.create_test_file(test_data)

        result_time = q1_time(file_path)
        result_memory = q1_memory(file_path)

        expected = [(date(2025, 1, i), f"user_{i}") for i in range(1, 11)]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_top_10_dates_with_encrease_activity(self):
        """Test with more than 10 dates, each having an increasing activity
        count, but different users.
        """
        test_data = []
        id_counter = 1
        for i in range(1, 21):
            # set up the date string, changes day for each step
            # in the loop, don't include seconds
            # the seconds will be different for each activity
            # this ensure we test different times for the same date
            date_str = f'2025-01-{i:02d}T00:00:'
            for j in range(i):
                test_data.append({
                    'date': date_str+f'{j:02d}',
                    'id': id_counter,
                    'user': {'username': f'user_{i}'},
                    'quotedTweet': None})
                id_counter += 1
        file_path = self.create_test_file(test_data)

        # Run both functions
        result_time = q1_time(file_path)
        result_memory = q1_memory(file_path)

        expected = [(date(2025, 1, i), f'user_{i}') for i in range(20, 10, -1)]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_two_dates_with_distinct_activity_quote_repead(self):
        """Test with two dates where each has a distinct top user with
        quoted tweet that already exists."""
        test_data = [
            {
                'date': '2025-01-01T00:00:00',
                'id': 1,
                'user': {'username': 'user_1'},
                'quotedTweet': {
                    'date': '2025-01-01T00:00:01',
                    'id': 2,
                    'user': {'username': 'user_1'},
                    'quotedTweet': {
                        'date': '2025-01-02T00:00:00',
                        'id': 3,
                        'user': {'username': 'user_1'},
                        'quotedTweet': None}
                    }},
            {
                'date': '2025-01-01T00:00:01',
                'id': 2,
                'user': {'username': 'user_1'},
                'quotedTweet': {
                    'date': '2025-01-02T00:00:00',
                    'id': 3,
                    'user': {'username': 'user_1'},
                    'quotedTweet': None}},
            {
                'date': '2025-01-02T00:00:00',
                'id': 3,
                'user': {'username': 'user_2'},
                'quotedTweet': None},
            {
                'date': '2025-01-02T00:10:00',
                'id': 4,
                'user': {'username': 'user_2'},
                'quotedTweet': None},
            {
                'date': '2025-01-02T00:00:02',
                'id': 5,
                'user': {'username': 'user_3'},
                'quotedTweet': None},
        ]
        file_path = self.create_test_file(test_data)

        result_time = q1_time(file_path)
        result_memory = q1_memory(file_path)

        expected = [
            (date(2025, 1, 2), 'user_2'),
            (date(2025, 1, 1), 'user_1')
        ]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

    def test_two_dates_with_distinct_activity_quote_new(self):
        """Test with two dates where each has a distinct top user with
        new quoted tweet."""
        test_data = [
            {
                'date': '2025-01-01T00:00:00',
                'id': 1,
                'user': {'username': 'user_1'},
                'quotedTweet': {
                    'date': '2025-01-01T00:00:01',
                    'id': 2,
                    'user': {'username': 'user_1'},
                    'quotedTweet': {
                        'date': '2025-01-02T00:00:00',
                        'id': 3,
                        'user': {'username': 'user_2'},
                        'quotedTweet': None}
                    }},
            {
                'date': '2025-01-01T00:00:01',
                'id': 2,
                'user': {'username': 'user_1'},
                'quotedTweet': {
                    'date': '2025-01-02T00:00:00',
                    'id': 3,
                    'user': {'username': 'user_2'},
                    'quotedTweet': None}},
            {
                'date': '2025-01-02T00:00:00',
                'id': 3,
                'user': {'username': 'user_2'},
                'quotedTweet': None},
            {
                'date': '2025-01-02T00:10:00',
                'id': 4,
                'user': {'username': 'user_2'},
                'quotedTweet': {
                    'date': '2025-01-02T00:11:00',
                    'id': 6,
                    'user': {'username': 'user_4'},
                    'quotedTweet': {
                        'date': '2025-01-02T00:12:00',
                        'id': 7,
                        'user': {'username': 'user_4'},
                        'quotedTweet': None}}},
            {
                'date': '2025-01-02T00:00:02',
                'id': 5,
                'user': {'username': 'user_3'},
                'quotedTweet': {
                    'date': '2025-01-02T00:13:00',
                    'id': 8,
                    'user': {'username': 'user_4'},
                    'quotedTweet': None}},
        ]
        file_path = self.create_test_file(test_data)

        result_time = q1_time(file_path)
        result_memory = q1_memory(file_path)

        expected = [
            (date(2025, 1, 2), 'user_4'),
            (date(2025, 1, 1), 'user_1')
        ]

        self.assertEqual(result_time, expected)
        self.assertEqual(result_memory, expected)

if __name__ == '__main__':
    unittest.main()
