"""Profile memory usage of functions in the project.

This script is done outside of the notebook to avoid memory leaks that
the Jupiter notebook might cause. The garbage collector is called after
each run to make sure that the memory is freed before the next run.

This script will create a folder `benchmark` in the directory of the
script and save the memory profile of each function in that folder.
"""

import pathlib
import gc
from typing import Callable, List, Any

from memory_profiler import memory_usage

from q1_time import q1_time
from q1_memory import q1_memory
from q2_time import q2_time
from q2_memory import q2_memory
from q3_time import q3_time
from q3_memory import q3_memory


def profile_function(
        func: Callable[[str], List[Any]],
        file_path: str,
        n: int,
        file_name: str,
        interval=0.05
        ) -> None:
    """Profile the memory usage of a function. Run the function n times and
    record the memory usage in a file.

    Parameters
    ----------
    func : Callable[[str], List[Any]]
        The function to profile.
    file_path : str
        Path to the JSON file containing the tweets data.
    n : int
        Number of times to run the function.
    file_name : str
        Name of the file to save the memory profile.
    interval : float, optional
        Interval to check memory usage in seconds, by default 0.05
    """

    # delete file if exists
    pathlib.Path(file_name).unlink(missing_ok=True)

    # Loop n times
    for _ in range(n):
        # profile memory usage
        mem_usage = memory_usage((func, (file_path,)), interval=interval)

        # append to file
        with open(file_name, "a") as f:
            f.write(str(mem_usage)[1:-1])
            f.write("\n")
            f.close()
        # print progress
        print(".", end="")
        # collect garbage to avoid memory leak
        gc.collect()



if __name__ == "__main__":
    # data file path
    file_path = "farmers-protest-tweets-2021-2-4.json"
    # number of runs
    n = 10

    # functions to run
    run_all = {
        'q1_time': q1_time,
        'q1_memory': q1_memory,
        'q2_time': q2_time,
        'q2_memory': q2_memory,
        'q3_time': q3_time,
        'q3_memory': q3_memory
    }

    # check if ../benchmark exists and create if not
    pathlib.Path("../benchmark").mkdir(exist_ok=True)

    # run all functions
    for label, func in run_all.items():
        print(f"Profiling {label}", end='')
        file_name = f"../benchmark/{label}_mprof.txt"
        profile_function(func, file_path, n, file_name)
        print(f"\nFinished profiling {label}.")
        print(f"Saved to {file_name}")
        print("")
