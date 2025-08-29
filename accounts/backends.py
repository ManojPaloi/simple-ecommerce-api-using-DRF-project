from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend.
    Allows users to log in with either email or username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            # Look up by email OR username (case insensitive)
            user = UserModel.objects.get(
                Q(email__iexact=username) | Q(username__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            # In rare cases of duplicates, fall back to email as unique
            try:
                user = UserModel.objects.get(email__iexact=username)
            except UserModel.DoesNotExist:
                return None

        # Validate password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
