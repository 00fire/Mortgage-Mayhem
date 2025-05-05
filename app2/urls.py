# app2/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("user-profile/", views.user_profile, name="user_profile"),  # Define your own app routes
    path('success/', views.success, name='success'),
]

from django.urls import path
from . import views

# urlpatterns = [
#     path('home/', views.index, name='index'),
#     # Add other URLs for the 'havenwatch' app
# ]
