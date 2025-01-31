from typing import List, Tuple

import json
from collections import Counter

import pandas as pd
import emoji


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """Find the top 10 emojis used in the main content of the tweets and
    the quoted content of the tweets. Only consider quoted content that
    is not a reply to another tweet, to avoid double counting.

    Note: For optimizing time, we use Pandas DataFrame to process the data
    which is usually very fast due to its vectorized operations.

    Parameters
    ----------
    file_path : str
        Path to the JSON file containing the tweets data.

    Returns
    -------
    List[Tuple[str, int]]
        A list of tuples containing the top 10 emoji and the number of times
        it was used.
    """

    # Use generator to avoid storing full list in memory
    # This is faster than using pd.read_json directly
    # because it avoids reading the entire file
    # consequently, it is also more memory efficient
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

    # Create DataFrame from generator
    df = pd.DataFrame(
        row_generator(),
        columns=[
            'main_content',
            'main_id',
            'quoted_content',
            'quoted_id',
            ]
    )

    # Get the quoted content and remove the None values
    quoted_df = (
        df[['quoted_content', 'quoted_id']]
        .dropna(subset=['quoted_content', 'quoted_id'])
    )

    # Remove quoted content that is a reply to another tweet,
    # to avoid double counting
    quoted_df = quoted_df[
        ~quoted_df['quoted_id'].isin(df['main_id'])
        ]

    # Get all the texts from the main content and quoted content
    texts = (
        df['main_content'].tolist() +
        quoted_df['quoted_content'].tolist()
    )

    # Make a list of all the emojis in the texts
    emojis_flat = [e['emoji'] for text in texts for e in emoji.emoji_list(text)]

    # Return the top 10 emojis and its count
    return Counter(emojis_flat).most_common(10)
