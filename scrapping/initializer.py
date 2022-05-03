from time import time
import interia
import avenue
import weatherChannel
import onet
import wp
import metroprog
# import schedule
# import time
import mysql.connector

try:
    interia_hrefs = {'https://pogoda.interia.pl/prognoza-szczegolowa-agh,cId,1233058':'agh'}
    avenue_hrefs = {'https://www.weatheravenue.com/pl/europe/pl/krakow/bronowice-hourly.html':'agh'}
    weatherChannel_hrefs = {'https://weather.com/weather/hourbyhour/l/e3172e6c71e631465847a819d8297d8cdb704d4662cb72af0699e437144d6980':'agh'}
    onet_hrefs = {'https://pogoda.onet.pl/prognoza-pogody/maly-plaszow-315521':'agh'}
    wp_hrefs = {'https://pogoda.wp.pl/pogoda-na-dzis/krakow/3094802':'agh'}
    metroprog_hrefs = {'https://www.meteoprog.pl/pl/meteograms/Krakow/':'agh'}

    connection = mysql.connector.connect(host='sql11.freemysqlhosting.net',
                                        database='sql11489741',
                                        user='sql11489741',
                                        password='YWlpqUE1zv',
                                        auth_plugin='mysql_native_password')
    # connection = mysql.connector.connect(host='localhost',
    #     database='weather',
    #     user='root',
    #     password='cybant17',
    #     auth_plugin='mysql_native_password')

    interia.main(interia_hrefs,connection)
    avenue.main(avenue_hrefs,connection)
    weatherChannel.main(weatherChannel_hrefs,connection)
    onet.main(onet_hrefs,connection)
    wp.main(wp_hrefs,connection)
    metroprog.main(metroprog_hrefs,connection) 

    # schedule.every().day.at("20:07").do(onet.main,onet_hrefs)
    # schedule.every().day.at("20:09").do(avenue.main,avenue_hrefs)
    # schedule.every().day.at("20:11").do(weatherChannel.main,weatherChannel_hrefs)
    # schedule.every().day.at("20:13").do(interia.main,interia_hrefs)
    # schedule.every().day.at("20:15").do(wp.main,wp_hrefs)
    # schedule.every().day.at("20:17").do(metroprog.main,metroprog_hrefs)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)
finally:
    connection.close()  