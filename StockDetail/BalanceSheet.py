from bs4 import BeautifulSoup
import requests
# from .BSEtickers import tickers
# from BSEtickers import tickers  # assumed to be a list of ticker strings
import sys
sys.stdout.reconfigure(encoding='utf-8')




BALANCE_SHEET = {}

url = "https://finance.yahoo.com/quote/NTPC.NS/balance-sheet/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
print(soup)


