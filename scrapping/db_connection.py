import mysql.connector

def db_insert(temperature,wind,humidity,rain,cloudiness,update_time,weather_time,hour,region,name,connection):
    try:
        connection = mysql.connector.connect(host='sql10.freemysqlhosting.net',
                                         database='sql10489794',
                                         user='sql10489794',
                                         password='IPELfw5A2X',
                                         auth_plugin='mysql_native_password')
        cursor = connection.cursor()
        query = "INSERT INTO "+ name + "(temperature,wind,humidity,rain,cloudiness,update_time,weather_time,hour,region) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        record  = (temperature,wind,humidity,rain,cloudiness,update_time,weather_time,hour,region)
        cursor.execute(query, record)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
    #         connection.close()

def db_delete(weather_time, hour, region, name,connection):
    try:
        connection = mysql.connector.connect(host='sql10.freemysqlhosting.net',
                                         database='sql10489794',
                                         user='sql10489794',
                                         password='IPELfw5A2X',
                                         auth_plugin='mysql_native_password')
        cursor = connection.cursor()
        query = "CALL delete_"+ name + " (%s,%s,%s);"
        record  = (weather_time, hour, region)
        cursor.execute(query, record)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to delete into MySQL table {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            # connection.close()   

