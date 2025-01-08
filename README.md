RAKT Food Truck locator

NOTE: Most of the coordinates of the Food trucks are near San Francisco, latitude=37.7601&longitude=-122.4188. It is best to select coordinates near this area.

INSTALLATION:
1. Create virtual environment then activate
    Command:
    python3 -m venv venv
    bash: source venv/bin/activate

2. Run requirements/dependencies
    Command: pip install -r requirements.txt

3. Run migration
    Command: python manage.py migrate

4. Run the server
    Command: python manage.py runserver

5. Usable endpoints
    http://localhost:8000/api/?latitude=37.7601&longitude=-122.4188
    http://localhost:8000/api/map/

APP FUNCTIONS
1. APIView - NearestFoodTrucks
    URL: http://localhost:8000/api/?latitude=37.7601&longitude=-122.4188
    GET method: 
    Will return the food trucks based on the latitude and longitude on the parameters.

2. TemplateView - FoodTruckMapView
    GET Method:
    Will return form to input Latitude and Longitude

    POST Method:
    Will return the nearest food trucks based on the Latitude and Longitude of the User's location

    Usage: Input the data in the form
    Latitude: 37.7601
    Longitude=-122.4188

3. BaseCommand to load the CSV data to the DB
    food_trucks/management/command/load_food_trucks_csv.py
    Command: python manage.py load_food_trucks_csv