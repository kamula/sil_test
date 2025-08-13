from django.urls import path
from .views import category_average_price

urlpatterns = [
    path(
        "categories/<int:category_id>/average-price/",
        category_average_price,
        name="category-average-price",
    ),
]
