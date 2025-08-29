"""
Project-level URL Configuration for drfcommerce.

This routes all the top-level endpoints of the project:
- Admin dashboard
- DRF's browsable API login/logout
- Accounts app (authentication, registration, profile, JWT)
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin dashboard
    path("admin/", admin.site.urls),

    # Django REST framework's built-in login/logout views
    # (useful for the browsable API)
    path("api-auth/", include("rest_framework.urls")),

    # Accounts app (custom auth, JWT, user management)
    # All routes inside accounts/urls.py are automatically
    # prefixed with `api/accounts/`
    path("api/accounts/", include("accounts.urls")),
]
