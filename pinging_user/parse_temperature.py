import requests
from bs4 import BeautifulSoup

requestedPage = requests.get('http://192.168.1.104')

code = requestedPage.text

parsed_html = BeautifulSoup(code, "html.parser")
temperature = parsed_html.body.find('p', attrs={'class':'temp'}).text
humidity = parsed_html.body.find('p', attrs={'class':'hum'}).text

print(temperature, humidity)