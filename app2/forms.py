from django import forms
#from .models import User
from .models import UserProfile
from .models import Properties
from .models import PurchaseOffer
from django.core.validators import RegexValidator
# app2/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import UserProfile, Properties     # import any other models you need
from django import forms
from django.forms import modelformset_factory
from django.forms import CharField

from .models import (
    Properties,
    PropertyImage,
    PurchaseOffer,
)
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
                  'property_bathrooms', 'property_square_meters_size', 'property_sold_status', 'property_image','property_type']


class SignUpForm(UserCreationForm):
    role=forms.ChoiceField(choices=UserProfile.ROLE_CHOICES,widget=forms.RadioSelect,label="I am signing up as a: ")
    class Meta:
        model  = User
        fields = ("username", "password1", "password2","role")

    
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

PropertyImageFormSet = modelformset_factory(
    PropertyImage,
    fields=('image',),     # your ImageField on PropertyImage
    extra=3,                # how many empty “upload” slots to show
    max_num=10,             # limit total images
    can_delete=True,        # allow deleting existing ones
)
# If you still reference "ProfileEditForm" in views:
ProfileEditForm = ProfileForm     


class ContactInfoForm(forms.Form):
    street_name = forms.CharField()
    city = forms.CharField()
    postal_code = forms.CharField()
    country = forms.ChoiceField(choices=[('Iceland', 'Iceland'), ('USA', 'USA')])
    national_pid = forms.CharField(label="National ID (Kennitala)")


PAYMENT_CHOICES=[('credit_card','Credit Card'),('bank_transfer', 'Bank Transfer'),('mortgage', ' Mortgage')]
class PaymentForm(forms.Form):
    
    payment_option = forms.ChoiceField(choices=PAYMENT_CHOICES)

    cardholder_name=forms.CharField(required=False,max_length=255)
    card_num=forms.CharField(required=False,max_length=16,validators=[RegexValidator(r'^\d{13,16}$', message="Card number must be 13 to 16 digits (no spaces or letters).")])
    expiration_date_card=forms.CharField(required=False,
        validators=[RegexValidator(r'^(0[1-9]|1[0-2])\/\d{2}$', message="Format must be DD/MM/YY")])
    cvc = forms.CharField(max_length=3,min_length=3,required=False,validators=[RegexValidator(r'^\d{3}$', 'Enter a valid 3-digit CVC')])

    bank_acc=forms.CharField(required=False,max_length=25)
    mortgage_prov=forms.CharField(required=False,max_length=25)
    def clean(self):
        Cleaned_data=super().clean()
        method=Cleaned_data.get('payment_option')
        if method == 'credit_card' or 'Credit Card':
            required = ['cardholder_name', 'card_num', 'expiration_date_card', 'cvc']
        elif method == 'bank_transfer' or 'Bank Transfer':
            required = ['bank_acc']
        elif method == 'mortgage' or 'Mortgage':
            required = ['mortgage_prov']
        else:
            required = []

        for field in required:
            if not Cleaned_data.get(field):
                self.add_error(field, 'This field is required.')

        return Cleaned_data