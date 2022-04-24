from cProfile import label
from distutils.command.build import build
from webbrowser import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from datetime import date, datetime, timedelta
import db_connection as db

avenue_hrefs = {'https://www.weatheravenue.com/pl/europe/pl/krakow/plaszow-hourly.html':'płaszów'}

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=1')

    return webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", options=chrome_options)

def main(hrefs_dict):
    driver = get_driver()
    hrefs = list(hrefs_dict.keys())
    selected_day = date.today()   
    
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
                try:
                    db.db_delete(
                        str(selected_day + timedelta(days=day_bonus)),
                        hour, 
                        hrefs_dict.get(link),
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
                        hrefs_dict.get(link),
                        "avenue")
                except:
                    pass
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
                try:
                    db.db_delete(
                        str(selected_day + timedelta(days=day_bonus)),
                        hour, 
                        hrefs_dict.get(link),
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
                        hrefs_dict.get(link),
                        "avenue")
                except:
                    pass
    print("AVENUE DONE")
