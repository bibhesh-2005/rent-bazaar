from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rentals.urls')),  # "/" now loads rental listings
    path('rentals/', include('rentals.urls')),  # "/rentals/" also loads rental listings
]
