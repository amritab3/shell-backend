# Generated by Django 4.2.6 on 2024-05-16 07:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="delivery_date",
            field=models.DateField(
                default=datetime.date(2024, 5, 18),
                verbose_name="delivery_date",
            ),
        ),
    ]
