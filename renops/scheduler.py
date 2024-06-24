import subprocess
import time
from datetime import datetime
from typing import Callable, Tuple, Union

import renops.config as conf
from renops.datafetcher import DataFetcher


def parse_time(time_string):
    return datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")


def wait_until(target_time):
    while int(time.time()) < target_time:
        time.sleep(conf.runtime.sleep_seconds)  # Sleep for a bit to not hog the CPU


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


class Scheduler():
    """
    Scheduler to optmise scheduling of energy intensive tasks
    Args:
        deadline (int): The deadline for the scheduled task.
        runtime (int): The runtime required for the task.
        location (str): The location where the task will be executed.
        action (Callable): The function to be executed.
        optimise_type (str, optional): The type of optimization optons are "price", "carbon_emmisions",
                                       "renewable_potential". Defaults to "renewable_potential".
        optimise_price (bool, optional): Deprecated. Use 'optimise_type' instead. Defaults to False.
        verbose (bool, optional): Flag to enable verbose output. Defaults to False.
        argument (Tuple[Union[int, str], ...], optional): Arguments for the action function. Defaults to ().
        kwargs (Union[dict, None], optional): Keyword arguments for the action function. Defaults to {}.

    Raises:
        DeprecationWarning: If 'optimise_price' is used.
        ValueError: If an invalid 'optimise_type' is provided.

    Attributes:
        deadline (int): The deadline for the scheduled task.
        runtime (int): The runtime required for the task.
        location (str): The location where the task will be executed.
        v (bool): Verbose flag.
        optimise_type (str): The type of optimization.
        action (Callable): The function to be executed.
        argument (Tuple[Union[int, str], ...]): Arguments for the action function.
        kwargs (dict): Keyword arguments for the action function.
    """
    def __init__(self,
                 deadline: int,
                 runtime: int,
                 location: str,
                 action: Callable,
                 optimise_type: str = "renewable_potential",
                 optimise_price: bool = False,
                 verbose: bool = False,
                 argument: Tuple[Union[int, str], ...] = (),
                 kwargs: Union[dict, None] = {},
                 ) -> None:
        if optimise_price:
            optimise_type = "price"
            raise DeprecationWarning(
                "'optimise_price' is deprecated and will be removed in future versions. Use 'optimise_type' instead."
            )
        self.deadline = deadline
        self.runtime = runtime
        self.location = location
        self.v = verbose
        # Allow optimise_type to be a string
        # Convert string optimise_type to OptimisationType enum
        try:
            self.optimise_type = conf.OptimisationType[optimise_type]
        except KeyError:
            raise ValueError(f"Invalid option '{optimise_type}', must be one of {[e.value for e in conf.OptimisationType]}.")  # noqa

        self.optimise_type = optimise_type
        self.action = action
        self.argument = argument
        self.kwargs = kwargs if kwargs is not None else {}

    def get_data(self):
        fetcher = DataFetcher(location=self.location)
        return fetcher.fetch(self.optimise_type)

    def _preprocess_data(self, data):

        # Resample to 2H buckets
        res = data.resample("2h").agg({
            "metric": "mean",
            "epoch": "first",
            "timestamps_hourly": "first",
        })

        # Sort to minimise renewable potential
        res = res.set_index("epoch")

        ascending = False if self.optimise_type == "carbon_emissions" else True

        res = res.sort_values(by=["metric"], ascending=ascending)

        return res

    def _extract_epochs(self):
        self.current_epoch = int(time.time())
        self.deadline_epoch = self.current_epoch + hour_to_second(self.deadline)
        self.start_execution_epoch = self.deadline_epoch - hour_to_second(self.runtime)

        return None

    def _filter_samples(self, res):
        filtered_res = res[
            (res.index >= self.current_epoch) & (res.index <= self.start_execution_epoch)
        ]
        filtered_res = filtered_res.loc[res.metric != 0]
        return filtered_res

    def _get_current_renewables(self, data):
        renewables_now = data[data.epoch >= self.current_epoch]
        renewables_now = renewables_now.metric.values[
            0
        ].round(2)
        return renewables_now

    def _update_global_config(self):
        conf.runtime.set_verbose(self.v)

    def run(self):
        self._update_global_config()
        data = self.get_data()
        res = self._preprocess_data(data)
        self._extract_epochs()  # extract deadilnes runtimes etc TODO
        filtered_res = self._filter_samples(res)

        if self.v:
            print("Task has to be finished by: ", to_datetime(self.deadline_epoch))
        if len(filtered_res) <= 1:
            renewables_now = self._get_current_renewables(data)
            filtered_res[self.current_epoch] = renewables_now
            optimal_time = self.current_epoch

            if self.v:
                print("No renewable window whitin a given deadline!")
                print("Current renewable potential is:")
                if self.optimise_type == "price":
                    print(
                        renewables_now,
                        "EUR/MWh",
                    )
                elif self.optimise_type == "carbon_emissions":
                    print(
                        renewables_now,
                        "gCO2eq/kWh",
                    )
                elif self.optimise_type == "renewable_potential":
                    print(
                       renewables_now,
                    )

        else:
            optimal_time = filtered_res.index[0]
            diff_seconds = optimal_time - self.current_epoch

            if self.v:
                print(
                    "Found optimal time between ",
                    to_datetime(filtered_res.index[0]),
                    "and",
                    to_datetime(filtered_res.index[0] + hour_to_second(self.runtime)),
                )
                if self.optimise_type == "price":
                    print(
                        "Energy price at that time is:",
                        filtered_res.metric.values[0].round(2),
                        "EUR/MWh",
                    )
                elif self.optimise_type == "carbon_emissions":
                    print(
                        "Carbon emissions at that time are:",
                        filtered_res.metric.values[0].round(2),
                        "gCO2eq/kWh",
                    )
                elif self.optimise_type == "renewable_potential":
                    print(
                        "Renewable potential at that time is:",
                        filtered_res.metric.values[0].round(2),
                    )

                print(
                    f"Waiting for"
                    f" {convert_seconds_to_hour(diff_seconds)} h"
                    f" {convert_seconds_to_minutes(diff_seconds)} min"
                    f"..."
                )

        wait_until(optimal_time)

        if self.v:
            print(f"Executing action now at {datetime.now()}")
        if self.v:
            print("----------------------------------------------------")
        self.action(*self.argument, **self.kwargs)
