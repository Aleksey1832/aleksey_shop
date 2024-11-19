from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payment/', views.payment, name='payment'),
    path('cancel/<int:order_id>', views.cancel_order, name='cancel_order'),
]
