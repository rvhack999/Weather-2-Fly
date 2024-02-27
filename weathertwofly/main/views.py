from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render
from .functions import weather_today
from .models import Day
from . import forms



# Create your views here.
# def index(request):
#     if request.method == 'POST':
#         form = forms.RequestCords(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#     else:
#         form = forms.RequestCords()
#
#     data = {
#         'title': 'Weather-2-Fly',
#         'form': form
#     }
#     return render(request, 'main/main.html', data)

def home(request):
    data = {
        'title': 'Weather-2-Fly',

    }
    update = weather_today(52.9179381485359, 103.56901371781483, 0)
    b = [i for i in update[1].values()]
    a = Day
    a.date = update[0].split()[0]
    a.time = update[0].split()[1]
    a.temperature_2m = b[0]
    a.temperature_120m = b[1]
    a.relative_humidity_2m = b[2]
    a.precipitation_probability = b[3]
    a.visibility = b[4]
    a.wind_speed_10m = b[5]
    a.wind_direction_10m = b[6]
    a.wind_gusts_10m = b[7]
    a.wind_speed_120m = b[8]
    a.wind_direction_120m = b[9]
    a.save()


    return render(request, 'main/main.html', data)


def weather_now(request):

    data = {
        'title': 'Weather-now',

    }
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
