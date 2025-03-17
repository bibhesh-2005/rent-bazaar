from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required  # Import login check
from .models import RentalItem
from .forms import RentalItemForm


@login_required(login_url='login')
def manage_listings(request):
    # Fetch listings owned by the logged-in user
    listings = RentalItem.objects.filter(owner=request.user)
    return render(request, 'rentals/manage_listings.html', {'listings': listings})

@login_required(login_url='login')
def edit_listing(request, id):
    # Fetch the listing to edit
    listing = get_object_or_404(RentalItem, id=id, owner=request.user)

    if request.method == "POST":
        form = RentalItemForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('manage_listings')
    else:
        form = RentalItemForm(instance=listing)

    return render(request, 'rentals/edit_listing.html', {'form': form})

@login_required(login_url='login')
def delete_listing(request, id):
    # Fetch the listing to delete
    listing = get_object_or_404(RentalItem, id=id, owner=request.user)

    if request.method == "POST":
        listing.delete()
        return redirect('manage_listings')

    return render(request, 'rentals/confirm_delete.html', {'listing': listing})



@login_required(login_url='login')
def add_rental(request):
    if request.method == "POST":
        form = RentalItemForm(request.POST, request.FILES)
        if form.is_valid():
            rental = form.save(commit=False)  # Don't save yet
            rental.owner = request.user  # Assign the logged-in user as owner
            rental.save()  # Now save
            return redirect('rental_list')
    else:
        form = RentalItemForm()
    
    return render(request, 'rentals/add_rental.html', {'form': form})


@login_required(login_url='login')
def user_dashboard(request):
    rentals = RentalItem.objects.filter(owner=request.user)  # Show only user's rentals
    return render(request, 'rentals/dashboard.html', {'rentals': rentals})


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # Create form with user input
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the new user
            return redirect('homepage')  # Redirect to homepage
    else:
        form = UserCreationForm()

    return render(request, 'rentals/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in
            return redirect('homepage')  # Redirect to homepage
    else:
        form = AuthenticationForm()

    return render(request, 'rentals/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('homepage')  # Redirect to homepage after logout

def homepage(request):
    return render(request, 'rentals/homepage.html')  # Load the homepage template

def rental_list(request):
    """Show all available rentals or filter by logged-in user's listings."""
    if request.GET.get('my_listings'):  # If "My Listings" is clicked
        if request.user.is_authenticated:
            rentals = RentalItem.objects.filter(owner=request.user, available=True)
        else:
            rentals = []  # Empty list if user is not logged in
    else:
        rentals = RentalItem.objects.filter(available=True)  # Default: Show all available rentals

    return render(request, 'rentals/rental_list.html', {'rentals': rentals})

@login_required(login_url='login')
def user_profile(request):
    return render(request, 'rentals/profile.html', {'user': request.user})

