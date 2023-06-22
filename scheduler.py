from datetime import datetime, timedelta

import pandas as pd

from utils.datafetcher import DataFetcher

url = "http://localhost:5689/forecast/renewable_potential"
lat = 14
lon = 46
runtime_hours = 2
deadline_hours = 48
location = {"lat": 40.7128, "lon": -74.0060}
fetcher = DataFetcher(url, "Ljubljana")
data = fetcher.fetch_data()
# data.date = pd.to_datetime(data.index, unit='s')

res = data.resample(str(runtime_hours) + "H").mean()
res = res.renewable_potential_forecast_hourly.sort_values(ascending=False)

current_date = pd.Timestamp(datetime.now())
deadline_date = pd.Timestamp(datetime.now() + timedelta(hours=deadline_hours))
filtered_res = res[(res.index > current_date) & (res.index < deadline_date)]

for i in range(10):
    print(
        "Optimal time between ",
        filtered_res.index[i],
        "and",
        filtered_res.index[i] + timedelta(hours=runtime_hours),
    )
