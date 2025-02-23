from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from orders.models import Order
from orders.pdf import generate_pdf


@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    pdf_file = generate_pdf(order)
    email = EmailMessage(
        subject=f'Ваш заказ от {order.created_at.strftime("%d.%m.%Y")}.',
        body=f'Спасибо за покупку {order.first_name}! В приложении информация о Вашем заказе.',
        from_email=settings.EMAIL_HOST_USER,
        to=[order.email]
    )
    email.attach(
        f'order_{order.id}_{order.created_at.strftime("%d.%m.%Y")}.pdf',
        pdf_file.getvalue(),
        'application/pdf'
    )
    email.send()


# @shared_task
# def order_created(order_id):
#     order = Order.objects.get(id=order_id)
#     subject = f'Заказ № {order_id} от {order.created_at}'
#     message = (f'Уважаемый, {order.first_name},\n'
#                f'Заказ № {order.id} успешно оформлен!\n'
#                f'На сумму: {order.get_total_cost()}.')
#     mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
#     return mail_sent
