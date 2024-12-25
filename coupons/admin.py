from django.contrib import admin
from coupons.models import Coupon, CouponType


@admin.register(CouponType)
class CouponTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active', 'type']
    list_filter = ['valid_from', 'valid_to']
