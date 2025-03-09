from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from coupons.models import Coupon
from coupons.forms import CouponApplyForm
from django.utils import timezone
from django.contrib import messages


@require_POST
def coupon_apply(request):
    """ Добавление купона (использование) """
    time_now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=time_now,
                valid_to__gte=time_now,
                active=True
            )

            if coupon.max_uses == 0:  # неограниченное количество использований
                print('1', coupon.max_uses, coupon.uses)
                messages.success(request, 'Купон успешно применен!')
                request.session['coupon_id'] = coupon.id

            elif coupon.max_uses > coupon.uses:
                coupon.uses += 1
                coupon.save()
                print('2', coupon.max_uses, coupon.uses)
                messages.success(request, 'Купон успешно применен!')
                request.session['coupon_id'] = coupon.id

            elif coupon.max_uses > 0 and coupon.max_uses == coupon.uses:
                print('3', coupon.max_uses, coupon.uses)
                messages.success(request, "Этот купон уже достиг своего максимального количества использований.")

        except Coupon.DoesNotExist:
            messages.error(request, 'Купон не найден или уже использован.')
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')


@require_POST
def coupon_remove(request):
    """ Отмена действия купона """
    if 'coupon_id' in request.session:
        del request.session['coupon_id']
        messages.success(request, 'Купон успешно отменён')
    else:
        messages.error(request, 'Активный купон не найден')
    return redirect('cart:cart_detail')
