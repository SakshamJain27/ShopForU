from django.contrib import admin

# Register your models here.
from .models import Product, Orders, Track

admin.site.register(Product)
admin.site.register(Orders)
admin.site.register(Track)
