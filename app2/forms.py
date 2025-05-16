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
        fields = ['role','bio', 'profile_picture', 'street', 'city', 'postal']

class UsernameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class PropertyForm(forms.ModelForm):
    class Meta:
        model=Properties
        fields=['property_country', 'property_street', 'property_city', 'property_postal', 
                  'property_price', 'property_description', 'property_rooms', 'property_bedrooms', 
                  'property_bathrooms', 'property_square_meters_size', 'property_image','property_type']


class SignUpForm(UserCreationForm):
    role=forms.ChoiceField(choices=UserProfile.ROLE_CHOICES,widget=forms.RadioSelect,label="I am signing up as a: ")
    class Meta:
        model  = User
        fields = ("username", "password1", "password2","role")

    
class ProfileForm(forms.ModelForm):
    SELLER_TYPE_CHOICES = [
        ('none', 'none'),
        ('individual', 'Individual'),
        ('agency', 'Real Estate Agency'),
    ]

    seller_type = forms.ChoiceField(choices=SELLER_TYPE_CHOICES, required=False)
    street = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100, required=True)
    postal = forms.CharField(max_length=20, required=True)

    class Meta:
        model  = UserProfile
        fields = ("bio", "profile_picture", 'seller_type', 'street', 'city', 'postal')

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
    extra=6,                # how many empty “upload” slots to show
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




import re
from django import forms

PAYMENT_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('bank_transfer', 'Bank Transfer'),
    ('mortgage', 'Mortgage'),
]

class PaymentForm(forms.Form):
    payment_option = forms.ChoiceField(choices=PAYMENT_CHOICES)
    cardholder_name = forms.CharField(required=False)
    card_num = forms.CharField(required=False, max_length=16)
    expiration_date_card = forms.CharField(required=False)
    cvc = forms.CharField(required=False, max_length=3)
    bank_acc = forms.CharField(required=False)
    mortgage_prov = forms.CharField(required=False)

    def clean(self):
        cleaned = super().clean()
        method = cleaned.get('payment_option')

        if method == 'credit_card':
            # Card number
            card_num = cleaned.get('card_num')
            if not card_num:
                self.add_error('card_num', 'Card number is required.')
            elif not card_num.isdigit() or not (13 <= len(card_num) <= 16):
                self.add_error('card_num', 'Card number must be 13–16 digits.')

            # Expiration date
            expiry = cleaned.get('expiration_date_card')
            if not expiry:
                self.add_error('expiration_date_card', 'Expiry date is required.')
            elif not re.match(r'^(0[1-9]|1[0-2])/\d{2}$', expiry):
                self.add_error('expiration_date_card', 'Expiry must be in MM/YY format (e.g. 09/25).')

            # CVC
            cvc = cleaned.get('cvc')
            if not cvc:
                self.add_error('cvc', 'CVC is required.')
            elif not cvc.isdigit() or len(cvc) != 3:
                self.add_error('cvc', 'CVC must be 3 digits.')

        elif method == 'bank_transfer':
            bank_acc = cleaned.get('bank_acc')
            if not bank_acc:
                self.add_error('bank_acc', 'Bank account is required.')
            elif not bank_acc.isdigit():
                self.add_error('bank_acc', 'Bank account must be numeric.')

        elif method == 'mortgage':
            if not cleaned.get('mortgage_prov'):
                self.add_error('mortgage_prov', 'Mortgage provider is required.')

        return cleaned
