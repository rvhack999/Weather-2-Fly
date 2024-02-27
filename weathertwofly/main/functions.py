import datetime as dt
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


def get_weather(latitude, longitude) -> dict:
    """ Функция для получения подробных данных погоды на 7 дней"""

    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "rain", "showers", "snowfall", "wind_speed_10m",
                    "wind_direction_10m", "wind_gusts_10m"],
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation_probability", "rain", "snowfall",
                   "visibility",
                   "wind_speed_10m", "wind_speed_120m", "wind_direction_10m", "wind_direction_120m", "wind_gusts_10m",
                   "temperature_120m"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_hours", "wind_speed_10m_max",
                  "wind_gusts_10m_max", "wind_direction_10m_dominant"],
        "timezone": "GMT"
    }

    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    """ Данные на 7 дней """
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
    hourly_visibility = [x / 1000 for x in hourly.Variables(5).ValuesAsNumpy()]
    hourly_wind_speed_10m = hourly.Variables(6).ValuesAsNumpy()
    hourly_wind_speed_120m = hourly.Variables(7).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(8).ValuesAsNumpy()
    hourly_wind_direction_120m = hourly.Variables(9).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(10).ValuesAsNumpy()
    hourly_temperature_120m = hourly.Variables(11).ValuesAsNumpy()

    hourly_data1 = pd.date_range(start=pd.to_datetime(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                 end=pd.to_datetime(hourly.TimeEnd(), unit='s'),
                                 freq=pd.Timedelta(seconds=hourly.Interval()),
                                 inclusive='left')
    date_list = [str(x) for x in hourly_data1]
    del_elem = (len(hourly_temperature_2m) - len(date_list))
    holy_data = {date: param for date, param in zip(date_list, zip(
        hourly_temperature_2m[del_elem:],
        hourly_temperature_120m[del_elem:],
        hourly_relative_humidity_2m[del_elem:],
        hourly_precipitation_probability[del_elem:],
        hourly_visibility[del_elem:],
        hourly_wind_speed_10m[del_elem:],
        hourly_wind_direction_10m[del_elem:],
        hourly_wind_gusts_10m[del_elem:],
        hourly_wind_speed_120m[del_elem:],
        hourly_wind_direction_120m[del_elem:],
    ))}
    return holy_data


def weather_today(lat, lon, ind=0):
    """ Функция для формирования подписей к параметрам по индексу дня (0-6)"""

    data = get_weather(latitude=lat, longitude=lon)
    day_now = list(data.keys())[ind]
    content_now = list(data[day_now])
    content_now_keys = [
        f'Температура над поверхностью земли ({chr(176)}С): ',
        f'Температура на высоте 120 м ({chr(176)}С): ',
        'Влажность (%): ',
        'Вероятность осадков (%): ',
        'Видимость (км): ',
        'Скорость ветра на высоте 10 м (м/с): ',
        'Направление ветра на высоте 10 м (град): ',
        'Порывы ветра (м/с): ',
        'Скорость ветра на высоте 120 м (м/с): ',
        'Направление ветра на высоте 120 м (град): ',
    ]
    out = {key: value for key, value in zip(content_now_keys, content_now)}
    return day_now, out

# for i in (weather_today(52.9179381485359, 103.56901371781483, 0)):
#     print(i)
# a = (get_weather(52.9179381485359, 103.56901371781483))
# for y in a.keys():
#     print(y)
# print(len(a.keys()))
# print(weather_today(52.9179381485359, 103.56901371781483, 0))
