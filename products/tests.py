import uuid
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from customers.models import Customer
from categories.models import Category
from .models import Product

@pytest.mark.django_db
class TestProduct:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.customer = Customer.objects.create(user=self.user, phone_number='+254700000000')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Bakery')
        self.product = Product.objects.create(name='Bread', category=self.category, price=10.00, stock=100)

    def test_product_creation(self):
        assert str(self.product) == 'Bread'
        assert isinstance(self.product.id, uuid.UUID)

    def test_list_products(self):
        response = self.client.get(reverse('product-list-create'))
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_create_product(self):
        response = self.client.post(reverse('product-list-create'), {
            'name': 'Cookie',
            'category_id': str(self.category.id),
            'price': 5.00,
            'stock': 50
        })
        assert response.status_code == 201
        assert Product.objects.count() == 2