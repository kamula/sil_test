import africastalking
from django.conf import settings  # <-- FIXED to use Django settings
from django.core.mail import send_mail


def send_sms_notification(phone_number, message):
    """
    Sends an SMS using Africa's Talking.
    """
    if not settings.AFRICASTALKING_USERNAME or not settings.AFRICASTALKING_API_KEY:
        raise RuntimeError("SMS service is not configured properly")

    africastalking.initialize(
        username=settings.AFRICASTALKING_USERNAME,
        api_key=settings.AFRICASTALKING_API_KEY,
    )
    sms = africastalking.SMS
    return sms.send(message=message, recipients=[phone_number])


def send_email_notification(subject, message, recipient_list):
    """
    Sends an email using Django's email backend.
    """
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        raise RuntimeError("Email service is not configured properly.")

    return send_mail(  # <-- FIXED to return result
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
    )
