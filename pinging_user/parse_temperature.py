import requests
from bs4 import BeautifulSoup
<<<<<<< Updated upstream

requestedPage = requests.get('http://192.168.1.104')

code = requestedPage.text

parsed_html = BeautifulSoup(code, "html.parser")
temperature = parsed_html.body.find('p', attrs={'class':'temp'}).text
humidity = parsed_html.body.find('p', attrs={'class':'hum'}).text

print(temperature, humidity)
=======
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

def parse_measurements(temp = True):
    requestedPage = requests.get('http://192.168.1.104')

    code = requestedPage.text

    parsed_html = BeautifulSoup(code, "html.parser")
    temperature = parsed_html.body.find('p', attrs={'class':'temp'}).text
    humidity = parsed_html.body.find('p', attrs={'class':'hum'}).text
    if (temp):
        return temperature
    else:
        return humidity

def start_telegram(update: Update, context: CallbackContext):
    update.message.reply_text("Welecome in WEATHER-MISTYFIKACJA, say: '/help' for help")

def help_telegram(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /temperature - to get temperature from sensor
    /humidity - to get humidity from sensor""")

def temperature_url_telegram(update: Update, context: CallbackContext):
    update.message.reply_text(f"Temperature: {parse_measurements()}")

def humidity_url_telegram(update: Update, context: CallbackContext):
    update.message.reply_text(f"Humidity: {parse_measurements(False)}")

def unknown_telegram(update: Update, context: CallbackContext):
    update.message.reply_text(f"Sorry {update.message.text} is not a valid command")

def unknown_text_telegram(update: Update, context: CallbackContext):
    update.message.reply_text(f"Sorry I can't recognize you , you said {update.message.text}")

def init_telegram_bot():
    updater = Updater("5384206076:AAHR9X-IZXfGE46Er1w1-0MoK3HIUfKIxAk", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start_telegram))
    updater.dispatcher.add_handler(CommandHandler('help', help_telegram))
    updater.dispatcher.add_handler(CommandHandler('temperature', temperature_url_telegram))
    updater.dispatcher.add_handler(CommandHandler('humidity', humidity_url_telegram))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_telegram))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown_telegram))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text_telegram))
    
    updater.start_polling()
>>>>>>> Stashed changes
