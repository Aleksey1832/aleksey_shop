from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    total_items = len(cart)
    ending_word = ending_word_items(len(cart))
    total_price_info = cart.get_total_price()
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'override': True}
        )
    return render(
        request,
        'cart/detail.html',
        {
            'cart': cart,
            'total_items': total_items,
            'ending_word': ending_word,
            'total_price': total_price_info['total_price'],
            'discounted_price': total_price_info['discounted_price'],
            'discount': total_price_info['discount']
        }
    )


def ending_word_items(count):
    if count % 10 == 1 and count % 100 != 11:
        return 'товар'
    elif count % 10 in (2, 3, 4) and count % 100 not in (12, 13, 14):
        return 'товара'
    else:
        return 'товаров'
