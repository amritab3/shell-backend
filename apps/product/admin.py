from django.contrib import admin

from .models import Product, ProductSize, ProductImage, ProductComment

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductSize)
admin.site.register(ProductImage)
admin.site.register(ProductComment)
