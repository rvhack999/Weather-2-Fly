from django.db import models


# Create your models here.
class Day(models.Model):
    date = models.TextField(max_length=30, help_text='Дата')
    time = models.TextField(max_length=30, help_text='Время')
    temperature_2m = models.CharField(max_length=10, help_text='Температура на 2м')
    temperature_120m = models.CharField(max_length=10, help_text='Температура на 120м')
    relative_humidity_2m = models.CharField(max_length=10, help_text='Влажность')
    precipitation_probability = models.CharField(max_length=10, help_text='Вероятность осадков')
    visibility = models.CharField(max_length=10, help_text='Видимость')
    wind_speed_10m = models.CharField(max_length=10, help_text='Скорость ветра на 10м')
    wind_speed_120m = models.CharField(max_length=10, help_text='Скорость ветра на 120м')
    wind_gusts_10m = models.CharField(max_length=10, help_text='Порывы ветра на 10м')
    wind_direction_10m = models.CharField(max_length=10, help_text='Направление ветра на 10м')
    wind_direction_120m = models.CharField(max_length=10, help_text='Направление ветра на 120м')
