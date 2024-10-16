from django.urls import path
from shop import views


app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    #path('products/', views.sort_method, name='sort_method'), ###
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('price_list/', views.price_list, name='price_list'),
    path('how_buy/', views.how_buy, name='how_buy'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
