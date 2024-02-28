from django.urls import path
from . import views




urlpatterns = [
    path('', views.home, name='home'),
    path('weather_now/', views.weather_now, name='weather_now'),
    path('about/', views.about, name='about'),
]
