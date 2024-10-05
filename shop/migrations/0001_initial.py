# Generated by Django 5.1.1 on 2024-10-05 19:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Категории товара')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL-категории товара')),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товаров',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductConstruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Конструкция товара',
                'verbose_name_plural': 'Конструкции товаров',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductFireclass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Класс пожара')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL-класса пожара')),
            ],
            options={
                'verbose_name': 'Класс пожара',
                'verbose_name_plural': 'Класс пожара',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductRangModelHearth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Модельный очаг пожара')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL-очага пожара')),
            ],
            options={
                'verbose_name': 'Ранг модельного очага',
                'verbose_name_plural': 'Ранг модельного очага',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Тип товара')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL-типа товара')),
            ],
            options={
                'verbose_name': 'Тип товара',
                'verbose_name_plural': 'Тип товара',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Применение товара')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Применение товара',
                'verbose_name_plural': 'Применение товаров',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('product_code', models.IntegerField(default=0, verbose_name='Код товара')),
                ('price', models.DecimalField(decimal_places=0, max_digits=7, verbose_name='Цена')),
                ('image', models.ImageField(upload_to='product_img', verbose_name='Фото')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создание товара')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменение товара')),
                ('available', models.BooleanField(default=True, verbose_name='Наличие товара')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL-товара')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Категория товара')),
                ('construction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.productconstruction', verbose_name='Конструкция товара')),
                ('fire_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.productfireclass', verbose_name='Класс пожара')),
                ('rang_model_hearth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.productrangmodelhearth', verbose_name='Модельный очаг пожара')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.producttype', verbose_name='Тип товара')),
                ('usage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.productusage', verbose_name='Применение товара')),
            ],
            options={
                'verbose_name': 'Товара',
                'verbose_name_plural': 'Все товары',
                'ordering': ['name'],
            },
        ),
    ]
