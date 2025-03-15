from django.shortcuts import render, redirect
from .models import RentalItem
from .forms import RentalItemForm

def homepage(request):
    return render(request, 'rentals/homepage.html')  # Load the homepage template

def rental_list(request):
    rentals = RentalItem.objects.filter(available=True)  # Show only available items
    return render(request, 'rentals/rental_list.html', {'rentals': rentals})

def add_rental(request):
    if request.method == "POST":
        form = RentalItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rental_list')  # Redirect to listings after saving
    else:
        form = RentalItemForm()
    
    return render(request, 'rentals/add_rental.html', {'form': form})
