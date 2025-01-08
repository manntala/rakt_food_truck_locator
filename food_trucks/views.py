from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FoodTruck
from .serializers import FoodTruckSerializer
from geopy.distance import geodesic
from django.core.serializers import serialize
from rest_framework.exceptions import NotFound

import logging

logger = logging.getLogger(__name__)

def get_nearest_trucks(latitude, longitude):
    """
    Helper method to find and return the nearest food trucks.
    """
    latitude = float(latitude)
    longitude = float(longitude)

    user_location = (latitude, longitude)

    # Calculate distances and filter top 5
    trucks = FoodTruck.objects.all()
    trucks_with_distance = [
        (truck, geodesic(user_location, (truck.latitude, truck.longitude)).miles)
        for truck in trucks
    ]
    trucks_with_distance.sort(key=lambda x: x[1])
    nearest_trucks = [truck[0] for truck in trucks_with_distance[:5]]

    return nearest_trucks

class NearestFoodTrucks(APIView):
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests, accepts latitude and longitude as query parameters.
        """
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')

        # Validate latitude and longitude
        if not latitude or not longitude:
            return Response(
                {"error": "latitude and longitude query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            return Response(
                {"error": "latitude and longitude must be valid numbers."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get nearest food trucks
        nearest_trucks = get_nearest_trucks(latitude, longitude)

        if not nearest_trucks:
            raise NotFound(detail="No food trucks found nearby.")

        # Serialize the nearest trucks
        serialized_trucks = FoodTruckSerializer(nearest_trucks, many=True).data

        return Response(serialized_trucks, status=status.HTTP_200_OK)

    
class FoodTruckMapView(TemplateView):
    template_name = "food_trucks/food_trucks_map.html"

    def get_context_data(self, **kwargs):
            """
            Handles GET requests, renders the form for latitude and longitude input.
            """
            context = super().get_context_data(**kwargs)
            context["error"] = ""  # Initialize error as an empty string
            return context


    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, accepts latitude and longitude in the request body.
        """
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if not latitude or not longitude:
            context = {
                "error": "Latitude and longitude are required in the request body.",
            }
            logger.error("Latitude and longitude are missing in the POST request.")
            return self.render_to_response(context)

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            context = {
                "error": "Invalid latitude or longitude values.",
            }
            logger.error(f"Invalid latitude or longitude values in POST request: {latitude}, {longitude}")
            return self.render_to_response(context)

        nearest_trucks = get_nearest_trucks(latitude, longitude)

        if not nearest_trucks:
            context["error"] = "No food trucks found nearby."
            logger.warning("No food trucks found to display in POST request.")
        else:
            food_trucks_serialized = serialize('json', nearest_trucks)
            logger.info(f"Serialized food trucks data from POST request: {food_trucks_serialized}")

            context = {
                "food_trucks": food_trucks_serialized,
                "latitude": latitude,
                "longitude": longitude,
                "error": "",
            }
        
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        if context.get("food_trucks"):  # Check if serialized data exists
            logger.info("Returning food truck map view with food truck data.")
            context["food_trucks_display"] = context["food_trucks"]  # This allows access in the template
        else:
            logger.warning("No food trucks found to display.")
            context["error"] = "No food trucks found nearby."

        return super().render_to_response(context, **response_kwargs)
