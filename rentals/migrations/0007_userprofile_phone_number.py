# Generated by Django 5.1.7 on 2025-03-18 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rentals", "0006_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="phone_number",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
