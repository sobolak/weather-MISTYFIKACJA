import requests
from bs4 import BeautifulSoup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import mysql.connector
from datetime import date, datetime

def parse_measurements():
    requestedPage = requests.get('http://192.168.1.105')

    code = requestedPage.text

    parsed_html = BeautifulSoup(code, "html.parser")
    temperature = parsed_html.body.find('p', attrs={'class':'temp'}).text
    humidity = parsed_html.body.find('p', attrs={'class':'hum'}).text
    return [temperature, humidity]

def update_database():
    meas_results = parse_measurements()
    db_insert_esp(meas_results[0], meas_results[1], date.today(), datetime.now().hour)

def start_telegram(update: Update, context: CallbackContext):
    update.message.reply_text("Welecome in WEATHER-MISTYFIKACJA, say: '/help' for help")

def help_telegram(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /measurements - both measurements from sensor
    /temperature - to get temperature from sensor
    /humidity - to get humidity from sensor
    /interia - actual interia weather
    /avenue - actual avenue weather
    /weatherChannel - actual weatherChannel weather
    /onet - actual onet weather
    /wp - actual wp weather
    /metroprog - actual metroprog weather
    /forecast - forecast from model""")

def measurements_telegram(update: Update, context: CallbackContext):
    update.message.reply_text(f"Temperature: {parse_measurements()[0]}\nHumidity: {parse_measurements()[1]}")

def temperature_telegram(update: Update, context: CallbackContext):
    update.message.reply_text(f"Temperature: {parse_measurements()[0]}")

def humidity_telegram(update: Update, context: CallbackContext):
    update.message.reply_text(f"Humidity: {parse_measurements()[1]}")

def unknown_telegram(update: Update, context: CallbackContext):
    update.message.reply_text(f"Sorry {update.message.text} is not a valid command")

def unknown_text_telegram(update: Update, context: CallbackContext):
    update.message.reply_text(f"Sorry I can't recognize you , you said {update.message.text}")

def init_telegram_bot():
    updater = Updater("5384206076:AAHR9X-IZXfGE46Er1w1-0MoK3HIUfKIxAk", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start_telegram))
    updater.dispatcher.add_handler(CommandHandler('help', help_telegram))
    updater.dispatcher.add_handler(CommandHandler('measurements', measurements_telegram))
    updater.dispatcher.add_handler(CommandHandler('temperature', temperature_telegram))
    updater.dispatcher.add_handler(CommandHandler('humidity', humidity_telegram))
    updater.dispatcher.add_handler(CommandHandler('interia', interia_weather_telegram))
    updater.dispatcher.add_handler(CommandHandler('avenue', avenue_weather_telegram))
    updater.dispatcher.add_handler(CommandHandler('weatherChannel', weatherChannel_weather_telegram))
    updater.dispatcher.add_handler(CommandHandler('onet', onet_weather_telegram))
    updater.dispatcher.add_handler(CommandHandler('wp', wp_weather_telegram))
    updater.dispatcher.add_handler(CommandHandler('metroprog', metroprog_weather_telegram))
    updater.dispatcher.add_handler(CommandHandler('forecast', forecast_weather_telegram))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_telegram))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown_telegram))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text_telegram))
    
    updater.start_polling()

def db_insert_esp(temperature, humidity, weather_time, hour):
    try:
        connection = mysql.connector.connect(host='sql10.freemysqlhosting.net',
                                         database='sql10489794',
                                         user='sql10489794',
                                         password='IPELfw5A2X',
                                         auth_plugin='mysql_native_password')
        cursor = connection.cursor()
        query = "INSERT INTO esp (temperature,humidity,weather_time,hour) VALUES(%s,%s,%s,%s)"
        record  = (temperature, humidity, weather_time, hour)
        cursor.execute(query, record)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def db_get_data(table, limit_ctr = 1, date_name = "weather_time"):
    try:
        connection = mysql.connector.connect(host='sql10.freemysqlhosting.net',
                                         database='sql10489794',
                                         user='sql10489794',
                                         password='IPELfw5A2X',
                                         auth_plugin='mysql_native_password')
        cursor = connection.cursor()
        query = f"SELECT * FROM {table} WHERE {date_name} = '{date.today()}' AND hour = {datetime.now().hour} LIMIT {limit_ctr}" # BETWEEN {datetime.now().hour} AND {datetime.now().hour + 4}
        cursor.execute(query)
        # connection.commit()

    except mysql.connector.Error as error:
        print("Failed to get data from MySQL table {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        return cursor.fetchall()

def interia_weather_telegram(update: Update, context: CallbackContext):
    interia_weather_results = db_get_data("interia")[0]
    update.message.reply_text(
        f"""
        Time: {interia_weather_results[7]} {interia_weather_results[8]}h\n
        Temperature: {interia_weather_results[1]}\n
        Humidity: {interia_weather_results[3]}\n
        Wind: {interia_weather_results[2]}\n
        Rain: {interia_weather_results[4]}\n
        Cloudiness: {interia_weather_results[5]}\n"""
        )

def interia_weather_telegram(update: Update, context: CallbackContext):
    interia_weather_results = db_get_data("interia")[0]
    update.message.reply_text(
        f"""
        Time: {interia_weather_results[7]} {interia_weather_results[8]}h\n
        Temperature: {interia_weather_results[1]}\n
        Humidity: {interia_weather_results[3]}\n
        Wind: {interia_weather_results[2]}\n
        Rain: {interia_weather_results[4]}\n
        Cloudiness: {interia_weather_results[5]}\n"""
        )

def avenue_weather_telegram(update: Update, context: CallbackContext):
    avenue_weather_results = db_get_data("avenue")[0]
    update.message.reply_text(
        f"""
        Time: {avenue_weather_results[7]} {avenue_weather_results[8]}h\n
        Temperature: {avenue_weather_results[1]}\n
        Humidity: {avenue_weather_results[3]}\n
        Wind: {avenue_weather_results[2]}\n
        Rain: {avenue_weather_results[4]}\n
        Cloudiness: {avenue_weather_results[5]}\n"""
        )

def weatherChannel_weather_telegram(update: Update, context: CallbackContext):
    weatherChannel_weather_results = db_get_data("weatherChannel")[0]
    update.message.reply_text(
        f"""
        Time: {weatherChannel_weather_results[7]} {weatherChannel_weather_results[8]}h\n
        Temperature: {weatherChannel_weather_results[1]}\n
        Humidity: {weatherChannel_weather_results[3]}\n
        Wind: {weatherChannel_weather_results[2]}\n
        Rain: {weatherChannel_weather_results[4]}\n
        Cloudiness: {weatherChannel_weather_results[5]}\n"""
        )

def onet_weather_telegram(update: Update, context: CallbackContext):
    onet_weather_results = db_get_data("onet")[0]
    update.message.reply_text(
        f"""
        Time: {onet_weather_results[7]} {onet_weather_results[8]}h\n
        Temperature: {onet_weather_results[1]}\n
        Humidity: {onet_weather_results[3]}\n
        Wind: {onet_weather_results[2]}\n
        Rain: {onet_weather_results[4]}\n
        Cloudiness: {onet_weather_results[5]}\n"""
        )

def wp_weather_telegram(update: Update, context: CallbackContext):
    wp_weather_results = db_get_data("wp")[0]
    update.message.reply_text(
        f"""
        Time: {wp_weather_results[7]} {wp_weather_results[8]}h\n
        Temperature: {wp_weather_results[1]}\n
        Humidity: {wp_weather_results[3]}\n
        Wind: {wp_weather_results[2]}\n
        Rain: {wp_weather_results[4]}\n
        Cloudiness: {wp_weather_results[5]}\n"""
        )

def metroprog_weather_telegram(update: Update, context: CallbackContext):
    metroprog_weather_results = db_get_data("metroprog")
    update.message.reply_text(
        f"""
        Time: {metroprog_weather_results[7]} {metroprog_weather_results[8]}h\n
        Temperature: {metroprog_weather_results[1]}\n
        Humidity: {metroprog_weather_results[3]}\n
        Wind: {metroprog_weather_results[2]}\n
        Rain: {metroprog_weather_results[4]}\n
        Cloudiness: {metroprog_weather_results[5]}\n"""
        )

def forecast_weather_telegram(update: Update, context: CallbackContext):
    forecast_weather_results = db_get_data("forecast", 4, "date")
    print(forecast_weather_results)
    reply_string = f"""
    Time: {forecast_weather_results[1]} {forecast_weather_results[2]}h\n
    Temperature: {forecast_weather_results[3]}\n
    Humidity: {forecast_weather_results[4]}\n
    Conditions: {forecast_weather_results[5]}\n"""
    update.message.reply_text(reply_string)