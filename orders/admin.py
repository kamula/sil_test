from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'created_at', 'updated_at')
    search_fields = ('id', 'customer__user__username')
    list_filter = ('created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'created_at', 'updated_at')
    search_fields = ('order__id', 'product__name')
    list_filter = ('order',)