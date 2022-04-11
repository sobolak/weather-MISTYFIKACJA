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

def main():
    driver = get_driver()
    hrefs = ['https://www.weatheravenue.com/pl/europe/pl/krakow/plaszow-hourly.html']#,'https://pogoda.interia.pl/prognoza-szczegolowa-krakow-stare-miasto,cId,13650']
    selected_day = date.today()
    region_counter = 1        
    
    for link in hrefs:
        driver.get(link)
        selected_day = date.today()
        day_bonus = 0
        weather_tables = BeautifulSoup(driver.page_source, 'html.parser')
        hours_tables = weather_tables.find_all("table", class_ = "display dataTable")
        for odd_buffor in hours_tables:
            table = odd_buffor.find_all("tr", class_ = "odd")
            for buffor in table:
                x = buffor.text.replace(" ","_").replace("\n"," ").replace("\xa0","").split(" ")
                x = list(filter(lambda a: a != "", x))
                # print(x[4][0:2].replace("_",""))
                # print(x[2][0:4].replace("°C_","").replace("°C",""))
                # print(x[6].replace("%",""))
                # print(x[3][0:5].replace("_","").replace("m",""))
                hour = x[0].replace(":00","")
                if hour[0] == "0":
                    hour.replace("0","")
                if hour == "00" or hour == "01":
                    day_bonus +=1
                db.db_delete(
                    str(selected_day + timedelta(days=day_bonus)),
                    hour, 
                    "płaszów",
                    "avenue")
                db.db_insert(
                    x[2][0:4].replace("°C_","").replace("°C",""),
                    x[4][0:2].replace("_",""),
                    x[6].replace("%",""),
                    x[3][0:5].replace("_","").replace("m",""), 
                    x[5].replace("%",""),
                    str(datetime.now())[:-7] , 
                    str(selected_day + timedelta(days=day_bonus)), 
                    hour, 
                    "płaszów",
                    "avenue")
        day_bonus = 0
        for even_buffor in hours_tables:
            table = even_buffor.find_all("tr", class_ = "even")
            for buffor in table:
                x = buffor.text.replace(" ","_").replace("\n"," ").replace("\xa0","").split(" ")
                x = list(filter(lambda a: a != "", x))
                hour = x[0].replace(":00","")
                if hour[0] == "0":
                    hour.replace("0","")
                if hour == "00" or hour == "01":
                    day_bonus +=1
                db.db_delete(
                    str(selected_day + timedelta(days=day_bonus)),
                    hour, 
                    "płaszów",
                    "avenue")
                db.db_insert(
                    x[2][0:4].replace("°C_","").replace("°C",""),
                    x[4][0:2].replace("_",""),
                    x[6].replace("%",""),
                    x[3][0:5].replace("_","").replace("m",""), 
                    x[5].replace("%",""),
                    str(datetime.now())[:-7] , 
                    str(selected_day + timedelta(days=day_bonus)), 
                    hour, 
                    "płaszów",
                    "avenue")
        region_counter += 1
    print("AVENUE DONE")
