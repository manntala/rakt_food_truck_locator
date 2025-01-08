import csv
from django.core.management.base import BaseCommand
from food_trucks.models import FoodTruck

class Command(BaseCommand):
    help = 'Load food truck data from CSV'

    def handle(self, *args, **kwargs):
        with open('food-truck-data.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                FoodTruck.objects.create(
                    applicant=row['Applicant'],
                    facility_type=row['FacilityType'],
                    location_description=row['LocationDescription'],
                    address=row['Address'],
                    latitude=float(row['Latitude']),
                    longitude=float(row['Longitude']),
                    food_items=row['FoodItems'],
                    status=row['Status']
                )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))
