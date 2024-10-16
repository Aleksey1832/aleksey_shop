from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    middle_name = models.CharField(max_length=30, verbose_name='Отчество')
    last_name = models.CharField(max_length=40, verbose_name='Фамилия')
    gender = models.CharField(max_length=7, verbose_name='Пол')
    date_birth = models.DateField(verbose_name='Дата рождения')
    email = models.EmailField(verbose_name='Email')
    phone_number = models.CharField(max_length=30, verbose_name='Номер телефона')
    city = models.CharField(max_length=30, verbose_name='Город')
    street = models.CharField(max_length=40, verbose_name='Улица/Проспект')
    house_number = models.IntegerField(verbose_name='Номер дома')
    litter_number = models.CharField(max_length=10, verbose_name='Корпус/Литера')
    apartments_number = models.CharField(max_length=5, verbose_name='Квартира/Офис')
    floor = models.CharField(max_length=2, verbose_name='Этаж')
    postal_code = models.CharField(max_length=6, verbose_name='Почтовый индекс')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order №: {self.id}'

    class Meta:

        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.id}'
