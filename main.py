from telegram.ext import Updater, CommandHandler
import requests

from secret import TOKEN, WEATHER_API_KEY


def weather(update, context):
    DEFAULT_CITY = 'Saint Petersburg, ru'

    try:
        city = context.user_data['city']
    except KeyError:
        city = DEFAULT_CITY

    URL = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&lang=ru&appid=' + WEATHER_API_KEY
    
    request = requests.get(URL)

    response = request.json()

    city_name = response['name'] + ', ' + response['sys']['country']

    temperature = response['main']['temp'] - 273.15
    wind = response['wind']['speed']
    weather = response['weather'][0]['description']

    temperature_output = '{:.0f}'.format(temperature) + '° C'
    wind_output = str(wind) + ' м/с'

    message = 'Погода в ' + city_name + ':\n\n' + 'Температура ' + temperature_output + '\n' + 'Ветер ' + wind_output + '\n' + weather.capitalize()

    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=message)

    


def hello(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text='Привет')


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
    
    dispatcher.add_handler(CommandHandler('hello', hello))
    dispatcher.add_handler(CommandHandler('weather', weather))
    dispatcher.add_handler(CommandHandler('city', city))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()