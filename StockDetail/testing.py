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






# Company_Name = ""
# Yearly_Balance_Sheet = []
# Share_Capital = []
# Reserve_And_Surplus = []
# Minority_Interest = []
# Non_Current_Liabilities = []
# Current_Liabilities = []
# Fixed_Assets = []
# Capital_Work_in_Progress = []
# Investments = []
# Other_Assets= []


# for ticker in tickers.keys():

#     url = f"https://dhan.co/stocks/{tickers[ticker]}-financial-results/"


#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     column_names = soup.find_all("th",class_="!px-4 !py-2.5 w-20")
#     row_names = soup.find_all("td",class_="!px-4 !py-2.5 text-left text-[#4f4f4f]")
#     row_data = soup.find_all("td",class_="!px-4 !py-2.5")
#     total_liabilites = soup.find_all("td",class_="!px-4 !py-2.5 !bg-[#fffbf8]")
#     total_assets = soup.find_all("td",class_="!px-4 !py-2.5 !bg-[#fffbf8]")


#     Yearly_Balance_Sheet = [ name.text for name in column_names[5:10]]

#     Share_Capital = [value.text for value in row_data[45:50]]
#     Reserve_And_Surplus = [value.text for value in row_data[50:55]]
#     Minority_Interest = [value.text for value in row_data[55:60]]
#     Non_Current_Liabilities = [value.text for value in row_data[60:65]]
#     Current_Liabilities = [value.text for value in row_data[65:70]]
#     Total_Liabilites = [value.text for value in total_liabilites[10:15]]
#     Fixed_Assets = [value.text for value in row_data[70:75]]
#     Capital_Work_in_Progress = [value.text for value in row_data[75:80]]
#     Investments = [value.text for value in row_data[80:85]]
#     Other_Assets= [value.text for value in row_data[85:90]]
#     total_assets = [value.text for value in total_assets[10:15]]





#     balance_sheet = {
#         "Company_Name": ticker,
#         "Yearly_Balance_Sheet :": Yearly_Balance_Sheet,
#         "Share_Capital :": Share_Capital,
#         "Reserve_And_Surplus :": Reserve_And_Surplus,
#         "Minority_Interest :": Minority_Interest,
#         "Non_Current_Liabilities :": Non_Current_Liabilities,
#         "Total_Liabilites :": Total_Liabilites,
#         "Current_Liabilities :": Current_Liabilities,
#         "Fixed_Assets :": Fixed_Assets,
#         "Capital_Work_in_Progress :": Capital_Work_in_Progress,
#         "Investments :": Investments,
#         "Other_Assets :": Other_Assets,
#         "total_assets :": total_assets,
#     }

#     print(balance_sheet)
























