import datetime as dt
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

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


def get_weather(latitude, longitude, days) -> dict:
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
                   "wind_speed_10m", "wind_speed_120m", "wind_direction_10m", "wind_direction_120m",
                   "wind_gusts_10m",
                   "temperature_120m"],
        "forecast_days": 7,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_hours", "wind_speed_10m_max",
                  "wind_gusts_10m_max", "wind_direction_10m_dominant"],
        "timezone": "auto"
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

    hourly_data1 = pd.date_range(start=pd.to_datetime(dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')),
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

    now_dates = [i for i in holy_data.keys()][:25]
    now_data = {i: holy_data[i] for i in holy_data.keys() if i in now_dates}
    if days == 1:
        return now_data
    elif days == 7:
        return holy_data
    else:
        return {}


if __name__ == '__main__':
    print(get_weather(52.8884, 103.4904, 1))
