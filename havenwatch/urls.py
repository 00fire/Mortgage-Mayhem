"""
URL configuration for havenwatch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# main/urls.py
# main/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    #path('', include('havenwatch.urls')),  # Havenwatch for the root path
    #path('admin/', admin.site.urls),  # Admin path
    #path('app2/', include('app2.urls')),  # Add app2 with its own path prefix
    
]


urlpatterns = [
    path('admin/', admin.site.urls),  # Admin path
    path('app2/', include('app2.urls')),
    path('', include('havenwatch.urls')),  # Add app2 with its own path prefix
    # Havenwatch for the root path THIS IS THE FUCKING ISSUE
]