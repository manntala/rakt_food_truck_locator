from rest_framework import serializers
from .models import FoodTruck

class FoodTruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodTruck
        fields = ['id', 'applicant', 'facility_type', 'location_description', 'address', 'latitude', 'longitude', 'food_items']