import os
import uuid
from dotenv import load_dotenv
from yookassa import Configuration, Payment


load_dotenv()

Configuration.account_id = os.getenv("YOOKASSA_ACCOUNT_ID")
Configuration.secret_key = os.getenv("YOOKASSA_SECRET_KEY")


def create_test_payment():
    payment = Payment().create(
        {
            "amount": {
                "value": "1000.00", "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect", "return_url": "https://example.com/return"
            },
            "capture": True,
            "description": "Test payment № 1",
        }, uuid.uuid4()
    )

    print("payment_id", payment.id)
    print("payment_status", payment.status)
    print("payment_url", payment.confirmation.confirmation_url)

    return payment


# if __name__ == '__main__':
#     create_test_payment()
