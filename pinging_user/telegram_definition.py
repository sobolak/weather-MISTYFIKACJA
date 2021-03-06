import requests
from bs4 import BeautifulSoup
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import mysql.connector
from datetime import date, datetime, timedelta
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import ParseMode

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
    /forecast - forecast from model
    /mail - send mail to adress list""")

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
    updater.dispatcher.add_handler(CommandHandler('mail', send_email))
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

def db_get_data(table, forecast = False, mail = False):
    try:
        connection = mysql.connector.connect(host='sql10.freemysqlhosting.net',
                                         database='sql10489794',
                                         user='sql10489794',
                                         password='IPELfw5A2X',
                                         auth_plugin='mysql_native_password')
        cursor = connection.cursor()
        actual_hour = datetime.now().hour
        today = date.today()
        if not forecast:
            query = f"SELECT * FROM {table} WHERE weather_time = '{today}' AND hour = {actual_hour}"
        else:
            if mail:
                date_name = "weather_time" 
                order = ""
            else:
                date_name = "date"
                order = "ORDER BY id DESC"
            if actual_hour < 21:
                query = f"SELECT * FROM {table} WHERE {date_name} = '{today}' AND hour BETWEEN {actual_hour} AND {actual_hour + 3} {order}"
            else:
                next_day = (datetime.today() + timedelta(days=1)).today().date()
                query = f"""SELECT * FROM {table} WHERE ({date_name} = '{today}' AND hour BETWEEN {actual_hour} AND {23}) OR 
                                                        ({date_name} = '{next_day}' AND hour BETWEEN {0} AND {actual_hour + 3 % 24})"""
                print("3")
        cursor.execute(query)

    except mysql.connector.Error as error:
        print("Failed to get data from MySQL table {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
        return cursor.fetchall()

def db_get_email():
    try:
        connection = mysql.connector.connect(host='sql10.freemysqlhosting.net',
                                         database='sql10489794',
                                         user='sql10489794',
                                         password='IPELfw5A2X',
                                         auth_plugin='mysql_native_password')
        cursor = connection.cursor()
        query = f"SELECT mail FROM mails"
        cursor.execute(query)

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
    metroprog_weather_results = db_get_data("metroprog")[0]
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
    forecast_weather_results = db_get_data("forecast", True)
    reply_string = f"""
