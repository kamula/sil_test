# orders/views.py
from orders.utils import send_email_notification, send_sms_notification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from products.models import Product
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method="post",
    request_body=OrderSerializer,
    responses={201: OrderSerializer, 400: "Bad Request"},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_create(request):
    try:
        customer = request.user.customer
    except ObjectDoesNotExist:
        return Response(
            {
                "error": "No customer profile associated with this user. Please update your profile."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        total = 0
        try:
            for item in request.data["items"]:
                product = Product.objects.get(id=item["product_id"])
                total += product.price * item["quantity"]
        except Product.DoesNotExist:
            return Response(
                {"error": "Invalid product_id"}, status=status.HTTP_400_BAD_REQUEST
            )

        order = serializer.save(customer=customer, total_amount=total)

        # Send SMS
        try:
            send_sms_notification(
                phone_number=customer.phone_number,
                message=f"Your order #{order.id} has been placed successfully. Total: KES {order.total_amount}",
            )
        except RuntimeError as e:           
            return Response(f"SMS not sent: {e}")

        # Send Email
        try:
            send_email_notification(
                subject=f"New Order #{order.id}",
                message=f"Order #{order.id} has been placed successfully. Total: KES {order.total_amount}",
                recipient_list=["admin@groceries.com"],
            )
        except RuntimeError as e:
            return Response(f"Email not sent: {e}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
