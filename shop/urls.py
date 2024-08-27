from django.urls import path
from shop import views


app_name = 'shop'

urlpatterns = [
    path(
        '',
        views.product_list,
        name='product_list'
    ),
    path(
        '<slug:slug>/',
        views.product_list,
        name='product_list_by_category'
    ),
]
