from typing import Any, Dict, Optional, Tuple, Union

import pandas as pd
import requests


class DataFetcher:
    def __init__(self, url: str, location: Union[str, Dict[str, float]]):
        """
        Initialize the DataFetcher class.
        Args:
            url (str): The URL of the server.
            location (Union[str, Dict[str, float]]): The location, either as a string (city name) or as coordinates
                (latitude and longitude).
        """
        self.url = url
        self.params = self._get_location_params(location)

    def _get_location_params(
        self, location: Union[str, Dict[str, float]]
    ) -> Dict[str, Any]:
        """
        Returns the parameters based on the provided location (city name or coordinates).
        Args:
            location (Union[str, Dict[str, float]]): The location, either as a string (city name) or as coordinates
                (latitude and longitude).
        Returns:
            dict: The parameters for the request.
        """
        if isinstance(location, str):
            lat, lon = self._geocode_location(location)
        elif isinstance(location, dict) and "lat" in location and "lon" in location:
            lat, lon = location["lat"], location["lon"]
        else:
            raise ValueError("Invalid location format")
        return {"lat": lat, "lon": lon}

    def _geocode_location(self, location: str) -> Tuple[float, float]:
        """
        Geocodes the provided location (city name) to obtain latitude and longitude.
        Args:
            location (str): The location (city name) to geocode.
        Returns:
            tuple: The latitude and longitude values.
        """
        response = requests.get(
            f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
        )
        # Check if the API request was successful
        if response.status_code == 200:
            data = response.json()
            # Check if the settlement was found
            if len(data) > 0:
                # Extract the latitude and longitude from the API response
                lat = data[0]["lat"]
                lng = data[0]["lon"]
                return lat, lng
            else:
                print(f'Settlement "{location}" not found.')
                return None, None
        else:
            print(f"API request failed with status code {response.status_code}.")
            return None, None

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
            data["Date"] = pd.to_datetime(data["timestamps_hourly"])  # To datetime
            data.set_index("Date", inplace=True)
            return data["renewable_potential_forecast_hourly"]
        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))
            return None
