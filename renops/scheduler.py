#!/usr/bin/env python3

import argparse
import subprocess
import time
from datetime import datetime

from renops.datafetcher import DataFetcher


def parse_time(time_string):
    return datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")


def wait_until(target_time):
    while int(time.time()) < target_time:
        time.sleep(5)  # Sleep for a bit to not hog the CPU


def execute_script(script_path):
    subprocess.run(["python3", script_path])


def hour_to_second(hour: int) -> int:
    "Converts hours to seconds"
    return hour * 3600


def convert_seconds_to_hour(seconds: int) -> int:
    "Converts seconds to hour with no residual"
    return int(seconds // 3600)


def convert_seconds_to_minutes(seconds: int) -> int:
    "Converts seconds to minutes with no residual"
    return int((seconds % 3600) // 60)


def to_datetime(epoch):
    return datetime.fromtimestamp(epoch).strftime("%Y-%d-%m %H:%M:%S")


def main():
    print("RUNNING RENOPS SCHEDULER...")
    parser = argparse.ArgumentParser()
    parser.add_argument("script_path", help="Path to the script to be executed.")
    parser.add_argument(
        "-l",
        "--location",
        default=None,
        help="Location in string - 'settlement,country' i.e 'Berlin, Germany')",
        required=True
    )
    parser.add_argument(
        "-r", "--runtime", type=int, default=None, help="Runtime in hours."
    )
    parser.add_argument(
        "-d",
        "--deadline",
        type=int,
        default=120,
        help="Deadline in hours, by when should script finish running",
    )
    parser.add_argument("-v", "--verbose", type=int, default=None, help="Verbose mode.")

    args = parser.parse_args()

    if not args.runtime:
        print("Runtime not specified, using default setting of 3 hours!")
        args.runtime = 3

    url = "https://renops-api-tango.xlab.si/forecast/renewable_potential"
    fetcher = DataFetcher(url, location=args.location)
    data = fetcher.fetch_data()

    res = data.resample(str(args.runtime) + "H").mean()
    res = res.set_index("epoch")
    res = res.sort_values(by=["renewable_potential_forecast_hourly"], ascending=False)

    current_epoch = int(time.time())
    deadline_epoch = current_epoch + hour_to_second(args.deadline)
    start_execution_epoch = deadline_epoch - hour_to_second(args.runtime)

    print("Task has to be finished by: ", to_datetime(deadline_epoch))
    filtered_res = res[
        (res.index >= current_epoch) & (res.index <= start_execution_epoch)
    ]
    filtered_res = filtered_res.loc[res.renewable_potential_forecast_hourly != 0]
    # Here you would call the function to get the optimal time, using the location, runtime and deadline
    # For now, let's just use the deadline time.

    if len(filtered_res) <= 1:
        optimal_time = current_epoch

        renewables_now = data[data.epoch >= optimal_time]
        renewables_now = renewables_now.renewable_potential_forecast_hourly.values[
            0
        ].round(2)
        filtered_res[int(time.time())] = renewables_now
        print("No renewable window whitin given deadline!")
        print(f"Current renewable potential is: {renewables_now}")
    else:
        optimal_time = filtered_res.index[0]

        diff_seconds = optimal_time - current_epoch
        wait_hours = convert_seconds_to_hour(diff_seconds)
        wait_minutes = convert_seconds_to_minutes(diff_seconds)

        print(
            "Found optimal time between ",
            to_datetime(filtered_res.index[0]),
            "and",
            to_datetime(filtered_res.index[0] + hour_to_second(args.runtime)),
        )
        print(
            "Renewable potential at that time is:",
            filtered_res.renewable_potential_forecast_hourly.values[0].round(2),
        )
        print(
            f"Waiting for {wait_hours} h {wait_minutes} min to execute {args.script_path}..."
        )

    wait_until(optimal_time)
    print(f"Executing {args.script_path} now at {datetime.now()}")
    print("----------------------------------------------------")
    execute_script(args.script_path)


if __name__ == "__main__":
    main()
