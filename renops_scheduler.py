#!/usr/bin/env python3

import argparse
import subprocess
import time
from datetime import datetime, timedelta

import pandas as pd

from utils.datafetcher import DataFetcher


def parse_time(time_string):
    return datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")


def wait_until(target_time):
    while datetime.now() < target_time:
        time.sleep(5)  # Sleep for a bit to not hog the CPU


def execute_script(script_path):
    subprocess.run(["python", script_path])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("script_path", help="Path to the script to be executed.")
    parser.add_argument(
        "-l", "--location", default=None, help="Location in string or coordinates."
    )
    parser.add_argument(
        "-r", "--runtime", type=int, default=3, help="Runtime in hours."
    )
    parser.add_argument(
        "-d", "--deadline", type=int, default=120, help="Deadline in hours."
    )
    parser.add_argument("-v", "--verbose", type=int, default=None, help="Verbose mode.")

    args = parser.parse_args()

    url = "http://localhost:5689/forecast/renewable_potential"
    fetcher = DataFetcher(url)
    data = fetcher.fetch_data()

    res = data.resample(str(args.runtime) + "H").mean()
    res = res.renewable_potential_forecast_hourly.sort_values(ascending=False)

    current_date = pd.Timestamp(datetime.now())
    deadline_date = pd.Timestamp(datetime.now() + timedelta(hours=args.deadline))
    filtered_res = res[(res.index > current_date) & (res.index < deadline_date)]

    # Here you would call the function to get the optimal time, using the location, runtime and deadline
    # For now, let's just use the deadline time.
    optimal_time = filtered_res.index[0]

    if len(filtered_res) == 1:
        optimal_time = datetime.now()

    print(
        "Found optimal time between ",
        filtered_res.index[0],
        "and",
        filtered_res.index[0] + timedelta(hours=args.runtime),
    )
    print("Renewable potential at that time is:", filtered_res[0].round(2))

    print(f"Waiting until {optimal_time} to execute {args.script_path}...")
    wait_until(optimal_time)
    print(f"Executing {args.script_path} now at {datetime.now()}")
    print("----------------------------------------------------")
    execute_script(args.script_path)


if __name__ == "__main__":
    main()
