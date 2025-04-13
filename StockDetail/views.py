from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from django.utils.timezone import make_aware
from datetime import datetime
import time
import yfinance as yf
from django.shortcuts import get_object_or_404, redirect
from .models import StockDetail, Nifty50GraphHistory,BSE_500_Stocks,BSE500GraphHistory
from .stock_data import StockData
from .livedata import LiveData
from datetime import datetime, timedelta
from django.utils import timezone
from datetime import timedelta
from .BSE_500_stock_data import BSE_Data
import json
from django.forms.models import model_to_dict
from .BSE_Live_Data import BSE_Live_Data
from .BSEtickers import tickers

class AddNifty50StockView(View):
    def add_nifty50_data(self): 
        stock_data = StockData()
        for i in range(50):
            try:
                data = stock_data.nifty_50_stock_data(id=i)  # Fetch stock data for each index
                if not data:  # Skip empty data
                    continue

                # Check if the stock is already present in the database
                company_name = data.get("company_name")
                if StockDetail.objects.filter(company_name=company_name).exists():
                    # Skip if the company is already in the database
                    continue

                # Create a new StockDetail record and save it to the database
                StockDetail.objects.create(
                    company_name=company_name,
                    fifty_two_week_high=data.get("fifty_two_week_high"),
                    fifty_two_week_low=data.get("fifty_two_week_low"),
                    dividend_yield=data.get("dividend_yield"),
                    book_value=data.get("book_value"),
                    enterprise_value=data.get("enterprise_value"),
                    earnings_yield=data.get("earnings_yield"),
                    peg_ratio=data.get("peg_ratio"),
                    dividend_payout_ratio=data.get("dividend_payout_ratio"),
                    avg_volume=data.get("avg_volume"),
                    exchange=data.get("exchange"),
                    eps=data.get("eps"),
                    year_revenue_growth=data.get("year_revenue_growth"),
                    price_perchng_1mon=data.get("price_perchng_1mon"),
                    price_perchng_1year=data.get("price_perchng_1year"),
                    price_perchng_3mon=data.get("price_perchng_3mon"),
                    price_perchng_3year=data.get("price_perchng_3year"),
                    price_perchng_5year=data.get("price_perchng_5year"),
                    roce=data.get("roce"),
                    revenue=data.get("revenue"),
                )
            except Exception as e:
                # Log the error and continue with the next iteration
                print(f"Error while processing stock {i}: {e}")
        return True

    def get(self, request):
        try:
            self.add_nifty50_data()  # Add data to the database
            return JsonResponse({"context": "Success"})
        except Exception as e:
            return JsonResponse({"context": "Failed", "error": str(e)})



class SearchView(View):
    def get(self, request):
        # Render the search page with a search bar
        return render(request, "search.html")

    def post(self, request):
        # Get the stock symbol from the form submission
        symbol = request.POST.get("symbol")
        if symbol:
            # Redirect to the stock details page with the symbol
            return redirect("stock-detail-view", symbol=symbol)  # Matches URL name in urls.py
        return render(request, "search.html", {"error": "Please enter a valid symbol"})


    


class StockDetailsView(View):
    def get(self, request, symbol):
        # Fetch the stock details from the database
        stock_detail = get_object_or_404(StockDetail, company_name__icontains=symbol)

        # Convert the stock details to a dictionary
        stock = stock_detail.__dict__
        stock.pop("_state", None)  # Remove Django's internal field

        # Fetch live data for the stock
        obj = LiveData()
        live_data = obj.data(stock["company_name"])

        # Merge live data into the stock dictionary
        if isinstance(live_data, dict):  # Ensure live_data is a dictionary
            live_data.pop("_state", None)
            stock.update(live_data)
        return JsonResponse({"stock":stock})    
    


