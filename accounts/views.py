from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from accounts.forms import CustomAuthenticationForm, CustomUserCreationForm, CustomPasswordChangeForm, ProfileEditForm
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
    return render(request, 'registration/registration.html', {"form": form})


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
    return render(request, 'registration/change_password.html', {"form": form})
