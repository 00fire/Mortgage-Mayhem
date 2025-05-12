from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio=models.TextField(max_length=500, blank=True,null=True)
    profile_picture= models.ImageField(upload_to='profile_pics/',default='default.jpg')
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
    
    property_image=models.ImageField(upload_to='propert_images/',blank=True,null=True)
    #property_available_from=models.DateField()
    #property_available_to= models.DateField()
    #property_owner=models.ForeignKey(User,on_delete)
    #property_
    
    def __str__(self):
            return f"{self.property_street}, {self.property_city}, {self.property_country}"