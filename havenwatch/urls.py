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

# urlpatterns = [
#     #path('', include('havenwatch.urls')),  # Havenwatch for the root path
#     #path('admin/', admin.site.urls),  # Admin path
#     #path('app2/', include('app2.urls')),  # Add app2 with its own path prefix
    
# ]
# urls.py
from django.conf import settings
from django.conf.urls.static import static

from django.conf import settings
from django.conf.urls.static import static

# Add this to serve static and media files in development mode


urlpatterns = [
    
    path('admin/', admin.site.urls),  # Admin path
    path('', include('app2.urls')),
    
    
    #path('', views.index_,name='index_'),
    #path("/register", views.register, name="register"),
    #path('', include("havenwatch.urls")),
        # Add app2 with its own path prefix
    # Havenwatch for the root path THIS IS THE FUCKING ISSUE
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
