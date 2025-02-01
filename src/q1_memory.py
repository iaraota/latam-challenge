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

    # Initialize counters for dates and users
    date_counts = Counter()
    user_counts = defaultdict(Counter)
    ids = set()

    with open(file_path, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            date = datetime.fromisoformat(tweet['date']).date()
            date_counts[date] += 1
            user_counts[date][tweet['user']['username']] += 1
            ids.add(tweet['id'])

    # now read the quoted tweets
    with open(file_path, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            # create a queue to process the quoted tweets
            queue = []
            if tweet.get('quotedTweet'):
                queue = [tweet.get('quotedTweet')]
            while queue:
                # pop the first tweet from the queue
                current = queue.pop(0)
                # process the tweet if it hasn't been processed yet
                if current['id'] not in ids:
                    date = datetime.fromisoformat(current['date']).date()
                    date_counts[date] += 1
                    user_counts[date][current['user']['username']] += 1
                    ids.add(current['id'])
                # get the next quoted tweet if it exists
                if current.get('quotedTweet'):
                    # append the quoted tweet to the queue
                    queue.append(current['quotedTweet'])

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
