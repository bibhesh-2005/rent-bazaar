from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class RentalItem(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('books', 'Books'),
        ('vehicles', 'Vehicles'),
        ('appliances', 'Appliances'),
        ('others', 'Others'),
    ]
    COLLEGE_CHOICES = [
        ('OUTR', 'OUTR'),
        ('Silicon', 'Silicon'),
        ('ITER', 'ITER'),
        ('IIIT BBSR', 'IIIT BBSR'),
        ('IIT BBSR', 'IIT BBSR'),
    ]

    
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=50, choices=COLLEGE_CHOICES, default='OUTR')  # Added college field

    image = models.ImageField(upload_to='rental_images/', blank=True, null=True, default='default_no_image.png')


    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    COLLEGE_CHOICES = [
        ('OUTR', 'OUTR'),
        ('Silicon', 'Silicon'),
        ('ITER', 'ITER'),
        ('IIIT BBSR', 'IIIT BBSR'),
        ('IIT BBSR', 'IIT BBSR'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=50, choices=COLLEGE_CHOICES, default='OUTR')
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username
