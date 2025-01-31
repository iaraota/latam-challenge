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
        A list of tuples where each tuple contains an emoji and its count.
        The list is sorted in descending order of the count.
    """

    # Use generator to avoid storing full list in memory
    # This is faster than using pd.read_json directly
    # because it avoids reading the entire file
    # consequently, it is also more memory efficient
    def row_generator():
        with open(file_path, 'r') as f:
            for line in f:
                tweet = json.loads(line)
                yield (
                    tweet['content'],
                    tweet['id'],
                    tweet['quotedTweet'],
                )

    # Create DataFrame from generator
    df = pd.DataFrame(
        row_generator(),
        columns=[
            'content',
            'id',
            'quotedTweet',
            ]
    )

    # Flatten all nested quoted tweets using a queue
    all_quoted = []
    queue = df['quotedTweet'].dropna().tolist()
    while queue:
        current = queue.pop(0)
        all_quoted.append(current)
        quoted = current.get('quotedTweet')
        if quoted is not None:
            queue.append(quoted)

    # Combine original and quoted tweets, removing duplicates
    quoted_df = pd.DataFrame(all_quoted)

    # keep only columns that are needed
    if not quoted_df.empty:
        quoted_df = quoted_df[['content', 'id']]

    df = pd.concat([df, quoted_df], ignore_index=True).drop_duplicates(subset='id')
    # Get all the texts from the main content and quoted content
    texts = df['content'].tolist()

    # Make a list of all the emojis in the texts
    emojis_flat = [e['emoji'] for text in texts for e in emoji.emoji_list(text)]

    # Return the top 10 emojis and its count
    return Counter(emojis_flat).most_common(10)
