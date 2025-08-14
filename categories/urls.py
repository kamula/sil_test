from django.urls import path
from .views import category_average_price

urlpatterns = [
    path(
        "categories/<uuid:category_id>/average-price/",
        category_average_price,
        name="category-average-price",
    ),
]
