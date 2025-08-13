from django.urls import path
from .views import profile, get_access_token, logout_view

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('token/', get_access_token, name='get-access-token'),
    path('logout/', logout_view, name='customer_logout'),
]