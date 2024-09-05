from django.db import models
from django.urls import reverse


class Category(models.Model):                         # категория
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Категории товара'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL-категории товара'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category',
            args=[self.slug]
        )


class ProductConstruction(models.Model):              # конструкция
    name = models.CharField(
        max_length=100,
        unique=True,
        null=True
        # verbose_name='Конструкции товара'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True
        # verbose_name='URL-конструкции товара'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Конструкция товара'
        verbose_name_plural = 'Конструкции товаров'

    def __str__(self):
        return self.name


class ProductFireclass(models.Model):                 # класс пожара
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Класс пожара'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL-класса пожара'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Класс пожара'
        verbose_name_plural = 'Класс пожара'

    def __str__(self):
        return self.name


class ProductUsage(models.Model):                     # использование
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Применение товара'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Применение товара'
        verbose_name_plural = 'Применение товаров'

    def __str__(self):
        return self.name


class ProductRangModelHearth(models.Model):           # ранг модельного очага
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Модельный очаг пожара'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL-очага пожара'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ранг модельного очага'
        verbose_name_plural = 'Ранг модельного очага'

    def __str__(self):
        return self.name


class ProductType(models.Model):                      # тип товара
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Тип товара'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL-типа товара'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Тип товара'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')  # наименование
    product_code = models.IntegerField(default=0, verbose_name='Код товара')  # код товара
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')  # цена
    image = models.ImageField(upload_to='media', verbose_name='Фото')  # адреса картинок
    description = models.TextField(blank=True, verbose_name='Описание')  # описание
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создание товара')  # создание товара
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменение товара')  # изменение товара (описания или изменение цены)
    available = models.BooleanField(default=True, verbose_name='Наличие товара')  # товар доступен или нет
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-товара')  # для ссылок поисковых машин

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория товара'
    )
    construction = models.ForeignKey(
        ProductConstruction,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Конструкция товара'
    )
    fire_class = models.ForeignKey(
        ProductFireclass,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Класс пожара'
    )
    usage = models.ForeignKey(
        ProductUsage,
        on_delete=models.CASCADE,
        verbose_name='Применение товара'
    )
    rang_model_hearth = models.ForeignKey(
        ProductRangModelHearth,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Модельный очаг пожара'
    )
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        verbose_name='Тип товара'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Товара'
        verbose_name_plural = 'Все товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'shop:product_detail',
            args=[self.id, self.slug]
        )
