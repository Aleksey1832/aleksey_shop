from django.shortcuts import render, redirect
from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order
from cart.views import ending_word_items
from django.contrib.auth.decorators import login_required


@login_required
def order_create(request):
    cart = Cart(request)
    total_items = len(cart)
    ending_word = ending_word_items(total_items)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # cart.clear()
            return render(
                request,
                'orders/order/success.html',
                {
                    'order': order,
                    'total_items': total_items,
                    'ending_word': ending_word
                })

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


def payment(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'orders/order/payment.html')


@login_required
def cancel_order(request, order_id):
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
