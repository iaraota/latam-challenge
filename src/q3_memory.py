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

    # Use generator to avoid storing full json in memory
    def row_generator():
        with open(file_path, 'r') as f:
            for line in f:
                tweet = json.loads(line)
                quoted_tweet = tweet.get('quotedTweet') or {}
                yield (
                    tweet['content'],
                    tweet['id'],
                    tweet['user']['username'],
                    quoted_tweet.get('content'),
                    quoted_tweet.get('id'),
                )

    # Initialize dictionaries to store the main and quoted content
    # and usernames
    main = defaultdict(str)
    quoted = defaultdict(str)
    usernames = set()

    # Store the main and quoted content in the dictionaries
    for content, main_id, user, quoted_content, quoted_id in row_generator():
        main[main_id] = content
        # Only store the quoted content if it exists,
        # this is good for memory optimization
        if quoted_content:
            quoted[quoted_id] = quoted_content
        usernames.add(user)

    # remove quotes that are replies, that is, there exists a main tweet
    # with the same id as the quoted tweet. This avoids duplicates
    main_ids = set(main.keys())
    quoted = {k: v for k, v in quoted.items() if k not in main_ids}

    # Get all the texts from the main content and quoted content
    texts = (
        list(main.values()) +
        list(quoted.values())
    )

    # Extract mentions from the texts, and filter out
    # mentions that are not in the usernames
    mentions = [
        mention
        for text in texts
        for mention in re.findall(r'@(\w+)', text)
        if mention in usernames
    ]

    # Count the mentions and return the top 10
    return Counter(mentions).most_common(10)
