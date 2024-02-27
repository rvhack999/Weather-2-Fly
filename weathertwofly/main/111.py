# from functions import weather_today

#
# def best_time(data: dict):
#     perfect_index = []
#     t1 = data[f'Температура над поверхностью земли ({chr(176)}С): ']
#     t2 = data[f'Температура на высоте 120 м ({chr(176)}С): ']
#     d = data['Видимость (км): ']
#     v1 = data['Скорость ветра на высоте 10 м (м/с): ']
#     v2 = data['Скорость ветра на высоте 120 м (м/с): ']
#
#     def t_ind(t):
#         if -10 <= t:
#             return 1
#
#         elif -15 <= t < -10:
#             return 0.75
#
#         elif -20 <= t < -15:
#             return 0.5
#
#         else:
#             return 0
#
#     def d_ind(d):
#         if 2 <= d:
#             return 1
#
#         elif 1 <= d < 2:
#             return 0.75
#
#         elif 0.5 <= d < 1:
#             return 0.5
#
#         else:
#             return 0
#
#     def v_ind(v):
#         if 3.6 > v:
#             return 1
#
#         elif 10.8 >= v > 3.6:
#             return 0.75
#
#         elif 18 >= v > 10.8:
#             return 0.5
#
#         else:
#             return 0
#
#     perfect_index.append(t_ind(t1))
#     perfect_index.append(t_ind(t2))
#     perfect_index.append(d_ind(d))
#     perfect_index.append(v_ind(v1))
#     perfect_index.append(v_ind(v2))
#
#     print(perfect_index)
#

# dat = weather_today(52.9179381485359, 103.56901371781483)
#
# print(dat)
# best_time(dat[1])
#
# for i in range(50):
#     best_time(weather_today(52.9179381485359, 103.56901371781483, i)[1])

test_class_dict = {'2024-02-02 18:00:00': (-21, -23, 56, 0.01, 2.45, 2, 143.76, 5, 4, 321.55)}


class WeatherNow:
    def __init__(self, *args):
        self.temperature_2m = args[0]
        self.temperature_120m = args[1]
        self.relative_humidity_2m = args[2]
        self.precipitation_probability = args[3]
        self.visibility = args[4]
        self.wind_speed_10m = args[5]
        self.wind_direction_10m = args[6]
        self.wind_gusts_10m = args[7]
        self.wind_speed_120m = args[8]
        self.wind_direction_120m = args[9]


# a = WeatherNow(*test_class_dict['2024-02-02 18:00:00'])
#
# print(a.visibility)


def best(t1, t2, d, v1, v2):
    list_best_par = {
        1: (-10, 2, 3.6),
        0.75: (-15, 1, 10.8),
        0.5: (-20, 0.5, 18),
    }
    for i, j in list_best_par.items():
        for k in j:
            pass

