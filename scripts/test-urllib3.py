# import 2 prebuilt packages

import urllib3
import rich

# call the zippopotam api to know latitude and longitude of a zip code.
response = urllib3.request(
    "GET",
    "https://api.zippopotam.us/us/94530"
)
result = response.json()
rich.print(result)
latitude = result['places'][0]['latitude']
longitude = result['places'][0]['longitude']
print(latitude, longitude)

# now call the sunset api
response = urllib3.request(
    "GET",
    f"https://api.sunrisesunset.io/json?lat={latitude}&lng={longitude}&timezone=UTC&date=today"
)
rich.print(response.json())
