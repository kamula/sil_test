from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method="get",
    responses={200: ProductSerializer(many=True)},
)
@swagger_auto_schema(
    method="post",
    request_body=ProductSerializer,
    responses={201: ProductSerializer, 400: "Bad Request"},
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def product_list_create(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
