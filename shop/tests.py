from django.test import TestCase
from shop.models import Category
from django.urls import reverse


class CategoryModelTest(TestCase):
    """ Test models/category model """
    def test_create_category(self):
        category = Category.objects.create(name='Vedro', slug='vedro')
        self.assertEqual(Category.objects.count(), 1)


class CategoryModelStrTest(TestCase):
    """ Test models/category model str """
    def test_create_str_category(self):
        category = Category.objects.create(name='Vedro', slug='vedro')
        saved_category = Category.objects.first()
        self.assertEqual(saved_category.name, 'Vedro')


class CategoryAbsoluteUrlRealModelTest(TestCase):
    """ Test метода get_absolute_url на правильность использования функции `reverse` для генерации URL """
    def setUp(self):
        # Создаем объект модели в тестовой базе данных
        self.category = Category.objects.create(name='Electron', slug='electron')
        print(self.category)

    def test_get_absolute_url_category(self):
        # Тестирует get_absolute_url для реальной модели Django, полагаясь на реальную конфигурацию URL.
        # Содержит строку URL, которую ожидаем получить от метода `get_absolute_url'
        # Строка URL, которую сгенерировали с помощью `reverse` вручную
        expected_url = reverse('shop:product_list_by_category', args=['electron'])
        print(expected_url)

        # Созданный объект в методе setUp
        # Строка URL, которую вернул метод `get_absolute_url` модели Category
        actual_url = self.category.get_absolute_url()
        print(actual_url)

        # Проверяет, равны ли два значения
        self.assertEqual(actual_url, expected_url)
