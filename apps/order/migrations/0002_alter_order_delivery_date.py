# Generated by Django 4.2.6 on 2024-05-16 06:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="delivery_date",
            field=models.DateField(default="", verbose_name="delivery_date"),
        ),
    ]
