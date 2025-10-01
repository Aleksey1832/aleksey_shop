import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order
from cart.views import pluralize
from django.contrib.auth.decorators import login_required
from coupons.models import Coupon
from orders.tasks import order_created
from orders.payment import create_payment
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse


@login_required
def order_create(request):
    """ Создание нового заказа """
    cart = Cart(request)
    total_items = len(cart)
    ending_word = pluralize(total_items, ['товар', 'товара', 'товаров'])
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.status = 'active'  # статус при создании
            if cart.coupon:
                try:
                    coupon = Coupon.objects.get(id=cart.coupon)
                    order.coupon = coupon
                    order.discount = coupon.discount

                except Coupon.DoesNotExist:
                    messages.warning(request, 'Купон не применен!')
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            messages.success(request, 'Ваш заказ успешно создан!')
            return redirect('orders:order_success', order_id=order.id)

        else:  # Если форма не валидна
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

    else:  # Если метод запроса не POST (например, GET)
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
    """ Страница успешного создания заказа """
    # order = Order.objects.get(id=order_id)
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        'orders/order/success.html',
        {'order': order}
        )


@transaction.atomic  # для атомарности операций с БД
def payment(request, order_id):
    """ Обработка платежа заказа """
    order = get_object_or_404(Order, id=order_id)
    if order.status == 'active':
        try:
            # 1. Создаем платеж
            order_payment = create_payment(order)
            order.payment_id = order_payment.id

            # 2. Отправка письма
            order_created.delay(order.id)

            return redirect(order_payment.confirmation.confirmation_url)

        except Exception as e:
            messages.error(
                    request,
                    f'Произошла ошибка {e} при обработке вашего платежа № {order_id}.'
                    ' Пожалуйста, попробуйте позже или свяжитесь с поддержкой.'
                )
            return redirect('cart:cart_detail', order_id=order.id)

    else:  # Если заказ уже не в статусе 'active'
        messages.warning(request, 'Этот заказ уже был оплачен.')
        return redirect('cart:cart_detail', order_id=order.id)


@csrf_exempt
@require_POST
def yookassa_webhook(request):
    """ Обработка webhook от Yookassa """
    event = json.loads(request.body.decode('utf-8'))
    event_type = event.get('event')
    payment_id = event.get('object').get('id')

    if event_type == 'payment.succeeded':
        order = Order.objects.get(payment_id=payment_id)
        order.paid = True

        # 2. Обновляем статус
        order.status = 'paid'  # статус при подтверждении
        order.save()  # Сохраняем payment_id и новый статус paid

        # 3. Очищаем корзину и купон
        cart = Cart(request)  # Возможно перенести в yookassa_webhook
        cart.clear()  # Возможно перенести в yookassa_webhook
        cart.del_coupon()  # Возможно перенести в yookassa_webhook

    elif event_type == 'payment.canceled':
        order = Order.objects.get(payment_id=payment_id)
        order.paid = False
        order.status = 'canceled'
    return JsonResponse({"status": "ok"})


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
