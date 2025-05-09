from django import forms
#from .models import User
from .models import UserProfile
from .models import Properties
class UserPForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields =['username', 'password']

class PropertyForm(forms.ModelForm):
    class Meta:
        model=Properties
        fields=['property_country', 'property_street', 'property_city', 'property_postal', 
                  'property_price', 'property_description', 'property_rooms', 'property_bedrooms', 
                  'property_bathrooms', 'property_square_meters_size', 'property_sold_status', 'property_image']


     