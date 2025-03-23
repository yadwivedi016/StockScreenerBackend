import requests
from bs4 import BeautifulSoup
import json       
import pandas as pd

class LiveData:
    def data(self, symbol):
        # Initialize live data fields
        live_data = {}

        try:
            # Dhan URL
            dhan = "https://dhan.co/all-stocks-list/"

            # Get response and parse with BeautifulSoup
            response_dhan = requests.get(dhan)
            response_dhan.raise_for_status()  # Check for request errors
            dhan_soup = BeautifulSoup(response_dhan.text, "html.parser")

            # Find the <script> tag with id="__NEXT_DATA__"
            script_tag = dhan_soup.find("script", id="__NEXT_DATA__", type="application/json")

            # Extract and parse JSON content from the script tag
            json_data = json.loads(script_tag.string)
            df = pd.DataFrame(json_data["props"]["pageProps"]["listData"]["data"])

            # Filter stock data by symbol
            stock = df[df["DispSym"] == symbol]

            if stock.empty:
                return {"error": f"Stock with symbol '{symbol}' not found."}

            # Extract relevant data and handle missing or invalid values
            stock = stock.iloc[0]  # Get the first (and expected only) matching row
            previous_close = float(stock["Ltp"]) / (1 + (float(stock["Pchange"]) / 100))

            # Build live data dictionary
            live_data = {
                "market_cap": stock.get("Mcap", "N/A"),
                "current_price": stock.get("Ltp", "N/A"),
                "percent_change": f"{float(stock['Pchange']):.3f}" if not pd.isna(stock["Pchange"]) else "N/A",
                "previous_close": f"{previous_close:.2f}" if not pd.isna(previous_close) else "N/A",
                "price_to_earning": stock.get("Pe", "N/A"),
                "price_to_book": f"{float(stock['Pb']):.3f}" if not pd.isna(stock["Pb"]) else "N/A",
                "dividend_yield": stock.get("DivYeild", "N/A"),
                "rsi": f"{float(stock['DayRSI14CurrentCandle']):.3f}" if not pd.isna(stock["DayRSI14CurrentCandle"]) else "N/A",
            }

        except requests.exceptions.RequestException as e:
            live_data["error"] = f"Error fetching data from Dhan: {e}"

        except Exception as e:
            live_data["error"] = f"An unexpected error occurred: {e}"

        return live_data


