from bs4 import BeautifulSoup
import requests

url = "https://chartink.com/screener/macd-bearish-or-bullish-crossover"
soup = BeautifulSoup(requests.get(url).text, "html.parser")

data = soup.find("a", class_="text-teal-700")

for i in data:
    print(i.text.strip())