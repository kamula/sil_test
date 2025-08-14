import pytest
from unittest.mock import patch, MagicMock
from orders import utils
from django.core.mail import send_mail
from config import settings


@pytest.mark.django_db
class TestSendSMSNotification:
    @patch("orders.utils.africastalking.SMS")
    @patch("orders.utils.africastalking.initialize")
    def test_send_sms_success(self, mock_initialize, mock_sms):
        """Should send SMS successfully using Africa's Talking."""
        mock_sms.send.return_value = {"status": "success"}

        phone_number = "+254712345678"
        message = "Test SMS"

        response = utils.send_sms_notification(phone_number, message)

        mock_initialize.assert_called_once_with(
            username=settings.AFRICASTALKING_USERNAME,
            api_key=settings.AFRICASTALKING_API_KEY,
        )
        mock_sms.send.assert_called_once_with(
            message=message, recipients=[phone_number]
        )
        assert response["status"] == "success"

    def test_sms_service_not_configured(self, settings):
        """Should raise RuntimeError if SMS config is missing."""
        settings.AFRICASTALKING_USERNAME = ""
        settings.AFRICASTALKING_API_KEY = ""

        with pytest.raises(RuntimeError) as excinfo:
            utils.send_sms_notification("+254712345678", "Hello")
        assert "SMS service is not configured properly" in str(excinfo.value)


@pytest.mark.django_db
class TestSendEmailNotification:
    @patch("orders.utils.send_mail")
    def test_send_email_success(self, mock_send_mail):
        """Should send email successfully."""
        mock_send_mail.return_value = 1

        subject = "Order Update"
        message = "Your order has been shipped."
        recipient_list = ["test@example.com"]

        response = utils.send_email_notification(subject, message, recipient_list)

        mock_send_mail.assert_called_once_with(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
        )
        assert response == 1

    def test_email_service_not_configured(self, settings):
        """Should raise RuntimeError if email config is missing."""
        settings.EMAIL_HOST_USER = ""
        settings.EMAIL_HOST_PASSWORD = ""

        with pytest.raises(RuntimeError) as excinfo:
            utils.send_email_notification("Subject", "Message", ["test@example.com"])
        assert "Email service is not configured properly." in str(excinfo.value)
