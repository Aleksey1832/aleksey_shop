from django.urls import path
from coupons import views

app_name = 'coupons'

urlpatterns = [
    path('apply/', views.coupon_apply, name='coupon_apply'),
    path('remove/', views.coupon_remove, name='coupon_remove'),
]
