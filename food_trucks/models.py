from django.db import models

class FoodTruck(models.Model):
    applicant = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=255)
    location_description = models.TextField()
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    food_items = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.applicant
