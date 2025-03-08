from django.shortcuts import render, get_object_or_404
from shop.models import (Product, Category, ProductConstruction,
                         ProductFireclass, ProductUsage,
                         ProductRangModelHearth, ProductType)
from cart.forms import CartAddProductForm
from shop.forms import ShopFormSorted
from shop.filters import SearchFilter
from django.core.cache import caches


views_cache = caches['views']
TOP_VIEWS = 'top_product_views'
TOP_VIEWS_LIMIT = 10


def product_views_tracker(product_id):
    """ Трекер просмотров """
    key = f'product_views:{product_id}'
    if views_cache.get(key) is None:
        views_cache.set(key, 0)

    views_cache.incr(key, delta=1)
    # views_cache.zincrby(TOP_VIEWS, 1, product_id)
    return views_cache.get(key, 0)


def get_product_top_view(limit=TOP_VIEWS_LIMIT):
    """ Список самых просматриваемых товаров """
    top = views_cache.zrevrange(TOP_VIEWS, 0, limit-1)
    top_ids = [int(item[0]) for item in top]
    return top_ids


def product_list(request, category_slug=None):
    """ Отображение всего каталога, страница list.html """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('name')
    sort_form = ShopFormSorted(request.POST or None)

    # Вызов рейтинга в каталоге
    # products_top = Product.objects.filter(id__in=get_product_top_view())

    if sort_form.is_valid():
        products = sort_method(request)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    product_filter = SearchFilter(request.GET, queryset=products)
    products = product_filter.qs

    no_products_found = not products.exists()

    cart_product_form = CartAddProductForm()
    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
            'cart_product_form': cart_product_form,
            'sort_form': sort_form,
            'filter': product_filter,
            'no_products_found': no_products_found,
            # 'product_top': products_top,  # отрисовка рейтинга на странице
        }
    )


def product_detail(request, id, slug):
    """ Отображение детализации одного товара, страница detail.html """
    product = get_object_or_404(
        Product,
        id=id,
        slug=slug,
        available=True
    )
    view_count = product_views_tracker(product.id)
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
            'cart_product_form': cart_product_form,
            'view_count': view_count,
        }
    )


def home(request):
    """ Главная """
    return render(request, 'shop/product/home.html')


def about(request):
    """ О нас """
    return render(request, 'shop/product/about.html')


def how_buy(request):
    """ Как купить """
    return render(request, 'shop/product/how_buy.html')


def faq(request):
    """ Часто задаваемые вопросы """
    return render(request, 'shop/product/faq.html')


def price_list(request, category_slug=None):
    """ Прайс-лист """
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
    """ Метод сортировки товаров для list.html """
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
