from django.conf import settings
from yookassa import Configuration, Payment
import uuid


Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def create_payment(order):
    payment = Payment().create(
        {
            "amount": {
                "value": str(order.get_total_cost()),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "http://127.0.0.1:8000/"
            },
            "capture": True,
            "description": f"Оплата заказа №{order.id}"
        }, uuid.uuid4()
    )
    return payment
