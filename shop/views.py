from django.shortcuts import render, get_object_or_404
from shop.models import (Product, Category, ProductConstruction,
                         ProductFireclass, ProductUsage,
                         ProductRangModelHearth, ProductType)
from cart.forms import CartAddProductForm
from shop.forms import ShopFormSorted


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    #
    sort_by = request.GET.get('sort', 'name')
    products_sort = Product.objects.all().order_by(sort_by)
    #
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    cart_product_form = CartAddProductForm()
    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
            'products_sort': products_sort,
            'cart_product_form': cart_product_form
        }
    )


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product,
        id=id,
        slug=slug,
        available=True
    )
    categories = Category.objects.all()
    construction = ProductConstruction.objects.all()
    fire_class = ProductFireclass.objects.all()
    usage = ProductUsage.objects.all()
    rang_model_hearth = ProductRangModelHearth.objects.all()
    product_type = ProductType.objects.all()
    cart_product_form = CartAddProductForm()

    return render(
        request,
        'shop/product/detail.html',
        {
            'product': product,
            'categories': categories,
            'construction': construction,
            'fire_class': fire_class,
            'usage': usage,
            'rang_model_hearth': rang_model_hearth,
            'product_type': product_type,
            'cart_product_form': cart_product_form
        }
    )


def home(request):
    return render(request, 'shop/product/home.html')


def about(request):
    return render(request, 'shop/product/about.html')


def how_buy(request):
    return render(request, 'shop/product/how_buy.html')


def price_list(request, category_slug=None):
    category = None
    products = Product.objects.all()
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        'shop/product/price_list.html',
        {'category': category, 'categories': categories, 'products': products}
    )


# def sort_method(request):
#     # form_sorted = ShopFormSorted(request.POST)
#     products = Product.objects.all()
#     form_sort_list = ShopFormSorted(request.GET or None)
#
#     if form_sort_list.is_valid():
#         sort_by = form_sort_list.cleaned_data.get('form_sort_list')
#         if sort_by == '1':
#             products = products.order_by('name')
#         elif sort_by == '2':
#             products = products.order_by('created_at')
#         elif sort_by == '3':
#             products = products.order_by('price')
#         elif sort_by == '4':
#             products = products.order_by('-price')
#
#     return render(request,
#                   'shop/product/list.html',
#                   {'products': products, 'form_sort_list': form_sort_list})
