# app2/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
#from django.contrib import admins?????????????????
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.root_redirect, name="root"),
    path('login/',views.login_view, name='login'),
    path("signup/", views.signup_view, name="signup"),
    path('home/', views.homepage, name='homepage'), 
    #path('property_detail/',views.property_detail,name='property_detail'),
    #path('user-profile/', views.user_profile, name='user_profile'),
    path('buyer_offer/', views.buyer_offer, name='buyer_offer'),
    path('profile_info/', views.profile_info, name='profile_info'),
    #path("user-profile/", views.user_profile, name="user_profile"),  # Define your own app routes
    path('add_property/',views.add_property, name='add_property'),
    path('property_detail/<int:id>/', views.property_detail, name='property_detail'),
    path('success/', views.success, name='success'),
    #path('register/', views.register, name='register'),
    path('search/', views.search_properties, name='search_properties'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

