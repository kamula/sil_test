from django.conf import settings
from django.shortcuts import redirect
from customers.models import Customer
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        """Create a User and associated Customer when a new user logs in via Auth0."""
        user = super().create_user(claims)
        self.create_customer(user, claims)
        return user

    def update_user(self, user, claims):
        """Update user and ensure Customer exists during authentication."""
        user = super().update_user(user, claims)
        self.create_customer(user, claims)
        return user

    def create_customer(self, user, claims):
        """Create or update Customer object for the user."""
        try:
            customer, created = Customer.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': claims.get('phone_number', '+254700000000'),  # Fallback phone number
                    'address': claims.get('address', '')
                }
            )
            if not created:
                # Update existing customer if needed
                customer.phone_number = claims.get('phone_number', customer.phone_number)
                customer.address = claims.get('address', customer.address)
                customer.save()            
        except Exception as e:
            return(f"Error creating/updating customer for {user.username}: {e}")



def oidc_logout_redirect():
    """
    Redirect the user to the configured OIDC logout endpoint
    and then back to the configured LOGOUT_REDIRECT_URL.
    """
    logout_url = getattr(settings, "OIDC_OP_LOGOUT_ENDPOINT", None)
    post_logout_redirect = getattr(settings, "LOGOUT_REDIRECT_URL", "/")

    if logout_url:
        return redirect(f"{logout_url}?post_logout_redirect_uri={post_logout_redirect}")
    return redirect(post_logout_redirect)
