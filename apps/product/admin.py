from django.contrib import admin

from .models import (
    Product,
    ProductSize,
    ProductImage,
    ProductComment,
    ProductRating,
)


class InStoreProduct(Product):
    class Meta:
        proxy = True


class InStoreProductAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(type="instore")


class ThriftProduct(Product):
    class Meta:
        proxy = True


class ThriftProductAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.filter(type="thrift")


admin.site.register(InStoreProduct, InStoreProductAdmin)
admin.site.register(ThriftProduct, ThriftProductAdmin)
admin.site.register(ProductSize)
admin.site.register(ProductImage)
admin.site.register(ProductComment)
admin.site.register(ProductRating)
