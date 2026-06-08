from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'product_name', 'quantity', 'order_date', 'status', 'created_at')
    list_filter = ('status', 'order_date')
    search_fields = ('customer_name', 'product_name')