|             Time           | Temp. | Humidity |      Conditions     |
|---------------------------|----------|----------------|-------------------------|
| {forecast_weather_results[0][1]} {forecast_weather_results[0][2]}:00 |    {forecast_weather_results[0][3]}     |        {forecast_weather_results[0][4]}       | {forecast_weather_results[0][5]} |
| {forecast_weather_results[1][1]} {forecast_weather_results[1][2]}:00 |    {forecast_weather_results[1][3]}     |        {forecast_weather_results[1][4]}       | {forecast_weather_results[1][5]} |
| {forecast_weather_results[2][1]} {forecast_weather_results[2][2]}:00 |    {forecast_weather_results[2][3]}     |        {forecast_weather_results[2][4]}       |           {forecast_weather_results[2][5]}          |
| {forecast_weather_results[3][1]} {forecast_weather_results[3][2]}:00 |    {forecast_weather_results[3][3]}     |        {forecast_weather_results[3][4]}       |           {forecast_weather_results[3][5]}          |
    """
    
    update.message.reply_text(reply_string, parse_mode = ParseMode.MARKDOWN)

def send_email(update: Update, context: CallbackContext):
    sender_email = "projektflask@gmail.com"
    receiver_email = db_get_email()

    interia_weather_results = db_get_data("interia", True, True)
    avenue_weather_results = db_get_data("avenue", True, True)

    message = MIMEMultipart("alternative")
    message["Subject"] = f"WEATHER-mistyfikacja - informacja {date.today()} godzina: {datetime.now().hour}"
    message["From"] = sender_email
    for mail in receiver_email:
        message["To"] = mail[0]

        html = f"""
        <html>
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Rubik:wght@300;400;500;600;700;800&family=Ubuntu:wght@400;500;700&display=swap" rel="stylesheet">
            <style>
            body{{
                background-color: rgb(54, 54, 73);
            }}

            *{{
                font-family: 'Roboto';
            }}

            .table tr th,td{{
                padding: 0 2rem;
            }}

            .table {{
                border-radius: 20px;
                padding: 1rem;
                background-color: rgb(85, 85, 116);
                color: rgb(212, 212, 212);
            }}

            a{{
                text-decoration: none;
                color: rgb(197, 197, 197);
            }}

            a:hover{{
                color: black;
            }}
            </style>
        </head>
        <body>
            <h2><a href="https://pogoda.interia.pl/prognoza-szczegolowa-krakow,cId,4970">Interia:</a></h2>
            <table  class="table">
                <tr>
                    <th>Time</th>
                    <th>Temperature</th>
                    <th>Wind</th>
                    <th>Humidity</th>
                    <th>Rain</th>
                    <th>Cloudiness</th>
                </tr>
                <tr>
                    <td>{interia_weather_results[0][7]} {interia_weather_results[0][8]}h</td>
                    <td>{interia_weather_results[0][1]}</td>
                    <td>{interia_weather_results[0][2]}</td>
                    <td>{interia_weather_results[0][3]}</td>
                    <td>{interia_weather_results[0][4]}</td>
                    <td>{interia_weather_results[0][5]}</td>
                </tr>
                <tr>
                    <td>{interia_weather_results[1][7]} {interia_weather_results[1][8]}h</td>
                    <td>{interia_weather_results[1][1]}</td>
                    <td>{interia_weather_results[1][2]}</td>
                    <td>{interia_weather_results[1][3]}</td>
                    <td>{interia_weather_results[1][4]}</td>
                    <td>{interia_weather_results[1][5]}</td>
                </tr>
                <tr>
                    <td>{interia_weather_results[2][7]} {interia_weather_results[2][8]}h</td>
                    <td>{interia_weather_results[2][1]}</td>
                    <td>{interia_weather_results[2][2]}</td>
                    <td>{interia_weather_results[2][3]}</td>
                    <td>{interia_weather_results[2][4]}</td>
                    <td>{interia_weather_results[2][5]}</td>
                </tr>
                <tr>
                    <td>{interia_weather_results[3][7]} {interia_weather_results[3][8]}h</td>
                    <td>{interia_weather_results[3][1]}</td>
                    <td>{interia_weather_results[3][2]}</td>
                    <td>{interia_weather_results[3][3]}</td>
                    <td>{interia_weather_results[3][4]}</td>
                    <td>{interia_weather_results[3][5]}</td>
                </tr>
            </table>
            <h2><a href="https://www.weatheravenue.com/pl/europe/pl/krakow/bronowice-hourly.html">Avenue:</a></h2>
            <table  class="table">
                <tr>
                    <th>Time</th>
                    <th>Temperature</th>
                    <th>Wind</th>
                    <th>Humidity</th>
                    <th>Rain</th>
                    <th>Cloudiness</th>
                </tr>
                <tr>
                    <td>{avenue_weather_results[0][7]} {avenue_weather_results[0][8]}h</td>
                    <td>{avenue_weather_results[0][1]}</td>
                    <td>{avenue_weather_results[0][2]}</td>
                    <td>{avenue_weather_results[0][3]}</td>
                    <td>{avenue_weather_results[0][4]}</td>
                    <td>{avenue_weather_results[0][5]}</td>
                </tr>
                <tr>
                    <td>{avenue_weather_results[1][7]} {avenue_weather_results[1][8]}h</td>
                    <td>{avenue_weather_results[1][1]}</td>
                    <td>{avenue_weather_results[1][2]}</td>
                    <td>{avenue_weather_results[1][3]}</td>
                    <td>{avenue_weather_results[1][4]}</td>
                    <td>{avenue_weather_results[1][5]}</td>
                </tr>
                <tr>
                    <td>{avenue_weather_results[2][7]} {avenue_weather_results[2][8]}h</td>
                    <td>{avenue_weather_results[2][1]}</td>
                    <td>{avenue_weather_results[2][2]}</td>
                    <td>{avenue_weather_results[2][3]}</td>
                    <td>{avenue_weather_results[2][4]}</td>
                    <td>{avenue_weather_results[2][5]}</td>
                </tr>
                <tr>
                    <td>{avenue_weather_results[3][7]} {avenue_weather_results[3][8]}h</td>
                    <td>{avenue_weather_results[3][1]}</td>
                    <td>{avenue_weather_results[3][2]}</td>
                    <td>{avenue_weather_results[3][3]}</td>
                    <td>{avenue_weather_results[3][4]}</td>
                    <td>{avenue_weather_results[3][5]}</td>
                </tr>
            </table>
        </body>
        </html>
        """

        message.attach(MIMEText(html, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, "Rokoko123!@")
            server.sendmail(sender_email, mail[0], message.as_string())
    
