from telegram.ext import Updater, CommandHandler

from secret import TOKEN


def hello(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text='Привет')


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('hello', hello))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()