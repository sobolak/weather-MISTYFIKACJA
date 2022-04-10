from distutils.command.build import build
from turtle import update
from webbrowser import get
from h11 import Data
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

def main():
    driver = get_driver()
    hrefs = ['https://pogoda.interia.pl/prognoza-szczegolowa-krakow-plaszow,cId,26191']#,'https://pogoda.interia.pl/prognoza-szczegolowa-krakow-stare-miasto,cId,13650']
    selected_day = date.today()
    left = "weather-forecast "
    right = " selected" 
    days = []
    for i in range(6):
        chosen_date = str(selected_day + timedelta(days=i))[0:5] + str(selected_day + timedelta(days=i))[5:6].replace("0","") + str(selected_day + timedelta(days=i))[6:8] + str(selected_day + timedelta(days=i))[8:9].replace("0","") + str(selected_day + timedelta(days=i))[9:10]
        date_heading = left + chosen_date + right
        days.append(date_heading)
    region_counter = 1
    for link in hrefs:
        driver.get(link)
        weather_page = BeautifulSoup(driver.page_source, 'html.parser')
        x = 0
        for day in days:
            update_time = str(datetime.now())[:-7]
            day_buffor = weather_page.find("div", class_ = day)
            hour_buffor = day_buffor.find_all("span", class_ = "hour")
            temp_buffor = day_buffor.find_all("span", class_ = "forecast-temp")
            wind_buffor = day_buffor.find_all("span", class_ = "speed-value")
            rain_buffor = day_buffor.find_all("span", class_ = "entry-precipitation-value rain")
            humidity_buffor = day_buffor.find_all("div", class_ = "entry-humidity-wrap")
            cloudiness_buffor = day_buffor.find_all("span", class_ = "entry-precipitation-value cloud-cover")
            for i in range(0,len(hour_buffor)):
                #print(str(selected_day + timedelta(days=i)) + " "+ hour_buffor[i].text + " " + temp_buffor[i].text.replace("°C","") + " " + wind_buffor[i].text +" "+rain_buffor[i].text[:-3] +" "+humidity_buffor[i].text.replace("%","")+cloudiness_buffor[i].text.replace("%",""))
                #print(rain_buffor[i].text[:-2])
                #print(type(datetime.now())
                db.db_delete(
                    str(selected_day + timedelta(days=x)),
                    hour_buffor[i].text,
                    "płaszów",
                    "interia")
                try:
                    db.db_insert(
                    temp_buffor[i].text.replace("°C",""),
                    wind_buffor[i].text,
                    humidity_buffor[i].text.replace("%","")[1:],
                    str(round(float(rain_buffor[i].text[:-2].replace(",",".")),1)), 
                    cloudiness_buffor[i].text.replace("%",""),
                    update_time, 
                    str(selected_day + timedelta(days=x)), 
                    hour_buffor[i].text, 
                    "płaszów",
                    "interia")
                except:
                    print(str(selected_day + timedelta(days=i)) + " "+ hour_buffor[i].text)
            x += 1
            #i += 1
        region_counter +=1
    print("INTERIA DONE")

