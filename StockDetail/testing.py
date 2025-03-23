import requests
from bs4 import BeautifulSoup

class StockData:
    def nifty_50_stock_data(self):
        # Placeholder values for missing data
        total_debt = 0
        cash = 0
        eps = None
        year_revenue_growth = None

        # Dhan URL
        dhan = "https://dhan.co/all-stocks-list/"
        response_dhan = requests.get(dhan)
        
        if response_dhan.status_code != 200:
            return f"Failed to fetch data, status code: {response_dhan.status_code}"

        dhan_soup = BeautifulSoup(response_dhan.text, "html.parser")

        # Extract stock names
        stock_elements = dhan_soup.find_all("p", class_="truncate")  # Use a general class
        
        stock_names = [stock.text.strip() for stock in stock_elements]

        return stock_names

data = StockData()
stocks = data.nifty_50_stock_data()
print(stocks)
