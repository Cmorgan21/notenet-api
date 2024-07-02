from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer
from .serializers import ChangePasswordSerializer

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        """
        Get the authenticated user.
        """
        return self.request.user
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

