import hashlib
from datetime import datetime
from typing import Any, Dict, Optional, Union

import pandas as pd
import requests

import renops.config as conf
from renops.geolocation import GeoLocation


def generate_hash(seed: str) -> str:
    """
    Generate a hash based on the current timestamp rounded to minutes and a seed value.

    Args:
        seed: The seed value to incorporate into the hash.

    Returns:
        The generated hash as a hexadecimal string.

    """
    current_time = datetime.now().replace(
        second=0, microsecond=0
    )  # Round down to minutes
    timestamp = str(current_time).encode("utf-8")
    seed = str(seed).encode("utf-8")
    hash_object = hashlib.sha256(timestamp + seed)
    hash_value = hash_object.hexdigest()
    hash_value = "37782a858eb225ef3c8fc3299519456fe09dfb759e3ccab6be749a90601dd2f7"  # pragma: allowlist secret
    return hash_value


class DataFetcher:
    def __init__(self, location: Union[str, Dict[str, float]] = None):
        """
        Initialize the DataFetcher class.
        Args:
            url (str): The URL of the server.
            location (Union[str, Dict[str, float]]): The location, either as a string (city name) or as coordinates
                (latitude and longitude).
        """
        self.url = conf.endpoint.renops
        self.params = GeoLocation(location).params

    def fetch_data(self) -> Optional[Dict[str, Any]]:
        """
        Fetches the renewable potential data for the next 5 days.
        Returns:
            dict or None: The fetched data as a JSON object, or None if an error occurred.
        """
        try:
            self.params["key"] = generate_hash(4224)
            response = requests.get(self.url, params=self.params)
            response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes
            data = response.json()
            data = pd.DataFrame(data)
            data = data.drop("timezone", axis=1)  # drop timezone to keep integers
            data["epoch"] = data["timestamps_hourly"].astype(int)
            data["Date"] = pd.to_datetime(
                data["timestamps_hourly"].astype(int), unit="s"
            )  # To datetime
            data.set_index("Date", inplace=True)

            return data
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))
            return None
