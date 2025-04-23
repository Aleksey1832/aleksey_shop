from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('payment/<int:order_id>', views.payment, name='payment'),
    path('cancel/<int:order_id>', views.cancel_order, name='cancel_order'),
]
