from django.conf import settings
from django.shortcuts import redirect

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
