from django.contrib import admin
# config/urls.py
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Groceries API",
        default_version="v1",
        description=(
            "API for managing products, categories, and orders.\n"
            "Authentication:\n"
            "1. Navigate to /oidc/authenticate/ to log in via Auth0.\n"
            "2. After login, you will be redirected to /oidc/callback/.\n"
            "3. Get the access token via GET /api/customers/token/ and use it in the Authorization header as 'Bearer <token>'.\n"
            "4. To log out, send a POST request to /api/customers/logout/.\n"
            "For more details, see [Auth0 Documentation](https://auth0.com/docs)."
        ),
        contact=openapi.Contact(email="admin@groceries.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def redirect_to_swagger(request):
    return redirect("schema-swagger-ui")

def redirect_to_oidc_logout(request):
    return redirect('customer_logout') 

urlpatterns = [
    path("", redirect_to_swagger, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("products.urls")),
    path("api/", include("categories.urls")),
    path("api/", include("orders.urls")),
    path("api/customers/", include("customers.urls")),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("accounts/logout/", redirect_to_oidc_logout, name="django_logout"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]