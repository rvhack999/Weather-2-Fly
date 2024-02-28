from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.shortcuts import render
from .functions import get_weather
from .models import Day


def home(request):
    data = {
        'title': 'Weather-2-Fly',
    }
    return render(request, 'main/main.html', data)


def weather_now(request):
    data = {
        'title': 'Weather-now',
    }
    if request.POST:
        latitude = request.POST.get("lat", "Undefined")
        longitude = request.POST.get("lon", "Undefined")
        weather_data = get_weather(latitude=latitude, longitude=longitude, days=1)
        for date_time in weather_data.keys():
            weather = Day()
            weather.date = date_time.split()[0]
            weather.time = date_time.split()[1]
            weather.temperature_2m = weather_data[date_time][0]
            weather.temperature_120m = weather_data[date_time][1]
            weather.relative_humidity_2m = weather_data[date_time][2]
            weather.precipitation_probability = weather_data[date_time][3]
            weather.visibility = weather_data[date_time][4]
            weather.wind_speed_10m = weather_data[date_time][5]
            weather.wind_direction_10m = weather_data[date_time][6]
            weather.wind_gusts_10m = weather_data[date_time][7]
            weather.wind_speed_120m = weather_data[date_time][8]
            weather.wind_direction_120m = weather_data[date_time][9]
            weather.save()
            # print(weather.time, weather_data[date_time])

    return render(request, 'main/weather_now.html', data)


def weather_7days(request):
    data = {
        'title': 'Weather-7-days',

    }
    return render(request, 'main/weather_7days.html', data)


def about(request):
    return render(request, 'main/about.html')


def page_not_found(request, exception):
    return HttpResponseNotFound(
        '<h1 style="color: red; text-align: center; margin: 0 auto;"> Нет такой страницы! </h1>')