class GraphView(View):
    def get(self, request, symbol):
        nifty50_tickers = {
        "Reliance Industries": "RELIANCE.NS",
        "Tata Consultancy Services": "TCS.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "Bharti Airtel": "BHARTIARTL.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "Infosys": "INFY.NS",
        "State Bank of India": "SBIN.NS",
        "Hindustan Unilever": "HINDUNILVR.NS",
        "Bajaj Finance": "BAJFINANCE.NS",
        "ITC": "ITC.NS",
        "LIC of India": "LICI.NS",
        "HCL Technologies": "HCLTECH.NS",
        "Larsen & Toubro": "LT.NS",
        "Sun Pharmaceutical": "SUNPHARMA.NS",
        "Maruti Suzuki": "MARUTI.NS",
        "Kotak Bank": "KOTAKBANK.NS",
        "Mahindra & Mahindra": "M&M.NS",
        "Wipro": "WIPRO.NS",
        "UltraTech Cement": "ULTRACEMCO.NS",
        "Axis Bank": "AXISBANK.NS",
        "NTPC": "NTPC.NS",
        "Oil & Natural Gas Corporation": "ONGC.NS",
        "Bajaj Finserv": "BAJAJFINSV.NS",
        "Titan": "TITAN.NS",
        "Adani Enterprises": "ADANIENT.NS",
        "Tata Motors": "TATAMOTORS.NS",
        "Power Grid Corporation of India": "POWERGRID.NS",
        "Avenue Supermarts DMart": "DMART.NS",
        "JSW Steel": "JSWSTEEL.NS",
        "Bajaj Auto": "BAJAJ-AUTO.NS",
        "Adani Ports & SEZ": "ADANIPORTS.NS",
        "Zomato": "ZOMATO.NS",
        "Hindustan Aeronautics": "HAL.NS",
        "Coal India": "COALINDIA.NS",
        "Asian Paints": "ASIANPAINT.NS",
        "Nestle": "NESTLEIND.NS",
        "Adani Power": "ADANIPOWER.NS",
        "Bharat Electronics": "BEL.NS",
        "Trent": "TRENT.NS",
        "Siemens": "SIEMENS.NS",
        "Hindustan Zinc": "HINDZINC.NS",
        "DLF": "DLF.NS",
        "Interglobe Aviation": "INDIGO.NS",
        "Tata Steel": "TATASTEEL.NS",
        "Indian Oil Corporation": "IOC.NS",
        "Vedanta": "VEDL.NS",
        "Tech Mahindra": "TECHM.NS",
        "IRFC": "IRFC.NS",
        "Grasim Industries": "GRASIM.NS",
        "LTI Mindtree": "LTIM.NS"
    }
        """Handles GET requests and fetches 1-minute interval stock data."""
        
        symbol = nifty50_tickers[symbol]  # Example stock symbol
        data = self.fetch_stock_data(symbol)
        return JsonResponse({"symbol": symbol, "data": data})  # JSON response

    def fetch_stock_data(self, symbol, period="1d", interval="1m"):
        """Fetch stock data at 1-minute intervals from Yahoo Finance."""
        ticker = yf.Ticker(f"{symbol}")  # Example stock symbol
        df = ticker.history(period=period, interval=interval)

        if df.empty:
            return []  # Return empty list if no data is available

        df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')  # Convert index to readable string format

        # Convert DataFrame to a dictionary format
        stock_data = df[['Close']].reset_index()
        stock_data.rename(columns={"Datetime": "date", "Close": "close_price"}, inplace=True)

        return stock_data.to_dict(orient='records')  # JSON-friendly format




