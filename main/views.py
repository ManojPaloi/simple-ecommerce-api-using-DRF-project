from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    User signup view
    """
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    """
    User login view -> returns JWT tokens + user data
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveAPIView):
    """
    Get logged-in user profile
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """
    Logout user by blacklisting refresh token
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    """
    Logout user from all devices by blacklisting all tokens
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)

        for token in tokens:
            try:
                BlacklistedToken.objects.get_or_create(token=token)
            except:
                pass

        return Response({"message": "Successfully logged out from all devices."}, status=status.HTTP_205_RESET_CONTENT)
