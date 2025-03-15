from django.urls import path
from .views import homepage, rental_list, add_rental  # Import homepage view

urlpatterns = [
    path('', homepage, name='homepage'),  # "/rentals/" loads homepage.html
    path('listings/', rental_list, name='rental_list'),  # "/rentals/listings/" for viewing rentals
    path('add/', add_rental, name='add_rental'),  # "/rentals/add/" for adding rentals
]
