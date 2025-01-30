from typing import List, Tuple
from datetime import datetime

import pandas as pd # <--- used to process data

from src.q1_time import q1_time

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    result = q1_time(file_path)

    return result
