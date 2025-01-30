from typing import List, Tuple
from datetime import datetime

import pandas as pd # used to process data

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """Find the top user for each of the top 10 dates with the most activity.

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

    # Read JSON file into a DataFrame
    df = pd.read_json(
        file_path,
        lines=True,          # each line is a JSON object
        )[['date', 'user']]  # only keep 'date' and 'user' columns

    # Convert 'date' to datetime.date and keep only the date part
    df['date'] = df['date'].dt.date
    # Extract 'username' from 'user' column
    df['username'] = df['user'].apply(lambda u: u['username'])
    # Drop 'user' column, as we no longer need it
    df.drop('user', axis=1, inplace=True)

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
