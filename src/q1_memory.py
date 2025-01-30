from typing import List, Tuple
from datetime import datetime

import json
from collections import defaultdict, Counter


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """Find the top user for each of the top 10 dates with the most activity.

    Note: For optimizing memory usage, we use Python objects, which doesn't
    have big overhead like Pandas DataFrames.

    Parameters
    ----------
    file_path : str
        Path to the JSON file containing the tweets data.

    Returns
    -------
    List[Tuple[datetime.date, str]]
        A list of tuples containing the date and the username of the top user
        for each of the top 10 dates with the most activity.
    """

    # Generator function to process lines in the file
    # using a generator to avoid loading the entire file into memory
    def read_json_lines(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                tweet = json.loads(line)
                dt = datetime.fromisoformat(tweet['date'])
                current_date = dt.date()
                username = tweet['user']['username']
                yield current_date, username

    # Initialize counters for dates and users
    date_counts = Counter()
    user_counts = defaultdict(Counter)

    # Process the file using the generator and update counters
    for current_date, username in read_json_lines(file_path):
        date_counts[current_date] += 1
        user_counts[current_date][username] += 1

    # Get the top 10 most active dates
    top_dates = [date for date, _ in date_counts.most_common(10)]

    # Determinine the top user for each of the top 10 dates
    result = []
    for date in top_dates:
        if user_counts[date]:
            # most_common(1) returns a list of tuple, that is the
            # tuple with the username and the count of tweets
            # we only need the username of the top user, hence the [0][0]
            top_user = user_counts[date].most_common(1)[0][0]
        else:
            # Handle the case where there are no tweets for a date
            # this should never happen, but just in case we handle it
            top_user = None
        result.append((date, top_user))

    return result
