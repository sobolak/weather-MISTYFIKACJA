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

metroprog_hrefs = {'https://www.meteoprog.pl/pl/meteograms/Podgorzemalopolska/':'płaszów'}

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=1')

    return webdriver.Chrome(executable_path="C:\\Users\\48508\\AppData\\Local\\Programs\\Python\\Python39\\chromedriver.exe", options=chrome_options)

def main(hrefs_dict):
    driver = get_driver()
    hrefs = list(hrefs_dict.keys())
    selected_day = date.today()
    plus = 0 
    for link in hrefs:
        driver.get(link)
        selected_day = date.today()
        weather_tables = BeautifulSoup(driver.page_source, 'html.parser')
        tables = weather_tables.find_all("table")
        for buffor in tables:
            hours = buffor.find_all("tr")
            hours = hours[1:]
            for x in hours:
                cybant = x.text.replace("\n"," ").split(" ")
                cybant = list(filter(lambda a: a != "", cybant))
                hour = cybant[0][0:2]
                temperature = cybant[1].replace("+","").replace("°","")
                rain = cybant[3].replace(",",".")
                wind = str(float(cybant[8]) * 3.6)
                humidity = cybant[7].replace("%","")
                cloudiness = cybant[2].replace("%","")
                db.db_delete(
                    str(selected_day + timedelta(days=plus)),
                    hour,
                    hrefs_dict.get(link),
                    "metroprog")
                db.db_insert(
                    temperature,
                    wind,
                    humidity,
                    rain,
                    cloudiness,
                    str(datetime.now())[:-7],
                    str(selected_day + timedelta(days=plus)),
                    hour,
                    hrefs_dict.get(link),
                    "metroprog")
            plus += 1 
    print("METROPROG DONE")