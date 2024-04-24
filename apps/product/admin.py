from django.contrib import admin

from .models import Product, ProductSize

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductSize)
