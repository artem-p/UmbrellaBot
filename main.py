from telegram.ext import Updater, CommandHandler
import logging
import requests
import datetime
from weather import Weather

from secret import TOKEN, WEATHER_API_KEY


def get_city(context):
    # Получаем город, который ввел пользователь или отдаем по умолчанию
    DEFAULT_CITY = 'Saint Petersburg, ru'

    try:
        city = context.user_data['city']
    except KeyError:
        city = DEFAULT_CITY

    return city


def current_weather(update, context):
    city = get_city(context)

    URL = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&lang=ru&units=metric&appid=' + WEATHER_API_KEY
    
    request = requests.get(URL)
    response = request.json()

    city_from_response = response['name'] + ', ' + response['sys']['country']
    timestamp = response['dt']
    temperature = response['main']['temp']
    wind_speed = response['wind']['speed']
    phenomena = response['weather'][0]['description']

    current_weather = Weather(city_from_response, timestamp, temperature, wind_speed, phenomena)

    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=current_weather.as_current_weather())


def forecast(update, context):
    city = get_city(context)
    
    URL = 'https://api.openweathermap.org/data/2.5/forecast?q=' + city + '&lang=ru&units=metric&appid=' + WEATHER_API_KEY

    request = requests.get(URL)

    response = request.json()

    city_from_response = response['city']['name'] + ', ' + response['city']['country']

    forecast_elements = response['list'][0:12]

    forecast_text = list(map(get_forecast_element, forecast_elements))

    update.message.reply_text("Прогноз погоды для " + city_from_response + '\n\n' +
                                ''.join(forecast_text))        


def get_forecast_element(forecast_element_json):
    # Получаем текст для элемента прогноза из соответствующего json
    timestamp = forecast_element_json['dt']
    temperature = forecast_element_json['main']['temp']
    wind_speed = forecast_element_json['wind']['speed']
    phenomena = forecast_element_json['weather'][0]['main']

    weather = Weather('', timestamp, temperature, wind_speed, phenomena)

    return weather.as_forecast_element()


def city(update, context):
    city = " ".join(context.args)

    if city:
        context.user_data['city'] = city

        update.message.reply_text("Я буду показывать погоду для " + city)
    else:
        update.message.reply_text("Введите город после команды, например, /city Лондон")


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    
    dispatcher.add_handler(CommandHandler('weather', current_weather))
    dispatcher.add_handler(CommandHandler('forecast', forecast))
    dispatcher.add_handler(CommandHandler('city', city))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()