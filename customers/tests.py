import uuid
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Customer

@pytest.mark.django_db
class TestCustomer:
    def test_customer_creation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        customer = Customer.objects.create(user=user, phone_number='+254700000000')
        assert str(customer) == 'testuser'
        assert isinstance(customer.id, uuid.UUID)

    def test_profile_view(self):
        client = APIClient()
        user = User.objects.create_user(username='testuser', password='testpass')
        Customer.objects.create(user=user, phone_number='+254700000000')
        client.force_authenticate(user=user)
        response = client.get(reverse('profile'))
        assert response.status_code == 200
        assert response.data['user'] == 'testuser'