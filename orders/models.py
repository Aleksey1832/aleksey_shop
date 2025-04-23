from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from coupons.models import Coupon
from shop.models import Product
from accounts.models import Address
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


ORDER_STATUS_CHOICES = (
    ('active', 'Активный'),  # Заказ создан
    ('paid', 'Оплачен'),  # Заказ оплачен
    ('completed', 'Выполненный'),  # Заказ успешно завершен (доставлен)
    ('canceled', 'Отмененный')  # Заказ отменен пользователем
)


class Order(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=40, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    phone_number = models.CharField(max_length=30, verbose_name='Номер телефона')
    shipping_address = models.ForeignKey(Address,
                                         related_name='shipping_address',
                                         on_delete=models.CASCADE,
                                         verbose_name='Адрес доставки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    paid = models.BooleanField(default=False, verbose_name='Статус оплаты')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20,
                              choices=ORDER_STATUS_CHOICES,
                              default='active',
                              verbose_name='Статус заказа')

    """ Если удаляется купон, весь заказ не удаляется """
    coupon = models.ForeignKey(Coupon,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               verbose_name='Промокод')
    """ При удалении промокода в базе осталась информация о скидки """
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(1),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order №: {self.id}'

    def get_total_cost_before_discount(self):
        """ Вычисляет общую стоимость товаров в заказе без учета скидки """
        return sum(item.total_price() for item in self.orderitem_set.all())

    def get_discount(self):
        """ Вычисляет сумму скидки, применяя процент скидки (self.discount) к общей стоимости заказа без скидки """
        if self.discount > 0:
            return self.get_total_cost_before_discount() * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        """ Вычисляет общую стоимость заказа с учетом скидки """
        return self.get_total_cost_before_discount() - self.get_discount()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    def total_price(self):
        return self.price * self.quantity
