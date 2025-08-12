from django.urls import path
from .views import order_create

urlpatterns = [
    path('orders/',order_create, name='order-create'),
]