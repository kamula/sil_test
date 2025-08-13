from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get',
    responses={200: openapi.Response('User profile', schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'user': openapi.Schema(type=openapi.TYPE_STRING)}
    ))},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response({'user': request.user.username})