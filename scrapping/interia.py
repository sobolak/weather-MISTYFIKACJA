from distutils.command.build import build
from turtle import update
from webbrowser import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.chrome.options import Options
from datetime import date, datetime, timedelta
import db_connection as db
import platform

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=1')

    if (platform.system() == "Windows"):
        path = "C:\\Users\\48508\\AppData\\Local\\Programs\\Python\\Python39\\chromedriver.exe"
    else:
        path = "/usr/lib/chromium-browser/chromedriver"
    
    return webdriver.Chrome(executable_path=path ,options=chrome_options)

def main(hrefs_dict):
    driver = get_driver()
    sleep(15)
    hrefs = list(hrefs_dict.keys())
    selected_day = date.today()
    left = "weather-forecast "
    right = " selected" 
    days = []
    for i in range(6):
        chosen_date = str(selected_day + timedelta(days=i))[0:5] + str(selected_day + timedelta(days=i))[5:6].replace("0","") + str(selected_day + timedelta(days=i))[6:8] + str(selected_day + timedelta(days=i))[8:9].replace("0","") + str(selected_day + timedelta(days=i))[9:10]
        date_heading = left + chosen_date + right
        days.append(date_heading)
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
                    hrefs_dict.get(link),
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
                    hrefs_dict.get(link),
                    "interia")
                except:
                    print(str(selected_day + timedelta(days=x)) + " "+ hour_buffor[i].text)
            x += 1
    print("INTERIA DONE")