class FetchNifty50StockGraphDataView(View):
    TIME_RANGES_MAPPING = {
        "1M": "1mo",
        "6M": "6mo",
        "1Y": "1y",
        "3Y": "3y",
        "5Y": "5y",
        "10Y": "10y",
    }

    NIFTY_50_STOCKS = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
        "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS",
        "BAJFINANCE.NS", "KOTAKBANK.NS", "LT.NS", "AXISBANK.NS", "ASIANPAINT.NS",
        "MARUTI.NS", "HCLTECH.NS", "TITAN.NS", "ULTRACEMCO.NS", "WIPRO.NS",
        "NESTLEIND.NS", "SUNPHARMA.NS", "TECHM.NS", "POWERGRID.NS", "ADANIENT.NS",
        "INDUSINDBK.NS", "TATASTEEL.NS", "ONGC.NS", "JSWSTEEL.NS", "BAJAJFINSV.NS",
        "NTPC.NS", "COALINDIA.NS", "HDFCLIFE.NS", "ADANIPORTS.NS", "DRREDDY.NS",
        "M&M.NS", "CIPLA.NS", "SBILIFE.NS", "EICHERMOT.NS", "BRITANNIA.NS",
        "HEROMOTOCO.NS", "GRASIM.NS", "DIVISLAB.NS", "BPCL.NS", "TATAMOTORS.NS",
        "APOLLOHOSP.NS", "UPL.NS", "BAJAJ-AUTO.NS", "SHREECEM.NS", "TATACONSUM.NS"
    ]

    def get(self, request):
        try:
            for i, stock_symbol in enumerate(self.NIFTY_50_STOCKS):
                stock = yf.Ticker(stock_symbol)

                for time_range, period in self.TIME_RANGES_MAPPING.items():
                    data = stock.history(period=period, interval="1d")
                    if data.empty:
                        continue

                    # Fetch existing records as a dictionary
                    existing_records = {
                        (entry.date.date(), entry.time_range): entry
                        for entry in Nifty50GraphHistory.objects.filter(
                            symbol=stock_symbol,
                            time_range=time_range
                        )
                    }

                    new_entries = []
                    updated_entries = []

                    for index, row in data.iterrows():
                        date = make_aware(datetime.strptime(str(index.date()), "%Y-%m-%d"))

                        record_key = (date.date(), time_range)  # Compare only the DATE

                        if record_key in existing_records:
                            #   Update existing record
                            record = existing_records[record_key]
                            record.open_price = row["Open"]
                            record.high_price = row["High"]
                            record.low_price = row["Low"]
                            record.close_price = row["Close"]
                            record.volume = row["Volume"]
                            updated_entries.append(record)
                        else:
                            #   Create new record
                            new_entries.append(Nifty50GraphHistory(
                                symbol=stock_symbol,
                                date=date,
                                time_range=time_range,
                                open_price=row["Open"],
                                high_price=row["High"],
                                low_price=row["Low"],
                                close_price=row["Close"],
                                volume=row["Volume"],
                            ))

                    #   Bulk Insert & Update in an atomic transaction
                    with transaction.atomic():
                        if new_entries:
                            Nifty50GraphHistory.objects.bulk_create(new_entries)
                        if updated_entries:
                            Nifty50GraphHistory.objects.bulk_update(
                                updated_entries,
                                ["open_price", "high_price", "low_price", "close_price", "volume"]
                            )

                #   Prevent API rate limit issues
                if (i + 1) % 5 == 0:
                    time.sleep(2)

            return JsonResponse({"message": "Stock data fetched, updated, and saved successfully."})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class GetNifty50StockGraphDataView(View):
    
    TIME_RANGES_MAPPING = {
        "1M": timedelta(days=30),
        "6M": timedelta(days=180),
        "1Y": timedelta(days=365),
        "3Y": timedelta(days=3*365),
        "5Y": timedelta(days=5*365),
        "10Y": timedelta(days=10*365),
    }

    NIFTY50_TICKERS = {
        "Reliance Industries": "RELIANCE.NS",
        "Tata Consultancy Services": "TCS.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "Bharti Airtel": "BHARTIARTL.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "Infosys": "INFY.NS",
        "State Bank of India": "SBIN.NS",
        "Hindustan Unilever": "HINDUNILVR.NS",
        "Bajaj Finance": "BAJFINANCE.NS",
        "ITC": "ITC.NS",
        "LIC of India": "LICI.NS",
        "HCL Technologies": "HCLTECH.NS",
        "Larsen & Toubro": "LT.NS",
        "Sun Pharmaceutical": "SUNPHARMA.NS",
        "Maruti Suzuki": "MARUTI.NS",
        "Kotak Bank": "KOTAKBANK.NS",
        "Mahindra & Mahindra": "M&M.NS",
        "Wipro": "WIPRO.NS",
        "UltraTech Cement": "ULTRACEMCO.NS",
        "Axis Bank": "AXISBANK.NS",
        "NTPC": "NTPC.NS",
        "Oil & Natural Gas Corporation": "ONGC.NS",
        "Bajaj Finserv": "BAJAJFINSV.NS",
        "Titan": "TITAN.NS",
        "Adani Enterprises": "ADANIENT.NS",
        "Tata Motors": "TATAMOTORS.NS",
        "Power Grid Corporation of India": "POWERGRID.NS",
        "Avenue Supermarts DMart": "DMART.NS",
        "JSW Steel": "JSWSTEEL.NS",
        "Bajaj Auto": "BAJAJ-AUTO.NS",
        "Adani Ports & SEZ": "ADANIPORTS.NS",
        "Zomato": "ZOMATO.NS",
        "Hindustan Aeronautics": "HAL.NS",
        "Coal India": "COALINDIA.NS",
        "Asian Paints": "ASIANPAINT.NS",
        "Nestle": "NESTLEIND.NS",
        "Adani Power": "ADANIPOWER.NS",
        "Bharat Electronics": "BEL.NS",
        "Trent": "TRENT.NS",
        "Siemens": "SIEMENS.NS",
        "Hindustan Zinc": "HINDZINC.NS",
        "DLF": "DLF.NS",
        "Interglobe Aviation": "INDIGO.NS",
        "Tata Steel": "TATASTEEL.NS",
        "Indian Oil Corporation": "IOC.NS",
        "Vedanta": "VEDL.NS",
        "Tech Mahindra": "TECHM.NS",
        "IRFC": "IRFC.NS",
        "Grasim Industries": "GRASIM.NS",
        "LTI Mindtree": "LTIM.NS"
    }
    
    # Create reverse mapping for direct ticker lookup
    TICKER_TO_COMPANY = {ticker: company for company, ticker in NIFTY50_TICKERS.items()}

    def get(self, request, symbol):
        # Validate time range
        # print("Okay printing", symbol)
        time_range = request.GET.get("time_frame", "1M")
        # print(f"Time frame received: {time_range}")  # Debugging line

        if time_range not in self.TIME_RANGES_MAPPING:
            return JsonResponse({"error": f"Invalid time range: {time_range}"}, status=400)

        # Handle symbol matching more flexibly
        symbol_ticker = None
        
        # Direct match if it's already a ticker
        if symbol.endswith(".NS"):
            symbol_ticker = symbol
        else:
            # Try to find symbol as a company name
            symbol_ticker = self.NIFTY50_TICKERS.get(symbol.strip())
            
            # If not found, try case-insensitive exact match
            if not symbol_ticker:
                for company, ticker in self.NIFTY50_TICKERS.items():
                    if company.lower() == symbol.lower().strip():
                        symbol_ticker = ticker
                        break
            
            # If still not found, check if symbol itself is a ticker prefix (without .NS)
            if not symbol_ticker:
                potential_ticker = f"{symbol.strip().upper()}.NS"
                if potential_ticker in self.NIFTY50_TICKERS.values():
                    symbol_ticker = potential_ticker

        if not symbol_ticker:
            return JsonResponse({"error": f"Invalid symbol: {symbol}"}, status=400)

        # Calculate start date
        start_date = timezone.now() - self.TIME_RANGES_MAPPING[time_range]

        # Fetch stored data from the database
        stock_data = Nifty50GraphHistory.objects.filter(
            symbol=symbol_ticker,
            date__gte=start_date,
            time_range=time_range
        ).values("date", "open_price", "high_price", "low_price", "close_price", "volume").order_by("date")

        # Convert queryset to a list
        data = [
            {
                "date": record["date"].strftime("%Y-%m-%d"),
                "open_price": record["open_price"],
                "high_price": record["high_price"],
                "low_price": record["low_price"],
                "close_price": record["close_price"],
                "volume": record["volume"],
            }
            for record in stock_data
        ]

        # Handle empty data response
        return JsonResponse({
            "symbol": symbol_ticker,
            "time_range": time_range,
            "data": data
        }, status=200)



