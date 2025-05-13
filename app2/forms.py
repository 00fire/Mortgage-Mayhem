from django import forms
#from .models import User
from .models import UserProfile
from .models import Properties
from .models import PurchaseOffer

# app2/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import UserProfile, Properties     # import any other models you need

User = get_user_model()       

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role','bio', 'profile_picture']


class PropertyForm(forms.ModelForm):
    class Meta:
        model=Properties
        fields=['property_country', 'property_street', 'property_city', 'property_postal', 
                  'property_price', 'property_description', 'property_rooms', 'property_bedrooms', 
                  'property_bathrooms', 'property_square_meters_size', 'property_sold_status', 'property_image']


class SignUpForm(UserCreationForm):
    class Meta:
        model  = User
        fields = ("username", "password1", "password2")

    
class ProfileForm(forms.ModelForm):
    class Meta:
        model  = UserProfile
        fields = ("bio", "profile_picture")

class PurchaseOfferForm(forms.ModelForm):
    class Meta:
        model = PurchaseOffer
        fields = ('offer_price', 'expiration_date')
        widgets = {
            'expiration_date': forms.SelectDateWidget()
        }

# If you still reference "ProfileEditForm" in views:
ProfileEditForm = ProfileForm     