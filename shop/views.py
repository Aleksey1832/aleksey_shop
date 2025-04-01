from django.shortcuts import render, get_object_or_404, redirect
from shop.models import (Product, Category, ProductConstruction,
                         ProductFireclass, ProductUsage,
                         ProductRangModelHearth, ProductType)
from cart.forms import CartAddProductForm
from shop.forms import ReviewAddForm
from shop.forms import ShopFormSorted
from shop.filters import SearchFilter
from django.core.cache import caches
from django.db.models import Case, When, IntegerField
from django.views.decorators.http import require_POST


views_cache = caches['views']
TOP_VIEWS = 'top_product_views'
TOP_VIEWS_LIMIT = 10


def product_views_tracker(product_id):
    """ Трекер просмотров """
    redis_client = views_cache.client.get_client()
    key = f'product_views:{product_id}'

    # Увеличиваем счетчик просмотров
    redis_client.incr(key)

    # Обновляем рейтинг популярных товаров
    redis_client.zincrby(TOP_VIEWS, 1, product_id)

    return int(redis_client.get(key) or 0)


def get_product_top_view(limit=TOP_VIEWS_LIMIT):
    """ Список самых просматриваемых товаров """
    redis_client = views_cache.client.get_client()
    top = redis_client.zrevrange(TOP_VIEWS, 0, limit - 1, withscores=False)

    return [int(item) for item in top]


def product_list(request, category_slug=None):
    """ Отображение всего каталога, страница list.html """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('name')
    sort_form = ShopFormSorted(request.POST or None)

    # Получает список ID топ-10 самых просматриваемых товаров
    top_product_ids = get_product_top_view()

    # Создает объект Case/When для сохранения порядка товаров, как он был получен из Redis
    preserved = Case(
        *[When(id=pk, then=pos) for pos, pk in enumerate(top_product_ids)],
        output_field=IntegerField()
    )

    # Запрашивает объекты Product с ID из top_product_ids и сортирует их согласно порядку, заданному preserved
    products_top = Product.objects.filter(id__in=top_product_ids).order_by(preserved)

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
            'product_top': products_top,  # отрисовка рейтинга на странице
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
    reviews = product.reviews.all()  # Получаем все отзывы, связанные с данным товаром

    view_count = product_views_tracker(product.id)  # трек просмотры
    review_add_form = ReviewAddForm()  # отзывы
    categories = Category.objects.all()
    construction = ProductConstruction.objects.all()
    fire_class = ProductFireclass.objects.all()
    usage = ProductUsage.objects.all()
    rang_model_hearth = ProductRangModelHearth.objects.all()
    product_type = ProductType.objects.all()
    cart_product_form = CartAddProductForm()  # Форма для добавления количества товара в корзину

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
            'review_add_form': review_add_form,
            'reviews': reviews,
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


@require_POST
def product_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ReviewAddForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        review.save()
    return redirect('shop:product_detail')
