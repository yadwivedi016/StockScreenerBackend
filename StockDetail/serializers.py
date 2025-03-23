from rest_framework import serializers
from .models import StockDetail

class StockDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockDetail
        fields = '__all__'  # or list specific fields you want to serialize
