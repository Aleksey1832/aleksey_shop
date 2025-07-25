# Generated by Django 5.2a1 on 2025-06-12 12:46

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('coupons', '0001_initial'),
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=40, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone_number', models.CharField(max_length=30, verbose_name='Номер телефона')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('paid', models.BooleanField(default=False, verbose_name='Статус оплаты')),
                ('status', models.CharField(choices=[('active', 'Активный'), ('paid', 'Оплачен'), ('completed', 'Выполненный'), ('canceled', 'Отмененный')], default='active', max_length=20, verbose_name='Статус заказа')),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coupons.coupon', verbose_name='Промокод')),
                ('shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_address', to='accounts.address', verbose_name='Адрес доставки')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
    ]
