from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CouponType(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='Тип промокода')

    class Meta:
        ordering = ['name']
        verbose_name = 'Тип промокода'
        verbose_name_plural = 'Типы промокодов'

    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(max_length=16, unique=True, verbose_name='Название промокода')
    valid_from = models.DateTimeField(verbose_name='Начало действия промокода')
    valid_to = models.DateTimeField(verbose_name='Конец действия промокода')
    discount = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(100)], verbose_name='Выбрать размер скидки-%')
    active = models.BooleanField(default=True, verbose_name='Активность')
    max_uses = models.PositiveIntegerField(default=1,
                                           help_text='Максимальное количество использований купона (0 - неограниченно)')
    uses = models.PositiveIntegerField(default=0, editable=False)
    type = models.ForeignKey(CouponType, on_delete=models.CASCADE, verbose_name='Выбрать тип промокода')

    class Meta:
        ordering = ['code']
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return self.code
