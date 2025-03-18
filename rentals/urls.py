from django.urls import path
from .views import (
    homepage, rental_list, add_rental, signup_view, login_view, logout_view,
    manage_listings, edit_listing, delete_listing, user_profile, edit_profile
)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('listings/', rental_list, name='rental_list'),
    path('add/', add_rental, name='add_rental'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('manage/', manage_listings, name='manage_listings'),
    path('edit/<int:id>/', edit_listing, name='edit_listing'),
    path('delete/<int:id>/', delete_listing, name='delete_listing'),
    path('profile/', user_profile, name='user_profile'),  # 👈 New profile route
    path('profile/edit/', edit_profile, name='edit_profile'),
]