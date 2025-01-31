import json
from collections import defaultdict, Counter
from typing import List, Tuple
import emoji


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
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
