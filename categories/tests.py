import uuid
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from customers.models import Customer
from .models import Category
from products.models import Product

@pytest.mark.django_db
class TestCategory:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.customer = Customer.objects.create(user=self.user, phone_number='+254700000000')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Bakery')

    def test_category_creation(self):
        assert str(self.category) == 'Bakery'
        assert isinstance(self.category.id, uuid.UUID)

    def test_category_average_price(self):
        product = Product.objects.create(name='Bread', category=self.category, price=10.00, stock=100)
        response = self.client.get(reverse('category-average-price', args=[self.category.id]))
        assert response.status_code == 200
        assert response.data['average_price'] == 10.00