from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta, datetime
from django.utils import timezone

@shared_task
def send_otp_mail(email, code):
    print("start")
    send_mail(
        "Регистрация в моем приложении",
        f"Ваш одноразовый код: {code}.",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    print("end")
    return "SENT!"

@shared_task
def delete_unactive_users():
    from users.models import CustomUser
    deleted = CustomUser.objects.filter(is_active=False).delete()
    return f"Deleted: {deleted}"

@shared_task
def delete_old_confirmation_codes():
    from users.models import ConfirmationCode

    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)
    
    old_codes = ConfirmationCode.objects.filter(created_at__lt=one_hour_ago)
    count = old_codes.count()
    old_codes.delete()
    
    print(f"Удалено: {count} устаревших кодов подтверждения")
    
    return count

@shared_task
def send_welcome_mail(email):
    subject = 'Добро пожаловать в Shop API!'
    message = (
        f'Привет!\n\n'
        f'Твоя регистрация подтверждена.\n'
        f'Теперь ты можешь создавать продукты и оставлять отзывы.\n\n'
        f'Удачи!'
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    
    print(f"Приветственное письмо отправлено на {email}")
    return f"Отправлено на {email}"