import django_filters
from django import forms
from shop.models import Product


MIN_PRICE = 1
MAX_PRICE = 100


class SearchFilter(django_filters.FilterSet):
    """
    Класс для создания несколько фильтров по разным параметрам (для поиска на сайте)
    """
    name = django_filters.CharFilter(
        label='Название товара',  # человечески понятная» метка для этого поля при его визуализации
        field_name='name',        # имя поля, которое используется для обращения к нему в запросах и шаблонах
        lookup_expr='icontains',  # поле поиска, используемое при фильтрации
        required=False,           # говорит о том, что поле не является обязательным
        widget=forms.TextInput(attrs={'class': 'filter'})  # TextInput вставка из фильтра
    )

    min_price = django_filters.NumberFilter(
        label='Минимальная цена',
        field_name='price',
        lookup_expr='gte',        # больше либо равно - greater then or equal
        required=False,
        widget=forms.NumberInput(attrs={'class': 'filter'})  # NumberInput вставка номера
    )

    max_price = django_filters.NumberFilter(
        label='Максимальная цена',
        field_name='price',
        lookup_expr='lte',        # меньше либо рано - less then or equal
        required=False,
        widget=forms.NumberInput(attrs={'class': 'filter'})
    )

    class Meta:
        model = Product
        fields = ['name', 'min_price', 'max_price']

    def clean_min_price(self):
        """ Функция, ограничивающая минимальное значение """
        value = self.form.cleaned_data.get['min_price']
        if value is not None and value < MIN_PRICE:
            value = MIN_PRICE
        return value

    def clean_max_price(self):
        """ Функция, ограничивающая максимальное значение """
        value = self.form.cleaned_data.get['max_price']
        if value is not None and value > MAX_PRICE:
            value = MAX_PRICE
        return value
