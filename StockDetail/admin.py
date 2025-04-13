from django.contrib import admin
from .models import StockDetail, Sector, Nifty50GraphHistory,BSE_500_Stocks,BSE500GraphHistory

# Register your other models
admin.site.register(Sector)
admin.site.register(StockDetail)
admin.site.register(BSE_500_Stocks)
admin.site.register(BSE500GraphHistory)

# Define custom admin class for Nifty50GraphHistory
class Nifty50GraphHistoryAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ("symbol", "date", "time_range", "open_price", "high_price", "low_price", "close_price", "volume")
    
    # Add filters to easily filter by time range, symbol, and date
    list_filter = ("symbol", "time_range", "date")
    
    # Enable searching by symbol and date
    search_fields = ("symbol", "date")
    
    # Add fields for better display on the detail view (form layout)
    fields = ("symbol", "date", "time_range", "open_price", "high_price", "low_price", "close_price", "volume")
    
    # List view pagination settings
    list_per_page = 25

# Register the custom admin class for Nifty50GraphHistory
admin.site.register(Nifty50GraphHistory, Nifty50GraphHistoryAdmin)
