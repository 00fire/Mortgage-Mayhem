from django import forms
#from .models import User
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields =['username', 'password']