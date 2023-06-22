from typing import Any, Dict, Optional, Union

import pandas as pd
import requests

from utils.geolocation import GeoLocation


class DataFetcher:
    def __init__(self, url: str, location: Union[str, Dict[str, float]] = None):
        """
        Initialize the DataFetcher class.
        Args:
            url (str): The URL of the server.
            location (Union[str, Dict[str, float]]): The location, either as a string (city name) or as coordinates
                (latitude and longitude).
        """
        self.url = url
        self.params = GeoLocation(location).params

    def fetch_data(self) -> Optional[Dict[str, Any]]:
        """
        Fetches the renewable potential data for the next 5 days.
        Returns:
            dict or None: The fetched data as a JSON object, or None if an error occurred.
        """
        try:
            response = requests.get(self.url, params=self.params)
            response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes
            data = response.json()
            data = pd.DataFrame(data)
            data["epoch"] = data["timestamps_hourly"]
            data["Date"] = pd.to_datetime(
                data["timestamps_hourly"], unit="s"
            )  # To datetime
            data.set_index("Date", inplace=True)
            return data
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))
            return None
