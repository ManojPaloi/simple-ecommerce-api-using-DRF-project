from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LoginView, LogoutView, ProfileView, UserListView


urlpatterns = [
    # Authentication (custom endpoints)
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("users/", UserListView.as_view(), name="users"),

    # User management (optional, for admin dashboards or staff APIs)
    path("accounts/users/", UserListView.as_view(), name="users"),

    # JWT token endpoints (standard DRF SimpleJWT)
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
