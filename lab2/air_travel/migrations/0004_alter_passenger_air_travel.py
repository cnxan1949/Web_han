# Generated by Django 4.1.1 on 2023-01-16 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "air_travel",
            "0003_remove_passenger_air_travel_alter_air_travel_airline_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="passenger",
            name="Air_travel",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="air_travel.air_travel"
            ),
        ),
    ]
