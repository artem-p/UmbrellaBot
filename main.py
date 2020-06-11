from telegram.ext import Updater, CommandHandler
import requests

from secret import TOKEN, WEATHER_API_KEY


def weather(update, context):
    CITY = 'Saint Petersburg, ru'
    URL = 'https://api.openweathermap.org/data/2.5/weather?q=' + CITY + '&lang=ru&appid=' + WEATHER_API_KEY
    
    request = requests.get(URL)

    response = request.json()

    city_name = response['name'] + ', ' + response['sys']['country']

    temperature = response['main']['temp'] - 273.15

    wind = response['wind']['speed']

    temperature_output = '{:.0f}'.format(temperature) + '° C'
    wind_output = str(wind) + ' м/с'

    message = 'Погода в ' + city_name + ':\n' + 'Температура ' + temperature_output + '\n' + 'Ветер ' + wind_output

    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=message)

    


def hello(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text='Привет')


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('hello', hello))
    dispatcher.add_handler(CommandHandler('weather', weather))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()