from django import forms
from .models import RentalItem
from django.contrib.auth.models import User
from .models import UserProfile


class SignupForm(forms.ModelForm):
    COLLEGE_CHOICES = [
        ('OUTR', 'OUTR'),
        ('Silicon', 'Silicon'),
        ('ITER', 'ITER'),
        ('IIIT BBSR', 'IIIT BBSR'),
        ('IIT BBSR', 'IIT BBSR'),
    ]

    college = forms.ChoiceField(choices=COLLEGE_CHOICES, required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {'password': forms.PasswordInput()}

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password'])  # Encrypt password
            user.save()
            UserProfile.objects.create(user=user, college=self.cleaned_data['college'],phone_number=self.cleaned_data['phone_number'])
        return user


class RentalItemForm(forms.ModelForm):
    class Meta:
        model = RentalItem
        fields = ['name', 'description', 'category', 'price_per_day', 'available','image','college']


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)  # From User model
    email = forms.EmailField(required=True)  # From User model
    college = forms.ChoiceField(choices=UserProfile.COLLEGE_CHOICES, required=True)  # From UserProfile
    phone_number = forms.CharField(max_length=15, required=True)  # From UserProfile

    class Meta:
        model = User  # We edit the User model for username & email
        fields = ['username', 'email']  # Only include fields that belong to User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.college = self.cleaned_data['college']
            user_profile.phone_number = self.cleaned_data['phone_number']
            user_profile.save()

        return user