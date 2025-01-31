from typing import List, Tuple

import json
from collections import Counter

import pandas as pd
import emoji


def q3_time(file_path: str) -> List[Tuple[str, int]]:
    """Finds the historical top 10 most influential users (username)
    based on the count of mentions (@) each one receives.

    Both the main tweet and the quoted tweet are considered to count.
    Double counting is avoided by removing the quoted content that is
    a reply to another tweet.

    Note: For optimizing time, Pandas DataFrame is used to process the data
    which is usually very fast due to its vectorized operations.

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
                    tweet['user']['username'],
                    quoted_tweet.get('content'),
                    quoted_tweet.get('id'),
                )

    # Create DataFrame from generator
    df = pd.DataFrame(
        row_generator(),
        columns=[
            'main_content',
            'main_id',
            'username',
            'quoted_content',
            'quoted_id',
            ]
    )

    # Get the quoted content and remove the None values
    quoted_df = (
        df[['quoted_content', 'quoted_id']]
        .dropna()
    )

    # Remove quoted content that is a reply to another tweet,
    # to avoid double counting
    quoted_df = quoted_df[
        ~quoted_df['quoted_id'].isin(df['main_id'])
        ]

    # Combine main and valid quoted content
    main_texts = df['main_content']
    quoted_texts = quoted_df['quoted_content']
    all_texts = pd.concat([main_texts, quoted_texts])

    # Extract mentions from all texts
    mentions = all_texts.str.findall(r'@(\w+)').explode().dropna()

    # Drop mentions that are not usernames
    usernames = df['username'].unique()
    mentions = mentions[mentions.isin(usernames)]

    # Count mentions and get top 10
    top_mentions = mentions.value_counts().head(10).reset_index()
    top_mentions.columns = ['username', 'count']

    # Convert DataFrame to list of tuples
    return list(top_mentions.itertuples(index=False, name=None))
