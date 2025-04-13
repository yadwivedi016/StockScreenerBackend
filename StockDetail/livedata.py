import requests
from bs4 import BeautifulSoup
import json       
import pandas as pd
import numpy as np

class LiveData:
    def data(self, symbol):
        live_data = {}

        try:
            # Dhan URL
            dhan = "https://dhan.co/all-stocks-list/"

            # Get response and parse with BeautifulSoup
            response_dhan = requests.get(dhan)
            response_dhan.raise_for_status()
            dhan_soup = BeautifulSoup(response_dhan.text, "html.parser")

            # Extract JSON data from script tag
            script_tag = dhan_soup.find("script", id="__NEXT_DATA__", type="application/json")
            json_data = json.loads(script_tag.string)
            df = pd.DataFrame(json_data["props"]["pageProps"]["listData"]["data"])

            # Filter by stock symbol
            stock = df[df["DispSym"] == symbol]

            if stock.empty:
                return {"error": f"Stock with symbol '{symbol}' not found."}

            # Extract stock details
            stock = stock.iloc[0]
            previous_close = float(stock["Ltp"]) / (1 + (float(stock["Pchange"]) / 100))

            # **Fix Market Cap Scaling**
            market_cap = stock.get("Mcap", "N/A")
            if market_cap != "N/A" and isinstance(market_cap, str):
                market_cap = market_cap.replace(",", "").strip()
                
                if "Cr" in market_cap:  # If stored in Crores
                    market_cap = float(market_cap.replace("Cr", "").strip()) * 10**7  # Convert to full rupees
                elif "L" in market_cap:  # If stored in Lakhs
                    market_cap = float(market_cap.replace("L", "").strip()) * 10**5  # Convert to full rupees
                else:
                    market_cap = float(market_cap)  # If already a number
                
                market_cap = np.float64(market_cap)  # Ensure consistent type

            # Build live data dictionary
            live_data = {
                "market_cap": market_cap,
                "current_price": np.float64(stock["Ltp"]) if not pd.isna(stock["Ltp"]) else "N/A",
                "percent_change": f"{float(stock['Pchange']):.3f}" if not pd.isna(stock["Pchange"]) else "N/A",
                "previous_close": f"{previous_close:.2f}" if not pd.isna(previous_close) else "N/A",
                "price_to_earning": np.float64(stock["Pe"]) if not pd.isna(stock["Pe"]) else "N/A",
                "price_to_book": f"{float(stock['Pb']):.3f}" if not pd.isna(stock["Pb"]) else "N/A",
                "dividend_yield": np.float64(stock["DivYeild"]) if not pd.isna(stock["DivYeild"]) else "N/A",
                "rsi": f"{float(stock['DayRSI14CurrentCandle']):.3f}" if not pd.isna(stock["DayRSI14CurrentCandle"]) else "N/A",
            }

        except requests.exceptions.RequestException as e:
            live_data["error"] = f"Error fetching data from Dhan: {e}"

        except Exception as e:
            live_data["error"] = f"An unexpected error occurred: {e}"

        return live_data


data = LiveData()
print(data.data("Reliance Industries"))
