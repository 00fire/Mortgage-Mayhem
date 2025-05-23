# app2/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
#from django.contrib import admins?????????????????
from django.conf import settings
from django.conf.urls.static import static
from .views import delete_property
urlpatterns = [
    path("", views.root_redirect, name="root"),
    path('login/',views.login_view, name='login'),
    path("signup/", views.signup_view, name="signup"),
    path('home/', views.homepage, name='homepage'), 
    path('property/<int:property_id>/offer/',views.make_offer,name='make_offer'),
    path('buyer_offer/', views.buyer_offer, name='buyer_offer'),
    path('profile_info/', views.profile_info, name='profile_info'),
    path('add_property/',views.add_property, name='add_property'),
    path("property/<int:property_id>/offer/",views.make_offer,name="make_offer",),
    path("property_detail/<int:pk>/", views.property_detail, name="property_detail"),
    path("seller/dashboard/",views.seller_dashboard,name="seller_dashboard"),
    path('seller/listings/',views.seller_listings,name='seller_listings'),
    path('seller/offer/<int:offer_id>/', views.respond_offer, name='respond_offer'),
    path("seller/offers/",views.incoming_offers,name="incoming_offers"),
    path('seller/<int:user_id>/', views.seller_profile, name='seller_profile'),
    path('success/', views.success, name='success'),
    path('property/<int:property_id>/finalize/contact/', views.contact_info, name='contact_info'),
    path('property/<int:property_id>/finalize/payment/', views.payment, name='payment'),
    path('property/finalize/confirmation/', views.confirmation, name='confirmation'),
    path('property/<int:property_id>/finalize/contact/', views.contact_info, name='contact_info'),
    path('property/<int:property_id>/finalize/review/', views.review, name='review'),
    path('property/<int:property_id>/delete/', delete_property, name='delete_property'),

    



    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

