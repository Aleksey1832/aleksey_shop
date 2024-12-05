from django.contrib import admin
from orders.models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    fields = ['product', 'price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'shipping_address'
    ]

    list_filter = ['paid', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
