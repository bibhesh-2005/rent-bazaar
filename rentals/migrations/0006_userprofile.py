# Generated by Django 5.1.7 on 2025-03-18 16:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rentals", "0005_rentalitem_college"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "college",
                    models.CharField(
                        choices=[
                            ("OUTR", "OUTR"),
                            ("Silicon", "Silicon"),
                            ("ITER", "ITER"),
                            ("IIIT BBSR", "IIIT BBSR"),
                            ("IIT BBSR", "IIT BBSR"),
                        ],
                        default="OUTR",
                        max_length=50,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
