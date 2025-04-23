from django.shortcuts import render, redirect
from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order
from cart.views import pluralize
from django.contrib.auth.decorators import login_required
from coupons.models import Coupon
from orders.tasks import order_created


@login_required
def order_create(request):
    """ Создание нового заказа """
    cart = Cart(request)
    total_items = len(cart)
    ending_word = pluralize(total_items, ['товар', 'товара', 'товаров'])
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.status = 'active'  # статус при создании
            if cart.coupon:
                coupon = Coupon.objects.get(id=cart.coupon)
                order.coupon = coupon
                order.discount = coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # cart.clear()
            #
            # cart.del_coupon()

            # order_created.delay(order.id)  # отправка письма

            return redirect('orders:order_success', order_id=order.id)
            # return render(
            #     request,
            #     'orders/order/success.html',
            #     {
            #         'order': order,
            #         'total_items': total_items,
            #         'ending_word': ending_word,
            #     })

    else:
        user = request.user
        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.profile.phone_number
        }
        form = OrderCreateForm(initial=initial)
    return render(
        request,
        'orders/order/create.html',
        {
            'cart': cart,
            'form': form,
            'total_items': total_items,
            'ending_word': ending_word
        })


@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    # if request.method == 'POST':

    order.save()

    # return redirect('orders:payment', order_id=order.id)
    return render(
        request,
        'orders/order/success.html',
        {'order': order}
    )


def payment(request, order_id):
    order = Order.objects.get(id=order_id)
    order_created.delay(order.id)  # отправка письма
    order.status = 'paid'  # статус при подтверждении
    order.save()
    cart = Cart(request)
    cart.clear()
    cart.del_coupon()
    return render(request, 'orders/order/payment.html', {'order': order})


@login_required
def cancel_order(request, order_id):
    """ Отмена заказа из личного кабинета """
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        order.status = 'canceled'
        order.save()
        return redirect('accounts:profile_view')
    return render(
        request,
        'orders/order/cancel_confirm.html',
        {'order': order}
    )
