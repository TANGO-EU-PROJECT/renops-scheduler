from utils.datafetcher import DataFetcher

url = "http://localhost:5689/forecast/renewable_potential"
lat = 14
lon = 46

fetcher = DataFetcher(url, lat, lon)
data = fetcher.fetch_data()

print(data)