class BSE500StockView(View):
    def addbse500data(self, request):
        obj = BSE_Data()
        data = obj.bse_data()  # Fetch stock data

        for company_name, stock_data in data.items():  # Iterate over companies
            try:
                BSE_500_Stocks.objects.update_or_create(
                    company_name=company_name,  # Lookup field
                    defaults={  # Fields to update
                        "fifty_two_week_high": float(stock_data["52W_High"].replace(",", "").strip()),
                        "fifty_two_week_low": float(stock_data["52W_Low"].replace(",", "").strip()),
                        "dividend_yield": self.safe_float(stock_data["Dividend"]),
                        "book_value": self.safe_float(stock_data["PB_Ratio"]),
                        "earnings_yield": round(1 / float(stock_data["PE_Ratio"]), 4) if self.safe_float(stock_data["PE_Ratio"]) else None,
                        "dividend_payout_ratio": self.safe_float(stock_data["Dividend"]),
                        "avg_volume": self.safe_int(stock_data["Volume"]),
                        "exchange": "BSE",  # Assuming all stocks are from BSE
                        "eps": self.safe_float(stock_data["EPS"]),
                        "price_perchng_1mon": self.safe_float(stock_data["1M__Returns"]),
                        "price_perchng_3mon": self.safe_float(stock_data["3M__Returns"]),
                        "price_perchng_1year": self.safe_float(stock_data["1_Yr_Returns"]),
                        "price_perchng_3year": self.safe_float(stock_data["3_Yr_Returns"]),
                        "price_perchng_5year": self.safe_float(stock_data["5_Yr_Returns"]),
                    }
                )
            except ValueError as e:
                print(f"Error processing {company_name}: {e}")

    def safe_float(self, value):
        """ Convert a string to float safely, handling commas, whitespace, and 'NA' values. """
        try:
            return float(value.replace(",", "").replace("%", "").strip()) if value not in ["NA", ""] else None
        except ValueError:
            return None

    def safe_int(self, value):
        """ Convert a string to int safely, handling commas and 'NA' values. """
        try:
            return int(value.replace(",", "").strip()) if value not in ["NA", ""] else None
        except ValueError:
            return None

    def get(self, request):
        self.addbse500data(request)
        return JsonResponse({"context": "success"})



