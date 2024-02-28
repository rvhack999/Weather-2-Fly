#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import datetime
# Дата и время на компьютере
date_and_time_now = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
print(date_and_time_now)

# Время сейчас
time_now = datetime.datetime.now().time().strftime('%H:%M:%S')
print(time_now)

# Дата сейчас
date_now = datetime.datetime.now().date().strftime('%d-%m-%Y')
print(date_now)

# UTC - всемирное координированное время, стандарт времени, принятый на Земле
time_utc_now = datetime.datetime.utcnow().time().strftime('%H:%M:%S')
print(time_utc_now)

# Время с учетом временной зоны
import pytz  # IANA Time Zone Database (Olson database)
# Список временных зон pytz.all_timezones или pytz.common_timezones
# Список временных зон РФ pytz.country_timezones['ru'], ISO 3166

# сейчас в Нью-Йорке (Америка)
time_zone = pytz.timezone('America/New_York')
print(datetime.datetime.now(time_zone).date().strftime('%d-%m-%Y'))
print(datetime.datetime.now(time_zone).time().strftime('%H:%M:%S'))

# сейчас в Иркутске (Россия)
time_zone = pytz.timezone('Asia/Irkutsk')
print(datetime.datetime.now(time_zone).date().strftime('%d-%m-%Y'))
print(datetime.datetime.now(time_zone).time().strftime('%H:%M:%S'))

# По названию города, определить координаты, найти часовой пояс по базе tzwhere
# https://stackoverflow.com/questions/16505501/get-timezone-from-city-in-python-django

