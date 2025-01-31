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

    # Use generator to avoid storing full list in memory
    def row_generator():
        with open(file_path, 'r') as f:
            for line in f:
                tweet = json.loads(line)
                quoted_tweet = tweet.get('quotedTweet') or {}
                yield (
                    tweet['content'],
                    tweet['id'],
                    quoted_tweet.get('content'),
                    quoted_tweet.get('id'),
                )

    # Initialize dictionaries to store the main and quoted content
    main = defaultdict(str)
    quoted = defaultdict(str)

    # Store the main and quoted content in the dictionaries
    for content, main_id, quoted_content, quoted_id in row_generator():
        main[main_id] = content
        # Only store the quoted content if it exists,
        # this is good for memory optimization
        if quoted_content:
            quoted[quoted_id] = quoted_content

    # remove quotes that are replies, that is, there exists a main tweet
    # with the same id as the quoted tweet. This avoids duplicates
    main_ids = set(main.keys())
    quoted = {k: v for k, v in quoted.items() if k not in main_ids}

    # Get all the texts from the main content and quoted content
    texts = (
        list(main.values()) +
        list(quoted.values())
    )

    # Make a list of all the emojis in the texts
    emojis_flat = [e['emoji'] for text in texts for e in emoji.emoji_list(text)]

    # Return the top 10 emojis and its count
    return Counter(emojis_flat).most_common(10)
