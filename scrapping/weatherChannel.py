from cProfile import label
from distutils.command.build import build
from webbrowser import get
from numpy import size
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dateutil.parser import parse
from selenium.webdriver.chrome.options import Options
from random import random, uniform, randint
from time import sleep
from datetime import date, datetime, timedelta
import db_connection as db


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=1')

    return webdriver.Chrome(executable_path="C:\\Users\\48508\\AppData\\Local\\Programs\\Python\\Python39\\chromedriver.exe", options=chrome_options)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def main():
    driver = get_driver()
    hrefs = ['https://weather.com/weather/hourbyhour/l/e3172e6c71e631465847a819d8297d8cdb704d4662cb72af0699e437144d6980']#,'https://pogoda.interia.pl/prognoza-szczegolowa-krakow-stare-miasto,cId,13650']
    selected_day = date.today()
    region_counter = 1        
    
    for link in hrefs:
        driver.get(link)
        selected_day = date.today()
        weather_page = BeautifulSoup(driver.page_source, 'html.parser')
        timeline = weather_page.find("div", class_ = "HourlyForecast--DisclosureList--3CdxR")
        direct_hours = timeline.find_all("details", class_ = "DaypartDetails--DayPartDetail--1up3g Disclosure--themeList--25Q0H")
        plus = 0
        for buffor in direct_hours:
            hour_buffor = buffor.find("h2" , class_="DetailsSummary--daypartName--2FBp2")
            
            if (hour_buffor.text[len(hour_buffor.text)-3:] == " pm"):
                hour = str(int(hour_buffor.text.replace(" pm",""))+12)
            else:
                hour = hour_buffor.text.replace(" am","")
            #print(hour_buffor.text.replace(" am","").replace(" pm",""))
            temp_buffor = buffor.find("span" , class_="DetailsSummary--tempValue--1K4ka")
            #print(str(round((int(temp_buffor.text.replace("°",""))-32)*(5/9))))
            wind_buffor = buffor.find("span" , class_="Wind--windWrapper--3aqXJ undefined")
            #print(round(int(find_between(wind_buffor.text,' ',' mph'))*1.609344))
            rain_buffor = buffor.find_all("span" , class_="DetailsTable--value--1q_qD")
            #print(round(float(rain_buffor[5].text.replace(" in",""))*2.54,1))
            humidity_buffor = buffor.find_all("span" , class_="DetailsTable--value--1q_qD")
            #print(humidity_buffor[2].text.replace("%",""))
            cloudiness_buffor = buffor.find_all("span" , class_="DetailsTable--value--1q_qD")
            #print(cloudiness_buffor[4].text.replace("%",""))

            db.db_delete(
                str(selected_day + timedelta(days=plus)),
                hour,
                "płaszów",
                "weatherChannel")

            db.db_insert(
                str(round((int(temp_buffor.text.replace("°",""))-32)*(5/9))),
                str(round(int(find_between(wind_buffor.text,' ',' mph'))*1.609344)),
                humidity_buffor[2].text.replace("%",""),
                str(round(float(rain_buffor[5].text.replace(" in",""))*2.54,1)),
                cloudiness_buffor[4].text.replace("%",""),
                str(datetime.now())[:-7],
                str(selected_day + timedelta(days=plus)),
                hour,
                "płaszów",
                "weatherChannel")
            if(hour_buffor.text == "11 pm"):
                plus +=1
        region_counter += 1
    print("WEATHER CHANNEL DONE")
