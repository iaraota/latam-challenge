from typing import List, Tuple
from datetime import datetime

import json
import pandas as pd

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """Find the top user for each of the top 10 dates with the most activity.

    Note: For optimizing time, we use Pandas DataFrame to process the data
    which is usually very fast due to its vectorized operations.

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

    # Read and process the JSON file line by line
    # This is faster than using pd.read_json directly
    # because it avoids reading the entire file
    # consequently, it is also more memory efficient

    # Use generator to avoid storing full list in memory
    # This is faster than using pd.read_json directly
    # because it avoids reading the entire file
    # consequently, it is also more memory efficient
    def row_generator():
        with open(file_path, 'r') as f:
            for line in f:
                tweet = json.loads(line)
                yield (
                    tweet['date'],
                    tweet['id'],
                    tweet['user'],
                    tweet['quotedTweet'],
                )

    # Create DataFrame from generator
    df = pd.DataFrame(
        row_generator(),
        columns=[
            'date',
            'id',
            'user',
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
    quoted_df = pd.DataFrame(all_quoted).drop_duplicates(subset='id')
    # keep only columns that are needed
    if not quoted_df.empty:
        quoted_df = quoted_df[['date', 'id', 'user']]
    # quoted_df = quoted_df[['date', 'id', 'user']]
    df = pd.concat([df, quoted_df], ignore_index=True).drop_duplicates(subset='id')

    # Extract the 'date' and 'username' columns
    df['username'] = df['user'].apply(lambda x: x['username'])
    df = df[['date', 'username']]

    # Convert 'date' to datetime.date and keep only the date part
    df['date'] = pd.to_datetime(df['date']).dt.date
    # Find top 10 dates with most activity
    n = 10
    top_dates = df['date'].value_counts().nlargest(n).reset_index()
    # Create a rank column, to be used for sorting later
    top_dates['rank'] = top_dates.index

    # Join df and top_dates to keep only the top dates and the number of dates
    merged = df.merge(top_dates, on='date')

    # Find the top user for each of the top 10 dates
    result = (
        merged.groupby(['date', 'rank'])  # group by date and rank
        [['date', 'rank', 'username']]    # select only these columns
        .apply(lambda g: g['username']    # get the username with most activity
               .value_counts().idxmax())
        .sort_index(level='rank',         # sort by rank
                    ascending=True)
        .droplevel('rank')                # remove rank
    )

    # Convert result to a list of tuples and return
    return list(result.items())
