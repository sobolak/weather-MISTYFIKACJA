from cProfile import label
from distutils.command.build import build
from webbrowser import get
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from datetime import date, datetime, timedelta
import db_connection as db

onet_hrefs = {'https://pogoda.onet.pl/prognoza-pogody/maly-plaszow-315521':'płaszów'}

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=1')

    return webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", options=chrome_options)

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
        hours_table = weather_tables.find_all("ul", class_ = "timelineListParams")
        hours = hours_table[0].find_all("li", class_ = "item")
        basic_tables = weather_tables.find_all("ul", class_ = "timelineList swiper-wrapper")
        basic = basic_tables[0].find_all("li", class_ = "item swiper-slide")
        
        if len(hours) != len(basic):
            hours = hours[(len(hours)-len(basic)):]
        
        for i in range(len(basic)):
            x = hours[i].text.replace("\n"," ").replace("\t","").split(" ")
            x = list(filter(lambda a: a != "", x))
            for t_finder in x:
                if t_finder == "T.":
                    x = x[x.index(t_finder):]
                    break
            hour = basic[i].find("div", class_ = "time").text.replace("\n","").replace("\t","")[0:2]
            # print(hour)
            temperature = basic[i].find("div", class_ = "temperature").text.replace(" ","").replace("\n","").replace("\t","").replace("°","")
            # print(temperature)
            wind = x[9]
            # print(wind)
            rain  = x[4].replace(",",".")
            # print(rain)
            humidity = x[18].replace("%","")
            # print(humidity)
            cloudiness = x[7].replace("%","")
            # print(cloudiness)

            db.db_delete(
                str(selected_day + timedelta(days=plus)),
                hour,
                hrefs_dict.get(link),
                "onet")

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
                "onet")

            if(hour == "23"):
                plus +=1
        print("ONET DONE")
