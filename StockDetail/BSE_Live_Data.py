import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

sys.stdout.reconfigure(encoding="utf-8")

class BSE_Live_Data():
    def __init__(self):
        self.selected_columns = [
            'LTP',
            'Change_%',
            'PE_Ratio',
            'PB_Ratio',
            'RSI',
            'ROCE',
            'Market_Cap_(Cr.)'
        ]

    def bse_live_data(self):
        url = "https://dhan.co/bse-stocks-list/bse-500/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        company_names = [name.text.strip() for name in soup.find_all("p", class_="truncate")]

        columns = [col.text.strip().replace(" ", "_") for col in soup.find_all("th", class_="cursor-pointer")]
        columns = columns[1:]  # skip serial number

        values = [val.text.strip() for val in soup.find_all("td", class_="font-CircularRegular")]

        num_cols = len(columns)
        data_rows = [values[i:i + num_cols] for i in range(0, len(values), num_cols)]

        df = pd.DataFrame(data_rows, columns=columns)

        if len(company_names) > len(df):
            company_names = company_names[:len(df)]

        df["Company_Name"] = company_names
        df = df[["Company_Name"] + [col for col in df.columns if col != "Company_Name"]]

        return df

    def get_company_data(self, company_name):
        df = self.bse_live_data()

        # Clean LTP column (remove "BS", " NSE", or any text that might sneak in)
        df["LTP"] = df["LTP"].str.replace(r'[^\d.,]', '', regex=True)

        company_row = df[df["Company_Name"].str.lower() == company_name.lower()]
        
        if company_row.empty:
            return {"error": f"Company '{company_name}' not found."}
        else:
            return company_row[["Company_Name"] + self.selected_columns].iloc[0].to_dict()


# # Run the script
# if __name__ == "__main__":
#     live_data = BSE_Live_Data()
#     company_input = "Reliance Industries"
#     result = live_data.get_company_data(company_input)
#     print(result)
