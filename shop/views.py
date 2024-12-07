from django.shortcuts import render, get_object_or_404
from shop.models import (Product, Category, ProductConstruction,
                         ProductFireclass, ProductUsage,
                         ProductRangModelHearth, ProductType)
from cart.forms import CartAddProductForm
from shop.forms import ShopFormSorted
from shop.filters import SearchFilter


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('name')
    sort_form = ShopFormSorted(request.POST or None)
    if sort_form.is_valid():
        products = sort_method(request)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    product_filter = SearchFilter(request.GET, queryset=products)
    products = product_filter.qs
    # cart_product_form = CartAddProductForm()
    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
            # 'cart_product_form': cart_product_form,
            'sort_form': sort_form,
            'filter': product_filter
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


def sort_method(request):
    sort_form = ShopFormSorted(request.POST)
    products = Product.objects.filter(available=True)
    if sort_form.is_valid():
        needed_sort = sort_form.cleaned_data.get('form_sorted')
        if needed_sort == 'name':
            products = products.order_by('name')
        elif needed_sort == 'price_asc':
            products = products.order_by('price')
        elif needed_sort == 'price_desc':
            products = products.order_by('-price')
    return products
