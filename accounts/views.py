from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from accounts.forms import (CustomAuthenticationForm,
                            CustomUserCreationForm,
                            CustomPasswordChangeForm,
                            ProfileEditForm,
                            AddressForm)
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItem
from accounts.models import Address


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:profile_view')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login_view')


@login_required(login_url='accounts:login_view')
def profile_view(request):
    active_orders = Order.objects.filter(user=request.user, status='active').order_by('-created_at')
    paid_orders = Order.objects.filter(user=request.user, status='paid').order_by('-created_at')
    completed_orders = Order.objects.filter(user=request.user, status='completed').order_by('-created_at')
    canceled_orders = Order.objects.filter(user=request.user, status='canceled').order_by('-created_at')
    addresses = Address.objects.filter(user=request.user)

    # Все заказы пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    order_id = request.GET.get('order_id')

    if order_id:
        try:
            order_id = int(order_id)
            orders = orders.filter(id=order_id)  # Фильтр списка заказов по id
            orders_item = OrderItem.objects.filter(
                order__id=order_id,
                order__user=request.user
            ).select_related('product')

        except (ValueError, TypeError):
            # Если order_id некорректный, то показывает все заказы
            orders_item = OrderItem.objects.filter(order__in=orders).select_related('product')

    else:  # Если order_id не указан, получаем товары для всех заказов пользователя
        orders_item = OrderItem.objects.filter(order__in=orders).select_related('product')

    product_data = []
    for item in orders_item:
        product_name = item.product.name
        product_image = item.product.image

        product_data.append({'name': product_name, 'image': product_image})

    context = {
        'active_orders': active_orders,
        'paid_orders': paid_orders,
        'canceled_orders': canceled_orders,
        'completed_orders': completed_orders,
        'addresses': addresses,
        'orders': orders,  # Передаем все заказы
        'orders_item': orders_item,  # Передаем все товары
        'product_data': product_data,
    }

    return render(request, 'registration/profile.html', context)


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile_view')
    else:
        form = ProfileEditForm(instance=profile)
    return render(request, 'registration/edit_profile.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login_view')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile_view')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})


@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('accounts:profile_view')
    else:
        form = AddressForm()
    return render(request, 'addresses/add_address.html', {'form': form})


@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if address.user != request.user:
        return redirect('accounts:login_view')
    if request.method == 'POST':
        address.delete()
        return redirect('accounts:profile_view')
    return render(request, 'addresses/address_confirm_delete.html', {'address': address})
