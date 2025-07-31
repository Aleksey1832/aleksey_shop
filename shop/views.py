from django.shortcuts import render, get_object_or_404, redirect
from shop.models import (Product, Category, ProductConstruction,
                         ProductFireclass, ProductUsage,
                         ProductRangModelHearth, ProductType)
from cart.forms import CartAddProductForm
from cart.views import pluralize
from shop.forms import ReviewAddForm
from shop.forms import ShopFormSorted
from shop.filters import SearchFilter
from django.core.cache import caches
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Case, When, IntegerField
from django.views.decorators.http import require_POST
from django.conf import settings
from orders.models import OrderItem


views_cache = caches['views']


def product_views_tracker(product_id):
    """ Трекер просмотров """
    redis_client = views_cache.client.get_client()
    key = f'product_views:{product_id}'

    # Увеличиваем счетчик просмотров
    redis_client.incr(key)

    # Обновляем рейтинг популярных товаров
    redis_client.zincrby(settings.TOP_VIEWS, 1, product_id)

    return int(redis_client.get(key) or 0)


def get_product_top_view(limit=settings.TOP_VIEWS_LIMIT):
    """ Список самых просматриваемых товаров """
    redis_client = views_cache.client.get_client()
    top = redis_client.zrevrange(settings.TOP_VIEWS, 0, limit - 1, withscores=False)

    return [int(item) for item in top]


def product_list(request, category_slug=None):
    """ Отображение всего каталога, страница list.html """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('name')
    sort_form = ShopFormSorted(request.POST or None)

    """ Получает список ID топ-10 самых просматриваемых товаров """
    top_product_ids = get_product_top_view()

    """ Создает объект Case/When для сохранения порядка товаров, как он был получен из Redis """
    preserved = Case(
        *[When(id=pk, then=pos) for pos, pk in enumerate(top_product_ids)],
        output_field=IntegerField()
    )

    """ Запрашивает объекты Product с ID из top_product_ids и сортирует их согласно порядку, заданному preserved """
    products_top = Product.objects.filter(id__in=top_product_ids).order_by(preserved)

    if sort_form.is_valid():
        products = sort_method(request)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    product_filter = SearchFilter(request.GET, queryset=products)
    products = product_filter.qs

    products_found = products.exists()

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
            'products_found': products_found,
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

    """ Купил ли пользователь товар """
    user_has_ordered = False
    """ Оставил ли пользователь отзыв об этом товаре """
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = product.reviews.filter(user=request.user).exists()
        user_has_ordered = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status='paid'
        ).exists()

    view_count = product_views_tracker(product.id)  # Трек просмотры - этот товар просматривали раз
    review_add_form = ReviewAddForm()  # Создание пустой формы для отправки отзыва. В шаблоне отобразится как <input>.
    reviews_count = product.reviews.count()  # Подсчет количества отзывов товара
    pluralize_extended = pluralize(reviews_count, ['отзыв', 'отзыва', 'отзывов'])

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
            'user_has_reviewed': user_has_reviewed,
            'user_has_ordered': user_has_ordered,
            'reviews_count': reviews_count,
            'pluralize_extended': pluralize_extended
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
def review_add(request, product_id):
    """
        Обрабатывает добавление отзыва к товару.
        Запрос приходит методом POST.
    """
    product = get_object_or_404(Product, id=product_id)

    """ Проверка, был ли заказ у user (user не должен оставить отзыв не купив товар) """
    if request.user.is_authenticated:
        has_ordered = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status='paid'
        ).exists()

        if not has_ordered:
            return redirect(
                'shop:product_detail',
                id=product.id,
                slug=product.slug
            )

    """ Проверка наличия уже оставленного отзыва """
    existing_review = product.reviews.filter(user_id=request.user).first()

    if existing_review:
        return redirect(
            'shop:product_detail',
            id=product.id,
            slug=product.slug
        )

    form = ReviewAddForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        try:
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
        except IntegrityError:
            messages.error(request, 'Вы не можете оставить более одного отзыва на этот товар!')
    else:
        messages.error(request, 'Проверьте правильность заполнения формы.')
    return redirect('shop:product_detail', id=product.id, slug=product.slug)
