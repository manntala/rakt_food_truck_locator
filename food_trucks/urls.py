from django.urls import path
from food_trucks.views import NearestFoodTrucks, FoodTruckMapView

urlpatterns = [
    path('', NearestFoodTrucks.as_view(), name='nearest_food_trucks'),
    path("map/", FoodTruckMapView.as_view(), name="food_trucks_api"),
    
    # http://localhost:8000/api/map/?latitude=37.7601&longitude=-122.4188

]