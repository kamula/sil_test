from customers.models import Customer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import logout
from .auth import oidc_logout_redirect


@swagger_auto_schema(
    method='get',
    responses={200: openapi.Response('User profile', schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'user': openapi.Schema(type=openapi.TYPE_STRING)}
    ))},
    operation_summary="Get logged-in user's profile",
    operation_description="Returns the username of the currently authenticated user."
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({'user': request.user.username})


@swagger_auto_schema(
    method='get',
    operation_summary="Get OIDC Access Token",
    operation_description="Returns the OIDC access token for the authenticated user, if available.",
    responses={
        200: openapi.Response('Access token', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'access_token': openapi.Schema(type=openapi.TYPE_STRING)}
        )),
        400: openapi.Response('Error', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'error': openapi.Schema(type=openapi.TYPE_STRING)}
        ))
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_access_token(request):    
    access_token = request.session.get('oidc_access_token')
    if not access_token:
        return Response({"error": "No access token available"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"access_token": access_token})


@swagger_auto_schema(
    method='post',
    operation_summary="Log out the current user",
    operation_description="Logs out the user, clears the session, and redirects to the OIDC logout endpoint.",
    responses={
        200: openapi.Response('Logout successful', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}
        )),
        401: 'Unauthorized'
    },
)
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request) 
    return oidc_logout_redirect()



@swagger_auto_schema(
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
            'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address'),
        },
        required=['phone_number']
    ),
    responses={
        200: openapi.Response('Customer profile updated', schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                'address': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )),
        400: 'Bad Request'
    },
    operation_summary="Update customer profile",
    operation_description="Updates the phone number and address for the authenticated user's customer profile."
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_customer_profile(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(
            user=request.user,
            phone_number=request.data.get('phone_number', '+254700000000'),
            address=request.data.get('address', '')
        )
    
    customer.phone_number = request.data.get('phone_number', customer.phone_number)
    customer.address = request.data.get('address', customer.address)
    customer.save()
    
    return Response({
        'phone_number': customer.phone_number,
        'address': customer.address
    }, status=status.HTTP_200_OK)