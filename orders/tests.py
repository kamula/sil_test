import uuid
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from customers.models import Customer
from categories.models import Category
from products.models import Product
from .models import Order
from unittest.mock import patch

@pytest.mark.django_db
class TestOrder:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.customer = Customer.objects.create(user=self.user, phone_number='+254700000000')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Bakery')
        self.product = Product.objects.create(name='Bread', category=self.category, price=10.00, stock=100)

    def test_order_creation(self):
        order = Order.objects.create(customer=self.customer, total_amount=20.00)
        assert str(order) == f"Order {order.id} by {self.customer}"
        assert isinstance(order.id, uuid.UUID)

    @patch('africastalking.SMS.send')
    @patch('django.core.mail.send_mail')
    def test_create_order(self, mock_send_mail, mock_sms_send):
        mock_sms_send.return_value = {'SMSMessageData': {'Recipients': [{'status': 'Success'}]}}
        mock_send_mail.return_value = 1
        
        response = self.client.post(reverse('order-create'), {
            'items': [{'product_id': str(self.product.id), 'quantity': 2, 'price': 10.00}]
        })
        assert response.status_code == 201
        assert Order.objects.count() == 1
        assert mock_sms_send.called
        assert mock_send_mail.called