from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from accounts.forms import (CustomAuthenticationForm,
                            CustomUserCreationForm,
                            CustomPasswordChangeForm,
                            ProfileEditForm,
                            AddressForm)
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItem
from accounts.models import Address, EmailVerificationCode, Profile
from accounts.tasks import send_verify_code
from django.contrib.auth.models import User


def login_view(request):
    """ Вход в аккаунт """
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)  # инициализирует кастомную форму аутентификации
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # генерация кода
                gen_code = EmailVerificationCode.generate_code()
                # сохранение кода в базе данных с привязкой к пользователю
                new_verification = EmailVerificationCode.objects.create(user=user, code=gen_code)
                # отправка кода
                send_verify_code.delay(user.email, gen_code)
                print(user.email, gen_code)
                # сохраняет в сессию id пользователя
                request.session['2FA_user_id'] = user.id
                # получаем время создания кода и передаем данные для таймера
                request.session['2FA_code_created_at'] = int(new_verification.created_at.timestamp())
                # время жизни кода (3 минуты)
                request.session['2FA_code_lifetime_seconds'] = 60 * 3

                return redirect(reverse('accounts:login_verify_code'))
            #return redirect('accounts:login_verify_code')
            else:
                # Обработка ошибки аутентификации, если пароль или имя пользователя неверны
                form.add_error(None, "Неверное имя пользователя или пароль.")

    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def login_verify_code(request):
    """ Двухфакторная аутентификация """
    user_id = request.session.get('2FA_user_id')
    if not user_id:
        # Если в сессии нет user_id, перенаправляем на логин
        return redirect(reverse('accounts:login_view'))

    user = get_object_or_404(User, id=user_id)
    error = None
    context = {'user': user}  # Передаем user в контекст, чтобы можно было проверить его наличие
    # Получаем данные для таймера из сессии
    context['code_lifetime_seconds'] = request.session.get('2FA_code_lifetime_seconds', 180)
    context['created_at'] = request.session.get('2FA_code_created_at')

    # Обрабатываем POST запросы
    if request.method == 'POST':
        # Проверяем, был ли это запрос на новый код
        if 'request_new_code' in request.POST:
            # Удаляем старый код
            EmailVerificationCode.objects.filter(user=user).delete()

            # Генерируем и отправляем новый код
            gen_code = EmailVerificationCode.generate_code()
            new_verification = EmailVerificationCode.objects.create(user=user, code=gen_code)
            send_verify_code.delay(user.email, gen_code)
            print(f"Request for new code. Sending new code {gen_code} to {user.email}")

            # Обновляем данные для таймера в сессии
            request.session['2FA_code_created_at'] = int(new_verification.created_at.timestamp())
            # Время жизни кода (может быть фиксированным или браться из настроек)
            request.session['2FA_code_lifetime_seconds'] = 180

            # Обновляем контекст для шаблона
            context['created_at'] = request.session['2FA_code_created_at']
            context['code_lifetime_seconds'] = request.session['2FA_code_lifetime_seconds']
            # Сбрасываем ошибку, если она была
            error = None
            # Перерисовываем шаблон с обновленным таймером
            return render(request, 'registration/verify_code.html', context)

        # Если это не запрос нового кода, то это попытка ввода кода
        code_input = request.POST.get('code')
        if not code_input:
            error = 'Пожалуйста, введите код.'
        else:
            try:
                verification = EmailVerificationCode.objects.filter(user=user).latest('created_at')

                # Проверяем, что код совпадает и он еще не истек
                if verification.code == code_input and not verification.is_expired():
                    login(request, user)  # Логинимся
                    del request.session['2FA_user_id']  # Удаляет id пользователя из сессии
                    # Удаляем данные таймера из сессии
                    request.session.pop('2FA_code_created_at', None)
                    request.session.pop('2FA_code_lifetime_seconds', None)
                    return redirect('accounts:profile_view')
                else:
                    error = 'Не корректный или истекший код!'
                    # Удаляем неверный код и пользователя из сессии
                    EmailVerificationCode.objects.filter(user=user).delete()
                    del request.session['2FA_user_id']
                    # Удаляем данные таймера из сессии
                    request.session.pop('2FA_code_created_at', None)
                    request.session.pop('2FA_code_lifetime_seconds', None)

            except EmailVerificationCode.DoesNotExist:
                error = 'Код не найден! Пожалуйста, запросите новый.'
                # Удаляем пользователя из сессии, если кода нет
                if '2FA_user_id' in request.session:
                    del request.session['2FA_user_id']
                # Удаляем данные таймера из сессии
                request.session.pop('2FA_code_created_at', None)
                request.session.pop('2FA_code_lifetime_seconds', None)

    # Если была ошибка, передаем ее в контекст
    if error:
        context['error'] = error
        # Если пользователь существует, но возникла ошибка, нам нужно снова показать форму ввода кода
        # и, возможно, кнопку запроса нового кода.
        # Если user_id был удален из сессии (например, из-за ошибки EmailVerificationCode.DoesNotExist),
        # то render ниже может не показать форму ввода кода.
        # Проверим, есть ли user_id в сессии, чтобы понять, нужно ли показывать форму ввода.
        if '2FA_user_id' not in request.session:
            # Если user_id отсутствует, значит, мы не должны показывать форму ввода кода
            # и, возможно, даже форму запроса нового кода.
            # Но поскольку мы хотим, чтобы пользователь мог запросить новый код,
            # нам нужно вернуть user_id в сессию, если он был удален из-за ошибки.
            # Это может быть немного запутанно, поэтому стоит продумать флоу.
            # В данном случае, если возникла ошибка, а user_id уже удален,
            # мы можем просто вернуть пользователю страницу с ошибкой и предложением запросить новый код.
            pass # В текущей логике, если user_id удален, контекст уже будет без user.

    return render(request, 'registration/verify_code.html', context)


    # user_id = request.session.get('2FA_user_id')
    # user = get_object_or_404(User, id=user_id)  # получает из сессии id пользователя
    # error = None
    # context = {}
    # try:
    #     # Проверяет, что код совпадает и он еще не истек
    #     verification = EmailVerificationCode.objects.filter(user=user).latest('created_at')
    #
    #     context = {
    #         'verification_code': verification.code,
    #         # Можно передать код, если нужно для JS (хотя обычно не передают)
    #         'code_lifetime_seconds': 3 * 60,  # Передаем время жизни в секундах для удобства JS
    #         'created_at': int(verification.created_at.timestamp())  # Передаем timestamp создания кода
    #     }
    #     if request.method == 'POST':
    #         code = request.POST.get('code')
    #
    #         if verification.code == code and not verification.is_expired():  # Проверяет, если код еще не истек
    #             login(request, user)  # Логинимся
    #             del request.session['2FA_user_id']  # Удаляет код из сессии
    #             return redirect('accounts:profile_view')
    #
    #         else:
    #             error = 'Не корректный или не существующий код!'
    #             EmailVerificationCode.objects.filter(user=user).delete()
    #             del request.session['2FA_user_id']
    #
    # except EmailVerificationCode.DoesNotExist:
    #     error = 'Код не найден!'
    #
    #     # return render(request, 'registration/verify_code.html', {'error': error})
    # if error:
    #     context['error'] = error
    # return render(request, 'registration/verify_code.html', context)


