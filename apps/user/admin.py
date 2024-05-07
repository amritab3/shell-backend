from django.contrib import admin
from .models import User, Role, CartItem, Cart

# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Cart)
admin.site.register(CartItem)
