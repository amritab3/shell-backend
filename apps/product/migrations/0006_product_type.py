# Generated by Django 4.2.6 on 2024-05-08 05:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0005_alter_product_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[("instore", "Instore"), ("thrift", "Thrift")],
                default="",
                max_length=20,
                verbose_name="product_type",
            ),
        ),
    ]
