from yookassa import Configuration, Payment
import uuid

Configuration.account_id = "YOUR_SHOP_ID"  # замените на ваш Shop ID
Configuration.secret_key = "YOUR_SECRET_KEY"  # замените на ваш Secret Key

def create_payment(amount, description):
    payment = Payment.create({
        "amount": {
            "value": str(amount),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/your_bot"  # ссылка для возврата в бот после оплаты
        },
        "capture": True,
        "description": description
    }, uuid.uuid4())

    return payment.confirmation.confirmation_url
