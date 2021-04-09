from django.contrib import admin
from .models import Sales
from .models import Products
from .models import Address
# Register your models here.

admin.site.register(Sales)
admin.site.register(Products)
admin.site.register(Address)