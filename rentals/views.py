from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required  # Import login check
from .models import RentalItem
from .forms import RentalItemForm
from .forms import SignupForm
from .forms import EditProfileForm
from .models import UserProfile


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
        form = RentalItemForm(request.POST, request.FILES, instance=listing)
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


from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after sign-up
            return redirect('homepage')  # Redirect to homepage
    else:
        form = SignupForm()

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


# def homepage(request):
#     return render(request, 'rentals/homepage.html')  # Load the homepage template
def homepage(request):
    rentals = RentalItem.objects.filter(available=True)

    # Search logic
    query = request.GET.get('q', '').strip()
    if query:
        rentals = rentals.filter(name__icontains=query)

    # Sorting logic
    sort_order = request.GET.get('sort', '')
    if sort_order == 'low_to_high':
        rentals = rentals.order_by('price_per_day')
    elif sort_order == 'high_to_low':
        rentals = rentals.order_by('-price_per_day')

    # College filtering
    selected_college = request.GET.get('college', '')
    if selected_college:
        rentals = rentals.filter(college=selected_college)

    colleges = ['OUTR', 'Silicon', 'ITER', 'IIIT BBSR', 'IIT BBSR']  # Available options

    return render(request, 'rentals/homepage.html', {
        'rentals': rentals,
        'query': query,
        'selected_college': selected_college,
        'colleges': colleges,
        'sort_order': sort_order
    })




def rental_list(request):
    """Show available rentals filtered by search query if provided."""
    query = request.GET.get('q')  # Get search term from the URL
    if query:
        rentals = RentalItem.objects.filter(name__icontains=query, available=True)
    else:
        rentals = RentalItem.objects.filter(available=True)

    return render(request, 'rentals/rental_list.html', {'rentals': rentals, 'query': query})


# @login_required(login_url='login')
# def user_profile(request):
#     return render(request, 'rentals/profile.html', {'user': request.user})
@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'rentals/profile.html', {'user': request.user, 'profile': profile})

# @login_required
# def edit_profile(request):
#     user = request.user
#     if request.method == "POST":
#         form = EditProfileForm(request.POST, instance=user.userprofile)
#         if form.is_valid():
#             form.save()
#             return redirect('user_profile')
#     else:
#         form = EditProfileForm(instance=user.userprofile)

#     return render(request, 'rentals/edit_profile.html', {'form': form})
@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            profile.college = form.cleaned_data['college']
            profile.phone_number = form.cleaned_data['phone_number']
            profile.save()
            return redirect('user_profile')

    else:
        form = EditProfileForm(instance=request.user, initial={'college': profile.college, 'phone_number': profile.phone_number})
    
    return render(request, 'rentals/edit_profile.html', {'form': form})