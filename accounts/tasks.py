from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_verify_code(email: str, code: str):
    """ Отправка кода """
    print(email, code)
    send_mail(
        subject='Проверочный код для входа в систему магазина',
        message=f'Проверочный код: {code}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