class BseStockDetailsView(View):
    def get(self, request, symbol):
        # Fetch the stock details from the database
        stock_detail = get_object_or_404(BSE_500_Stocks, company_name__icontains=symbol)
        company_name = stock_detail.company_name
        LiveData = BSE_Live_Data()
        LiveData = dict(LiveData.get_company_data(company_name))
        # Convert the stock details to a dictionary
        stock_dict = model_to_dict(stock_detail)  # Converts the model instance to a dictionary
        stock_dict.update(LiveData)  # Merge live data into the stock dictionary
        return JsonResponse({"stock": stock_dict})
    
class BSEGraphView(View):
    def get(self, request, symbol):
        
        """Handles GET requests and fetches 1-minute interval stock data."""
        
        symbol = tickers[symbol]  # Example stock symbol
        data = self.fetch_stock_data(f"{symbol}.BO")
        return JsonResponse({"symbol": symbol, "data": data})  # JSON response

    def fetch_stock_data(self, symbol, period="1d", interval="1m"):
        """Fetch stock data at 1-minute intervals from Yahoo Finance."""
        ticker = yf.Ticker(f"{symbol}")  # Example stock symbol
        df = ticker.history(period=period, interval=interval)

        if df.empty:
            return []  # Return empty list if no data is available

        df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')  # Convert index to readable string format

        # Convert DataFrame to a dictionary format
        stock_data = df[['Close']].reset_index()
        stock_data.rename(columns={"Datetime": "date", "Close": "close_price"}, inplace=True)

        return stock_data.to_dict(orient='records')  # JSON-friendly format
    


#------------------------------------------------------------------
#Fetch BSE 500 stock graph data from y finance API 

