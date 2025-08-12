from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from products.models import Product
from django.core.mail import send_mail
import africastalking 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import os

@swagger_auto_schema(
    method='post',
    request_body=OrderSerializer,
    responses={201: OrderSerializer, 400: 'Bad Request'},
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order_create(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        total = 0
        for item in request.data['items']:
            product = Product.objects.get(id=item['product_id'])
            total += product.price * item['quantity']
        
        order = serializer.save(customer=request.user.customer, total_amount=total)
        
        # Initialize Africa's Talking SMS service
        africastalking.initialize(
            username=os.getenv('AFRICASTALKING_USERNAME'),
            api_key=os.getenv('AFRICASTALKING_API_KEY')
        )
        sms = africastalking.SMS
        
        # Send SMS to customer
        sms.send(
            message=f"Your order #{order.id} has been placed successfully. Total: {order.total_amount}",
            recipients=[request.user.customer.phone_number]
        )

        # Send email to admin
        send_mail(
            subject=f"New Order #{order.id}",
            message=f"Order #{order.id} placed by {request.user.customer}. Total: {order.total_amount}",
            from_email='no-reply@groceries.com',
            recipient_list=['admin@groceries.com'],
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)