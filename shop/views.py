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
            #
            # 'products_sort': products_sort,
            #
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


def sort_method(request):
    sort_by = request.GET.get('sort', 'price')  # Параметр 'sort' из URL
    if sort_by:
        products = Product.objects.all().order_by('-price')  # Сортировка по убыванию
    else:
        products = Product.objects.all().order_by('price')  # Сортировка по возрастанию

    return render(request, 'shop/product/list.html', {'products': products})



    # form_sorted = ShopFormSorted(request.POST)
    # products = Product.objects.filter(available=True)
    # # form_sort_list = ShopFormSorted(request.GET or None)
    # # choices=[('ПУ', 'По умолчанию'), ('ДТ', 'По дате'), ('ДЕД', 'От дешевых к дорогим'), ('ДОД', 'От дорогих к дешевым')])
    #
    # if form_sorted.is_valid():
    #     sort_by = form_sorted.cleaned_data.get('form_sorted')
    #     if sort_by == "ДТ":
    #         products = products.order_by("created")
    #     elif sort_by == "ДЕД":
    #         products = products.order_by("price")
    #     elif sort_by == "ДОД":
    #         products = products.order_by("-price")
    #
    # return render(request,
    #               'shop/product/list.html',
    #               {'products': products, 'form_sorted': form_sorted})
