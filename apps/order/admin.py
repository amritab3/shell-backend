from django.contrib import admin

from apps.order.models import Order, OrderItem, OrderPayment

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderPayment)
