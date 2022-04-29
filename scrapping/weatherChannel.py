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

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def main(hrefs_dict):
    driver = get_driver()
    sleep(15)
    hrefs = list(hrefs_dict.keys())
    selected_day = date.today()
    
    
    for link in hrefs:
        driver.get(link)
        selected_day = date.today()
        weather_page = BeautifulSoup(driver.page_source, 'html.parser')
        timeline = weather_page.find("div", class_ = "HourlyForecast--DisclosureList--3CdxR")
        direct_hours = timeline.find_all("details", class_ = "DaypartDetails--DayPartDetail--1up3g DaypartDetails--ctaShown--2cYCl Disclosure--themeList--25Q0H")
        plus = 0
        print(len(direct_hours))
        for buffor in direct_hours:
            hour_buffor = buffor.find("h3" , class_="DetailsSummary--daypartName--2FBp2")    
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
                hrefs_dict.get(link),
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
                hrefs_dict.get(link),
                "weatherChannel")
            if(hour_buffor.text == "11 pm"):
                plus +=1

    print("WEATHER CHANNEL DONE")
