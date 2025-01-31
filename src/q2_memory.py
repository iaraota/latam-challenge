import json
from collections import defaultdict, Counter
from typing import List, Tuple
import emoji


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """Find the top 10 emojis used in the main content of the tweets and
    the quoted content of the tweets. Only consider quoted content that
    is not a reply to another tweet, to avoid double counting.

    Note: For optimizing memory usage, we use Python objects, which doesn't
    have big overhead like Pandas DataFrames.

    Parameters
    ----------
    file_path : str
        Path to the JSON file containing the tweets data.

    Returns
    -------
    List[Tuple[str, int]]
        A list of tuples where each tuple contains an emoji and its count.
        The list is sorted in descending order of the count.
    """

    # Initialize dictionaries to store the main and quoted content
    content = defaultdict(str)

    with open(file_path, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            content[tweet['id']] = tweet['content']

    # remove quotes that are replies, that is, there exists a main tweet
    # with the same id as the quoted tweet. This avoids duplicates
    ids = set(content.keys())

    # now read the quoted tweets
    with open(file_path, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            queue = []
            if tweet.get('quotedTweet'):
                queue = [tweet.get('quotedTweet')]
            while queue:
                current = queue.pop(0)
                if current['id'] not in ids:
                    content[current['id']] = current['content']
                    ids.add(current['id'])
                if current.get('quotedTweet'):
                    queue.append(current['quotedTweet'])

    # Get all the texts from tweets
    texts = list(content.values())

    # Make a list of all the emojis in the texts
    emojis_flat = [e['emoji'] for text in texts for e in emoji.emoji_list(text)]

    # Return the top 10 emojis and its count
    return Counter(emojis_flat).most_common(10)
