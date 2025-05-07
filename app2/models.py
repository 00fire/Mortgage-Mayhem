from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    
# class User2(models.Model):
#     username = models.CharField(max_length=255)
#     password = models.CharField(max_length=255)

class Properties(models.Model):
    property_country = models.CharField(max_length=50)
    property_street = models.CharField(max_length=255)
    property_city = models.CharField(max_length=255)
    property_postal = models.CharField(max_length=255)
    property_price = models.DecimalField(max_digits=20,decimal_places=2)
    property_description = models.TextField()
    property_rooms = models.IntegerField()
    property_bedrooms = models.IntegerField()
    property_bathrooms = models.IntegerField()
    property_square_meters_size = models.DecimalField(max_digits=10,decimal_places=3)
    property_sold_status = models.BooleanField()
    
 