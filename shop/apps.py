from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # продуктам будет присваиваться порядковый номер id
    name = 'shop'
    verbose_name = 'Товары'
