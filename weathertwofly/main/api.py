import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import numpy as np
import json

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 52.8884,
    "longitude": 103.4904,
    "current": ["temperature_2m", "relative_humidity_2m", "rain", "showers", "snowfall", "wind_speed_10m",
                "wind_direction_10m", "wind_gusts_10m"],
    "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "rain", "snowfall", "visibility",
               "wind_speed_10m", "wind_speed_120m", "wind_direction_10m", "wind_direction_120m", "wind_gusts_10m",
               "temperature_120m"],
    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_hours", "wind_speed_10m_max",
              "wind_gusts_10m_max", "wind_direction_10m_dominant"],
    "timezone": "auto"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
# print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
# print(f"Elevation {response.Elevation()} m asl")
# print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
# print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_relative_humidity_2m = current.Variables(1).Value()
current_rain = current.Variables(2).Value()
current_showers = current.Variables(3).Value()
current_snowfall = current.Variables(4).Value()
current_wind_speed_10m = current.Variables(5).Value()
current_wind_direction_10m = current.Variables(6).Value()
current_wind_gusts_10m = current.Variables(7).Value()

# print(f"Current time {current.Time()}")
# print(f"Current temperature_2m {current_temperature_2m}")
# print(f"Current relative_humidity_2m {current_relative_humidity_2m}")
# print(f"Current rain {current_rain}")
# print(f"Current showers {current_showers}")
# print(f"Current snowfall {current_snowfall}")
# print(f"Current wind_speed_10m {current_wind_speed_10m}")
# print(f"Current wind_direction_10m {current_wind_direction_10m}")
# print(f"Current wind_gusts_10m {current_wind_gusts_10m}")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
hourly_rain = hourly.Variables(3).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(4).ValuesAsNumpy()
hourly_visibility = hourly.Variables(5).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(6).ValuesAsNumpy()
hourly_wind_speed_120m = hourly.Variables(7).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(8).ValuesAsNumpy()
hourly_wind_direction_120m = hourly.Variables(9).ValuesAsNumpy()
hourly_wind_gusts_10m = hourly.Variables(10).ValuesAsNumpy()
hourly_temperature_120m = hourly.Variables(11).ValuesAsNumpy()

# print(hourly_temperature_2m)


hourly_data = {"date": pd.date_range(
    start=pd.to_datetime(hourly.Time(), unit="s"),
    end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
    freq=pd.Timedelta(seconds=hourly.Interval()),
    inclusive="left"
)}
hourly_data1 = pd.date_range(start=pd.to_datetime(hourly.Time(), unit='s'),
                             end=pd.to_datetime(hourly.TimeEnd(), unit='s'),
                             freq=pd.Timedelta(seconds=hourly.Interval()),
                             inclusive='left')
date_list = [str(i) for i in hourly_data1]

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["rain"] = hourly_rain
hourly_data["snowfall"] = hourly_snowfall
hourly_data["visibility"] = hourly_visibility
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["wind_speed_120m"] = hourly_wind_speed_120m
hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
hourly_data["wind_direction_120m"] = hourly_wind_direction_120m
hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
hourly_data["temperature_120m"] = hourly_temperature_120m

hourly_dataframe = pd.DataFrame(data=hourly_data)

print({date: params for date, params in zip(date_list, zip(
                                                            hourly_data["temperature_2m"],
                                                            hourly_data["relative_humidity_2m"],
                                                            hourly_data["precipitation_probability"],
                                                            hourly_data["rain"],
                                                            hourly_data["snowfall"],
                                                            hourly_data["visibility"],
                                                            hourly_data["wind_speed_10m"],
                                                            hourly_data["wind_speed_120m"],
                                                            hourly_data["wind_direction_10m"],
                                                            hourly_data["wind_direction_120m"],
                                                            hourly_data["wind_gusts_10m"],
                                                            hourly_data["temperature_120m"],
                                                           )
                                            )
       }
      )

# print(hourly_data['temperature_2m'])
