from django.conf import settings
from shop.models import Product
from decimal import *


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __len__(self):
        """
        Считаем товарные позиции
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        sum_item = self.__len__()
        total = 0
        for item in self.cart.values():
            total += Decimal(item['price']).quantize(Decimal('1.00')) * Decimal(sum_item).quantize(Decimal('1.00'))

        return total

