from functions import weather_today


class Date:
    def __init__(self, data: tuple):
        self.date = data[0].split()[0]
        self.time = data[0].split()[1]
        self.weather = data[1]



temp = Date(weather_today(52.9179381485359, 103.56901371781483, 0))
print(temp.date, temp.time)
print()
for j, k in temp.weather.items():
    print(j, k)
