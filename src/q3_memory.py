from typing import List, Tuple

import re
import json
from collections import defaultdict, Counter


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """Finds the historical top 10 most influential users (username)
    based on the count of mentions (@) each one receives.

    Both the main tweet and the quoted tweet are considered to count.
    Double counting is avoided by removing the quoted content that is
    a reply to another tweet.

    Parameters
    ----------
    file_path : str
        Path to the JSON file containing the tweets data.

    Returns
    -------
    List[Tuple[str, int]]
        A list of tuples containing the top 10 most influential users
        and the count of mentions each one receives.
    """

    # Initialize dictionaries to store the main and quoted content
    mentioned = Counter()
    ids = set()

    with open(file_path, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            ids.add(tweet['id'])
            # count mentions username
            if tweet.get('mentionedUsers'):
                for mention in tweet['mentionedUsers']:
                    username = mention['username']
                    mentioned[username] += 1


    # now read the quoted tweets
    with open(file_path, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            # create a queue to process the quoted tweets
            queue = []
            if tweet.get('quotedTweet'):
                queue = [tweet.get('quotedTweet')]
            while queue:
                # pop the first element
                current = queue.pop(0)
                if current['id'] not in ids:
                    # count mentions username
                    if current.get('mentionedUsers'):
                        for mention in current['mentionedUsers']:
                            username = mention['username']
                            mentioned[username] += 1
                    ids.add(current['id'])
                # add the quoted tweet of the current tweet to the queue
                # if it exists
                if current.get('quotedTweet'):
                    queue.append(current['quotedTweet'])

    # Count the mentions and select the top 10
    return mentioned.most_common(10)
