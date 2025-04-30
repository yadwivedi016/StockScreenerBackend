import yfinance as yf
import time
import pandas as pd
from .BSEtickers import tickers

class FetchData:
    @staticmethod
    def get_data_for_all(time_range):
        """
        Fetch historical data for all companies in the tickers dictionary using bulk download.
        Returns a dict with company name as key and list of data dicts as value.
        """
        period_map = {
            "1M": ("1mo", "1d"),
            "6M": ("6mo", "1d"),
            "1Y": ("1y", "1wk"),
            "3Y": ("3y", "1mo"),
            "5Y": ("5y", "1mo"),
            "10Y": ("10y", "1mo"),
        }

        if time_range not in period_map:
            print("Invalid time range")
            return {}

        period, interval = period_map[time_range]
        symbols_map = {f"{symbol}.BO": name for name, symbol in tickers.items()}
        symbols = list(symbols_map.keys())

        print("Starting bulk download...")
        try:
            # Bulk download
            data = yf.download(
                tickers=symbols,
                period=period,
                interval=interval,
                group_by="ticker",
                auto_adjust=False,
                threads=True,
                progress=False
            )
        except Exception as e:
            print(f"Bulk download failed: {e}")
            return {}

        all_data = {}

        for symbol in symbols:
            company_name = symbols_map[symbol]
            if symbol not in data.columns.levels[0]:
                print(f"No data for {symbol}")
                continue

            symbol_data = data[symbol].fillna(0)  # Handle NaNs globally
            company_data = []

            for date, row in symbol_data.iterrows():
                try:
                    company_data.append({
                        "date": date.date(),
                        "open_price": float(row["Open"]),
                        "high_price": float(row["High"]),
                        "low_price": float(row["Low"]),
                        "close_price": float(row["Close"]),
                        "volume": int(row["Volume"]),
                    })
                except Exception as row_error:
                    print(f"Error parsing row for {symbol} on {date}: {row_error}")

            all_data[company_name] = company_data

        return all_data
