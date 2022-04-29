from cProfile import label
from distutils.command.build import build
from webbrowser import get
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from random import random, uniform, randint
from datetime import date, datetime, timedelta
import db_connection as db
from random import randint

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=1')

    return webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver" ,options=chrome_options)

def main(hrefs_dict):
    driver = get_driver()
    sleep(15)
    hrefs = list(hrefs_dict.keys())
    selected_day = date.today()
    plus = 0 
    for link in hrefs:
        driver.get(link)
        selected_day = date.today()
        weather_tables = BeautifulSoup(driver.page_source, 'html.parser')
        tables = weather_tables.find_all("div", class_="list")
        for buffor in tables:
            hours = buffor.find_all("div", class_ = "item")
            
            for i in range(len(hours)):
                x = hours[i].text.split(" ")
                for opad_finder in x:
                    if opad_finder == "Opad:":
                        hour_temp = x[1:4]
                        cloud_buffor = x[6:x.index(opad_finder)] 
                        rest = x[x.index(opad_finder)+1:]
                        break
                hour = hour_temp[0][0:2]
                temperature = hour_temp[2].replace("°C","")
                wind = rest[6]
                rain = rest[0]
                humidity = rest[9].replace("%","")
                try:
                    if cloud_buffor[0] == "Prawie" or cloud_buffor[0] == "Prawie,": 
                        cloudiness = str(randint(3,17))
                    elif cloud_buffor[0] == "Bezchmurnie" or cloud_buffor[0] == "Bezchmurnie,":
                        cloudiness = str(0)
                    else:
                        if cloud_buffor[1] == "małe," or cloud_buffor[1] == "małe" :
                            cloudiness = str(randint(18,41))
                        elif cloud_buffor[1] == "umiarkowane," or cloud_buffor[1] == "umiarkowane":
                            cloudiness = str(randint(45,65))
                        elif cloud_buffor[1] == "duże," or cloud_buffor[1] == "duże":
                            cloudiness = str(randint(65,100))
                        else:
                            cloudiness = str(randint(30,70))
                except:
                    cloudiness = str(randint(30,70))
                db.db_delete(
                    str(selected_day + timedelta(days=plus)),
                    hour,
                    hrefs_dict.get(link),
                    "wp")
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
                    "wp")
            plus += 1
            
    print("WP DONE")
  