class FetchBSEMonthYearStockGraphDataView(View):
    TIME_RANGES_MAPPING = {
        "1M": "1mo",
        "6M": "6mo",
        "1Y": "1y",
        "3Y": "3y",
        "5Y": "5y",
        "10Y": "10y",
    }

    BSE_500_STOCK = ['GMRAIRPORT', 'TATAMOTORS', 'DIXON', 'RELIANCE', 'TCS', 'INFY', 'KALYANKJIL', 'MAZDOCK', 'HDFCBANK', 'TATASTEEL', 'CELLO', 'HAL', 'BEL', 'SUZLON', 'HINDUNILVR', 'SBIN', 'FINPIPE', 'KAYNES', 'LT', 'ADANIGREEN', 'TRENT', 'BAJFINANCE', 'HCLTECH', 'BHARTIARTL', 'MASTEK', 'HINDALCO', 'LUPIN', 'ADANIPOWER', 'KOTAKBANK', 'VEDL', 'MUTHOOTFIN', 'ADANIENT', 'AMBUJACEM', 'JIOFIN', 'M&M', 'COCHINSHIP', 'COFORGE', 'ICICIBANK', 'NBCC', 'COALINDIA', 'SIEMENS', 'AMBER', 'TEJASNET', 'ONGC', 'REC', 'BDL', 'TATAPOWER', 'TITAN', 'ATUL', 'POLYCAB', 'WIPRO', 'ADANIPORTS', 'PAYTM', 'HUDCO', 'ITC', 'PIIND', 'AXISBANK', 'PERSISTENT', 'BAJAJFINSV', 'NTPC', 'CIPLA', 'NATIONALUM', 'PNBHOUSING', 'ANANTRAJ', 'MOTILALOFS', 'MOTHERSON', 'CANBK', 'KPITTECH', 'PFC', 'RVNL', 'NESTLEIND', 'JINDALSTEL', 'POWERGRID', 'IREDA', 'HINDPETRO', 'JSWSTEEL', 'HBLENGINE', 'BANKBARODA', 'ADANIENSOL', 'GRSE', 'UJJIVANSFB', 'DMART', 'NH', 'SUNPHARMA', 'WELSPUNLIV', 'MCX', 'SAIL', 'COROMANDEL', 'LAURUSLABS', 'INDUSINDBK', 'OLECTRA', 'ZEEL', 'CGPOWER', 'CHENNPETRO', 'VBL', 'BANKINDIA', 'AARTIIND', 'EASEMYTRIP', 'SRF', 'INDIGO', 'BLS', 'APLAPOLLO', 'NHPC', 'TATAELXSI', 'BHEL', 'CHAMBLFERT', 'LTIM', 'IDFCFIRSTB', 'ASAHIINDIA', 'MARUTI', 'ASIANPAINT', 'IRFC', 'DLF', 'TATACONSUM', 'PAGEIND', 'SONACOMS', 'BEML', 'SOLARINDS', 'YESBANK', 'NMDC', 'DRREDDY', 'DELHIVERY', 'ANGELONE', 'MRF', 'TRITURBINE', 'CHOLAFIN', 'DIVISLAB', 'PNB', 'BIOCON', 'VOLTAS', 'IRB', 'JWL', 'LICI', 'HSCL', 'HINDCOPPER', 'BPCL', 'ASTRAL', 'CAMS', 'MAXHEALTH', 'INOXWIND', 'INDUSTOWER', 'HINDZINC', 'GODREJPROP', 'IOC', 'NATCOPHARM', 'LODHA', 'ZYDUSLIFE', 'BHARATFORG', 'AFFLE', 'DABUR', 'UNIONBANK', 'IOB', 'PCBL', 'JYOTHYLAB', 'INDHOTEL', 'SWANENERGY', 'ULTRACEMCO', 'SHRIRAMFIN', 'HAVELLS', 'RKFORGE', 'CASTROLIND', 'BAJAJ-AUTO', 'DEEPAKFERT', 'OIL', '360ONE', 'ATGL', 'TITAGARH', 'IGL', 'REDINGTON', 'AEGISLOG', 'NEWGEN', 'KEI', 'PATANJALI', 'COLPAL', 'TECHM', 'AAVAS', 'ACI', 'GAIL', 'TANLA', 'TATACHEM', 'JSWENERGY', 'POWERINDIA', 'FSL', 'NCC', 'JBMA', 'SJVN', 'MANAPPURAM', 'HDFCAMC', 'MAHABANK', 'J&KBANK', 'NAUKRI', 'HFCL', 'PPLPHARMA', 'SWSOLAR', 'BHARTIHEXA', 'GODREJCP', 'APOLLOHOSP', 'AUROPHARMA', 'UPL', 'ZENSARTECH', 'CHOLAHLDNG', 'FORTIS', 'LLOYDSME', 'TATATECH', 'IRCTC', 'POLICYBZR', 'GRASIM', 'FEDERALBNK', 'HDFCLIFE', 'ABCAPITAL', 'LICHSGFIN', 'BAJAJHLDNG', 'GLENMARK', 'GRANULES', 'TRIDENT', 'PVRINOX', 'DATAPATTNS', 'MARICO', 'ARE&M', 'TORNTPOWER', 'JUBLFOOD', 'NAM-INDIA', 'UCOBANK', 'ABB', 'IIFL', 'MRPL', 'TECHNOE', 'MEDANTA', 'IFCI', 'DEVYANI', 'CENTRALBK', 'BLUESTARCO', 'EXIDEIND', 'MFSL', 'APOLLOTYRE', 'JUBLPHARMA', 'BRITANNIA', 'HAPPSTMNDS', 'MGL', 'PHOENIX', 'HEROMOTOCO', 'CONCOR', 'AUBANK', 'NYKAA', 'OFSS', 'CCL', 'LTF', 'POONAWALLA', 'KFINTECH', 'ICICIPRULI', 'MANKIND', 'MPHASIS', 'RCF', 'PRAJIND', 'INTELLECT', 'NAVINFLUOR', 'VTL', 'HOMEFIRST', 'RAINBOW', 'KIRLOSBROS', 'ELGIEQUIP', 'CUB', 'ANANDRATHI', 'GSPL', 'EICHERMOT', 'GLAND', 'IDBI', 'JUBLINGREA', 'BOSCH', 'ASHOKLEY', 'AWL', 'BALKRISIND', 'JUSTDIAL', 'PIDILITIND', 'ICICIGI', 'ESCORTS', 'TVSMOTOR', 'GODFRYPHLP', 'OBEROIRLTY', 'ASTRAZEN', 'GESHIP', 'TIINDIA', 'ENGINERSIN', 'BANDHANBNK', 'UNOMINDA', 'KEC', 'TATAINVEST', 'CEAT', 'KNRCON', 'CYIENT', 'IRCON', 'JSL', 'M&MFIN', 'GODREJAGRO', 'RITES', 'RBLBANK', 'WELCORP', 'HEG', 'KPRMILL', 'CREDITACC', 'NUVAMA', 'NLCINDIA', 'TTML', 'IEX', 'FLUOROCHEM', 'MAPMYINDIA', 'CUMMINSIND', 'GRAPHITE', 'ABFRL', 'ASTERDM', 'PSB', 'APARINDS', 'TATACOMM', 'SUPREMEIND', 'KIRLOSENG', 'SAMMAANCAP', 'BSOFT', 'JKCEMENT', 'JINDALSAW', 'BERGEPAINT', 'SIGNATURE', 'SHREECEM', 'KAMAHOLD', 'ABREL', 'NSLNISP', 'RAJESHEXPO', 'POLYMED', 'BIKAJI', 'ACC', 'LTTS', 'ALKYLAMINE', 'ERIS', 'GILLETTE', 'SUNTV', 'JMFINANCIL', 'SBICARD', 'RHIM', 'GSFC', 'MMTC', 'SONATSOFTW', 'LALPATHLAB', 'SHYAMMETL', 'STARHEALTH', 'SUMICHEM', 'CRISIL', 'RENUKA', 'MAHSEAMLES', 'MAHLIFE', 'JSWINFRA', 'RAMCOCEM', 'APL', 'PRESTIGE', 'KAJARIACER', 'UNITDSPR', 'CGCL', 'CROMPTON', 'SCHNEIDER', 'GLAXO', 'LEMONTREE', 'TIMKEN', 'NETWORK18', 'SBILIFE', 'GMDC', 'FIVESTAR', 'GODREJIND', 'INDIANB', 'MANYAVAR', 'PEL', 'WHIRLPOOL', 'MEDPLUS', 'RRKABEL', 'BALRAMCHIN', 'BALAMINES', 'TVSH', 'SUVENPHAR', 'CHALET', 'EQUITASBNK', 'PTCIL', '3MINDIA', 'BRIGADE', 'ENDURANCE', 'GPPL', 'FINCABLES', 'ABSLAMC', 'IPCALAB', 'LINDEINDIA', 'ANURAS', 'FINEORG', 'CESC', 'ACE', 'TBOTEK', 'GNFC', 'GICRE', 'ROUTE', 'UTIAMC', 'PETRONET', 'KIMS', 'BATAINDIA', 'SANOFI', 'EIHOTEL', 'SPARC', 'EIDPARRY', 'CONCORDBIO', 'ZFCVINDIA', 'ECLERX', 'BASF', 'MSUMI', 'KANSAINER', 'CLEAN', 'PFIZER', 'JBCHEPHARM', 'THERMAX', 'BBTC', 'CANFINHOME', 'SAPPHIRE', 'ITI', 'MIDHANI', 'SUNTECK', 'CAMPUS', 'MAHSCOOTER', 'CARBORUNIV', 'LATENTVIEW', 'ABBOTINDIA', 'LMW', 'TORNTPHARM', 'RELAXO', 'BIRLACORPN', 'SOBHA', 'INDIACEM', 'PNCINFRA', 'GODIGIT', 'AIIL', 'KPIL', 'MINDACORP', 'CENTURYPLY', 'EMAMI', 'AIAENG', 'APTUS', 'METROPOLIS', 'USHAMART', 'DALBHARAT', 'CRAFTSMAN', 'PGHH', 'SUNDRMFAST', 'RADICO', 'GRINFRA', 'VGUARD', 'VINATIORGA', 'ZYDUSWELL', 'NIACL', 'GALAXYSURF', 'SYNGENE', 'LXCHEM', 'AJANTPHARM', 'FDC', 'INDIAMART', 'BAYERCROP', 'BLUEDART', 'AETHER', 'UBL', 'SCHAEFFLER', 'HONASA', 'MHRIL', 'CERA', 'METROBRAND', 'SKFINDIA', 'HATSUN', 'INGERRAND', 'DCMSHRIRAM', 'NUVOCO', 'GRINDWELL', 'ALKEM', 'TTKPRESTIG', 'SFL', 'GARFIBRES', 'VARROC', 'STARCEMENT', 'HONAUT', 'ESABINDIA', 'SPLPETRO', 'CIEINDIA', 'TMB', 'AKZOINDIA', 'SHOPERSTOP', 'PRSMJOHNSN', 'RATNAMANI', 'PGHL', 'WESTLIFE', 'KIOCL', 'JKLAKSHMI', 'CHEMPLASTS']

    def get(self, request):
        try:
            for i, stock_symbol in enumerate(self.BSE_500_STOCK):
                stock = yf.Ticker("stock_symbol")

                for time_range, period in self.TIME_RANGES_MAPPING.items():
                    data = stock.history(period=period, interval="1d")
                    if data.empty:
                        continue

                    # Fetch existing records as a dictionary
                    existing_records = {
                        (entry.date.date(), entry.time_range): entry
                        for entry in Nifty50GraphHistory.objects.filter(
                            symbol=stock_symbol,
                            time_range=time_range
                        )
                    }

                    new_entries = []
                    updated_entries = []

                    for index, row in data.iterrows():
                        date = make_aware(datetime.strptime(str(index.date()), "%Y-%m-%d"))

                        record_key = (date.date(), time_range)  # Compare only the DATE

                        if record_key in existing_records:
                            #   Update existing record
                            record = existing_records[record_key]
                            record.open_price = row["Open"]
                            record.high_price = row["High"]
                            record.low_price = row["Low"]
                            record.close_price = row["Close"]
                            record.volume = row["Volume"]
                            updated_entries.append(record)
                        else:
                            #   Create new record
                            new_entries.append(Nifty50GraphHistory(
                                symbol=stock_symbol,
                                date=date,
                                time_range=time_range,
                                open_price=row["Open"],
                                high_price=row["High"],
                                low_price=row["Low"],
                                close_price=row["Close"],
                                volume=row["Volume"],
                            ))

                    #   Bulk Insert & Update in an atomic transaction
                    with transaction.atomic():
                        if new_entries:
                            BSE500GraphHistory.objects.bulk_create(new_entries)
                        if updated_entries:
                            BSE500GraphHistory.objects.bulk_update(
                                updated_entries,
                                ["open_price", "high_price", "low_price", "close_price", "volume"]
                            )

                #   Prevent API rate limit issues
                if (i + 1) % 5 == 0:
                    time.sleep(2)

            return JsonResponse({"message": "Stock data fetched, updated, and saved successfully."})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

