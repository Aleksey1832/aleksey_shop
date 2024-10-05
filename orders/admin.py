from django.contrib import admin

from orders.models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'middle_name',
        'last_name',
        'gender',
        'date_birth',
        'email',
        # 'phone_number',
        'city',
        'street',
        'house_number',
        'litter_number',
        # 'apartments_number',
        # 'floor',
        'postal_code'
    ]

    list_filter = ['paid', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
