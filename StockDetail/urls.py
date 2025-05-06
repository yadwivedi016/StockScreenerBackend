from django.urls import path
from .views import AddNifty50StockView, StockDetailsView, SearchView, GraphView, FetchNifty50StockGraphDataView, GetNifty50StockGraphDataView, BSE500StockView, BseStockDetailsView, BSEGraphView, GetBSEMonthAndYearStockGraphDataView, FetchBSEMonthYearStockGraphDataView, BalanceSheetScraperView, BalanceSheetDataView

urlpatterns = [
    path("", SearchView.as_view(), name="search-view"),  # Search page
   
    path("stockdetail/<str:symbol>/", StockDetailsView.as_view(), name="stock-detail-view"),  # Stock detail page
   
    path("add-nifty50-data/", AddNifty50StockView.as_view(), name="add-Nifty-50-Stock-View"),  # Add Nifty50 stocks,
   
    path('graph/<str:symbol>/', GraphView.as_view(), name='graph'),
   
    path("fetch-graph-data/", FetchNifty50StockGraphDataView.as_view(), name="fetch-graph-data-view"),
   
    path('get-graph-data/<str:symbol>/', GetNifty50StockGraphDataView.as_view(), name='get-graph-data-view'),
   
    path('add-bse-500-stock-data/', BSE500StockView.as_view(), name='add-bse-500-stock-view'),  # BSE 500 stock data view

    path('fetch-bse-500-stock-data/<str:symbol>/', BseStockDetailsView.as_view(),
    name="fetch-bse-500-stock-data"),

    path('bse-graph/<str:symbol>/', BSEGraphView.as_view(), name='bse-graph'),

    path('bse-year-month-graph-data/<str:symbol>/', GetBSEMonthAndYearStockGraphDataView.as_view(), name='fetch-bse-graph-data-view'),
    
    path("fetch-bse-month-year-graph-data/", FetchBSEMonthYearStockGraphDataView.as_view(), name="fetch-bse-month-year-graph-data-view"),
   
    # path("balance-sheet-fetch", BalanceSheetScraperView.as_view(), name="balance-sheet-fetch-view"),

    # path("balance-sheet-data/", BalanceSheetDataView.as_view(), name="balance_sheet_data"),  # All data
   
    path("balance-sheet-data/<str:company_name>/", BalanceSheetDataView.as_view(), name="balance_sheet_data_company"),  # Data for a specific company
]
