import pyotp
from django.conf import settings
from django.core.mail import send_mail

from .models import User


def generate_otp(user: User) -> str:
    """
        Функция генерирует одноразовый код на основе библиотеки pyotp.
    И присваивает этот код в поле email_otp к пользователю, для которого
    этот код был сгенерирован.
    """

    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    user.email_otp = totp.now()
    user.save()

    return totp.now()

def verify_otp(otp: str, user: User) -> bool:
    """
        Сверяет данные одноразового кода который ввел пользователь.
    С тем, который на самом деле привязан к пользователю.
    """

    return otp == user.email_otp

def send_email_otp(user: User) -> None:
    """
        Отправляет сообщение на почту с кодом подтверждения.
    """

    email = user.email
    email_otp = user.email_otp

    send_mail(
        'Подтверждение почты с помощью одноразового кода',
        f'Ваш код подтверждения для регистрации на сайте: {email_otp}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )