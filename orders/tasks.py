from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from orders.models import Order
from orders.pdf import generate_pdf


#@shared_task   - , send_mail
#def sent_email_after_order_created(order_id):
#    order = Order.objects.get(id=order_id)
#    subject = f'Заказ № {order_id} от {order.created_at.strftime("%d.%m.%Y")}'
#    message = (f'Уважаемый(ая), {order.first_name}!\n'
#               f'Ваш заказ № {order_id} успешно оформлен!\n'
#               f'На сумму {order.get_total_cost()}')
#    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
#    return mail_sent


@shared_task
def order_created(order_id):
    print(f"Starting order_created task for order_id: {order_id}")
    try:
        order = Order.objects.get(id=order_id)
        print(f"Order found: {order.id}, email: {order.email}")
        pdf_file = generate_pdf(order)
        print("PDF generated.", pdf_file)
        email = EmailMessage(
            subject=f'Заказ № {order_id} от {order.created_at.strftime("%d.%m.%Y")}',
            body=f'Уважаемый(ая), {order.first_name}!\n'
                 f'Ваш заказ № {order_id} успешно оформлен!\n'
                 f'На сумму {order.get_total_cost()}',
            from_email=settings.EMAIL_HOST_USER,
            to=[order.email]
        )
        print("Email object created.")

        email.attach(
            filename=f'order_{order.id}_{order.created_at.strftime("%d.%m.%Y")}.pdf',
            content=pdf_file,
            # content=pdf_file.getvalue(),
            mimetype='application/pdf'
        )
        print("PDF attached to email.")
        # pdf_file.close()
        email.send()
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred in order_created task: {e}")
        import traceback
        traceback.print_exc()
