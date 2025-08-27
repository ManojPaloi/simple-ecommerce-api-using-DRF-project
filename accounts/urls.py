# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("accounts/", views.accounts_api, name="accounts_api"),  # simple test route
]
