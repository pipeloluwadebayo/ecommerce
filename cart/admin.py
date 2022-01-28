from django.contrib import admin
from .models import Order, OrderItem, UserProfile, Address
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserProfile)
admin.site.register(Address)