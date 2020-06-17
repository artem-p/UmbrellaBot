import datetime


class Weather():
    def __init__(self, city, timestamp, temperature, wind_speed, phenomena):
        super().__init__()
        self.city = city
        self.timestamp = timestamp
        self.temperature = temperature
        self.wind_speed = wind_speed
        self.phenomena = phenomena

    def as_current_weather(self):
        # Представление для текущей погоды
        return  'Погода в ' + self.city + ':\n\n' + 'Температура ' + self.__formatted_temperature() + '\n' + 'Ветер ' + self.__formatted_wind_speed() + '\n' + self.phenomena.capitalize()

    def as_forecast_element(self):
        # Представление для элемента прогноза
        time = datetime.datetime.fromtimestamp(self.timestamp).strftime("%H:%M")

        return time + '\n' + self.__formatted_temperature() + '\n' + self.__formatted_wind_speed() + '\n\n'


    def __formatted_temperature(self):
        # Округляем температуру до целых и добавляем градусы Цельсия
        return '{:.0f}'.format(self.temperature) + ' °C'

    def __formatted_wind_speed(self):
        # Скорость ветра до целых + м/с
        return '{:.0f}'.format(self.wind_speed) + ' м/с'
