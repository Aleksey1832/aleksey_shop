from django.conf import settings
from shop.models import Product
from decimal import Decimal, ROUND_HALF_UP
from coupons.models import Coupon


class Cart:
    """ Класс корзины покупок """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon = self.session.get('coupon_id')

    def get_coupon(self):
        """ Возвращает объект Coupon на основе сохраненного ID купона """
        if self.coupon:
            try:
                return Coupon.objects.get(id=self.coupon)
            except Coupon.DoesNotExist:
                pass
            return None

    def save(self):
        """ Сохраняет изменения в сессии """
        self.session.modified = True

    def add(self, product, quantity=1, override_quantity=False):
        """ Добавляет товар в корзину """
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
        """ Удаляет товар из корзины. Аналогичен `add`, но удаляет элемент """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """ Очищает корзину """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def del_coupon(self):
        """ Метод для удаления купона из корзины при переходе на страницу оплаты """
        if 'coupon_id' in self.session:
            del self.session['coupon_id']
        self.save()

    def __iter__(self):
        """ Итератор для обхода товаров в корзине """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """ Возвращает общее количество товаров в корзине """
        return sum(item['quantity'] for item in self.cart.values())

    def get_discount(self):
        """ Вычисляет сумму скидки, используя информацию о купоне """
        if self.coupon:
            discount = (self.get_coupon().discount / Decimal(100)) * self.get_total_price()
            return discount.quantize(Decimal('0.00'), ROUND_HALF_UP)
        return Decimal(0).quantize(Decimal('0.00'), ROUND_HALF_UP)

    def get_total_price(self):
        """ Вычисляет общую стоимость товаров без учета скидки """
        total = sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
        # return total.quantize(Decimal('0.00'), ROUND_HALF_UP)
        return Decimal(total).quantize(Decimal('0.00'), ROUND_HALF_UP)

    def get_total_price_sale(self):
        """ Вычисляет общую стоимость товаров с учетом скидки """
        total_sale = self.get_total_price() - self.get_discount()
        return total_sale.quantize(Decimal('0.00'), ROUND_HALF_UP)
