
---

##  Features & Responsibilities

- **Web Scraping**  
  - `BalanceSheet.py`: Scrapes company balance sheets from Screener.in using BeautifulSoup.  
  - `BSE_500_stock_data.py`: Scrapes BSE 500 stock list from Dhan.co.  
  - `BSE_Live_Data.py`: Provides real-time metrics (LTP, PE, PB, RSI, etc.) for BSE-listed companies.

- **Stock Data Fetching**  
  - `bsegraphdata.py`: Retrieves historical stock data using `yfinance`, supports timeframes from 1 month to 10 years via bulk downloads.

- **Ticker Mappings**  
  - `BSEtickers.py`: Contains mappings for company names to limited ticker symbols and URL slugs.

- **REST APIs & Data Models**  
  - `models.py`, `serializers.py`, and `views.py`: Define data structures, serialization, and API logic.
  - `urls.py`: Routes for the StockDetail app.

- **Django Configuration**  
  - `Backend/settings.py`: Standard Django setup with installed apps (`rest_framework`, `corsheaders`, `StockDetail`), CORS (`http://localhost:5173`), database using SQLite, and development configs.
  - `Backend/urls.py`: Includes admin and StockDetail app routes.

- **Admin Site**  
  - `admin.py`: Registers models for Django admin, complete with custom model views (e.g., `Nifty50GraphHistoryAdmin`, `BSE500GraphHistoryAdmin`) for filtering, search, and pagination.

---

##  Getting Started

```bash
# 1. Create virtual environment & activate
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# 2. Install dependencies
pip install -r requirment.txt

# 3. Setup database
python manage.py migrate

# 4. Run development server
python manage.py runserver

# 5. API endpoints are available under the routes defined in StockDetail/urls.py