#------------------------------------------------------------------
#Fetch BSE 500 stock graph data from model

class GetBSEMonthAndYearStockGraphDataView(View):
    
    TIME_RANGES_MAPPING = {
        "1M": timedelta(days=30),
        "6M": timedelta(days=180),
        "1Y": timedelta(days=365),
        "3Y": timedelta(days=3*365),
        "5Y": timedelta(days=5*365),
        "10Y": timedelta(days=10*365),
    }

    
    # Create reverse mapping for direct ticker lookup
    TICKER_TO_COMPANY = {ticker: company for company, ticker in tickers.items()}

    def get(self, request, symbol):
        # Validate time range
        # print("Okay printing", symbol)
        time_range = request.GET.get("time_frame", "1M")
        # print(f"Time frame received: {time_range}")  # Debugging line

        if time_range not in self.TIME_RANGES_MAPPING:
            return JsonResponse({"error": f"Invalid time range: {time_range}"}, status=400)

        # Handle symbol matching more flexibly
        symbol_ticker = None
        
        # Direct match if it's already a ticker
        if symbol.endswith(".BO"):
            symbol_ticker = symbol
        else:
            # Try to find symbol as a company name
            symbol_ticker = tickers.get(symbol.strip())
            
            # If not found, try case-insensitive exact match
            if not symbol_ticker:
                for company, ticker in self.NIFTY50_TICKERS.items():
                    if company.lower() == symbol.lower().strip():
                        symbol_ticker = ticker
                        break
            
            # If still not found, check if symbol itself is a ticker prefix (without .NS)
            if not symbol_ticker:
                potential_ticker = f"{symbol.strip().upper()}.BO"
                if potential_ticker in self.NIFTY50_TICKERS.values():
                    symbol_ticker = potential_ticker

        if not symbol_ticker:
            return JsonResponse({"error": f"Invalid symbol: {symbol}"}, status=400)

        # Calculate start date
        start_date = timezone.now() - self.TIME_RANGES_MAPPING[time_range]

        # Fetch stored data from the database
        stock_data = BSE500GraphHistory.objects.filter(
            symbol=symbol_ticker,
            date__gte=start_date,
            time_range=time_range
        ).values("date", "open_price", "high_price", "low_price", "close_price", "volume").order_by("date")

        # Convert queryset to a list
        data = [
            {
                "date": record["date"].strftime("%Y-%m-%d"),
                "open_price": record["open_price"],
                "high_price": record["high_price"],
                "low_price": record["low_price"],
                "close_price": record["close_price"],
                "volume": record["volume"],
            }
            for record in stock_data
        ]

        # Handle empty data response
        return JsonResponse({
            "symbol": symbol_ticker,
            "time_range": time_range,
            "data": data
        }, status=200)
