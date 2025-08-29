from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .models import CustomUser
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    ProfileUpdateSerializer,
)


class RegisterView(generics.CreateAPIView):
    """
    User Registration API

    - Allows anyone to register a new user account.
    - Uses the `RegisterSerializer` to validate input and create the user.
    - Does not require authentication (open endpoint).
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    """
    User Login API with JWT (rotating refresh tokens)

    - Accepts email/username and password.
    - Returns an access token (short-lived) and a refresh token (long-lived).
    - Refresh token rotates on every login for better security.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Validate login credentials with the serializer
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "Login successful",
                "access": str(refresh.access_token),  # short-lived access token
                "refresh": str(refresh),              # long-lived refresh token
                "user": UserSerializer(user).data,    # serialized user data
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    User Logout API

    - Requires authentication.
    - Accepts a refresh token (via body or query param).
    - Blacklists the refresh token so it cannot be reused.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return self._logout(request)

    def get(self, request):
        return self._logout(request)

    def _logout(self, request):
        refresh_token = request.data.get("refresh") or request.query_params.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Add token to blacklist
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    User Profile API

    - Requires authentication.
    - GET: Retrieve the full profile of the logged-in user.
    - PUT/PATCH: Update profile details.
    """
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Return the current authenticated user
        return self.request.user

    def get(self, request, *args, **kwargs):
        # Override GET to return full user data (not just limited fields)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserListView(generics.ListAPIView):
    """
    Admin User List API

    - Only accessible by admins/staff.
    - Returns a list of all registered users.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
