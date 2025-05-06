from bs4 import BeautifulSoup
import requests
from .BSEtickers import tickers
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

class BalanceSheet:
    def data(self,symbol):
        target_labels = [
            "Equity Capital", "Reserves", "Net Worth", "Long Term Borrowings",
            "Short Term Borrowings", "Total Debt", "Total Liabilities",
            "Fixed Assets", "CWIP", "Investments", "Other Assets", "Total Assets"
        ]

        
        ticker = tickers[symbol]
        BALANCE_SHEET = {}

        url = f"https://www.screener.in/company/{ticker}/consolidated/#balance-sheet"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

       
        table = soup.select_one("section#balance-sheet table")

        
        ths = table.select("thead tr th")[1:]  # Skip the first 'Particulars' column
        BALANCE_SHEET["date"] = [th.text.strip() for th in ths]

        
        rows = table.select("tbody tr")

        for row in rows:
            cells = row.find_all("td")
            if not cells:
                continue

            label = cells[0].text.strip()
            if label in target_labels:
                BALANCE_SHEET[label] = [cell.text.strip() for cell in cells[1:]]

        
        return BALANCE_SHEET