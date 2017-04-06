import telegram #telegram bot API
from config import TOKEN
from telegram.ext import Updater

bot=telegram.Bot(token=TOKEN)
updater=Updater(token=TOKEN)
dispatcher=updater.dispatcher

from func_parser import handlers, error_callback

for handler in handlers:
    dispatcher.add_handler(handler)
dispatcher.add_error_handler(error_callback)
