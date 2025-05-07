# app2/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('login/',views.login_view, name='login'),
    path('user-profile/', views.user_profile, name='user_profile'), 
    #path("user-profile/", views.user_profile, name="user_profile"),  # Define your own app routes
    
    path('success/', views.success, name='success'),
    #path('register/', views.register, name='register'),
    
]


