from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Avg
from .models import Category
from products.models import Product
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method="get",
    responses={
        200: openapi.Response(
            "Average price for category",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "category": openapi.Schema(type=openapi.TYPE_STRING),
                    "average_price": openapi.Schema(type=openapi.TYPE_NUMBER),
                },
            ),
        ),
        404: openapi.Response("Category not found"),
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def category_average_price(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        descendants = category.get_descendants(include_self=True)
        avg_price = Product.objects.filter(category__in=descendants).aggregate(
            Avg("price")
        )["price__avg"]
        return Response({"category": category.name, "average_price": avg_price or 0})
    except Category.DoesNotExist:
        return Response(
            {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
        )
