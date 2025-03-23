from django.urls import path
from .views import AddNifty50StockView, StockDetailsView, SearchView,GraphView,FetchNifty50StockGraphDataView,GetNifty50StockGraphDataView

urlpatterns = [
    path("", SearchView.as_view(), name="search-view"),  # Search page
    path("stockdetail/<str:symbol>/", StockDetailsView.as_view(), name="stock-detail-view"),  # Stock detail page
    path("add/", AddNifty50StockView.as_view(), name="add-Nifty-50-Stock-View"),  # Add Nifty50 stocks,
    path('graph/<str:symbol>/', GraphView.as_view(), name='graph'),
    path("fetch-graph-data/", FetchNifty50StockGraphDataView.as_view(), name="fetch-graph-data-view"),
    path('get-graph-data/<str:symbol>/', GetNifty50StockGraphDataView.as_view(), name='get-graph-data-view'),
    
]
