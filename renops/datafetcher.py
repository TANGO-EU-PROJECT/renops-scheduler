import sys
from typing import Any, Dict, List, Optional, Union

import pandas as pd
import requests

import renops.config as conf
from renops.geolocation import GeoLocation


class DataFetcher:
    def __init__(self, location: Union[str, Dict[str, float]] = None):
        """
        Initialize the DataFetcher class.
        Args:
            url (str): The URL of the server.
            location (Union[str, Dict[str, float]]): The location, either as a string (city name) or as coordinates
                (latitude and longitude).
        """
        self.params = GeoLocation(location).params

    def filter_dict(self, in_dict: Dict, keys_to_keep: List) -> Dict:
        """
        Return dictionary with keys we want to keep
        """
        return {key: in_dict[key] for key in keys_to_keep}

    def fetch_data(self) -> Optional[Dict[str, Any]]:
        """
        Fetches the renewable potential data for the next 5 days.
        Returns:
            dict or None: The fetched data as a JSON object, or None if an error occurred.
        """
        try:
            response = requests.get(
                conf.renopsapi.renewable_potential, params=self.params, headers={"key": conf.renopsapi.key}
            )
            response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes
            data_full = response.json()

            # Define needed keys for calculating renewable potential
            keys_to_keep = ["timestamps_hourly", "renewable_potential_forecast_hourly"]

            # Filter needed keys
            data = self.filter_dict(data_full, keys_to_keep)

            # Convert to DataFrame
            data = pd.DataFrame(data)

            # Convert to epoch
            data["epoch"] = data["timestamps_hourly"].astype(int)
            data["Date"] = pd.to_datetime(data["timestamps_hourly"].astype(int), unit="s")  # To datetime
            data.set_index("Date", inplace=True)

            return data

        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))
            sys.exit(1)
