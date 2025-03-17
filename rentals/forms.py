from django import forms
from .models import RentalItem

class RentalItemForm(forms.ModelForm):
    class Meta:
        model = RentalItem
        fields = ['name', 'description', 'category', 'price_per_day', 'available','image']
