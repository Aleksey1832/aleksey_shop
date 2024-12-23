from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# class CouponType(models.Model):
#     name = models.CharField(max_length=32)
#
#     def __str__(self):
#         return self.name


class Coupon(models.Model):
    code = models.CharField(max_length=16, unique=True, verbose_name='Промокод')
    valid_from = models.DateTimeField(verbose_name='Начало действия')
    valid_to = models.DateTimeField(verbose_name='Конец действия')
    discount = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(100)], verbose_name='Скидка')
    active = models.BooleanField(default=True, verbose_name='Активна')

    TYPE_CHOICES = (
        ('standard', 'Стандарт'),
        ('personal', 'Персональная')
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='standard',
        verbose_name='Тип скидки'
    )

    # type = models.ForeignKey(CouponType, on_delete=models.CASCADE, verbose_name='Тип скидки')

    class Meta:
        ordering = ['code']
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return self.code
