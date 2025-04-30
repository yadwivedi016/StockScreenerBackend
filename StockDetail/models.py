from django.db import models

# Create your models here.
from django.db import models

class Sector(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
class StockDetail(models.Model):
    company_name = models.CharField(max_length=255) 
    fifty_two_week_high = models.FloatField(null=True, blank=True)
    fifty_two_week_low = models.FloatField(null=True, blank=True)
    dividend_yield = models.FloatField(null=True, blank=True)
    book_value = models.FloatField(null=True, blank=True)
    enterprise_value = models.FloatField(null=True, blank=True)
    earnings_yield = models.FloatField(null=True, blank=True)  
    peg_ratio = models.FloatField(null=True, blank=True)
    dividend_payout_ratio = models.FloatField(null=True, blank=True)
    avg_volume = models.BigIntegerField(null=True, blank=True)  
    exchange = models.CharField(max_length=255, null=True, blank=True)  
    eps = models.FloatField(null=True, blank=True)
    year_revenue_growth = models.FloatField(null=True, blank=True)
    price_perchng_1mon = models.FloatField(null=True, blank=True)
    price_perchng_1year = models.FloatField(null=True, blank=True)
    price_perchng_3mon = models.FloatField(null=True, blank=True)
    price_perchng_3year = models.FloatField(null=True, blank=True)
    price_perchng_5year = models.FloatField(null=True, blank=True)
    roce = models.FloatField(null=True, blank=True)   
    revenue = models.FloatField(null=True, blank=True)


    def __str__(self):
        return self.company_name


class Nifty50GraphHistory(models.Model):
    TIME_RANGES = [
        ("1M", "1 Month"),
        ("6M", "6 Months"),
        ("1Y", "1 Year"),
        ("3Y", "3 Years"),
        ("5Y", "5 Years"),
        ("10Y", "10 Years"),
    ]

    symbol = models.CharField(max_length=10)  # Stock symbol
    date = models.DateField()  # Date of entry
    time_range = models.CharField(max_length=5, choices=TIME_RANGES)  # Time range (1M, 6M, etc.)

    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ("symbol", "date", "time_range")  # Prevent duplicates
        ordering = ["-date"]

    def __str__(self):
        return f"{self.symbol} - {self.time_range} - {self.date}"

    

class BSE_500_Stocks(models.Model):
    company_name = models.CharField(max_length=255)          
    fifty_two_week_high = models.FloatField(null=True, blank=True)
    fifty_two_week_low = models.FloatField(null=True, blank=True)
    dividend_yield = models.FloatField(null=True, blank=True)
    book_value = models.FloatField(null=True, blank=True)
    earnings_yield = models.FloatField(null=True, blank=True)
    dividend_payout_ratio = models.FloatField(null=True, blank=True)
    avg_volume = models.FloatField(null=True, blank=True)
    exchange = models.CharField (max_length=10, default="BSE")
    eps = models.FloatField(null=True, blank=True)
    price_perchng_1mon = models.FloatField(null=True, blank=True)
    price_perchng_3mon = models.FloatField(null=True, blank=True)
    price_perchng_1year = models.FloatField(null=True, blank=True)
    price_perchng_3year = models.FloatField(null=True, blank=True)
    price_perchng_5year = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.company_name

class BSE500GraphHistory(models.Model):
    TIME_RANGES = [
        ("1M", "1 Month"),
        ("6M", "6 Months"),
        ("1Y", "1 Year"),
        ("3Y", "3 Years"),
        ("5Y", "5 Years"),
        ("10Y", "10 Years"),
    ]

    symbol = models.CharField(max_length=10)  # Stock symbol
    date = models.DateField()  # Date of entry
    time_range = models.CharField(max_length=5, choices=TIME_RANGES)  # Time range (1M, 6M, etc.)

    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ("symbol", "date", "time_range")  # Prevent duplicates
        ordering = ["-date"]

    def __str__(self):
        return f"{self.symbol} - {self.time_range} - {self.date}"




from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class BalanceSheet(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    year = models.CharField(max_length=10)

    share_capital = models.CharField(max_length=100, blank=True, null=True)
    reserve_and_surplus = models.CharField(max_length=100, blank=True, null=True)
    minority_interest = models.CharField(max_length=100, blank=True, null=True)
    non_current_liabilities = models.CharField(max_length=100, blank=True, null=True)
    current_liabilities = models.CharField(max_length=100, blank=True, null=True)
    total_liabilities = models.CharField(max_length=100, blank=True, null=True)

    fixed_assets = models.CharField(max_length=100, blank=True, null=True)
    capital_work_in_progress = models.CharField(max_length=100, blank=True, null=True)
    investments = models.CharField(max_length=100, blank=True, null=True)
    other_assets = models.CharField(max_length=100, blank=True, null=True)
    total_assets = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.company.name} - {self.year}"


