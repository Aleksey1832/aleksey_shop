from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required

from orders.models import Order


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('shop:product_list')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login_view')


@login_required(login_url='accounts:login_view')
def profile_view(request):
    active_orders = Order.objects.filter(user=request.user, status='active').order_by('-created_at')
    canceled_orders = Order.objects.filter(user=request.user, status='canceled').order_by('-created_at')
    completed_orders = Order.objects.filter(user=request.user, status='completed').order_by('-created_at')
    context = {'active_orders': active_orders,
               'canceled_orders': canceled_orders,
               'completed_orders': completed_orders}

    return render(request, 'registration/profile.html', context)


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login_view')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/registration.html', {"form": form})
