from django.contrib import admin

from shop.models import Category, ProductConstruction, ProductFireclass, ProductUsage
from shop.models import ProductRangModelHearth, ProductType, Product
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductConstruction)
class ProductConstructionAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductFireclass)
class ProductFireclassAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductUsage)
class ProductUsageAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductRangModelHearth)
class ProductRangModelHearthAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'product_code',
        'price',
        'available',
        'updated_at'
    ]  # задает набор выводимых в списке полей

    prepopulated_fields = {'slug': ('name',)}  # атрибут, который автоматически генерирует slug из поля name
    list_filter = ['available', 'updated_at']  # создает возможность фильтровать продукты по указанным параметрам
    list_editable = ['price', 'available']  # задает возможность править поля, непосредственно на странице
                                            # списка записей, не переходя на страницу продукта
