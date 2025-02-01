from typing import List, Tuple
import json

import pandas as pd


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
                yield (
                    tweet['id'],
                    tweet['mentionedUsers'],
                    tweet['quotedTweet'],
                )

    # Create DataFrame from generator
    df = pd.DataFrame(
        row_generator(),
        columns=[
            'id',
            'mentionedUsers',
            'quotedTweet',
            ]
    )

    # Flatten all nested quoted tweets using a queue
    all_quoted = []
    # Create a queue to process quoted tweets
    queue = df['quotedTweet'].dropna().tolist()
    while queue:
        # Pop the first element from the queue
        current = queue.pop(0)
        # Add to the list of all quoted tweets
        all_quoted.append(current)
        # Get the next quoted tweet
        quoted = current.get('quotedTweet')
        # If there is a quoted tweet, add to the queue
        if quoted is not None:
            queue.append(quoted)

    # Combine original and quoted tweets, removing duplicates
    quoted_df = pd.DataFrame(all_quoted)

    # keep only columns that are needed
    if not quoted_df.empty:
        quoted_df = quoted_df[['id', 'mentionedUsers', 'quotedTweet']]

    # Combine original and quoted tweets, removing duplicates
    df = pd.concat([df, quoted_df], ignore_index=True).drop_duplicates(subset='id')

    # Transform mentionedUsers column, which is a list of dictionaries,
    # into a dataframe and get the username column
    username = pd.json_normalize(
        df['mentionedUsers']
        .dropna()
        .explode()
        .reset_index(drop=True)
        )

    # Get the username column
    if not username.empty:
        username = username['username']
    # If no usernames are found, return empty list
    else:
        return []

    # Count the number of mentions for each username
    # and get the top 10
    top_mentions = username.value_counts().head(10).reset_index()

    # Convert to list of tuples and return
    return top_mentions.to_records(index=False).tolist()
