import requests
from bs4 import BeautifulSoup
import json

# Headers to avoid bot detection
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/get-quotes/equity?symbol=RELIANCE",
}

# Start a session
session = requests.Session()

# Request the page
url = "https://dhan.co/stocks/market/golden-crossover-stocks/"
response = session.get(url, headers=headers)

# Parse HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the script tag containing the JSON data
data = soup.find_all("p",class_='truncate')


stocks = [item.text.strip() for item in data]
    
print(stocks)
print(soup.prettify())
