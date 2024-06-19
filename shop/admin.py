# src/mvc/admin.py

from django.contrib import admin
from shop.models import Product  # оновлено імпорт

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')