def logout_view(request):
    """ Выход из личного кабинета """
    logout(request)
    return redirect('accounts:login_view')


@login_required(login_url='accounts:login_view')
def profile_view(request):
    """ Личный кабинет """
    active_orders = Order.objects.filter(user=request.user, status='active').order_by('-created_at')
    paid_orders = Order.objects.filter(user=request.user, status='paid').order_by('-created_at')
    completed_orders = Order.objects.filter(user=request.user, status='completed').order_by('-created_at')
    canceled_orders = Order.objects.filter(user=request.user, status='canceled').order_by('-created_at')
    addresses = Address.objects.filter(profile__user_id=request.user.id)

    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    order_id = request.GET.get('order_id')

    if order_id:
        try:
            order_id = int(order_id)
            orders = orders.filter(id=order_id)
            orders_item = OrderItem.objects.filter(
                order__id=order_id,
                order__user=request.user
            ).select_related('product')

        except (ValueError, TypeError):
            orders_item = OrderItem.objects.filter(order__in=orders).select_related('product')

    else:
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
        'orders': orders,
        'orders_item': orders_item,
        'product_data': product_data,
    }

    return render(request, 'registration/profile.html', context)


@login_required
def edit_profile(request):
    """ Редактирование профиля """
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
    """ Регистрация на сайте """
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
    """ Смена пароля """
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
    """ Добавление адреса """
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            profile = Profile.objects.get(user=request.user)
            address.profile = profile
            address.save()
            return redirect('accounts:profile_view')
    else:
        form = AddressForm()
    return render(request, 'addresses/add_address.html', {'form': form})


@login_required
def delete_address(request, address_id):
    """ Удаление адреса """
    address = get_object_or_404(Address, id=address_id, profile__user_id=request.user.id)
    print(address)
    if request.method == 'POST':
        address.delete()
        return redirect('accounts:profile_view')
    return render(request, 'addresses/address_confirm_delete.html', {'address': address})
