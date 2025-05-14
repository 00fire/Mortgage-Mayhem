from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from .utils.uploads import upload_to_profile, upload_to_property


PROPERTY_TYPE_CHOICES = [
    ('villa',     'Villa'),
    ('house',     'House'),
    ('townhouse', 'Townhouse'),
    ('apartment', 'Apartment'),
    ('castle',    'Castle'),
]



class UserProfile(models.Model):
    ROLE_CHOICES=(('buyer','Buyer'),('seller','Seller'))

    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role=models.CharField(max_length=10,choices=ROLE_CHOICES,default='buyer')
    bio=models.TextField(max_length=500, blank=True,null=True)
    profile_picture = models.ImageField(
        upload_to=upload_to_profile,
        default="profile_pics/default.jpg",
        blank=True,)

    role = models.CharField(max_length=255) # e.g. Buyer/Seller

    acc_made_time = models.DateTimeField(auto_now_add=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal = models.CharField(max_length=20, null=True, blank=True)
    logo = models.ImageField(upload_to='sellers/logos/', null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
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
    property_type=models.CharField(max_length=20,choices=PROPERTY_TYPE_CHOICES,default='house',help_text="most fitting description.")
    property_rooms = models.IntegerField()
    property_bedrooms = models.IntegerField()
    property_bathrooms = models.IntegerField()
    property_square_meters_size = models.DecimalField(max_digits=10,decimal_places=3)
    property_sold_status = models.BooleanField(default=False)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="listings")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="owned_properties",null=True,blank=True,)
    property_image=models.ImageField(upload_to='propert_images/',blank=True,null=True)
    listed_at=models.DateField(auto_now_add=True)
    
    def __str__(self):
            return f"{self.property_street}, {self.property_city}, {self.property_country}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Properties, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="property_images/")
    position    = models.PositiveSmallIntegerField(default=0,help_text="Sort order: lower numbers come first.")
    class Meta:
        ordering = ["position", "pk"]

    def __str__(self):
        return f"{self.property} — img#{self.pk}"



class PurchaseOffer(models.Model):
    STATUS_CHOICES=[('pending',   'Pending'),
        ('accepted',  'Accepted'),
        ('rejected',  'Rejected'),
        ('contingent','Contingent'),
        ('finalized', 'Finalized'),]
    property = models.ForeignKey(Properties, on_delete=models.CASCADE,related_name='offers')
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='offers_made',
        limit_choices_to={'profile__role': 'buyer'}
    )
    offer_price = models.DecimalField(max_digits=12,decimal_places=2)
    expiration_date = models.DateField()
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')  
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = (('property', 'buyer'),)
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.buyer.username} → {self.property.title} @ {self.offer_price}"


class FinalizedOffer(models.Model):
    purchase_offer = models.ForeignKey(PurchaseOffer, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    national_pid = models.CharField(max_length=255)
    pay_method = models.TextField()  # credit/banktransfer/mortgage
    card_name = models.TextField()
    card_num = models.IntegerField()
    expiration_date_card = models.TextField()
    cvc = models.IntegerField()
    bank_acc = models.TextField()
    mortgage_prov = models.TextField()
    confirm_time = models.DateTimeField()

    def __str__(self):
        return f"{self.purchase_offer}, {self.card_name}, {self.national_pid}, {self.street}"
