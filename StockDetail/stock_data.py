import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

class StockData:
    def nifty_50_stock_data(self, id):
        try:
            # Placeholder values for missing data
            total_debt = 0
            cash = 0
            eps = None
            year_revenue_growth = None

            # Dhan URL
            dhan = "https://dhan.co/all-stocks-list/"
            response_dhan = requests.get(dhan)
            dhan_soup = BeautifulSoup(response_dhan.text, "html.parser")

            # Find the <script> tag with id="__NEXT_DATA__"
            script_tag = dhan_soup.find("script", id="__NEXT_DATA__", type="application/json")
            if not script_tag:
                raise Exception("Failed to find stock data in the script tag")

            json_data = json.loads(script_tag.string)  # Parse JSON content from the script tag
            df = pd.DataFrame(json_data["props"]["pageProps"]["listData"]['data'])

            # Select the stock data by ID
            stock = df.iloc[id]

            # Extract values
            data = {
                "company_name": stock.get("DispSym", ""),
                "market_cap": stock.get("Mcap", ""),
                "exchange": stock.get("Exch", ""),
                "current_price": stock.get("Ltp", ""),
                "avg_volume": stock.get("Volume", ""),
                "fifty_two_week_high": stock.get("High1Yr", ""),
                "fifty_two_week_low": stock.get("Low1Yr", ""),
                "price_to_earning": stock.get("Pe", ""),
                "price_to_book": stock.get("Pb", ""),
                "dividend_yield": stock.get("DivYeild", ""),
                "eps": stock.get("Eps", ""),
                "year_revenue_growth": stock.get("Year1RevenueGrowth", ""),
                "price_perchng_1mon": stock.get("PricePerchng1mon", ""),
                "price_perchng_1year": stock.get("PricePerchng1year", ""),
                "price_perchng_3mon": stock.get("PricePerchng3mon", ""),
                "price_perchng_3year": stock.get("PricePerchng3year", ""),
                "price_perchng_5year": stock.get("PricePerchng5year", ""),
                "roce": stock.get("ROCE", ""),
                "revenue": stock.get("Revenue", "")
            }

            # Calculate missing values if needed
            if data["price_to_book"] and data["current_price"]:
                data["book_value"] = float(data["current_price"]) / float(data["price_to_book"]) if float(data["price_to_book"]) != 0 else None

            data["enterprise_value"] = float(data["market_cap"]) + total_debt - cash if data["market_cap"] else None
            data["earnings_yield"] = (1 / float(data["price_to_earning"]) * 100) if data["price_to_earning"] else None
            data["peg_ratio"] = float(data["price_to_earning"]) / float(data["year_revenue_growth"]) if data["year_revenue_growth"] else None
            data["dividend_payout_ratio"] = (float(data["dividend_yield"]) * float(data["current_price"])) / float(data["eps"]) * 100 if data["dividend_yield"] and data["eps"] else None

            return data

        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return None




