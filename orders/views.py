from django.shortcuts import render
from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem
from cart.views import ending_word_items


def order_create(request):
    cart = Cart(request)
    total_orders = cart.get_total_price()
    total_items = len(cart)
    ending_word = ending_word_items(total_items)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
                cart.clear()
                return render(
                    request,
                    'orders/order/success.html',
                    {
                        'order': order,
                        'total_items': total_items,
                        'total_price': total_orders['total_price'],
                        'ending_word': ending_word
                    }
                )

    form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form}
    )


def payment(request):
    return render(request, 'orders/order/payment.html')
