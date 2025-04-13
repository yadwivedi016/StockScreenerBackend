import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import json

sys.stdout.reconfigure(encoding="utf-8")

class BSE_Data():
    def bse_data(self):
        # URL of Dhan's BSE 500 stock list
        dhan = "https://dhan.co/bse-stocks-list/bse-500/"
        response_dhan = requests.get(dhan)
        dhan_soup = BeautifulSoup(response_dhan.text, "html.parser")

        # Extracting company names
        company_names = dhan_soup.find_all("p", class_="truncate")
        company_names = [name.text for name in company_names]

        #extracting all columns names
        columns = dhan_soup.find_all("th", class_="cursor-pointer")
        columns = [col.text for col in columns]
        columns = [col.strip() for col in columns]
        columns = [col.replace(" ", "_") for col in columns]

        #extracting all rows data
        values = dhan_soup.find_all("td",class_="font-CircularRegular")
        values = [value.text for value in values]

        columns = columns[1:]
        # print(len(values), len(columns))
        stock_data = {}
        data = {}
        i = 0
        j = 0
        for company in company_names:
            stock_data[company] = {}
            for column in columns:
                stock_data[company][column] = values[i]
                i += 1
                j = i

        return stock_data

        


